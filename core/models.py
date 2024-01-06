from django.db import models
from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
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
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'utilisateur'

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

class Famille(models.Model):
    nom = models.CharField( primary_key=True,max_length=255)

    def __str__(self):
        return self.nom 
    
    class Meta:
        db_table = 'famille'


class Fleur(models.Model):
    id_fleur = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=255)
    origine = models.CharField(max_length=255, blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    remise = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/')
    qt_stock = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    id_famille = models.ForeignKey(Famille, models.DO_NOTHING, db_column='famille', blank=True, null=True)
    
    FLEUR = 1
    PLANTE = 2
    TYPE_CHOICES = [
        (FLEUR, 'Fleur'),
        (PLANTE, 'Plante')
    ]
    categorie = models.IntegerField(choices=TYPE_CHOICES, default=FLEUR)

    def __str__(self):
        return f"{self.nom} de Catégorie {self.categorie}"
        
    class Meta:
        db_table = 'fleur'
        unique_together = (('nom', 'categorie'),)

    def save(self, *args, **kwargs):
        if not self.code:
            # Find the latest code in the database
            latest_code = Fleur.objects.order_by('-id_fleur').first()
            if latest_code:
                latest_code = latest_code.code
                # Extract the numeric part of the code and increment it
                code_number = int(''.join(filter(str.isdigit, latest_code)))
                code_number += 1
            else:
                # If there are no existing instances, start with 0
                code_number = 0

            # Format the code and save it
            self.code = f'FL{code_number:03d}'

        super(Fleur, self).save(*args, **kwargs)

class Fichesoin(models.Model):
    id_fichesoin = models.AutoField(primary_key=True)    
    instruction_entretien = models.TextField(blank=True, null=True)
    frequence_arosage = models.TextField(blank=True, null=True)
    exposition_lumiere = models.TextField(blank=True, null=True)
    temperature_ideal = models.TextField(blank=True, null=True)
    engrais_commandes = models.TextField(blank=True, null=True)
    id_fleur = models.OneToOneField('Fleur', models.DO_NOTHING, db_column='id_fleur')
    
    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'fichesoin'


from django.db import models




class Commande(models.Model):
    id_commande = models.AutoField(primary_key=True)
    date_commande = models.DateField(auto_now_add=True)
    id_commandant = models.ForeignKey('Utilisateur', models.DO_NOTHING, db_column='id_commandant', blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    statut = models.CharField(max_length=255, blank=True, null=True)
    adresse_livraison = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'commande'

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


