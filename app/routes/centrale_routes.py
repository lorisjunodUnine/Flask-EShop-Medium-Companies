from flask import Blueprint, render_template
from ..models.models import Centrale, UserType, CommandeClient, CarteFidelite
centrale_bp = Blueprint('centrale', __name__, url_prefix="/centrale")

@centrale_bp.route('/dashboard')
def centrale_dashboard():
	return render_template('dashboard.html', user_type='centrale')

@centrale_bp.route('/list')
def centrale_list():
    all_centrales = Centrale.query.all()
    return render_template('centrale/list_centrale.html', centrales=all_centrales)


