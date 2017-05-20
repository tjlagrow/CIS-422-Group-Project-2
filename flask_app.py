import os
from flask import Flask, render_template, request
#redirect, url_for, send_from_directory
#from werkzeug import secure_filename


app = Flask(__name__)
#app.secret_key = "secret_key"

'''
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower in 'ALLOWED_EXTENSIONS'
'''
#main page
@app.route('/')
def main():
    """Say Hello"""
    #return 'Hello, world!'
    return render_template('main.html')

@app.route('/', methods=['POST'])
def process():
    # Retrieve the HTTP POST request parameter value from 'request.form' dictionary
    _username = request.form.get('username')  # get(attr) returns None if attr is not present
 
    # Validate and send response
    if _username:
        return 'Please go back and enter your name...' 
        #return render_template('response.html', username=_username)
    else:
        return 'Please go back and enter your name...', 400 


'''
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
#
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route that will process the file upload
#@app.route('/upload', methods=['POST'])
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # Get the name of the uploaded file
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
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

    return 
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    


@app.route('/upload', methods = ['GET', 'POST'])
def upload():
  if request.method == 'POST':
     file = request.files['file']
#      extension = os.path.splitext(file.filename)[1]
#      print "uploading image..."
#      f_name = str(uuid.uuid4()) + extension
#      app.config['UPLOAD_FOLDER'] = 'static/Uploads'
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
     file.save(secure_filename(file.filename))
     return 'file save successfully'
  if request.method == 'GET':
     return 'booo'
#      return json.dumps({'filename':f_name})
#app.run(host="0.0.0.0", port = 8080, debug = True)

'''
if __name__ == '__main__':
    app.run(debug = True)
