import click
from flask import current_app
from flask.cli import with_appcontext
from app import db
from app.models.models import Article, Categorie, SousCategorie, SousSousCategorie, Client, CarteFidelite, Panier, LignePanier, Marque, Garantie, LigneCommandeClient, CommandeClient, LigneLivraisonClient, LivraisonClient, ModeLivraison, StatutCommande, StatutPaiementCommande, StatutLivraison, ModePaiement, Coupon, ModeCommunication, Magasin, Centrale, LigneDemandeCentrale, DemandeCentrale, LigneLivraisonCentrale, LivraisonCentrale, Filiale, LigneLivraisonFiliale, LivraisonFiliale, LigneCommandeFiliale, CommandeFiliale, Fournisseur, LigneCommandeFournisseur, CommandeFournisseur, LigneLivraisonFournisseur, LivraisonFournisseur
import pymysql


@click.command("init-db")
@with_appcontext
def init_db_command():
    try:
        connection = pymysql.connect(                
            host='localhost',
            user='root',
            password='root',
            port=8889
        )
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS commande_K_db " \
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        db_connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            port=8889,
            database='commande2_db'
        )
        db_connection.close()
        db.create_all()
        click.echo("Base de données initialisées")

            #db_connection = pymysql.connect(
            #    host='localhost',
            #    password='root',
            #    user='root',
            #    port=8889,
            #    database='commande_K_db'
            #)
            
    except Exception as e:
        print(f"Erreur de l'initialisation : {str(e)}")
        db.session.rollback()
