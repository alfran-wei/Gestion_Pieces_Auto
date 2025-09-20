from django.contrib import admin
from .models import Marque, Piece, Transaction

@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ('nom_piece','marque','reference','stock_reel','stock_securite','statut')
    search_fields = ('nom_piece','reference','marque__nom')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('piece','type','quantite','date')
    list_filter = ('type','date')
