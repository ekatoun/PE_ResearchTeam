# ================================================
#  backend/models.py
#  Modèles SQLAlchemy
# ================================================

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


# ── Utilisateur (accès admin) ────────────────
class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateurs'

    id       = db.Column(db.Integer, primary_key=True)
    nom      = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email    = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role     = db.Column(db.Enum('admin', 'lecteur'), default='lecteur', nullable=False)
    cree_le  = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Utilisateur {self.username}>'


# ── Réponse questionnaire ────────────────────
class Reponse(db.Model):
    __tablename__ = 'reponses'

    id = db.Column(db.Integer, primary_key=True)

    # Section A
    id_etude        = db.Column(db.String(20))
    date_entretien  = db.Column(db.Date)
    date_naissance  = db.Column(db.Date)
    age_actuel      = db.Column(db.SmallInteger)
    poids           = db.Column(db.Numeric(5, 1))
    taille          = db.Column(db.SmallInteger)
    imc             = db.Column(db.Numeric(5, 2))
    imc_categorie   = db.Column(db.String(50))
    education       = db.Column(db.String(30))
    residence       = db.Column(db.Enum('urbain', 'rural'))

    # Section B
    ddr              = db.Column(db.Date)
    ag_semaines      = db.Column(db.SmallInteger)
    ag_jours         = db.Column(db.SmallInteger)
    methode_datation = db.Column(db.Enum('ddr', 'echographie'))
    type_grossesse   = db.Column(db.Enum('unique', 'gemellaire', 'multiple'))

    # Section C – HTA
    hta                    = db.Column(db.Enum('oui', 'non', 'ne_sait_pas'))
    hta_date_diag          = db.Column(db.String(10))
    hta_duree              = db.Column(db.SmallInteger)
    hta_medicaments        = db.Column(db.Enum('oui', 'non'))
    hta_medicaments_detail = db.Column(db.Text)
    tas_avant              = db.Column(db.SmallInteger)
    tad_avant              = db.Column(db.SmallInteger)

    # Section C – Rénale
    renale            = db.Column(db.Enum('oui', 'non', 'ne_sait_pas'))
    renale_type       = db.Column(db.JSON)
    renale_type_autre = db.Column(db.String(200))
    dialyse           = db.Column(db.Enum('dialyse', 'transplantation', 'non'))

    # Section C – Diabète
    diabete           = db.Column(db.Enum('oui', 'non', 'ne_sait_pas'))
    diabete_type      = db.Column(db.Enum('type1', 'type2'))
    diabete_ttt       = db.Column(db.JSON)
    diabete_ttt_autre = db.Column(db.String(200))

    # Section C – Auto-immunes
    autoimmune        = db.Column(db.JSON)
    autoimmune_autre  = db.Column(db.String(200))

    # Section C – Autres conditions
    autres_conditions      = db.Column(db.JSON)
    cardio_detail          = db.Column(db.String(200))
    thrombophilie_detail   = db.Column(db.String(200))
    autre_chronique_detail = db.Column(db.String(200))

    # Section C – Familiaux
    atcd_familiaux = db.Column(db.JSON)

    # Section D – Parité
    nb_grossesses    = db.Column(db.SmallInteger)
    nb_accouchements = db.Column(db.SmallInteger)
    parite           = db.Column(db.Enum('nullipare', 'primipare', 'multipare'))

    # Section D – Prééclampsie
    atcd_pe             = db.Column(db.Enum('oui', 'non', 'ne_sait_pas'))
    pe1_annee           = db.Column(db.SmallInteger)
    pe1_ag_diag         = db.Column(db.SmallInteger)
    pe1_severite        = db.Column(db.Enum('legere', 'severe', 'ne_sait_pas'))
    pe1_ag_accouchement = db.Column(db.SmallInteger)
    pe1_complic         = db.Column(db.JSON)
    pe1_complic_autre   = db.Column(db.String(200))
    pe2_annee           = db.Column(db.SmallInteger)
    pe2_ag_diag         = db.Column(db.SmallInteger)
    pe2_severite        = db.Column(db.Enum('legere', 'severe', 'ne_sait_pas'))
    pe2_ag_accouchement = db.Column(db.SmallInteger)
    pe2_complic         = db.Column(db.JSON)
    pe2_complic_autre   = db.Column(db.String(200))

    # Section D – Autres complications
    complic_ant = db.Column(db.JSON)

    # Section D – Fausses couches
    fcs        = db.Column(db.Enum('oui', 'non'))
    fcs_nombre = db.Column(db.SmallInteger)

    # Section D – Intervalle
    intervalle = db.Column(db.Enum('moins2ans', '2_5ans', '6_10ans', 'plus10ans'))

    # Métadonnées
    ip_saisie = db.Column(db.String(45))
    cree_le   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<Reponse #{self.id} – {self.id_etude}>'
