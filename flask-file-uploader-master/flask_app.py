#!flask/bin/python

# Author: Daniel Su
# Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import sys
import os
import PIL
from PIL import Image
import simplejson
import traceback
import json

from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
#from Food_Files.tag_images import process_all_images
from lib.upload_file import uploadfile


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

#Uncomment to run on pythonanywhere
#app.config['UPLOAD_FOLDER'] = '/home/422Hopper/CIS-422-Group-Project-2/Food_Files/input_images/'
#app.config['THUMBNAIL_FOLDER'] = '/home/422Hopper/CIS-422-Group-Project-2/flask-file-uploader-master/data/thumbnail/'
app.config['OUTPUT'] = '/Food_Files/output/foods.json'
app.config['RECIPIE'] = 'CIS-422-Group-Project-2/Recipe_Files/JSON_Files/recipiesOutput.json'
app.config['THUMBNAIL_FOLDER'] = 'Food_Files/input_images/thumbnail'
app.config['UPLOAD_FOLDER'] = 'Food_Files/input_images/'
#app.config['UPLOAD_FOLDER'] = '../Food_Files/input_images/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['gif', 'png', 'jpg', 'jpeg', 'bmp', 'JPG'])
IGNORED_FILES = set(['.gitignore'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):

    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename


def create_thumbnail(image):
    try:
        base_width = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))

        return True

    except:
        print (traceback.format_exc())
        return False

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']

        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename)
            mime_type = files.content_type

            if not allowed_file(files.filename):
                result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                files.save(uploaded_file_path)

                # create thumbnail after saving
                if mime_type.startswith('image'):
                    create_thumbnail(filename)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mime_type, size=size)
            tag_images()
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) and f not in IGNORED_FILES ]

        for f in os.listdir(app.config['UPLOAD_FOLDER']):
          f = os.path.join(app.config['UPLOAD_FOLDER'], f)
          if os.path.isfile(f) and f not in IGNORED_FILES:
            files = [f]

        file_display = []

        for f in files:
            #size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            size = os.path.getsize(f)
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))

@app.route('/tag_images', methods=['GET', 'POST'])
def tag_images():
    # Activate Clarifai here.
    #process_all_images()
    anythin = read_file(app.config['OUTPUT'], 0)
    #session['anythin'] = anythin

    return render_template('index.html', anythin = anythin)

@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})

# serve static files
@app.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename=filename)


@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)

#@app.route('/table', methods=['GET', 'POST'])
def read_file(filename, output_type):
    try:
        with open(os.getcwd() + filename, 'r') as json_data:
                d = json.load(json_data)
                #print (type(d))
                con_lis = []
                #print (con_lis)
        #print ('starting')
        if not output_type == 0:
        #print (d)
            for key, value in d.iteritems():
            #for key, value in d.items():
                con_lis.append([key, value[0], value[1], value[2], value[3], value[4], value[5], value[6]])
            return con_lis
            
        elif output_type == 1:
            for key, value in d.iteritems():
                con_lis.append(key, 
            return d
    except:
        print ('false!!')


@app.route('/recipes', methods=['GET', 'POST'])
def show_recipe_full():
    d = read_file(app.config['RECIPIE'], 1)
    return render_template('index.html', d = d)

@app.route('/', methods=['GET', 'POST'])
def index():
    session['anythin'] = ''
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
