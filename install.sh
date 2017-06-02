#!/bin/sh

git clone https://github.com/tjlagrow/CIS-422-Group-Project-2.git
cd CIS-422-Group-Project-2/flask-file-uploader-master
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
clarifai config
#need creds