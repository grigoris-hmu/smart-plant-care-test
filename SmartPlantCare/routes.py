from flask import render_template, redirect, url_for

from SmartPlantCare import app


### ERROR HANDLERS START ###

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(415)
def unsupported_media_type(e):
    return render_template('415.html'), 415

@app.errorhandler(500)
def unsupported_media_type(e):
    return render_template('500.html'), 500

### ERROR HANDLERS END ###

### Home Page ###
@app.route("/")
def root():
    return render_template("index.html")
    #return render_template("foo.html")
    #return redirect(url_for('crop.crops'))