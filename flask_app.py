import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = "secret_key"


#main page 
@app.route('/')
def main():
    return render_template('CIS-422-Group-Project-2/templates/main.html')

@app.route('/dashboard',methods=('GET',))
def dashboard():
    return render_template('dashboard.html')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      file = request.files['file']
      extension = os.path.splitext(file.filename)[1]
      print "uploading image..."
      f_name = str(uuid.uuid4()) + extension
      app.config['UPLOAD_FOLDER'] = 'static/Uploads'
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
      return json.dumps({'filename':f_name})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port = 8080, debug = True)
