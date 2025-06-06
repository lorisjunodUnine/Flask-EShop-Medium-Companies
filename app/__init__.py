from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()

from app.models.models import *

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'un_secret'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/commande_K_db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['UPLOAD_FOLDER'] = 'static/media'

	db.init_app(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)
	@login_manager.user_loader
	def load_user(user_id):
		user_type, user_id_str = user_id.split(":")
		user_id = int(user_id_str)
		if user_type == 'client':
			return Client.query.get(user_id)
		elif user_type == 'filiale':
			return Filiale.query.get(user_id)
		elif user_type == 'centrale':
			return Centrale.query.get(user_id)
		elif user_type == 'fournisseur':
			return Fournisseur.query.get(user_id)
		return None

	
	from app.commands.init_db import init_db_command
	app.cli.add_command(init_db_command)

	@app.context_processor
	def inject_user_data():
		return dict(user_type=session.get('user_type'), user_id=session.get('user_id'), user_name=session.get('user_name'))

	from app.routes.home_routes import home_bp
	from app.routes.auth import auth_bp
	from app.routes.client_routes import client_bp
	from app.routes.filiale_routes import filiale_bp
	from app.routes.fournisseur_routes import fournisseur_bp
	from app.routes.centrale_routes import centrale_bp

	app.register_blueprint(home_bp)
	app.register_blueprint(auth_bp)
	app.register_blueprint(client_bp)
	app.register_blueprint(filiale_bp)
	app.register_blueprint(fournisseur_bp)
	app.register_blueprint(centrale_bp)

	
	return app

