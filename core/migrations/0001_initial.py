# Generated by Django 5.0 on 2024-01-06 21:59

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bouquet',
            fields=[
                ('id_bouquet', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remise', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('photo', models.ImageField(upload_to='uploads/Bouquet/')),
            ],
            options={
                'db_table': 'bouquet',
            },
        ),
        migrations.CreateModel(
            name='Famille',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
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
                ('code', models.CharField(max_length=255)),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remise', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('photo', models.ImageField(upload_to='uploads/parfum/')),
            ],
            options={
                'db_table': 'parfum',
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'Propriétaire'), (2, 'Vendeur'), (3, 'Abonne')], default=1)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'utilisateur',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
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
                ('date_commande', models.DateField(auto_now_add=True)),
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
                ('code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('origine', models.CharField(blank=True, max_length=255, null=True)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remise', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('photo', models.ImageField(upload_to='uploads/fleur/')),
                ('qt_stock', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('categorie', models.IntegerField(choices=[(1, 'Fleur'), (2, 'Plante')], default=1)),
                ('id_famille', models.ForeignKey(blank=True, db_column='famille', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.famille')),
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
                ('id_fleur', models.OneToOneField(db_column='id_fleur', on_delete=django.db.models.deletion.DO_NOTHING, to='core.fleur')),
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
