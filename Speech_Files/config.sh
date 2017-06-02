#!/bin/bash


#updating pip:
sudo apt-get install software-properties-common
sudo apt-add-repository universe
sudo apt-get update
sudo apt-get install python-pip

#installing pyaudio:
sudo apt-get install portaudio19-dev
sudo python3 -m pip install pyaudio