import os
import time
import json
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'videos'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "TESTSTRING"

# db initialization

import dbconnection
import models
dbconnection.init_db()

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/recordings', methods=['GET'])
def view_recordings():
	recordings = models.Recording.query.all()
	print(type(recordings))
	s = []

	for r in recordings:
		s.append(r.getCollection())
	# return thumbnail
	return jsonify(s)

	# return .json file

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		if 'json' not in request.files:
			flash('No json part')
			return redirect(request.url)
		json_data = request.files['json']
		json_thing = json.load(json_data)

		# Start analysis

		#print("This is an example how to call a first corner location's y-coordinate: " + str(json_thing['cornerLocations'][0][1]))
		print("json dump: "+json.dumps(json_thing['cornerLocations']))
		models.Recording(
			"Esko Esimerkki",
			json.dumps(json_thing['cornerLocations']),
			filename
			)

	return "Server is running."

from werkzeug import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
	build_only=True)

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/uploads':  app.config['UPLOAD_FOLDER']
})