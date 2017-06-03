## This is the Food_Files folder for the Hopper's Heapin' Jalapeños.

This directory contains code which is adapted from goberoi's github. The files here handle the image tagging functionality of the app.
Contents:

* README.md: this README file.
* output: a directory which contains the filtered output in a file called foods.json. 
* input_images: a directory which contains the images that the user selected to be uploaded to the application.
* vendors: a directory which contains the program to call the API (contains only a program to call Clarifai for now)
* __init__.py: allows for flask_app.py to import this directory's programs and run the functions of the programs.
* tag_images.py: the main program which will got through all of the photos in input_images and tag the images with
  foods that the API thinks are in the given pictures.
