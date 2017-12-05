from flask import Flask, flash, render_template, abort, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import chem3
from chem3.chemkin import *
import os
 

def get_data(filename):
    system = ReactionSystem(filename=filename)

    data = {}
    data['equations'] = []
    # data['species'] = chemkin_data['species']
    for reaction in system.reactions:
        data['equations'].append(reaction.equation)
    return data, system

app = Flask(__name__)
app.secret_key = "super secret key"
UPLOAD_FOLDER = '/uploaded_files/'
ALLOWED_EXTENSIONS = set(['xml', 'txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')

#-------------------------------- Upload files -------------------------------------------#
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if allowed_file(file.filename):
            file.save(secure_filename(file.filename))
            flash(file.filename + ' uploaded Successfully!')

            data, system = get_data(file.filename)
            print(data)
            return redirect(request.url)
        else:
            flash('Incorrect file format!')
            return redirect(request.url)

#-------------------------------- Get T and concs -------------------------------------------#
@app.route('/', methods = ['GET', 'POST'])
def upload_text():
    if request.method == 'POST':
        T = request.form['temp']
        concs = request.form['concs']
        flash(T + ' ' + concs)
        return redirect(request.url)        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)