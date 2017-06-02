#!/bin/bash


#updating pip:
apt-get install software-properties-common
apt-add-repository universe
apt-get update
apt-get install python-pip

#installing pyaudio:
apt-get install portaudio19-dev
python -m pip install pyaudio
