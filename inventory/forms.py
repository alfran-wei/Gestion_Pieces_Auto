from django import forms
from django.utils import timezone
from .models import Piece, Transaction, Marque

class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ['marque','nom_piece','reference','photo','stock_initial','stock_securite']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['piece', 'type', 'quantite', 'date', 'commentaire']
        widgets = {
            'piece': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class StockImportForm(forms.Form):
    fichier = forms.FileField(label="Fichier Excel", required=True)

def clean_quantite(self):
        q = self.cleaned_data.get('quantite')
        if q is None or q <= 0:
            raise forms.ValidationError("La quantité doit être un entier positif.")
        return q

def clean(self):
        cleaned = super().clean()
        # on vérifie le stock si c'est une sortie
        ttype = cleaned.get('type')
        quantite = cleaned.get('quantite')
        piece = cleaned.get('piece')
        if ttype == 'OUT' and piece and quantite is not None:
            # stock_reel est la property du modèle
            if piece.stock_reel < quantite:
                raise forms.ValidationError(f"Stock insuffisant pour la sortie (stock réel = {piece.stock_reel}).")
        return cleaned