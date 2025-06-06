from flask import Flask, Blueprint, request, render_template, redirect, session, url_for, flash
from app.models.models import Article, Categorie, SousCategorie, SousSousCategorie, Marque, Garantie, LigneCommandeClient, CommandeClient, Tag
from app import db
from sqlalchemy import inspect, func
from datetime import datetime
import json
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('home.html')

@home_bp.route('/categories')
def categories():
    id_categorie = request.args.get('id_categorie', type=int)
    id_sous_categorie = request.args.get('id_sous_categorie', type=int)

    all_categories = Categorie.query.all()
    sous_categories = SousCategorie.query.filter_by(id_categorie=id_categorie).all() if id_categorie else []
    sous_sous_categories = SousSousCategorie.query.filter_by(id_sous_categorie=id_sous_categorie).all() if id_sous_categorie else []

    return render_template(
        'categorie.html',
        categories=all_categories,
        sous_categories=sous_categories,
        sous_sous_categories=sous_sous_categories,
        selected_categorie=id_categorie,
        selected_sous_categorie=id_sous_categorie
    )

@home_bp.route('/articles', methods=['GET', 'POST'])
def articles(): 
    selected_categorie = request.args.get('libel_categorie')
    selected_marque = request.args.get('libel_marque')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    tag_string = []
    if request.method == 'POST':
        raw_tags = request.form.get("tags")
        if raw_tags:
            tag_string = json.loads(raw_tags)
            print("tags recus :", tag_string)
        for tag in tag_string:
            libel = tag['libel']
            color = tag['color']
            print(f"tag : {libel}, couleur : {color}")


    query = Article.query

    if selected_categorie:
        query = query.join(Categorie).filter(Categorie.libel_categorie == selected_categorie)
    if selected_marque:
        query = query.join(Marque).filter(Marque.libel_marque == selected_marque)
    if min_price is not None:
        query = query.filter(Article.prix_unitaire >= min_price)
    if max_price is not None:
        query = query.filter(Article.prix_unitaire <= max_price)

    articles = query.all()
    categories = Categorie.query.all()
    marques = Marque.query.all()
    class DummyCommandes:
        commande_id = 1
    commande = DummyCommandes()
    return render_template('articles.html', articles=articles, commande=commande, categories=categories, marques=marques, tag_string=tag_string)

@home_bp.route('/article/<int:id_article>', methods=['GET', 'POST'])
def article_detail(id_article):
    article = Article.query.get_or_404(id_article)
    reference_date = request.args.get('reference_date')
    #tag_string = []

    #if request.method == 'POST':
    #    raw_tags = request.form.get("tags")
    #    print("Contenu brut des tags :", raw_tags)
    #    print("Requête POST reçue")
    #    if raw_tags:
    #        try:
    #            print('tags recus:', tag_string)
    ##            tag_string = json.loads(raw_tags)
    #            if isinstance(tag_string, list):
    #                Tag.query.filter_by(id_article=id_article).delete()
    ##                db.session.commit()
    #                for tag in tag_string:
    #                    libel = tag['libel']
    #                    color = tag['color']
    #                    new_tag = Tag(id_article=id_article, libel=libel, color=color)
    #                    db.session.add(new_tag)
    #                db.session.commit()
    #                print("Tags mis à jour.")
    #            else:
    #                print("Format invalide : les tags ne sont pas une liste.")
    #        except Exception as e:
    #            print("Erreur JSON :", e)
    #tags_en_base = Tag.query.filter_by(id_article=id_article).all()
    #tag_string = [{'libel':t.libel, 'color':t.color} for t in tags_en_base]
    if request.method == 'POST':
        # Les tags envoyés dans un champ caché JSON string
        tags_json = request.form.get('tags')
        if tags_json:
            try:
                tags_list = json.loads(tags_json)
            except Exception as e:
                flash("Erreur lors du traitement des tags.", "danger")
                return redirect(url_for('home.article_detail', id_article=id_article))

            # id_category_default à adapter selon ta logique (exemple 1)
            id_category_default = 1

            # Synchronise les tags de l'article avec ceux reçus
            Tag.add_tags_to_entity(article, tags_list, id_category_default)
            flash("Tags mis à jour avec succès.", "success")
            return redirect(url_for('home.article_detail', id_article=id_article))

    # Pour le GET, on prépare la variable tag_string pour le JS
    # Convertir les tags SQLAlchemy en liste de dicts
    tag_string = [
        {'libel': tag.libel, 'color': tag.color} for tag in article.tags
    ]
    ventes_sorties = db.session.query(
        func.coalesce(func.sum(LigneCommandeClient.quantite),0)).join(CommandeClient).filter(LigneCommandeClient.id_article == id_article)

    if reference_date:
        reference_date = datetime.strptime(reference_date, '%Y-%m-%d').date()
        ventes_sorties = ventes_sorties.filter(CommandeClient.date <= reference_date)

    vente_sorties_total = ventes_sorties.scalar() or 0
    return render_template(
        'article_detail.html',
        article=article,
        reference_date=reference_date,
        vente_sorties_total=vente_sorties_total, tag_string=tag_string)
    


        



