import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = "secret_key"

app.config['input_images'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

#main page
@app.route('/')
def main():
    return render_template('main.html')

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['input_images'], filename)


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

#@app.route('/upload', methods = ['GET', 'POST'])
#def upload():
#   if request.method == 'POST':
#      file = request.files['file']
#      extension = os.path.splitext(file.filename)[1]
#      print "uploading image..."
#      f_name = str(uuid.uuid4()) + extension
#      app.config['UPLOAD_FOLDER'] = 'static/Uploads'
#      file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
#      return json.dumps({'filename':f_name})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080, debug = True)
