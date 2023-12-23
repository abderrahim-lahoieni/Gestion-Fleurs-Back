# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Abonne(models.Model):
    id_abonne = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    numero = models.CharField(unique=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    id_user = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='id_user', blank=True, null=True, default=0)

    class Meta:
        db_table = 'abonne'


class Bouquet(models.Model):
    id_bouquet = models.AutoField(primary_key=True)
    nom = models.CharField(unique=True, max_length=255)
    image = models.BinaryField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    remise = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'bouquet'


class Commande(models.Model):
    id_commande = models.AutoField(primary_key=True)
    date_commande = models.DateField()
    id_commandant = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='id_commandant', blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    statut = models.CharField(max_length=255, blank=True, null=True)
    adresse_livraison = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'commande'


class Famille(models.Model):
    nom = models.CharField(primary_key=True, max_length=255)

    class Meta:
        db_table = 'famille'


class Fichesoin(models.Model):
    id_fichesoin = models.AutoField(primary_key=True)    
    instruction_entretien = models.TextField(blank=True, null=True)
    frequence_arosage = models.TextField(blank=True, null=True)
    exposition_lumiere = models.TextField(blank=True, null=True)
    temperature_ideal = models.TextField(blank=True, null=True)
    engrais_commandes = models.TextField(blank=True, null=True)
    id_fleur = models.OneToOneField('Fleur', models.DO_NOTHING, db_column='id_fleur', blank=True, null=True)

    class Meta:
        db_table = 'fichesoin'


class Fleur(models.Model):
    id_fleur = models.AutoField(primary_key=True)    
    nom = models.CharField(max_length=255)
    origine = models.CharField(max_length=255, blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    remise = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/')
    qt_stock = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    id_famille = models.ForeignKey(Famille, models.DO_NOTHING, db_column='id_categorie', blank=True, null=True)
    
    FLEUR = 1
    PLANTE =2
    TYPE_CHOICES = [
        (FLEUR, 'Fleur'),
        (PLANTE , 'Plante')
    ]
    categorie = models.IntegerField(choices=TYPE_CHOICES, default=FLEUR)

    class Meta:
        db_table = 'fleur'
        unique_together = (('nom', 'categorie'),)


class LigneCommande(models.Model):
    id_lignecommande = models.AutoField(primary_key=True)    
    commande = models.ForeignKey(Commande, models.DO_NOTHING, blank=True, null=True)
    produit_id = models.IntegerField(blank=True, null=True)
    type_produit = models.CharField(max_length=255, blank=True, null=True)
    quantite_commande = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ligne_commande'
        unique_together = (('commande', 'produit_id', 'type_produit'),)


class Magasin(models.Model):
    id_magasin= models.AutoField(primary_key=True)    
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)

    class Meta:
        db_table = 'magasin'


class Parfum(models.Model):
    id_parfum= models.AutoField(primary_key=True)    
    nom = models.CharField(unique=True, max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    remise = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'parfum'


class Utilisateur(models.Model):
    id_user = models.AutoField(primary_key=True)    
    PROPRIETAIRE = 1
    VENDEUR = 2
    ABONNE =3
    
    TYPE_CHOICES = [
        (PROPRIETAIRE, 'Propriétaire'),
        (VENDEUR, 'Vendeur'),
        (ABONNE, 'Abonne'),
    ]

    type = models.IntegerField(choices=TYPE_CHOICES, default=PROPRIETAIRE)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'utilisateur'
