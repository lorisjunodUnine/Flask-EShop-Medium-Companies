from flask import Blueprint, render_template, redirect, flash,request, url_for
from app import db
from sqlalchemy.orm import joinedload
from ..models.models import Filiale, CommandeClient, Client, LigneCommandeClient, Article, SousCategorie, Categorie, SousSousCategorie, CommandeFiliale, LigneCommandeFiliale, LigneDemandeCentrale, LigneLivraisonFiliale, LigneLivraisonClient, LivraisonClient, LivraisonCentrale, LivraisonFiliale

filiale_bp = Blueprint('filiale', __name__, url_prefix="/filiale")

@filiale_bp.route('/dashboard')
def filiale_dashboard():
	return render_template('dashboard.html', user_type='filiale')

@filiale_bp.route('/list')
def filiale_list():
    all_filiales = Filiale.query.all()
    return render_template('filiale/list_filiale.html', filiales=all_filiales)

@filiale_bp.route('/filiale_dashboard')
def filiale_dashboard_cmd():
    filiale = Filiale.query.first()
    commandes = CommandeClient.query.filter_by(id_filiale=filiale.id_filiale).all()
    return render_template('filiale/filiale_dashboard.html', filiale=filiale, commandes_filiales=commandes)
@filiale_bp.route('/preparer-commande', methods=['GET', 'POST'])
def preparer_commande():
    commande_id = request.args.get('commande_id', type=int)
    if commande_id:
        return redirect(url_for('filiale.preparer_commande_detail', commande_id=commande_id))
    filiales = Filiale.query.all()
    commandes = []
    filiale_id = request.args.get('filiale_id', type=int)

    if filiale_id:
        commandes=CommandeClient.query.filter_by(id_filiale=filiale_id).all()
        filiale_sel= Filiale.query.get(filiale_id)
    else:
        filiale_sel=None
    return render_template('filiale/liste_commande_a_preparer.html', filiales=filiales,commandes=commandes,filiale_sel=filiale_sel)


@filiale_bp.route('/preparer-commande/<int:commande_id>', methods=['GET', 'POST'])
def preparer_commande_detail(commande_id):
    commande= CommandeClient.query.options(
        joinedload(CommandeClient.client),
        joinedload(CommandeClient.articles_choisis)).get_or_404(commande_id)
    if request.method == 'POST':
        for item in commande.articles_choisis:
            key= f'quantite_preparee_{item.id_ligne_commande_client}'
            qte_preparee_str = request.form.get(key, '0')
            try:
                qte_preparee = int(qte_preparee_str)
            except ValueError:
                qte_preparee = 0
            if qte_preparee < 0:
                qte_preparee = 0
            elif qte_preparee > item.quantite:
                qte_preparee = item.quantite
            item.quantite_preparee = qte_preparee
        total_commande = sum(a.quantite for a in commande.articles_choisis)
        print("DEBUG - commande.total_preparee type:", type(commande.total_preparee))
        total_preparee = sum(item.quantite_preparee for item in commande.articles_choisis)
        if total_preparee == total_commande:
            commande.id_statut_commande = 79767323
        elif total_preparee > 0:
            commande.id_statut_commande = 79767322
        else:
            commande.id_statut_commande = 79767321

        db.session.commit()

        flash('Préparation mise à jour!', 'success')
        return redirect(url_for('filiale.preparer_commande_detail', commande_id=commande_id))
    return render_template('filiale/preparer_commande_detail.html', commande=commande)

@filiale_bp.route('/demander-stock', methods=['POST'])
def demander_stock():
    pass

@filiale_bp.route('/commande/<int:commande_id>/commande_pret', methods=['POST', 'GET'])
def commande_pret(commande_id):
    commande = CommandeClient.query.get_or_404(commande_id)
    if commande.id_statut_paiement_commande !=3:
        flash("La commande doit encore être payée pour être marqueé comme prête à emporter", "danger")
        return redirect(url_for('filiale.preparer_commande'))
    if commande.id_mode_livraison == 34871891:
        commande.id_statut_commande = 79767324
    elif commande.id_mode_livraison == 34871892:
        commande.id_statut_commande = 79767325
    else: 
        flash('Mode de livraison non géré', 'warning')
        return redirect(url_for('preparer_commande'))
    db.session.commit()
    flash('Commande marquée comme prête', 'success')
    return redirect(url_for('filiale.preparer_commande'))

@filiale_bp.route('/commande/<int:commande_id>/livrer_ou_retirer_commande', methods=['POST', 'GET'])
def livrer_ou_retirer_commande(commande_id):
    commande = CommandeClient.query.get_or_404(commande_id)
    if commande.id_statut_paiement_commande !=3:
        flash("La commande doit encore être payée pour être marqueé comme prête à emporter", "danger")
        return redirect(url_for('filiale.preparer_commande'))
    if commande.id_mode_livraison == 34871891:
        commande.id_statut_commande = 79767328
    elif commande.id_mode_livraison == 34871892:
        commande.id_statut_commande = 79767327
    else: 
        flash('Mode de livraison non géré', 'warning')
        return redirect(url_for('filiale.preparer_commande'))
    db.session.commit()
    flash('Commande marquée comme livrée ou retirée', 'success')
    return redirect(url_for('filiale.preparer_commande'))
