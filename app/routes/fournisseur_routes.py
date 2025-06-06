from flask import Blueprint, render_template, session, request, redirect, flash
from ..models.models import Fournisseur, UserType

fournisseur_bp = Blueprint('fournisseur', __name__, url_prefix="/fournisseur")

@fournisseur_bp.route('/dashboard')
def filiale_dashboard():
	return render_template('dashboard.html', user_type='fournisseur')

@fournisseur_bp.route('/list')
def fournisseur_list():
    all_fournisseurs = Fournisseur.query.all()
    user_type = session.get('user_type', None)
    return render_template('fournisseur/list_fournisseur.html', fournisseurs=all_fournisseurs, user_type=user_type)

@fournisseur_bp.route('/fournisseur/<int:client_id>')
def fournisseur_profile(client_id):
    user_type = session.get('user_type', None)
    client = Client.query.get_or_404(client_id)
    commande = CommandeClient.query.filter_by(client_id=client.id_client).all()
    return render_template('client_profile.html', user_type='client', client=client, commande=commande)


