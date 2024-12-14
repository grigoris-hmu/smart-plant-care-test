from pickle import FALSE
from tokenize import String
from flask import render_template, redirect, url_for, request, flash, abort
from SmartPlantCare.forms import SignupForm, LoginForm, NewCropForm, AccountUpdateForm
from SmartPlantCare.models import User, Crop
from flask_login import login_user, current_user, logout_user, login_required

import secrets
from PIL import Image
import os

from datetime import datetime as dt

from SmartPlantCare import app, db, bcrypt

from PIL import Image

current_year = dt.now().year


### Μέθοδος μετονομασίας και αποθήκευσης εικόνας ###
def image_save(image, where, size):
    random_filename = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(image.filename)
    image_filename = random_filename + file_extension
    image_path = os.path.join(app.root_path, 'static/images/'+ where, image_filename)

    image_size = size # this must be a tupe in the form of: (150, 150)
    img = Image.open(image)
    img.thumbnail(image_size)

    img.save(image_path)

    return image_filename


### ERROR HANDLERS START ###

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(415)
def unsupported_media_type(e):
    return render_template('415.html'), 415

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

### ERROR HANDLERS END ###

### Αρχική Σελίδα ###
@app.route("/home/")
@app.route("/")
def root():

    ## ταξινόμηση ανά όνομα, τοποθεσία
    ## με σωστή σελιδοποίηση για την κάθε περίπτωση.
    ordering_by = request.args.get('ordering_by')

    ## Pagination: page value from 'page' parameter from url
    page = request.args.get('page', 1, type=int)

    ## Query για ανάσυρση των Καλλιεργειών από τη βάση δεδομένων με το σωστό pagination και ταξινόμηση
    if ordering_by==None:
        crops = Crop.query.order_by(Crop.crop_area.asc()).paginate(per_page=5, page=page)
    elif ordering_by=='name':
        crops = Crop.query.order_by(Crop.name.asc()).paginate(per_page=5, page=page)
    elif ordering_by=='location':
        crops = Crop.query.order_by(Crop.location.desc()).paginate(per_page=5, page=page)
    else:
        return render_template('404.html'), 404

    ## Υπενθύμιση: το context είναι το σύνολο των παραμέτρων που περνάμε
    ##             μέσω της render_template μέσα στα templates μας
    ##             στην παρακάτω περίπτωση το context περιέχει μόνο το crops=crops
    #return render_template("index.html", crops=crops, ordering_by=ordering_by)
    return render_template("index.html", crops=crops, ordering_by=ordering_by)


@app.route("/signup/", methods=['GET','POST'])
def signup():

    ## Έλεγχος για το αν ο χρήστης έχει κάνει login ώστε αν έχει κάνει,
    ## να μεταφέρεται στην αρχική σελίδα
    if current_user.is_authenticated:
        return redirect(url_for("root"))

    '''Create an instance of the Sign Up form'''
    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():


        ## Ο κώδικας που φορτώνει τα στοιχεία της φόρμας και τα αποθηκεύει στη βάση δεδομένων
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        encrypted_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Ο λογαριασμός για το χρήστη: <b>{username}</b> δημιουργήθηκε με επιτυχία', 'success')

        return redirect(url_for('login_page'))

    return render_template("signup.html", form=form)


## Σελίδα Λογαριασμού Χρήστη με δυνατότητα αλλαγής των στοιχείων του
## Δίνεται ο σωστός decorator για υποχρεωτικό login
@app.route("/account/", methods=['GET','POST'])
@login_required
def account():

    ## Αρχικοποίηση φόρμας με προσυμπληρωμένα τα στοιχεία του χρήστη
    form = AccountUpdateForm(username=current_user.username, email=current_user.email)

    if request.method == 'POST' and form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data

        ## Έλεγχος αν έχει δοθεί νέα εικόνα προφίλ, αλλαγή ανάλυσης της εικόνας
        ## και αποθήκευση στον δίσκο του server και στον χρήστη (δηλαδή στη βάση δεδομένων).
        if form.profile_image.data:

            try:
                image_file = image_save(form.profile_image.data, 'profiles_images', (150, 150))
            except:
                abort(415)

            current_user.profile_image = image_file

        ## Αποθήκευση των υπόλοιπων στοιχείων του χρήστη.
        db.session.commit()

        flash(f'Ο λογαριασμός του χρήστη: <b>{current_user.username}</b> ενημερώθηκε με επιτυχία', 'success')

        return redirect(url_for('root'))
    else:
        return render_template("account_update.html", form=form)


### Σελίδα Login ###
@app.route("/login/", methods=['GET','POST'])
def login_page():

    ## Έλεγχος για το αν ο χρήστης έχει κάνει login ώστε αν έχει κάνει,
    ## να μεταφέρεται στην αρχική σελίδα
    if current_user.is_authenticated:
        return redirect(url_for("root"))

    form = LoginForm() ## Αρχικοποίηση φόρμας Login

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        ## Ανάκτηση χρήστη από τη βάση με το email του
        ## και έλεγχος του password.
        ## Εάν είναι σωστά, γίνεται login με τη βοήθεια του Flask-Login
        ## Σε κάθε περίπτωση εμφανίζονται τα αντίστοιχα flash messages
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Η είσοδος του χρήστη με email: {email} στη σελίδα μας έγινε με επιτυχία.", "success")
            login_user(user, remember=form.remember_me.data)

            next_link = request.args.get("next")

            return redirect(next_link) if next_link else redirect(url_for("root"))
        else:
            flash("Η είσοδος του χρήστη ήταν ανεπιτυχής, παρακαλούμε δοκιμάστε ξανά με τα σωστά email/password.", "warning")

    return render_template("login.html", form=form)


### Σελίδα Logout ###
@app.route("/logout/")
def logout_page():

    ## Αποσύνδεση Χρήστη
    logout_user()

    flash('Έγινε αποσύνδεση του χρήστη.', 'success')
    
    ## Ανακατεύθυνση στην αρχική σελίδα
    return redirect(url_for("root"))


### Σελίδα Εισαγωγής Νέας Καλλιέργειας ###

## Ο decorator για τη σελίδα με route 'new_crop'
## καθώς και ο decorator για υποχρεωτικό login
@app.route("/new_crop/", methods=["GET", "POST"])
@login_required
def new_crop():
    form = NewCropForm()

        ## Υλοποίηση της λειτουργίας για ανάκτηση και έλεγχο (validation) των δεδομένων της φόρμας
        ## Τα πεδία που έρχονται είναι τα παρακάτω:
        ## name, location, location_longitude, location_latitude
        ## Το πεδίο image ελέγχεται αν περιέχει εικόνα και αν ναι
        ## μετατρέπει την ανάλυσή της σε (640, 640) και την αποθηκεύει στο δίσκο και τη βάση
        ## αν όχι, αποθηκεύει τα υπόλοιπα δεδομένα και αντί εικόνας μπαίνει το default crop image
        
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        location = form.location.data
        location_longitude = form.location_longitude.data
        location_latitude = form.location_latitude.data
        prefecture = form.prefecture.data
        area = form.area.data
        crop_area = form.crop_area.data
        crop_type = form.crop_type.data
        soil_type = form.soil_type.data

        if form.image.data:
            try:
                image_file = image_save(form.image.data, 'crops_images', (640, 640))
            except:
                abort(415)
        
            crop = Crop(name=name,
                        location = location,
                        location_longitude = location_longitude,
                        location_latitude = location_latitude,
                        prefecture = prefecture,
                        area = area,
                        crop_area = crop_area,
                        crop_type = crop_type,
                        soil_type = soil_type,
                        image=image_file)
        else:
            crop = Crop(name=name,
                        location=location,
                        location_longitude=location_longitude,
                        location_latitude=location_latitude,
                        prefecture = prefecture,
                        area = area,
                        crop_area = crop_area,
                        crop_type = crop_type,
                        soil_type = soil_type)

        db.session.add(crop)
        db.session.commit()


        flash(f'Η Καλλιέργεια με όνομα: "{name}" δημιουργήθηκε με επιτυχία', 'success')

        return redirect(url_for('root'))


    return render_template("new_crop.html", form=form, page_title="Εισαγωγή Νέας Καλλιέργειας")


### Πλήρης σελίδα καλλιέργειας ###

## Ο decorator για τη σελίδα με route 'crop'
## και επιπλέον δέχεται το id της καλλιέργειας ('crop_id')
@app.route("/crop/<int:crop_id>", methods=["GET"])
def crop(crop_id):

    ## Ανάκτηση της καλλιέργειας με βάση το crop_id
    ## ή εμφάνιση σελίδας 404 page not found
    crop = Crop.query.get_or_404(crop_id)

    return render_template("crop.html", crop=crop)


### Σελίδα Αλλαγής Στοιχείων καλλιέργειας ###

## Ο decorator για τη σελίδα με route 'edit_crop'
## και επιπλέον δέχεται το id της καλλιέργειας προς αλλαγή ('crop_id')
## και προστεθεί και ο decorator για υποχρεωτικό login
@app.route("/edit_crop/<int:crop_id>", methods=['GET', 'POST'])
@login_required
def edit_crop(crop_id):

    ## Ανάκτηση καλλιέργειας βάσει των crop_id, user_id, ή, εμφάνιση σελίδας 404 page not found
    crop = Crop.query.filter_by(id=crop_id).first_or_404()

    ## Έλεγχος αν βρέθηκε η καλλιέργειας
    ## αν ναι, αρχικοποίηση της φόρμας ώστε τα πεδία να είναι προσυμπληρωμένα
    ## έλεγχος των πεδίων (validation) και αλλαγή (ή προσθήκη εικόνας) στα στοιχεία της καλλιέργειας
    ## αν δε βρέθηκε η καλλιέργειας, ανακατεύθυνση στην αρχική σελίδα και αντίστοιχο flash μήνυμα στο χρήστη

    form = NewCropForm(
        name = crop.name,
        location = crop.location,
        location_longitude = crop.location_longitude,
        location_latitude = crop.location_latitude,
        prefecture = crop.prefecture,
        area = crop.area,
        crop_area = crop.crop_area,
        crop_type = crop.crop_type,
        soil_type = crop.soil_type)

    if request.method == 'POST' and form.validate_on_submit():

        crop.name = form.name.data
        crop.location = form.location.data
        crop.location_longitude = form.location_longitude.data
        crop.location_latitude = form.location_latitude.data
        crop.prefecture = form.prefecture.data
        crop.area = form.area.data
        crop.crop_area = form.crop_area.data
        crop.crop_type = form.crop_type.data
        crop.soil_type = form.soil_type.data

        if form.image.data:
            try:
                image_file = image_save(form.image.data, 'crops_images', (640, 640))
            except:
                abort(415)

            crop.image = image_file

        db.session.commit()
    
        flash(f'Η επεξεργασία της καλλιέργειας έγινε με επιτυχία', 'success')

        return redirect(url_for('crop', crop_id=crop.id))

    return render_template("new_crop.html", form=form, crop=crop, page_title="Αλλαγή στοιχείων καλλιέργειας")
    

    flash(f'Δε βρέθηκε η καλλιέργεια', 'info')

    return redirect(url_for("root"))


### Σελίδα Διαγραφής καλλιέργειας ###

## Ο decorator για τη σελίδα με route 'delete_crop'
## και επιπλέον δέχεται το id της καλλιέργειας προς αλλαγή ('crop_id')
## και προστεθεί και ο decorator για υποχρεωτικό login
@app.route("/delete_crop/<int:crop_id>", methods=["GET", "POST"])
@login_required
def delete_crop(crop_id):

    crop = Crop.query.filter_by(id=crop_id).first_or_404() ## Ανάκτηση καλλιέργειας βάσει των crop_id), ή, εμφάνιση σελίδας 404 page not found

    ## Εάν βρεθεί η καλλιέργεια, κάνουμε διαγραφή και εμφανίζουμε flash message επιτυχούς διαγραφής
    ## με ανακατεύθυνση στην αρχική σελίδα
    ## αλλιώς εμφανίζουμε flash message ανεπιτυχούς διαγραφής
    ## με ανακατεύθυνση στην αρχική σελίδα
    if crop:

        db.session.delete(crop)
        db.session.commit()

        flash("Η καλλιέργεια διεγράφη με επιτυχία.", "success")

        return redirect(url_for("root"))

    flash("Η καλλιέργεια δε βρέθηκε.", "warning")

    return redirect(url_for("root"))
