from flask import Blueprint, render_template, session, flash, redirect, request, url_for
from ..models.models import Client, UserType, CommandeClient, CarteFidelite, LigneCommandeClient, Article, Categorie, SousCategorie, SousSousCategorie, Panier, ModePaiement, LignePanier, ModeLivraison, StatutCommande, Filiale
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin
import json
from app import db
client_bp = Blueprint('client', __name__, url_prefix="/client")


@client_bp.route('/dashboard')
def client_dashboard():
    user_type = session.get('user_type', None)
    return render_template('dashboard.html', user_type='client')

@client_bp.route('/client')
def client():
    user_type = session.get('user_type', None)
    all_clients = Client.query.all()
    return render_template('clients.html', clients=all_clients, user_type='client')

@client_bp.route('/client/<int:client_id>', methods=['GET'])
def client_profile(client_id):
    if session.get('user_type') != 'client':
        flash("Accès non autorisé", 'danger')
        return redirect(url_for('auth.login'))
    user_id = session.get('user_id')
    client = Client.query.get_or_404(user_id)
    commandesclient = CommandeClient.query.filter_by(client_id=client.id_client).all()
    return render_template('client/client_profile.html', user_type='client', client=client, commandesclient=commandesclient)#, user=client)

@client_bp.route('/list')
def client_list():
    all_clients = Client.query.all()
    return render_template('client/list_client.html', clients=all_clients)

@client_bp.route("/add/<id_article>", methods=['POST', 'GET'])
def ajouter_au_panier(id_article):
    if not current_user.is_authenticated:
        flash('You must login first! Login now!','error')
        return redirect(url_for('auth.login'))
    panier = Panier.query.filter_by(id_client=current_user.id_client).first()
    if not panier:
        panier = Panier(client=current_user)
        db.session.add(panier)
        db.session.flush()
    article = Article.query.get_or_404(id_article)

    quantite_str = request.form.get('quantite')
    if quantite_str and quantite_str.isdigit():
        quantite = int(quantite_str)
        panier.ajouter_article(article, quantite)
    else :
        delta_str = request.form.get('delta')
        if not delta_str or not delta_str.lstrip('-').isdigit():
            flash('modification de quantite invalide', 'error')
            return redirect(url_for(client.afficher_panier))
        delta=int(delta_str)
        actuel_qte = panier.quantite_article(article)
        nouvelle_qte = actuel_qte + delta
        panier.ajouter_article(article, nouvelle_qte)
        flash(f'{delta} x {article.nom_article} modifié dans le panier', 'success')
    db.session.commit()
    from_panier = request.form.get('from_panier', False)
    if from_panier == 'true':
        return redirect(url_for('client.afficher_panier'))
    else:
        return redirect(url_for('client.afficher_panier'))

@client_bp.route("/remove/<id_article>/<quantite>") 
def remove(id_article, quantite):
    if not current_user.is_authenticated:
        flash('You must login first! Login now!','error')
        return redirect(url_for('auth.login'))
    panier = Panier.query.filter_by(id_client=current_user.id_client).first()
    if not panier:
        flash('Aucun panier trouvé', 'error')
        return redirect(url_for('client.afficher_panier'))
    article = Article.query.get_or_404(id_article)
    panier.enlever_article(article, int(quantite))
    db.session.commit()
    flash('Article retiré du panier', 'success')
    return redirect(url_for('client.afficher_panier'))

@client_bp.route('/item/<int:id_article>')
def item(id_article):
	item = Article.query.get(id_article)
	return render_template('home/article_detail.html', item=item)

@client_bp.route("/panier")
@login_required
def afficher_panier():
    client = current_user
    modes_paiement = ModePaiement.query.all()
    modes_livraison = ModeLivraison.query.all()
    filiales = Filiale.query.all()
    if not modes_paiement:
        flash("Veuillez sélectionner un mode de paiement", "danger")
        return redirect(url_for('client.afficher_panier'))
    if not filiales:
        flash("Veuillez sélectionner une filiale", "danger")
        return redirect(url_for('client.afficher_panier'))
    panier = Panier.query.filter_by(id_client=current_user.id_client).first()
    if panier is None:
        lignes =[]
    else:
        db.session.refresh(panier)
        lignes = panier.lignes_panier.all()
        print(f"Lignes panier: {lignes}")
    prix = 0
    articles = []
    quantite = []
    price_ids = []
    for ligne in lignes:
        articles.append(ligne.article)
        quantite.append(ligne.quantite)
        #price_id_dict = {
		#	"prix_unitaire": ligne.article.prix_unitaire,
		#	"quantite": ligne.quantite,
		#	}
        price_ids.append({
            "prix_unitaire": ligne.article.prix_unitaire,
            "quantite" : ligne.quantite
        })
    articles_with_qty = list(zip(articles, quantite))
    prix = panier.montant_panier
    print(f"Lignes panier: {lignes}")
    return render_template('client/panier.html', client=client, articles=articles, prix=prix, price_ids=price_ids, quantite=quantite, articles_with_qty=articles_with_qty, modes_paiement=modes_paiement, modes_livraison=modes_livraison, filiales=filiales)


@client_bp.route('/valider_panier', methods=['POST', 'GET'])
@login_required
def valider_paiement():
    client = current_user
    panier = client.panier
    prix = panier.montant_panier
    statut_confirme = StatutCommande.query.filter_by(libel='Commande créée').first()
    if not statut_confirme:
        flash("le statut de la commande est introuvable", 'error')
        return redirect(url_for('client.afficher_panier'))
    modes_livraison = ModeLivraison.query.all()
    modes_paiement = ModePaiement.query.all()
    filiale_id_str = request.form.get('filiale_id', '').strip()
    if not filiale_id_str:
        flash('Veuillez sélectionner une filiale', 'warning')
        return redirect(url_for('client.afficher_panier'))
    try:
        filiale_id = int(filiale_id_str)
    except ValueError:
        flash('ID de filiale invalide', 'danger')
        return redirect(url_for('client.afficher_panier'))
    filiale = Filiale.query.get(filiale_id)
    if not filiale:
        flash('filiale introuvable', 'danger')
        return redirect(url_for('client.afficher_panier'))
    if request.method=='POST':
        mode_paiement_str = request.form.get('mode_paiement', '').strip()
        if not mode_paiement_str:
            flash("Veuillez sélectionner un mode de paiement", 'warning')
            return redirect(url_for('client.afficher_panier'))
        try:
            mode_id = int(mode_paiement_str)
        except ValueError:
            flash("Mode de paiement invalide", 'danger')
            return redirect(url_for('client.afficher_panier'))
        mode = ModePaiement.query.get(mode_id)
        if not mode:
            flash("Mode de paiement non trouvé", 'danger')
            return redirect(url_for('client.afficher_panier'))
        if mode.libel.lower() == 'compte_kaufmann':
            if panier.montant_panier > client.montant_initial:
                flash("Solde insuffisant", 'danger')
                return redirect(url_for('afficher_panier'))
            client.montant_initial -= panier.montant_panier
        
        print("Lignes panier au moment de générer commande:", panier.lignes_panier.all())
        commande = panier.generer_commande(statut=statut_confirme, mode_paiement=mode, filiale=filiale)
        for ligne in panier.lignes_panier.all():
            db.session.delete(ligne)
        db.session.flush()
        db.session.refresh(panier)
        print("Après commit, lignes panier:", panier.lignes_panier.all())
        db.session.commit()
        print("Après commit, lignes panier:", panier.lignes_panier.all())
        flash("Commande validée ‘", 'success')
        #return render_template('client/valider_panier.html', id_commande_client=commande.id_commande_client, 
        #                       modes_paiement=modes_paiement, modes_livraison=modes_livraison, prix=prix)
        return render_template('client/confirmation_commande.html', commande=commande)
    return redirect(url_for('client.afficher_panier'))
@client_bp.route('/confirmation_commande/<int:id_commande>')
@login_required
def confirmation_commande(id_commande):
    commande = CommandeClient.query.get_or_404(id_commande)
    return render_template('client/confirmation_commande.html', commande=commande)
