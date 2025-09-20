from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import require_password
from .models import Piece, Transaction, Marque
from django.db import models
from django.utils import timezone
from django.contrib import messages
from .forms import PieceForm, TransactionForm, StockImportForm
from django.db.models.functions import TruncDate
from django.http import JsonResponse, HttpResponse
from django.db.models import F, ExpressionWrapper, IntegerField, Sum
import urllib.parse
import json
import pandas as pd

def dashboard(request):
    total_pieces = Piece.objects.count()

    # Pièces en alerte (stock restant < stock sécurité)
    alertes_qs = Piece.objects.annotate(
        stock_restant=(F('stock_initial') + F('quantite_entree') - F('quantite_sortie'))
    ).filter(stock_restant__lt=F('stock_securite'))

    alertes = alertes_qs.count()

    # Dernières transactions
    last_transactions = Transaction.objects.order_by('-date')[:5]

    # 📊 1. Répartition du stock par marque
    stock_par_marque = Piece.objects.values("marque__nom").annotate(
        total=Sum("stock_initial") + Sum("quantite_entree") - Sum("quantite_sortie")
    )
    chart_pie_labels = [item["marque__nom"] for item in stock_par_marque]
    chart_pie_data = [item["total"] for item in stock_par_marque]

    # 📊 2. Top 5 pièces les plus stockées
    top_pieces = Piece.objects.annotate(
        stock_restant=(F('stock_initial') + F('quantite_entree') - F('quantite_sortie'))
    ).order_by('-stock_restant')[:5]

    chart_bar_labels = [p.nom_piece for p in top_pieces]
    chart_bar_data = [p.stock_restant for p in top_pieces]

    # 📊 3. Flux des transactions (entrées vs sorties)
    flux = Transaction.objects.annotate(
        jour=TruncDate("date")
    ).values("jour", "type").annotate(total=Sum("quantite")).order_by("jour")

    flux_dates = sorted(set([f["jour"].strftime("%d/%m") for f in flux]))
    flux_entrees = []
    flux_sorties = []

    for date in flux_dates:
        entrees = sum(f["total"] for f in flux if f["jour"].strftime("%d/%m") == date and f["type"] == "ENTREE")
        sorties = sum(f["total"] for f in flux if f["jour"].strftime("%d/%m") == date and f["type"] == "SORTIE")
        flux_entrees.append(entrees)
        flux_sorties.append(sorties)

    context = {
        "total_pieces": total_pieces,
        "alertes": alertes,
        "alertes_qs": alertes_qs,  # Pour lister les pièces en alerte
        "last_transactions": last_transactions,

        "chart_pie_labels": json.dumps(chart_pie_labels),
        "chart_pie_data": json.dumps(chart_pie_data),

        "chart_bar_labels": json.dumps(chart_bar_labels),
        "chart_bar_data": json.dumps(chart_bar_data),

        "flux_dates": json.dumps(flux_dates),
        "flux_entrees": json.dumps(flux_entrees),
        "flux_sorties": json.dumps(flux_sorties),
    }
    return render(request, "inventory/dashboard.html", context)

def pieces_list(request):
    pieces = Piece.objects.all()
    return render(request, "inventory/pieces_list.html", {"pieces": pieces})

def api_pieces(request):
    qs = Piece.objects.all().select_related('marque')
    data = []
    for p in qs:
        stock_reel = p.stock_initial + p.quantite_entree - p.quantite_sortie
        statut = "ALERTE" if stock_reel < p.stock_securite else "OK"
        data.append({
            "marque": p.marque.nom if p.marque else "",
            "nom_piece": p.nom_piece,
            "reference": p.reference,
            "stock_initial": p.stock_initial,
            "quantite_entree": p.quantite_entree,
            "quantite_sortie": p.quantite_sortie,
            "stock_reel": stock_reel,
            "stock_securite": p.stock_securite,
            "statut": statut,
        })
    return JsonResponse({"data": data})  # ⚠️ très important

@login_required
def piece_add(request):
    if request.method == 'POST':
        form = PieceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Pièce ajoutée avec succès")
            return redirect('inventory:pieces_list')
        else:
            messages.error(request, "❌ Formulaire invalide")
    else:
        form = PieceForm()
    return render(request, 'inventory/piece_form.html', {'form': form})

@login_required
def transaction_add(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()   # le save() du modèle mettra à jour les totaux de la pièce
            return redirect('inventory:pieces_list')
    else:
        # initial pour le champ datetime-local (format attendu : YYYY-MM-DDTHH:MM)
        now_local = timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M')
        form = TransactionForm(initial={'date': now_local})
    server_now_display = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S')
    return render(request, 'inventory/transaction_form.html', {
        'form': form,
        'server_now': server_now_display
    })

@login_required
def import_stock(request):
    rapport = []

    if request.method == 'POST' and request.FILES.get('fichier'):
        fichier = request.FILES['fichier']

        try:
            # Lire le fichier Excel à partir de la ligne 2 (skiprows=1)
            df = pd.read_excel(fichier, skiprows=1)

            # Vérifier les colonnes disponibles pour debug
            print("Colonnes trouvées :", df.columns.tolist())

            for i, row in df.iterrows():
                try:
                    # Colonnes exactes comme dans ton Excel
                    marque_nom = row['Marques']
                    nom_piece = row['Pièces ']
                    reference = row['References']

                    # Conversion sécurisée pour les champs numériques
                    stock_initial = 0 if pd.isna(row['Stock initial']) else int(row['Stock initial'])
                    stock_securite = 0 if pd.isna(row['Stock de sécurité']) else int(row['Stock de sécurité'])
                    quantite_entree = 0 if pd.isna(row['Quantité entrant']) else int(row['Quantité entrant'])
                    quantite_sortie = 0 if pd.isna(row['Quantité sortant']) else int(row['Quantité sortant'])

                    # Création ou récupération de la marque
                    marque_obj, _ = Marque.objects.get_or_create(nom=marque_nom)

                    # Création ou mise à jour de la pièce
                    piece, created = Piece.objects.update_or_create(
                        reference=reference,
                        defaults={
                            'marque': marque_obj,
                            'nom_piece': nom_piece,
                            'stock_initial': stock_initial,
                            'stock_securite': stock_securite,
                            'quantite_entree': quantite_entree,
                            'quantite_sortie': quantite_sortie,
                        }
                    )

                    if created:
                        rapport.append(f"Ligne {i+2} : Pièce '{nom_piece}' créée ✅")
                    else:
                        rapport.append(f"Ligne {i+2} : Pièce '{nom_piece}' mise à jour 🔄")

                except Exception as e_line:
                    rapport.append(f"Ligne {i+2} : Erreur - {e_line}")

            messages.success(request, "Import terminé. Vérifie le rapport ci-dessous.")
            return render(request, 'inventory/import_stock.html', {'rapport': rapport})

        except Exception as e:
            messages.error(request, f"Erreur lors de la lecture du fichier : {e}")
    


    return render(request, 'inventory/import_stock.html', {'rapport': rapport})


def export_stock(request):
    query = request.GET.get("q", "").strip().lower()  # recherche

    qs = Piece.objects.select_related('marque').all()

    # 🔎 Si recherche, filtrer
    if query:
        qs = qs.filter(
            models.Q(nom_piece__icontains=query) |
            models.Q(reference__icontains=query) |
            models.Q(marque__nom__icontains=query)
        )

    data = []
    for p in qs:
        stock_reel = p.stock_initial + p.quantite_entree - p.quantite_sortie
        observation = 'ALERTE' if stock_reel < p.stock_securite else 'RAS'
        data.append({
            'Marque': p.marque.nom if p.marque else "",
            'Pièce': p.nom_piece,
            'Référence': p.reference,
            'Stock initial': p.stock_initial,
            'Quantité entrante': p.quantite_entree,
            'Quantité sortante': p.quantite_sortie,
            'Stock réel': stock_reel,
            'Stock de sécurité': p.stock_securite,
            'Observation': observation,
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    filename = "stock_filtré.xlsx" if query else "stock_export.xlsx"
    response['Content-Disposition'] = f'attachment; filename={urllib.parse.quote(filename)}'
    df.to_excel(response, index=False)
    return response
