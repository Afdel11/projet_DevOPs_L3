from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Remplacez par une clé secrète appropriée

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèles de base de données
class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    subject_name = db.Column(db.String(50), nullable=False)
    involvement = db.Column(db.Integer, nullable=False)
    initial_knowledge = db.Column(db.Integer, nullable=False)
    current_knowledge = db.Column(db.Integer, nullable=False)
    professor_motivation = db.Column(db.Integer, nullable=False)
    tools_methodology = db.Column(db.Integer, nullable=False)
    examples_exercises = db.Column(db.Integer, nullable=False)
    explanations_clarity = db.Column(db.Integer, nullable=False)
    practical_skills = db.Column(db.String(3), nullable=False)
    course_organization = db.Column(db.String(3), nullable=False)
    overall_satisfaction = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(500), nullable=True)

class SurveyForm(FlaskForm):
    involvement = RadioField(
        'Quel est votre niveau d\'implication dans le cours ?', 
        choices=[(str(i), str(i)) for i in range(11)],
        validators=[DataRequired()]
    )
    initial_knowledge = RadioField(
        'Quel était votre niveau de compétences/connaissances en début ?', 
        choices=[(str(i), str(i)) for i in range(11)],
        validators=[DataRequired()]
    )
    current_knowledge = RadioField(
        'Quel est votre niveau de compétences/connaissances actuel ?', 
        choices=[(str(i), str(i)) for i in range(11)],
        validators=[DataRequired()]
    )
    professor_motivation = RadioField(
        'Comment évaluez-vous la motivation et les échanges avec le professeur ?', 
        choices=[(str(i), str(i)) for i in range(11)],
        validators=[DataRequired()]
    )
    tools_methodology = RadioField(
        'Comment trouvez-vous les outils et méthodologies développés par le professeur ?', 
        choices=[(str(i), str(i)) for i in range(11)],
        validators=[DataRequired()]
    )
    examples_exercises = RadioField(
        'Veuillez noter les exemples employés et les exercices réalisés', 
        choices=[(str(i), str(i)) for i in range(11)],
        validators=[DataRequired()]
    )
    explanations_clarity = RadioField(
        'Veuillez noter la pertinence et la clarté des explications', 
        choices=[(str(i), str(i)) for i in range(11)],
        validators=[DataRequired()]
    )
    practical_skills = SelectField(
        'Pensez-vous être capable de mettre en pratique les acquisitions ?', 
        choices=[('oui', 'Oui'), ('non', 'Non')],
        validators=[DataRequired()]
    )
    course_organization = SelectField(
        'Êtes-vous satisfait(e) des conditions d\'organisation du cours (salle, installation, matériels, etc.) ?', 
        choices=[('oui', 'Oui'), ('non', 'Non')],
        validators=[DataRequired()]
    )
    overall_satisfaction = RadioField(
        'Quel est votre niveau de satisfaction générale ?', 
        choices=[(str(i), str(i)) for i in range(11)],
        validators=[DataRequired()]
    )
    feedback = TextAreaField('Commentaires supplémentaires')
    submit = SubmitField('Soumettre')

# Stockage sécurisé des mots de passe
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = generate_password_hash('adminpassword')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    class_name = session.get('class_name')
    subject_name = session.get('subject_name')

    form = SurveyForm()

    if request.method == 'POST':
        if form.validate():
            new_response = SurveyResponse(
                class_name=class_name,
                subject_name=subject_name,
                involvement=int(form.involvement.data),
                initial_knowledge=int(form.initial_knowledge.data),
                current_knowledge=int(form.current_knowledge.data),
                professor_motivation=int(form.professor_motivation.data),
                tools_methodology=int(form.tools_methodology.data),
                examples_exercises=int(form.examples_exercises.data),
                explanations_clarity=int(form.explanations_clarity.data),
                practical_skills=form.practical_skills.data,
                course_organization=form.course_organization.data,
                overall_satisfaction=int(form.overall_satisfaction.data),
                feedback=form.feedback.data
            )
            db.session.add(new_response)
            db.session.commit()
            return redirect(url_for('result'))
        else:
            flash('Veuillez corriger les erreurs dans le formulaire.', 'danger')
    
    return render_template('survey.html', form=form)


@app.route('/admin')
def admin():
    if not session.get('admin'):
        flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
        return redirect(url_for('login'))

    classes = Classe.query.all()
    matieres = Matiere.query.all()

    print("Classes:", classes)
    print("Matières:", matieres)

    return render_template('admin.html', classes=classes, matieres=matieres)


@app.route('/change_credentials', methods=['GET', 'POST'])
def change_credentials():
    global ADMIN_USERNAME, ADMIN_PASSWORD_HASH
    if not session.get('admin'):
        flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        old_username = request.form['old_username']
        old_password = request.form['old_password']
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        if old_username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, old_password):
            ADMIN_USERNAME = new_username
            ADMIN_PASSWORD_HASH = generate_password_hash(new_password)
            flash('Nom d\'utilisateur et mot de passe mis à jour avec succès.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('L\'ancien nom d\'utilisateur ou mot de passe est incorrect.', 'danger')

    return render_template('change_credentials.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin'] = True
            flash('Vous êtes connecté.', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('login'))

@app.route('/class_subject', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        classe_id = request.form.get('classe')
        matiere_id = request.form.get('matiere')

        if classe_id and matiere_id:
            classe = Classe.query.get(classe_id)
            matiere = Matiere.query.get(matiere_id)
            session['class_name'] = classe.nom
            session['subject_name'] = matiere.nom
            return redirect(url_for('survey'))
        else:
            flash('Veuillez sélectionner une classe et une matière.', 'danger')

    classes = Classe.query.all()
    matieres = Matiere.query.all()
    return render_template('class_subject.html', classes=classes, matieres=matieres)

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/report', methods=['GET', 'POST'])
def generate_report():
    classe_name = request.form.get('classe')
    matiere_name = request.form.get('matiere')

    # Récupérer les données de la base de données
    responses = SurveyResponse.query.filter_by(class_name=classe_name, subject_name=matiere_name).all()

    if not responses:
        flash('Aucune donnée trouvée pour cette classe et matière.', 'warning')
        return redirect(url_for('admin'))

    # Calcul des moyennes
    avg_involvement = sum([resp.involvement for resp in responses]) / len(responses)
    avg_initial_knowledge = sum([resp.initial_knowledge for resp in responses]) / len(responses)
    avg_current_knowledge = sum([resp.current_knowledge for resp in responses]) / len(responses)
    avg_professor_motivation = sum([resp.professor_motivation for resp in responses]) / len(responses)
    avg_tools_methodology = sum([resp.tools_methodology for resp in responses]) / len(responses)
    avg_examples_exercises = sum([resp.examples_exercises for resp in responses]) / len(responses)
    avg_explanations_clarity = sum([resp.explanations_clarity for resp in responses]) / len(responses)
    avg_satisfaction_general = sum([resp.overall_satisfaction for resp in responses]) / len(responses)
    practical_skills_yes = sum([1 for resp in responses if resp.practical_skills == 'oui'])
    course_organization_yes = sum([1 for resp in responses if resp.course_organization == 'oui'])

    # Champs de saisie pour synthèse des avis et actions correctives
    if request.method == 'POST':
        

        return render_template('report.html', 
            classe_name=classe_name, 
            matiere_name=matiere_name, 
            avg_involvement=avg_involvement,
            avg_initial_knowledge=avg_initial_knowledge,
            avg_current_knowledge=avg_current_knowledge,
            avg_professor_motivation=avg_professor_motivation,
            avg_tools_methodology=avg_tools_methodology,
            avg_examples_exercises=avg_examples_exercises,
            avg_explanations_clarity=avg_explanations_clarity,
            avg_satisfaction_general=avg_satisfaction_general,
            practical_skills_yes=practical_skills_yes,
            course_organization_yes=course_organization_yes,
            responses_len=len(responses),
           
        )

   

@app.route('/reset_survey_responses', methods=['POST'])
def reset_survey_responses():
    if not session.get('admin'):
        flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
        return redirect(url_for('login'))

    try:
        db.session.query(SurveyResponse).delete()
        db.session.commit()
        flash('Tous les résultats ont été réinitialisés avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la réinitialisation des résultats : {}'.format(e), 'danger')
    
    return redirect(url_for('admin'))

@app.route('/show_table', methods=['GET'])
def show_table():
    class_name = request.args.get('class_name', None)
    
    if class_name:
        # Filtrer les réponses par classe
        survey_responses = SurveyResponse.query.filter_by(class_name=class_name).all()
    else:
        # Afficher toutes les réponses si aucune classe n'est spécifiée
        survey_responses = SurveyResponse.query.all()
    
    return render_template('show_table.html', survey_responses=survey_responses)

@app.route('/add_matiere', methods=['POST'])
def add_matiere():
    matiere_name = request.form.get('matiere_name')
    if matiere_name:
        new_matiere = Matiere(nom=matiere_name)
        db.session.add(new_matiere)
        db.session.commit()
        flash('Matière ajoutée avec succès.', 'success')
    return redirect(url_for('admin'))

@app.route('/delete_matiere', methods=['POST'])
def delete_matiere():
    matiere_id = request.form.get('matiere_id')
    if matiere_id:
        matiere_to_delete = Matiere.query.get(matiere_id)
        if matiere_to_delete:
            db.session.delete(matiere_to_delete)
            db.session.commit()
            flash('Matière supprimée avec succès.', 'success')
    return redirect(url_for('admin'))

@app.route('/add_classe', methods=['POST'])
def add_classe():
    classe_name = request.form.get('classe_name')
    if classe_name:
        new_classe = Classe(nom=classe_name)
        db.session.add(new_classe)
        db.session.commit()
        flash('Classe ajoutée avec succès.', 'success')
    return redirect(url_for('admin'))

@app.route('/delete_classe', methods=['POST'])
def delete_classe():
    classe_id = request.form.get('classe_id')
    if classe_id:
        classe_to_delete = Classe.query.get(classe_id)
        if classe_to_delete:
            db.session.delete(classe_to_delete)
            db.session.commit()
            flash('Classe supprimée avec succès.', 'success')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)