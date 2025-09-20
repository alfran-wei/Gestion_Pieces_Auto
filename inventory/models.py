from django.db import models
from django.utils import timezone

class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nom

class Piece(models.Model):
    marque = models.ForeignKey(Marque, on_delete=models.PROTECT, related_name='pieces')
    nom_piece = models.CharField(max_length=200)
    reference = models.CharField(max_length=200, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to='pieces/', blank=True, null=True)
    stock_initial = models.IntegerField(default=0)
    quantite_entree = models.IntegerField(default=0)
    quantite_sortie = models.IntegerField(default=0)
    stock_securite = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def stock_reel(self):
        return self.stock_initial + self.quantite_entree - self.quantite_sortie

    @property
    def statut(self):
        return "ALERTE" if self.stock_reel < self.stock_securite else "OK"

    def __str__(self):
        return f"{self.nom_piece} ({self.reference})"

class Transaction(models.Model):
    TYPE_CHOICES = (('IN', 'Entrée'), ('OUT', 'Sortie'))
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    quantite = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    commentaire = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
        # si création, mettre à jour les totaux de la pièce
        if creating:
            if self.type == 'IN':
                Piece.objects.filter(pk=self.piece.pk).update(quantite_entree=models.F('quantite_entree') + self.quantite)
            else:
                Piece.objects.filter(pk=self.piece.pk).update(quantite_sortie=models.F('quantite_sortie') + self.quantite)
