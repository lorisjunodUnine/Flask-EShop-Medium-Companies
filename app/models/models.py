from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import enum
db = SQLAlchemy()

#Model 1 - 4
class Article(db.Model):
    __tablename__ = 'article'
    id_article = db.Column(db.BigInteger, primary_key=True, nullable=True, unique=True)
    id_categorie = db.Column(db.Integer, db.ForeignKey('categorie.id_categorie'))
    id_sous_categorie = db.Column(db.Integer, db.ForeignKey('sous_categorie.id_sous_categorie'))
    id_sous_sous_categorie = db.Column(db.Integer, db.ForeignKey('sous_sous_categorie.id_sous_sous_categorie'))
    id_marque = db.Column(db.Integer, db.ForeignKey('marque.id_marque'))
    id_garantie = db.Column(db.Integer, db.ForeignKey('garantie.id_garantie'))
    nom_article = db.Column(db.String(100))
    article_description = db.Column(db.String(300))
    prix_unitaire = db.Column(db.Float, nullable=True)
    unite = db.Column(db.String(10))
    poids = db.Column(db.String(10))
    dimension = db.Column(db.String(150))
    longueur = db.Column(db.Integer)
    largeur = db.Column(db.Integer)
    hauteur = db.Column(db.Integer)
    unite_dimension = db.Column(db.String(10))
    image_url = db.Column(db.String(100))
    
    lignes_commandes_client = db.relationship('LigneCommandeClient', back_populates='articles_commandes_client')
    lignes_livraisons_client = db.relationship('LigneLivraisonClient', back_populates='articles_livraisons_client')
    
    lignes_demandes_centrale = db.relationship('LigneDemandeCentrale', back_populates='articles_demandes_centrale')
    lignes_livraisons_centrale = db.relationship('LigneLivraisonCentrale', back_populates='articles_livraisons_centrale')

    lignes_commandes_filiale = db.relationship('LigneCommandeFiliale', back_populates='articles_commandes_filiale')
    lignes_livraisons_filiale = db.relationship('LigneLivraisonFiliale', back_populates='articles_livraisons_filiale')

    lignes_commandes_fournisseur = db.relationship('LigneCommandeFournisseur', back_populates='articles_commandes_fournisseur')
    lignes_livraisons_fournisseur = db.relationship('LigneLivraisonFournisseur', back_populates='articles_livraisons_fournisseur')
    
    tags = db.relationship('Tag', back_populates='article', cascade='all, delete-orphan')
    
    sous_sous_categorie = db.relationship('SousSousCategorie', back_populates='articles')
    sous_categorie = db.relationship('SousCategorie', back_populates='articles')
    categorie = db.relationship('Categorie', back_populates='articles')
    marque = db.relationship('Marque', back_populates='articles')
    garantie = db.relationship('Garantie', back_populates='articles')
    def __repr__(self):
        return(f'<Article {self.nom_article}>')
      
class Categorie(db.Model):
    __tablename__= 'categorie'
    id_categorie = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libel_categorie = db.Column(db.String(100))
    tva = db.Column(db.Float)
    description = db.Column(db.String(200))

    articles = db.relationship('Article', back_populates='categorie')
    sous_categories = db.relationship('SousCategorie', back_populates='categorie')
    def __repr__(self):
        return f'<Categorie {self.libel_categorie}, TVA {self.tva}>'
class SousCategorie(db.Model):
    __tablename__= 'sous_categorie'
    id_sous_categorie = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_categorie = db.Column(db.Integer, db.ForeignKey('categorie.id_categorie'))
    libel_sous_categorie = db.Column(db.String(100))
    description = db.Column(db.String(200))

    articles = db.relationship('Article', back_populates='sous_categorie')
    categorie = db.relationship('Categorie', back_populates='sous_categories')
    sous_sous_categories = db.relationship('SousSousCategorie', back_populates='sous_categorie')

    def __repr__(self):
        return f'<SousCategorie {self.libel_sous_categorie}>'
class SousSousCategorie(db.Model):
    __tablename__ = 'sous_sous_categorie'
    id_sous_sous_categorie = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sous_categorie = db.Column(db.Integer, db.ForeignKey('sous_categorie.id_sous_categorie'))
    libel_sous_sous_categorie = db.Column(db.String(100))
    description = db.Column(db.String(200))

    articles = db.relationship('Article', back_populates='sous_sous_categorie')
    sous_categorie = db.relationship('SousCategorie', back_populates='sous_sous_categories')

    def __repr__(self):
        return f'<SousSousCategorie {self.libel_sous_sous_categorie}>'
#Model 5 - 10
class Marque(db.Model):
    __tablename__= 'marque'
    id_marque = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libel_marque = db.Column(db.String(100))
    articles = db.relationship('Article', back_populates='marque')

    def __repr__(self):
        return f'<Marque {self.libel_marque}>'    
class Garantie(db.Model):
    __tablename__ = 'garantie'
    id_garantie = db.Column(db.Integer, primary_key=True)
    libel_garantie = db.Column(db.String(100))

    articles = db.relationship('Article', back_populates='garantie')

    def __repr__(self):
        return f'<Garantie {self.libel_garantie}>'
class UserType(db.Model):
    __tablename__ = 'user_type'
    id_user_type = db.Column(db.Integer, primary_key=True)
    libel = db.Column(db.String(20), unique =True)



class Client(db.Model, UserMixin):
    __tablename__ = 'client'
    id_client = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    adresse = db.Column(db.String(100))
    numero = db.Column(db.Integer)
    code_postal = db.Column(db.Integer)
    commune = db.Column(db.String(100))
    canton = db.Column(db.String(5))
    id_pays = db.Column(db.Integer, db.ForeignKey('pays.id_pays'))
    telephone = db.Column(db.Integer)
    email = db.Column(db.String(100))
    id_carte_fidelite = db.Column(db.Integer, db.ForeignKey('carte_fidelite.id_carte_fidelite'))
    montant_initial = db.Column(db.Float)
    id_user_type = db.Column(db.Integer, db.ForeignKey('user_type.id_user_type'), default='1')
    
    panier = db.relationship('Panier', back_populates='client', uselist=False)
    commandes = db.relationship('CommandeClient', back_populates='client')
    livraisons_client = db.relationship('LivraisonClient', back_populates='client')
    carte_fidelite = db.relationship('CarteFidelite', back_populates='clients')
    user_type = db.relationship('UserType')

    def __repr__(self):
        return f'<Client {self.nom}>'
    def peut_payer(self):
        return self.montant_initial >= self.panier.montant_panier
    def payer(self):
        if self.peut_payer():
            self.montant_initial -=self.panier.montant_panier
            self.panier_vider()
            db.session.commit()
            return True
        return False
    def get_id(self):
        return f"client:{self.id_client}"
class CarteFidelite(db.Model):
    __tablename__='carte_fidelite'
    id_carte_fidelite = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)

    clients = db.relationship('Client', back_populates='carte_fidelite', uselist=False)

class ModePaiement(db.Model):
    __tablename__='mode_paiement'
    id_mode_paiement = db.Column(db.Integer, primary_key=True)
    libel = db.Column(db.String(50))
    #paniers = db.relationship('Panier', back_populates='mode_paiement')

class StatutCommande(db.Model):
    __tablename__='statut_commande'
    id_statut_commande = db.Column(db.Integer, primary_key=True)
    libel = db.Column(db.String(50), default='Commande créée')
    order = db.Column(db.Integer)
    orderlibel_categorie = db.Column(db.String(50))

    historique_precedent = db.relationship('HistoriqueStatutCommande', foreign_keys='HistoriqueStatutCommande.id_statut_commande_prec', back_populates='statut_precedent')
    historique_suivant = db.relationship('HistoriqueStatutCommande', foreign_keys='HistoriqueStatutCommande.id_statut_commande_suiv', back_populates='statut_suivant')

class TagCategory(db.Model):
    __tablename__ = 'tag_category'
    id_category = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    label = db.Column(db.String(50), nullable=False)

class Tag(db.Model):
    __tablename__='tag'
    id_tag = db.Column(db.Integer, primary_key=True)
    libel = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(8))
    id_category = db.Column(db.Integer, db.ForeignKey('tag_category.id_category'), nullable=False)
    id_article = db.Column(db.Integer, db.ForeignKey('article.id_article'))

    article = db.relationship('Article', back_populates='tags')
    category = db.relationship('TagCategory', backref='tags')
    @classmethod
    def add_tags_to_entity(cls, entity, tags_list, id_category_default):
        # On suppose que entity.tags existe (relation SQLAlchemy)
        # Synchroniser les tags existants avec la liste reçue

        # Libellés des tags envoyés (en minuscule pour comparaison)
        new_libels = {tag_data['libel'].strip().lower() for tag_data in tags_list}

        # Supprimer les tags qui ne sont plus dans la nouvelle liste
        for tag in list(entity.tags):  # on fait list() car on modifie pendant l'itération
            if tag.libel.lower() not in new_libels:
                entity.tags.remove(tag)
                db.session.delete(tag)

        # Ajouter les tags nouveaux qui n'existent pas déjà
        existing_libels = {tag.libel.lower() for tag in entity.tags}

        for tag_data in tags_list:
            libel = tag_data['libel'].strip()
            color = tag_data.get('color', '#000000')

            if libel.lower() not in existing_libels:
                new_tag = cls(libel=libel, color=color, id_category=id_category_default)
                # Associer au bon attribut selon le type d'entité
                # Ici exemple pour Article:
                if hasattr(entity, 'tags'):
                    entity.tags.append(new_tag)
                db.session.add(new_tag)

        db.session.commit()

    @classmethod
    def remove_tag_from_entity(cls, entity, libel):
        tag_to_remove = next((t for t in entity.tags if t.libel.lower() == libel.lower()), None)
        if tag_to_remove:
            entity.tags.remove(tag_to_remove)
            db.session.delete(tag_to_remove)
            db.session.commit()

class HistoriqueStatutCommande(db.Model):
    __tablename__ = 'historique_statut_commande'
    id_hsc = db.Column(db.BigInteger, primary_key=True)
    id_commande_client = db.Column(db.Integer, db.ForeignKey('commande_client.id_commande_client'))
    id_statut_commande_prec = db.Column(db.Integer, db.ForeignKey('statut_commande.id_statut_commande'))
    id_statut_commande_suiv = db.Column(db.Integer, db.ForeignKey('statut_commande.id_statut_commande'))
    date_change = db.Column(db.DateTime)

    statut_precedent = db.relationship('StatutCommande', foreign_keys='HistoriqueStatutCommande.id_statut_commande_prec', back_populates='historique_precedent')
    statut_suivant = db.relationship('StatutCommande', foreign_keys = 'HistoriqueStatutCommande.id_statut_commande_suiv', back_populates='historique_suivant')
    commande = db.relationship('CommandeClient', back_populates='historique_statuts')

    def _repr_(self):
        return f"<HistoriqueStatutCommande {self.id_commande_client} - {self.statut_commande.libel} @ {self.date_changement}>"
class LignePanier(db.Model):
    __tablename__ = 'ligne_panier'
    id_ligne_panier = db.Column(db.Integer, primary_key=True)
    id_panier = db.Column(db.Integer, db.ForeignKey('panier.id_panier'))
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite =  db.Column(db.Integer, nullable=False)
    article = db.relationship('Article')
    panier = db.relationship('Panier', back_populates='lignes_panier')
    @property
    def total_ligne(self):
        return self.quantite * self.article.prix_unitaire

class Panier(db.Model):
    __tablename__ = 'panier'
    id_panier = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'), unique=True)
    client = db.relationship('Client', back_populates='panier')
   # id_mode_paiement = db.Column(db.Integer, db.ForeignKey('mode_paiement.id_mode_paiement'))
    lignes_panier = db.relationship('LignePanier', back_populates='panier', cascade='all, delete-orphan', lazy='dynamic')
    #mode_paiement = db.relationship('ModePaiement', back_populates='paniers')
    
    def ajouter_article(self, article, quantite=1):
        if quantite < 1:
            return #
        ligne = next((l for l in self.lignes_panier.all() if l.id_article == article.id_article), None)
        if ligne:
            ligne.quantite = quantite
        else:
            ligne = LignePanier(id_panier=self.id_panier, id_article=article.id_article, quantite=quantite)
            db.session.add(ligne)
            print(f"Ajout article: {article.nom_article} | qte={quantite} | panier={self.id_panier}")
    def quantite_article(self, article):
        item = next((item for item in self.lignes_panier.all() if item.id_article == article.id_article), None)
        return item.quantite if item else 0
    def enlever_article(self, article, quantite=1):
        ligne = next((l for l in self.lignes_panier.all() if l.id_article == article.id_article), None)
        if ligne:
            ligne.quantite -= quantite
            if ligne.quantite <= 0:
                db.session.delete(ligne)
        db.session.flush()
    def vider(self):
        for ligne in self.lignes_panier.all():
            db.session.delete(ligne)
        db.session.flush()
    @property
    def montant_panier(self):
        return sum(ligne.total_ligne for ligne in self.lignes_panier.all())
    def generer_commande(self, statut : StatutCommande, mode_paiement: ModePaiement = None, filiale : 'Filiale'=None):
        if not self.lignes_panier.count():
            raise ValueError("Le panier est vide")
        commande = CommandeClient(
            client=self.client,
            id_statut_commande = statut.id_statut_commande,
            mode_paiement=mode_paiement, filiale=filiale
        
        )
        for ligne in self.lignes_panier.all():
            ligne_commande = LigneCommandeClient(
                id_article=ligne.article.id_article,
                quantite=ligne.quantite,
                prix_unitaire=ligne.article.prix_unitaire,
                commande_client=commande
            )
            db.session.add(ligne_commande)
            commande.articles_choisis.append(ligne_commande)
        db.session.add(commande)
        #db.session.commit()
        return commande

#Model 11 - 20
class LigneCommandeClient(db.Model): #OrderItem
    __tablename__ = 'ligne_commande_client' #order_item
    id_ligne_commande_client = db.Column(db.Integer, primary_key=True)
    id_commande_client = db.Column(db.Integer, db.ForeignKey('commande_client.id_commande_client')) #order_id
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite = db.Column(db.Integer)
    quantite_preparee = db.Column(db.Integer)
    prix_unitaire = db.Column(db.Integer, nullable = False)

    articles_commandes_client = db.relationship('Article', back_populates='lignes_commandes_client') #order_item
    commande_client = db.relationship('CommandeClient', back_populates='articles_choisis')#, backref='ligne_commande_client')
    @property
    def sous_total(self):
        return self.article.prix_unitaire * self.quantite
class CommandeClient(db.Model):
    __tablename__ = 'commande_client'
    id_commande_client = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id_client'))
    id_filiale = db.Column(db.Integer, db.ForeignKey('filiale.id_filiale'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    id_coupon = db.Column(db.Integer, db.ForeignKey('coupon.id_coupon'))
    id_mode_livraison = db.Column(db.Integer, db.ForeignKey('mode_livraison.id_mode_livraison'))
    id_statut_commande =db.Column(db.Integer, db.ForeignKey('statut_commande.id_statut_commande'))
    id_mode_paiement = db.Column(db.Integer, db.ForeignKey('mode_paiement.id_mode_paiement'))
    id_statut_paiement_commande = db.Column(db.Integer, db.ForeignKey('statut_paiement_commande.id_statut_paiement_commande'), nullable=False, default=1)
    id_mode_communication = db.Column(db.Integer, db.ForeignKey('mode_communication.id_mode_communication'))
    
    articles_choisis = db.relationship('LigneCommandeClient', back_populates='commande_client')#back_populates='commande', lazy='dynamic')
    livraisons_client = db.relationship('LivraisonClient', back_populates='commande_client')
    client = db.relationship('Client', back_populates='commandes', lazy="joined")
    mode_livraison = db.relationship('ModeLivraison', backref='mode_livraison')
    statut_commande = db.relationship('StatutCommande', backref='commande_statut')
    mode_paiement = db.relationship('ModePaiement', backref='mode_paiement')
    statut_paiement_commande = db.relationship('StatutPaiementCommande', backref='commande_statut_paiement')
    filiale = db.relationship('Filiale', backref='commandes')
    historique_statuts = db.relationship('HistoriqueStatutCommande', back_populates='commande', order_by='HistoriqueStatutCommande.date_change.desc()')
    
    @property
    def total_preparee(self):
        return sum(ligne.quantite_preparee for ligne in self.articles_choisis)  
    @property
    def montant_total(self):
        if not self.articles_choisis:
            return 0
        return sum(ligne.article.prix_unitaire * ligne.quantite for ligne in self.articles_choisis)
    def changer_statut(self, commande_id, ancien_id, nouvel_id):
        ancien_id = self.id_statut_commande
        if ancien_id != nouvel_id:
            self.id_statut_commande = nouvel_id
            Filiale.enregistrer_changement_statut(self, commande_id, ancien_id, nouvel_id)
            db.session.commit()

class LigneLivraisonClient(db.Model):
    __tablename__ = 'ligne_livraison_client'
    id_ligne_livraison_client = db.Column(db.Integer, primary_key=True)
    id_livraison_client = db.Column(db.Integer, db.ForeignKey('livraison_client.id_livraison_client'))
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite_livre = db.Column(db.Integer)
    articles_livraisons_client = db.relationship('Article', back_populates='lignes_livraisons_client')
    livraisons_client = db.relationship('LivraisonClient', back_populates='lignes_livraison_client')
class LivraisonClient(db.Model):
    __tablename__='livraison_client'
    id_livraison_client = db.Column(db.Integer, primary_key=True)
    id_commande_client = db.Column(db.Integer, db.ForeignKey('commande_client.id_commande_client'))
    id_client = db.Column(db.Integer, db.ForeignKey('client.id_client'))
    date_livraison = db.Column(db.DateTime)
    id_statut_commande = db.Column(db.Integer)
    id_statut_livraison = db.Column(db.Integer, db.ForeignKey('statut_livraison.id_statut_livraison'))


    commande_client = db.relationship('CommandeClient', back_populates ='livraisons_client')
    lignes_livraison_client = db.relationship('LigneLivraisonClient', back_populates='livraisons_client')
    statut_livraison = db.relationship('StatutLivraison', back_populates='livraisonclient')
    client = db.relationship('Client', back_populates='livraisons_client')

class ModeLivraison(db.Model):
    __tablename__ = 'mode_livraison'
    id_mode_livraison = db.Column(db.Integer, primary_key=True)
    libel = db.Column(db.String(50))


class StatutPaiementCommande(db.Model):
    __tablename__ = 'statut_paiement_commande'
    id_statut_paiement_commande = db.Column(db.Integer, primary_key=True)
    libel = db.Column(db.String(20))

class StatutLivraison(db.Model):
    __tablename__ = 'statut_livraison'
    id_statut_livraison = db.Column(db.Integer, primary_key = True)
    libel = db.Column(db.String(25))


    livraisons_fournisseur = db.relationship('LivraisonFournisseur', back_populates='statut_livraison')
    livraisoncentrale = db.relationship('LivraisonCentrale', back_populates='statut_livraison')
    livraisonfiliale = db.relationship('LivraisonFiliale', back_populates='statut_livraison')
    livraisonclient = db.relationship('LivraisonClient', back_populates='statut_livraison')



class Coupon(db.Model):
    __tablename__='coupon'
    id_coupon = db.Column(db.Integer, primary_key=True)
    libel=db.Column(db.String(50))

class ModeCommunication(db.Model):
    __tablename__='mode_communication'
    id_mode_communication = db.Column(db.Integer, primary_key=True)
    libel = db.Column(db.String(50))
#Model 21 - 27

class Pays(db.Model):
    __tablename__='pays'
    id_pays=db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    code_iso = db.Column(db.String(3))
    
class Magasin(db.Model):
    __tablename__='magasin'
    id_magasin = db.Column(db.Integer, primary_key=True)
    nom= db.Column(db.String(50))
class Centrale(db.Model, UserMixin):
    __tablename__='centrale'
    id_centrale = db.Column(db.Integer, primary_key=True)
    id_magasin = db.Column(db.Integer, db.ForeignKey('magasin.id_magasin'))
    nom=db.Column(db.String(50))
    adresse = db.Column(db.String(100))
    numero = db.Column(db.Integer)
    code_postal = db.Column(db.Integer)
    commune = db.Column(db.String(100))
    canton = db.Column(db.String(5))
    telephone = db.Column(db.Integer)
    email = db.Column(db.String(100))
    id_pays = db.Column(db.Integer, db.ForeignKey('pays.id_pays'))
    id_user_type = db.Column(db.Integer, db.ForeignKey('user_type.id_user_type'), default='2')
    
    livraisons_centrale = db.relationship('LivraisonCentrale', back_populates='centrale')
    demandes_centrale = db.relationship('DemandeCentrale', back_populates='centrale')
    user_type = db.relationship('UserType')

    def get_id(self):
        return f"centrale:{self.id_centrale}"
class LigneDemandeCentrale(db.Model):
    __tablename__= 'ligne_demande_centrale'
    id_ligne_demande_centrale = db.Column(db.Integer, primary_key=True)
    id_demande_centrale = db.Column(db.Integer, db.ForeignKey('demande_centrale.id_demande_centrale'))
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite_cmd = db.Column(db.Integer)
    demande_central = db.relationship('DemandeCentrale', back_populates='lignes_demande')
    articles_demandes_centrale = db.relationship('Article', back_populates='lignes_demandes_centrale')



class DemandeCentrale(db.Model):
    __tablename__ = 'demande_centrale'
    id_demande_centrale = db.Column(db.Integer, primary_key=True)
    id_centrale = db.Column(db.Integer, db.ForeignKey('centrale.id_centrale'))
    id_filiale = db.Column(db.Integer, db.ForeignKey('filiale.id_filiale'))
    statut = db.Column(db.String(20), default='en_attente') #en_attente, prepartion, expediee, livree
    date_demande = db.Column(db.Date)


    lignes_demande = db.relationship('LigneDemandeCentrale', back_populates='demande_central')
    centrale = db.relationship('Centrale', back_populates='demandes_centrale')

class LigneLivraisonCentrale(db.Model):
    __tablename__ = "ligne_livraison_centrale"
    id_ligne_livraison_centrale = db.Column(db.Integer, primary_key=True)
    id_livraison_centrale = db.Column(db.Integer, db.ForeignKey('livraison_centrale.id_livraison_centrale'))
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite_livree = db.Column(db.Integer)
    quantite_cmd =db.Column(db.Integer)
    
    

    livraison_centrale = db.relationship('LivraisonCentrale', back_populates='lignes_livraison_centrale')
    articles_livraisons_centrale = db.relationship('Article', back_populates='lignes_livraisons_centrale')
class LivraisonCentrale(db.Model):
    __tablename__ = 'livraison_centrale'
    id_livraison_centrale = db.Column(db.Integer, primary_key=True)
    id_centrale= db.Column(db.Integer, db.ForeignKey('centrale.id_centrale'))
    id_demande_centrale = db.Column(db.Integer, db.ForeignKey('demande_centrale.id_demande_centrale'))
    id_statut_livraison = db.Column(db.Integer, db.ForeignKey('statut_livraison.id_statut_livraison'))
    statut =db.Column(db.String(20), default='preparation')
    date_livraison = db.Column(db.Date)

    lignes_livraison_centrale = db.relationship('LigneLivraisonCentrale', back_populates='livraison_centrale')
    centrale = db.relationship('Centrale', back_populates ='livraisons_centrale')
    statut_livraison = db.relationship('StatutLivraison', back_populates='livraisoncentrale')
#Model 28 - 32
class Filiale(db.Model, UserMixin):
    __tablename__= 'filiale'
    id_filiale = db.Column(db.Integer, primary_key=True)
    id_magasin = db.Column(db.Integer, db.ForeignKey('magasin.id_magasin'))
    nom = db.Column(db.String(100))
    adresse = db.Column(db.String(100))
    ville = db.Column(db.String(100))
    email = db.Column(db.String(100))
    id_user_type = db.Column(db.Integer, db.ForeignKey('user_type.id_user_type'), default='3')

    user_type = db.relationship('UserType')
    #filiales = db.relationship('Stock', backref='filiale', lazy='dynamic')
    livraisons = db.relationship('LivraisonFiliale', back_populates="filiale")
    def __repr__(self):
        return f'<Filiale {self.nom}>'
    def get_id(self):
        return f"filiale:{self.id_filiale}"
    @classmethod
    def enregistrer_changement_statut(cls, commande_client, ancien_id, nouvel_id):
        historique = HistoriqueStatutCommande(
            id_commande_client = commande_client.id_commande_client,
            id_statut_commande_prec = ancien_id,
            id_statut_commande_suiv = nouvel_id,
            date_change = datetime.utcnow()

        )
        db.session.add(historique)
        db.session.commit()




    
class LigneCommandeFiliale(db.Model):
    __table_name__ = 'ligne_commande_filiale'
    id_ligne_commande_filiale = db.Column(db.Integer, primary_key=True)
    id_commande_filiale = db.Column(db.Integer, db.ForeignKey('commande_filiale.id_commande_filiale'))
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite_cmd =db.Column(db.Integer)
    articles_commandes_filiale = db.relationship('Article', back_populates='lignes_commandes_filiale')

class CommandeFiliale(db.Model):
    __tablename__ = 'commande_filiale'
    id_commande_filiale = db.Column(db.Integer, primary_key=True)
    id_filiale= db.Column(db.Integer, db.ForeignKey('filiale.id_filiale'))
    id_centrale = db.Column(db.Integer, db.ForeignKey('centrale.id_centrale'))
    statut =db.Column(db.String(20), default='preparation')
    date_commande = db.Column(db.Date)
    



class LigneLivraisonFiliale(db.Model):
    __tablename__ = 'ligne_livraison_filiale'
    id_ligne_livraison_filiale = db.Column(db.Integer, primary_key=True)
    id_livraison_filiale = db.Column(db.Integer, db.ForeignKey('livraison_filiale.id_livraison_filiale'))
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite_livree = db.Column(db.Integer)
    date_livraison = db.Column(db.DateTime)

    articles_livraisons_filiale = db.relationship('Article', back_populates='lignes_livraisons_filiale')
    livraisons_filiale = db.relationship('LivraisonFiliale', back_populates='lignes_livraison')
class LivraisonFiliale(db.Model):
    __tablename__ ='livraison_filiale'
    id_livraison_filiale = db.Column(db.Integer, primary_key=True)
    id_filiale = db.Column(db.Integer, db.ForeignKey('filiale.id_filiale'))
    id_commande_filiale = db.Column(db.Integer, db.ForeignKey('commande_filiale.id_commande_filiale'))
    id_statut_livraison = db.Column(db.Integer, db.ForeignKey('statut_livraison.id_statut_livraison'))
    date_livraison = db.Column(db.DateTime)
    filiale = db.relationship('Filiale', back_populates="livraisons")
    
    lignes_livraison = db.relationship('LigneLivraisonFiliale', back_populates='livraisons_filiale')
    statut_livraison = db.relationship('StatutLivraison', back_populates='livraisonfiliale')

#Model 32 - 36
class Fournisseur(db.Model, UserMixin):
    __tablename__='fournisseur'
    id_fournisseur = db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(50))
    adresse = db.Column(db.String(100))
    numero = db.Column(db.Integer)
    code_postal = db.Column(db.Integer)
    commune = db.Column(db.String(100))
    canton = db.Column(db.String(5))
    telephone = db.Column(db.Integer)
    email = db.Column(db.String(100))
    id_pays = db.Column(db.Integer, db.ForeignKey('pays.id_pays'))
    jour_de_livraison = db.Column(db.String(10))
    id_user_type = db.Column(db.Integer, db.ForeignKey('user_type.id_user_type'), default='4')
    
    user_type = db.relationship('UserType')
    commandes_fournisseur = db.relationship('CommandeFournisseur', back_populates='fournisseur')

    def get_id(self):
        return f"fournisseur:{self.id_fournisseur}"

class LigneCommandeFournisseur(db.Model):
    __tablename__='ligne_commande_fournisseur'
    id_ligne_commande_fournisseur = db.Column(db.Integer, primary_key=True)
    id_commande_fournisseur = db.Column(db.Integer, db.ForeignKey('commande_fournisseur.id_commande_fournisseur'))
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite_cmd =db.Column(db.Integer)
    date_commande =db.Column(db.Date)

    articles_commandes_fournisseur = db.relationship('Article', back_populates='lignes_commandes_fournisseur')
    commandes_fournisseur = db.relationship('CommandeFournisseur', back_populates='lignes_commande_fournisseur')

    
class CommandeFournisseur(db.Model):
    __tablename__ = 'commande_fournisseur'
    id_commande_fournisseur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_fournisseur = db.Column(db.Integer, db.ForeignKey('fournisseur.id_fournisseur'))
    date_livraison = db.Column(db.Date)
    transporteur = db.Column(db.String(100))
    numero_suivi = db.Column(db.String(100))

    fournisseur = db.relationship('Fournisseur', back_populates="commandes_fournisseur")
    lignes_commande_fournisseur = db.relationship('LigneCommandeFournisseur', back_populates='commandes_fournisseur')
    livraisons = db.relationship('LivraisonFournisseur', back_populates='commande_fournisseur')
    def __repr__(self):
        return f'<CommandeFournisseur {self.id_commande_fournisseur} - Article {self.id_article}>'

class LigneLivraisonFournisseur(db.Model):
    __tablename__ = 'ligne_livraison_fournisseur'
    id_ligne_livraison_fournisseur = db.Column(db.Integer, primary_key = True)
    id_ligne_commande_fournisseur = db.Column(db.Integer, db.ForeignKey('ligne_commande_fournisseur.id_ligne_commande_fournisseur'))
    id_article = db.Column(db.BigInteger, db.ForeignKey('article.id_article'))
    quantite_cmd =db.Column(db.Integer)
    quantite_livree = db.Column(db.Integer)
    date_livraison =db.Column(db.Date)

    
    articles_livraisons_fournisseur = db.relationship('Article', back_populates='lignes_livraisons_fournisseur')
    livraisons_fournisseur = db.relationship('LivraisonFournisseur', back_populates='lignes_livraison_fournisseur')
    

class LivraisonFournisseur(db.Model):
    __tablename__="livraison_fournisseur"
    id_livraison_fournisseur = db.Column(db.Integer, primary_key=True)
    id_fournisseur = db.Column(db.Integer, db.ForeignKey('fournisseur.id_fournisseur'))
    id_commande_fournisseur = db.Column(db.Integer, db.ForeignKey('commande_fournisseur.id_commande_fournisseur'))
    id_ligne_livraison_fournisseur = db.Column(db.Integer, db.ForeignKey('ligne_livraison_fournisseur.id_ligne_livraison_fournisseur'))
    id_statut_livraison = db.Column(db.Integer, db.ForeignKey('statut_livraison.id_statut_livraison'))

    fournisseur = db.relationship('Fournisseur', backref='livraisons')
    commande_fournisseur = db.relationship('CommandeFournisseur', back_populates='livraisons')
    lignes_livraison_fournisseur = db.relationship('LigneLivraisonFournisseur', back_populates='livraisons_fournisseur')
    statut_livraison = db.relationship('StatutLivraison', back_populates='livraisons_fournisseur')

    def __repr__(self):
        return f'< LivraisonFournisseur {self.id_livraison_fournisseur} - Commande {self.id_commande_fournisseur}>'
    

MODELS = [Article, Categorie, SousCategorie, SousSousCategorie, Client, CarteFidelite, Panier, LignePanier, Marque, Garantie, LigneCommandeClient, CommandeClient, LigneLivraisonClient, LivraisonClient, ModeLivraison, StatutCommande, StatutPaiementCommande, StatutLivraison, ModePaiement, Coupon, ModeCommunication,
Magasin, Centrale, LigneDemandeCentrale, DemandeCentrale, LigneLivraisonCentrale, LivraisonCentrale, Filiale, LigneLivraisonFiliale, LivraisonFiliale, LigneCommandeFiliale, CommandeFiliale, Fournisseur, LigneCommandeFournisseur, CommandeFournisseur, LigneLivraisonFournisseur, LivraisonFournisseur]


    