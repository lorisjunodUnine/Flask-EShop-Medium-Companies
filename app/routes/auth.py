from flask import Flask, Blueprint, request, render_template, redirect, session, url_for, flash
from ..models.models import Client, Centrale, Filiale, Fournisseur, UserType, db
from flask_login import login_user
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        user_type_libel = request.form.get('user_type')

        if not all([email, user_type_libel]):
            flash('Veuillez remplir tous les champs', 'erreur')
            return render_template('auth/login.html')
        
        user_type = UserType.query.filter_by(libel=user_type_libel).first()
        
        if not user_type:
            flash('Type d\'utlisateur invalide', 'error')
            return redirect(url_for('auth.login'))
        model_map ={
            'client': Client, 
            'centrale': Centrale,
            'filiale': Filiale,
            'fournisseur': Fournisseur
            }
        if user_type_libel not in model_map:
            flash('type inconnu', 'error')
            return redirect(url_for('auth.login'))
        user = db.session.query(model_map[user_type_libel]).filter_by(email=email).first()
        if user:
            session['user_type'] = user_type_libel
            session['user_name'] = user.nom
            if user_type_libel == 'client':
                session['user_id'] = user.id_client
            elif user_type_libel == 'centrale':
                session['user_id'] = user.id_centrale
            elif user_type_libel == 'filiale':
                session['user_id'] = user.id_filiale
            elif user_type_libel == 'fournisseur':
                session['user_id'] = user.id_fournisseur
            login_user(user)

            print("redirection vers la page welcome")
            return redirect(url_for('auth.welcome'))

        flash('Identifiant incorrect', 'erreur')
        return render_template('auth/login.html')
    return render_template('auth/login.html') 
        
@auth_bp.route('/auth/welcome')
def welcome():
    user_name = session.get('user_name', 'utilisateur')
    user_type = session.get('user_type', None)
    user_id = session.get('user_id', None)

    model_map ={
            'client': Client, 
            'centrale': Centrale,
            'filiale': Filiale,
            'fournisseur': Fournisseur
            }
    
    user_obj = None
    if user_type in model_map:
        user_obj = db.session.get(model_map[user_type], user_id)
    return render_template(
        'auth/welcome.html')
#        user_name = user_name,
#        user_type =user_type,
#        user_id = user_id,
#        user = user_obj
#    )
