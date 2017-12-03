from flask import Flask, render_template, abort, request, redirect, url_for
from werkzeug import secure_filename
 
app = Flask(__name__)
 
@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html')
 
@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        if request.files['file']:
            f = request.files['file']
            f.save(secure_filename(f.filename))
            return redirect(url_for('home', messages=f.filename + ' uploaded successfully!'))

@app.route('/upload_text', methods = ['GET', 'POST'])
def upload_text():
    T = request.form['temp']
    concs = request.form['concs']
    print(T, concs)
    return redirect(url_for('home', messages='Input successfully!'))        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)