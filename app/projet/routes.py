from re import U
from flask import render_template, flash, url_for, redirect, request, session, g, jsonify
from .. import db, bcrypt
from ..models import Donation, Rubrique, User, Publication, Categorie, Historique, Commentaire, Comment, Galerie, Album, Fichier, Evenement, Media, Parrainage
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, date
import flask_sijax
from ..utilites.utility import recent_artcile_footer, webmaster_admin, recent_artcile, les_visteurs_aujourd8, ver_enre_article, ver_enre_lu, enr_art, lesvisteurs, title_page, slug_publication, message_historique, date_modification,user_mac
from . import projet
import timeago
from datetime import datetime, date
from .forms import FormCommetaire, FormCommetaired, FormDonation
from flask_wtf.csrf import generate_csrf
import paypalrestsdk



# paypalrestsdk.configure({
#   "mode": "sandbox", # sandbox or live
#   "client_id": "AZnijnhEFfRmVNt2Z3y4JnYOFyIhEs3fTvy3DfO8dPL_sLThcbWtq435c4HFcBaTwLcYf5cQiruwmyG7",
#   "client_secret": "EMKR8xTd4S4cHtjnFSkhlo3gJR3tKAM0U5TFI2TiwJ8rZENxkvQn3oUFsa6s0ua9WaUsDUkMFFWKUAHv" })


paypalrestsdk.configure({
  "mode": "live", # sandbox or live
  "client_id": "Ab8G3V3gIkjuPbA6RdM4eN66KX8RElsYunxXjp_Lc3YP0CIFas_aOapxXSf02YDnhI92C3nobIt3zdRZ",
  "client_secret": "EKK0gDlS86q-lIKErr4w9lQQ40atVbXfdGLK0jZ-DY8NVEFltAdB4owxjasMYvrY_VzgstiSsLRRF_He" })


@projet.after_request
def set_xsrf_cookie(response):
   response.set_cookie('CSRF-TOKEN', generate_csrf())
   return response

#Age 
@projet.context_processor
def utility_processor():
   def age_naissance(date_time):
      today = date.today()
      age = today.year - date_time.year - ((today.month, today.day) < (date_time.month, date_time.day))
      return age
   return dict(age_naissance=age_naissance)

#Time ago
@projet.context_processor
def utility_processor():
    def timeagos(date_time):
        date_maintenant = datetime.now()
        date_encours=timeago.format(date_time, date_maintenant, 'fr')
        return date_encours
    return dict(timeagos=timeagos)

@projet.context_processor
def utility_processor():
   def verification_date(date_1, date_2):
      date_maintenant = date.today()
      if date_1 > date_maintenant and date_2  > date_maintenant :
         return "Avant"
      elif date_1 == date_maintenant or date_maintenant <= date_2:
         return "Encours" 
      elif date_2  < date_maintenant and  date_1 < date_maintenant :
         return "Passé"
   return dict(verification_date=verification_date)   


@projet.context_processor
def utility_processor():
    def date_french(date_sp):
        mois_anglais=date_sp.strftime('%B')
        mois_francais=None
        jour_francais=date_sp.strftime('%d')
        annee_francais=date_sp.strftime('%Y')
        #Les jours en anglais
        if mois_anglais=='January':
            mois_francais="Janvier"
        elif mois_anglais=="February":
            mois_francais="Février"
        elif mois_anglais=="March":
            mois_francais="Mars"
        elif mois_anglais=="April":
            mois_francais="Avril"
        elif mois_anglais=="May":
            mois_francais="Mai"
        elif mois_anglais=="June":
            mois_francais="Juin"
        elif mois_anglais=="July":
            mois_francais="Juillet"
        elif mois_anglais=="August":
            mois_francais="Août"
        elif mois_anglais=="September":
            mois_francais="Septembre"
        elif mois_anglais=="October":
            mois_francais="Octobre"
        elif mois_anglais=="November":
            mois_francais="Novembre"
        elif mois_anglais=="December":
            mois_francais="Décembre"
        #Date formatage complete
        date_complete=f"{jour_francais} {mois_francais} {annee_francais}"
        return date_complete
    return dict(date_french=date_french)


""" Acceuil """
@projet.route("/", methods=['GET','POST'])
def accueil():
    #Titre de l'onglet
    title=title_page('Home')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    fichier=None
    pub=[]
    photo=[]
    #Liste des actualités sur la plateforme
    message=f"Visite de l'acceuil"
    message_historique(message=message, internaute=mac_utilisateur)
    
    cate_id=Categorie.query.filter_by(nom="Actualités").first()
    if cate_id is not None:
        #Publication
        pub=Publication.query.filter_by(statut=True, categorie_id=cate_id.id).order_by(Publication.id.asc()).limit(3).all()
    #Photo
    photo=Galerie.query.filter(Album.statut==True).order_by(Galerie.id.asc()).limit(4).all() #Les photos
    #Photo à une
    ala_une=Publication.query.filter(Publication.statut==True,Publication.pred_jour==True, Categorie.nom=='Prédications').first()
    #Evenement de l'Eglise
    date_actuelle=datetime.utcnow()
    evenements=Evenement.query.filter(date_actuelle <= Evenement.date_fin , Evenement.statut==True).order_by(Evenement.date_even.desc()).limit(3).all()
    #Requête des audio
    video_alaune=Media.query.filter_by(alaune=True, statut=True).first()
    #Video à la une
    media_predication=Media.query.order_by(Media.id.desc()).limit(3).all()
    #Ala une  
    if ala_une is not None:
        fichier_doc=Fichier.query.filter_by(publication_id=ala_une.id).first()
        if fichier_doc is not None:
            fichier=fichier_doc.url_pdf
    
    #Categirisation des donations
    form=FormDonation()
    session.pop('resume',None)
    session.pop('noms_rub',None)
    session.pop('montant',None)
    session.pop('image_rub',None)
    session.pop('id_rub',None)
    session.pop('email_don',None)
    session.pop('sponsor_confirm',None)
    session.pop('donate_confirm',None)
    session.pop('enfant',None)
    session.pop('mail',None)
    session.pop('adresse',None)
    session.pop('tel',None)
    session.pop('pays',None)
    session.pop('montant',None)
    session.pop('nom',None)
    session.pop('prenom',None)
    
    session["ver"]=None
    
    
    
    return render_template('projet/index.html',footer_pub=recent_artcile_footer(), form=form, media_predication=media_predication,video_alaune=video_alaune, evenements=evenements, title=title, pub=pub, photos=photo, ala_une=ala_une,fichier=fichier)

#Donation
@projet.route('/donation/<string:nopay>', methods=['GET','POST'])
def donation(nopay):
    #Titre de l'onglet
    title=title_page('Donation')
    form=FormDonation()

    

    #Nofication
    notification=None
    vrai="b326b5062b2f0e69046810717534cb09"
    faux="68934a3e9455fa72420237eb05902327"
    if nopay==vrai:
        notification=True
    elif nopay==faux:
        notification=False
    #Validation du formulaire
    if form.validate_on_submit():
        session["resume"]=form.cause.data.resume
        session["noms_rub"]=form.cause.data.nom
        session["montant"]=form.montant.data
        session["image_rub"]=form.cause.data.image_rubrique
        session["id_rub"]=form.cause.data.id
        session["donateur_rub"]=form.noms.data
        session["do_adresse_mail"]=form.adresse_mail.data
        session["ver"]=None


    if "noms_rub" not in session:
        return redirect(url_for('projet.accueil'))  

    #La date d'aujourdui
    date_transanction=date.today()
    

    return render_template('projet/donation.html',date_transanction=date_transanction, title=title, notification=notification, footer_pub=recent_artcile_footer())

#Donation
@projet.route('/final/donation', methods=['GET','POST'])
def donation_final():
    #Titre de l'onglet
    title=title_page('Donation')
    if "noms_rub" not in session:
        return redirect(url_for('projet.accueil'))   
    
    if request.method=="POST":
        data=request.get_json()
        rubrique_id=session["id_rub"]
        somme=session["montant"]
        noms=session["donateur_rub"]
        identi_payement=data["donnateur"]
        email=session["do_adresse_mail"]
        session["donate_confirm"]=False
        #Enregistrement de la donation
        don=Donation(rubrique_id=rubrique_id, noms=noms, date_payements=date.today(),identi_payement=identi_payement,
                          somme=somme, email=email)
        db.session.add(don)
        db.session.commit()
        flash("Thank you for your donation!",'success')
        #return redirect(url_for('projet.donation', nopay="b326b5062b2f0e69046810717534cb09"))   
    return render_template('projet/donation.html',title=title, footer_pub=recent_artcile_footer())

#Donation
@projet.route('/sponsor/<int:enf_id>', methods=['GET','POST'])
def sponsor_child(enf_id):
    title=title_page('Sponsor')
    enfant=Parrainage.query.filter_by(id=enf_id, statut=True).first_or_404()
    session["enfant"]=enf_id
    
    return render_template('projet/sponsor.html',title=title, enfant=enfant , footer_pub=recent_artcile_footer())

#Donation & adresse contact
@projet.route('/montant', methods=['GET','POST'])
def montant_child():
    title=title_page('Sponsor')
    id_enf=None
    if "enfant" in session:
        id_enf=session["enfant"]
    enfant=Parrainage.query.filter_by(id=id_enf, statut=True).first_or_404()
        
    if request.method == "POST":
        montant = request.form.get("montant")
        session["montant"]=montant
    return render_template('projet/sponsor.html',title=title, enfant=enfant, footer_pub=recent_artcile_footer())

@projet.route('/identite', methods=['GET','POST'])
def identite():
    title=title_page('Sponsor')
    #Information de l'enfant
    id_enf=None
    if "enfant" in session:
        id_enf=session["enfant"]
    enfant=Parrainage.query.filter_by(id=id_enf, statut=True).first_or_404()
        
    if request.method == "POST":
        nom = request.form.get("nom")
        prenom=request.form.get("prenom")
        session["nom"]=nom
        session["prenom"]=prenom
    return render_template('projet/sponsor.html',title=title, enfant=enfant, footer_pub=recent_artcile_footer())

@projet.route('/data/contact', methods=['GET','POST'])
def ad():
    title=title_page('Sponsor')
    #Information de l'enfant
    id_enf=None
    if "enfant" in session:
        id_enf=session["enfant"]
    enfant=Parrainage.query.filter_by(id=id_enf, statut=True).first_or_404()
        
    if request.method == "POST":
        adresse = request.form.get("adresse")
        mail = request.form.get("mail")
        tel = request.form.get("tel")
        pays = request.form.get("pays")
        session["mail"]=mail
        session["adresse"]=adresse
        session["tel"]=tel
        session["pays"]=pays
    return render_template('projet/sponsor.html',title=title, enfant=enfant, footer_pub=recent_artcile_footer())

@projet.route('/sponsor-child', methods=['GET','POST'])
def parrainer():
    title=title_page('Sponsor a child')
    #Information de l'enfant
    page= request.args.get('page', 1, type=int)
    parrainage=Parrainage.query.filter_by(statut=True).order_by(Parrainage.id.desc()).paginate(page=page, per_page=6)

    return render_template('projet/sponsor_ch.html',parrainage=parrainage, title=title, footer_pub=recent_artcile_footer())

@projet.route('/sponsor/child', methods=['GET','POST'])
def sponsor_childe_payement():
    title=title_page('Sponsor')
    #Information de l'enfant
    id_enf=None
    if "enfant" in session:
        id_enf=session["enfant"]
    enfant=Parrainage.query.filter_by(id=id_enf, statut=True).first_or_404()
    #Vérification de la validité des infromation
    if "enfant" not in session and "mail" not in session and "adresse" not in session and "tel" not in session and "pays" not in session and "montant" not in session and "nom" not in session and "prenom" not in session:
        return redirect(url_for('projet.sponsor_child', enf_id=session["enfant"]))      

    return render_template('projet/sponsor_payement.html',title=title, enfant=enfant, footer_pub=recent_artcile_footer())

@projet.route('/final/sponsor', methods=['GET','POST'])
def sponsor_final():
    #Titre de l'onglet
    title=title_page('Sponspor')
    
    id_enf=None
    if "enfant" in session:
        id_enf=session["enfant"]
    enfant=Parrainage.query.filter_by(id=id_enf, statut=True).first_or_404()
    
    if "enfant" not in session or "mail" not in session or "adresse" not in session or "tel" not in session or "pays" not in session or "montant" not in session or "nom" not in session or "prenom" not in session or "post_nom" not in session:
        return redirect(url_for('projet.sponsor_child', enf_id=session["enfant"]))   
    
    if request.method=="POST":
        data=request.get_json()
        identi_payement=data["donnateur"]
        noms=f"{session['nom']} {session['prenom']}"
        #Enregistrement de la donation
        don=Donation(parrainage_id=session["enfant"], noms=noms, date_payements=date.today(),identi_payement=identi_payement,
                          somme=session["montant"], adresse=session["adresse"], pays=session["pays"], telephone=session["tel"], email=session["mail"])
        db.session.add(don)
        db.session.commit()
        flash("Thank you for your donation!",'success')
  
    return render_template('projet/sponsor_payement.html',title=title, enfant=enfant, footer_pub=recent_artcile_footer())
    
# """ Article """
@projet.route('/article/<string:slug>')
def article(slug):
    #Article de verification.
    article_pu=Publication.query.filter_by(slug=slug).first_or_404()
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
        
    if article_pu is not None:
        session["id_pu"] = article_pu.id

    #Nombre des lis de l'article
    article=ver_enre_article(article_pu.id)
    var_lu_art=ver_enre_lu(article_pu.id)
    enr_art(article,var_lu_art,article_pu)
    
    message=f"Visite de l'actualité :{article_pu.titre} "
    message_historique(message=message, internaute=mac_utilisateur)

    post_recent=Publication.query.filter(Publication.nbr_lu > 10 , Publication.statut==True, Categorie.nom=='Actualités').order_by(Publication.nbr_lu.desc()).limit(6).all()
    album=Album.query.filter_by(statut=True).order_by(Album.id.asc()).all()
    #Fichier encours d'éxecution
    print(article_pu.id)
    fichier_docu=Fichier.query.filter_by(publication_id=article_pu.id).first()
        
    return render_template('projet/actua_une_c.html',footer_pub=recent_artcile_footer(),  post_recent=post_recent, article_pu=article_pu,  album=album, fichier_docu=fichier_docu)

@projet.route('/actus')
def actualites():
    #Titre de l'onglet
    title=title_page('Blog')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    page="Prédication"
    #Prédication
    message=f"Visite des actualités"
    message_historique(message=message, internaute=mac_utilisateur)
    #Liste des actualités
    page= request.args.get('page', 1, type=int)
    cate_id=Categorie.query.filter_by(nom="Actualités").first()
    actualites=Publication.query.filter(Publication.statut==True,Publication.categorie_id==cate_id.id).order_by(Publication.id.desc()).paginate(page=page, per_page=6)
    return render_template('projet/actualites.html',title=title, page=page, actualites=actualites, footer_pub=recent_artcile_footer())

@projet.route('/contact')
def contact():
    #Titre de l'onglet
    title=title_page('Contact')
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    message=f"Visite des contact"
    message_historique(message=message, internaute=mac_utilisateur)
    
    return render_template('projet/contact.html',title=title, footer_pub=recent_artcile_footer())

@projet.route('/donation/payement', methods=['POST', 'GET'])
def payement_donation():
    
    payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"},
    "redirect_urls": {
        "return_url": "http://localhost:3000/payment/execute",
        "cancel_url": "http://localhost:3000/"}, 
    "transactions": [{
        "item_list": {
            "items": [{
                "name":"{}".format(session["noms_rub"]),
                "sku": "{}".format(session["noms_rub"]),
                "price": "{}".format(session["montant"]),
                "currency": "USD",
                "quantity": 1}]},
        "amount": {
            "total": "{}".format(session["montant"]),
            "currency": "USD"},
        "description": "Ce payement est un parrainage pour l'enfant {}".format(session["noms_rub"])}]})

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)
    
    return jsonify({'paymentID':payment.id})

@projet.route('/donation/execute', methods=['POST','GET'])
def execute_donation():
    success=False
    payment=paypalrestsdk.Payment.find(request.form['paymentID'])
    
    if payment.execute({'payer_id': request.form['payerID']}):
        rubrique_id=session["id_rub"]
        somme=session["montant"]
        noms=session["donateur_rub"]
        email=session["do_adresse_mail"]
        #Enregistrement de la donation
        don=Donation(rubrique_id=rubrique_id, noms=noms, date_payements=date.today(),identi_payement=request.form['payerID'],
                          somme=somme, email=email)
        db.session.add(don)
        db.session.commit()
        session["donate_confirm"]=True
        
    else:
        print(payment.error)
    
    return jsonify({'success':success})

@projet.route('/donate/confirm')
def donate_conform():
    #Titre de l'onglet
    title=title_page('Donate')
    #Visteur en ligne
    donate=None
    
    if 'donate_confirm' in session:
        donate=session["donate_confirm"]
        if donate==False:
            return redirect(url_for('projet.accueil'))
        session.pop('resume',None)
        session.pop('noms_rub',None)
        session.pop('montant',None)
        session.pop('image_rub',None)
        session.pop('id_rub',None)
        session.pop('email_don',None)
        session["ver"]=None
    else:
        return redirect(url_for('projet.accueil'))
    
    return render_template('projet/conform_donate.html',title=title, footer_pub=recent_artcile_footer())

@projet.route('/sponsor/payement', methods=['POST', 'GET'])
def payement_sponsor():
    
    if "enfant" in session:
        id_enf=session["enfant"]
    enfant=Parrainage.query.filter_by(id=id_enf, statut=True).first_or_404()
    
    if "enfant" not in session and "mail" not in session and "adresse" not in session and "tel" not in session and "pays" not in session and "montant" not in session and "nom" not in session and "prenom" not in session:
        return redirect(url_for('projet.sponsor_child', enf_id=session["enfant"]))    
    
    payment = paypalrestsdk.Payment({
    "intent": "sale",
    "payer": {
        "payment_method": "paypal"},
    "redirect_urls": {
        "return_url": "http://localhost:3000/payment/execute",
        "cancel_url": "http://localhost:3000/"}, 
    "transactions": [{
        "item_list": {
            "items": [{
                "name":"Parrainage",
                "sku": "Parrainage",
                "price": "{}".format(session["montant"]),
                "currency": "USD",
                "quantity": 1}]},
        "amount": {
            "total": "{}".format(session["montant"]),
            "currency": "USD"},
        "description": "Ce payement est une donation pour la cause de {}".format(enfant.noms )}]})

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)
    
    return jsonify({'paymentID':payment.id})

@projet.route('/sponsor/execute', methods=['POST','GET'])
def execute_sponsor():
    success=False
    payment=paypalrestsdk.Payment.find(request.form['paymentID'])
    
    if payment.execute({'payer_id': request.form['payerID']}):
        noms=f"{session['nom']} {session['prenom']}"
        #Enregistrement de la donation
        don=Donation(parrainage_id=session["enfant"], noms=noms, date_payements=date.today(),identi_payement=request.form['payerID'],
                          somme=session["montant"], adresse=session["adresse"], pays=session["pays"], telephone=session["tel"], email=session["mail"])
        db.session.add(don)
        db.session.commit()
        session["sponsor_confirm"]=True
        
    else:
        print(payment.error)
    
    return jsonify({'success':success})

@projet.route('/sponsor/confirm')
def sponsor_conform():
    #Titre de l'onglet
    title=title_page('Sponsor')
    #Visteur en ligne
    donate=None
    
    if 'sponsor_confirm' in session:
        donate=session["sponsor_confirm"]
        if donate==False:
            return redirect(url_for('projet.accueil'))
        session.pop('enfant',None)
        session.pop('mail',None)
        session.pop('adresse',None)
        session.pop('tel',None)
        session.pop('pays',None)
        session.pop('montant',None)
        session.pop('nom',None)
        session.pop('prenom',None)

    else:
        return redirect(url_for('projet.accueil'))
    
    return render_template('projet/sponsor_donate.html',title=title, footer_pub=recent_artcile_footer())

@projet.route('/about')
def apropos():
    #Titre de l'onglet
    title=title_page('About')
    #Visteur en ligne
    #Visteur en ligne
    lesvisteurs()
    # L'utilisateur en cours
    mac_utilisateur=user_mac()
    message=f"Apropos de nous"
    message_historique(message=message, internaute=mac_utilisateur)
    return render_template('projet/about.html',title=title, footer_pub=recent_artcile_footer())

