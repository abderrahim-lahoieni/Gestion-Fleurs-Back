# Generated by Django 5.0 on 2024-01-03 10:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'Propriétaire'), (2, 'Vendeur'), (3, 'Abonne')], default=1)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255, unique=True)),
                ('reset_code', models.CharField(blank=True, max_length=4, null=True)),
                ('reset_code_expiry', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'utilisateur',
            },
        ),
        migrations.CreateModel(
            name='Bouquet',
            fields=[
                ('id_bouquet', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('image', models.BinaryField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remise', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'bouquet',
            },
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('nom', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'famille',
            },
        ),
        migrations.CreateModel(
            name='Magasin',
            fields=[
                ('id_magasin', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('fax', models.CharField(blank=True, max_length=255, null=True)),
                ('telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'magasin',
            },
        ),
        migrations.CreateModel(
            name='Parfum',
            fields=[
                ('id_parfum', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remise', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'parfum',
            },
        ),
        migrations.CreateModel(
            name='Abonne',
            fields=[
                ('id_abonne', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=255, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('id_user', models.ForeignKey(blank=True, db_column='id_user', default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'abonne',
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id_commande', models.AutoField(primary_key=True, serialize=False)),
                ('date_commande', models.DateField()),
                ('telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('statut', models.CharField(blank=True, max_length=255, null=True)),
                ('adresse_livraison', models.CharField(blank=True, max_length=255, null=True)),
                ('id_commandant', models.ForeignKey(blank=True, db_column='id_commandant', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'commande',
            },
        ),
        migrations.CreateModel(
            name='Fleur',
            fields=[
                ('id_fleur', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
                ('origine', models.CharField(blank=True, max_length=255, null=True)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remise', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('photo', models.ImageField(upload_to='uploads/')),
                ('qt_stock', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('categorie', models.IntegerField(choices=[(1, 'Fleur'), (2, 'Plante')], default=1)),
                ('id_famille', models.ForeignKey(blank=True, db_column='id_categorie', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.famille')),
            ],
            options={
                'db_table': 'fleur',
                'unique_together': {('nom', 'categorie')},
            },
        ),
        migrations.CreateModel(
            name='Fichesoin',
            fields=[
                ('id_fichesoin', models.AutoField(primary_key=True, serialize=False)),
                ('instruction_entretien', models.TextField(blank=True, null=True)),
                ('frequence_arosage', models.TextField(blank=True, null=True)),
                ('exposition_lumiere', models.TextField(blank=True, null=True)),
                ('temperature_ideal', models.TextField(blank=True, null=True)),
                ('engrais_commandes', models.TextField(blank=True, null=True)),
                ('id_fleur', models.OneToOneField(blank=True, db_column='id_fleur', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.fleur')),
            ],
            options={
                'db_table': 'fichesoin',
            },
        ),
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id_lignecommande', models.AutoField(primary_key=True, serialize=False)),
                ('produit_id', models.IntegerField(blank=True, null=True)),
                ('type_produit', models.CharField(blank=True, max_length=255, null=True)),
                ('quantite_commande', models.IntegerField(blank=True, null=True)),
                ('commande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.commande')),
            ],
            options={
                'db_table': 'ligne_commande',
                'unique_together': {('commande', 'produit_id', 'type_produit')},
            },
        ),
    ]
