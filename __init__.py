import os
from google.cloud import storage
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
bucket_name = 'hurdling.appspot.com'
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "TESTSTRING"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            name = '/{}/{}'.format(bucket_name, filename)
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob = storage.Blob(name, bucket)
            blob.upload_from_filename(filepath)
    return "Works"