import pandas as pd
from django.core.management.base import BaseCommand
from inventory.models import Marque, Piece

class Command(BaseCommand):
    help = "Importer les données de stock depuis un fichier Excel"

    def add_arguments(self, parser):
        parser.add_argument('fichier_excel', type=str)

    def handle(self, *args, **options):
        fichier_excel = options['fichier_excel']

        df = pd.read_excel(fichier_excel, sheet_name="SUIVI DE STOCK", header=1)
        print("Colonnes trouvées :", df.columns.tolist())
        # Remplacer les NaN par 0 pour éviter les erreurs
        df = df.fillna(0)

        for _, row in df.iterrows():
            marque, _ = Marque.objects.get_or_create(nom=row['Marques'])
            Piece.objects.create(
                marque=marque,
                nom_piece=row['Pièces '],   # attention il y a un espace
                reference=row['References'],
                stock_initial=row['Stock initial'],
                quantite_entree=row['Quantité entrant'],
                quantite_sortie=row['Quantité sortant'],
                stock_securite=row['Stock de sécurité'],
            )
        self.stdout.write(self.style.SUCCESS("✅ Import terminé avec succès"))
