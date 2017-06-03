"""
filename: 
	record.py
author: 
	Theodore J. LaGrow
language: 
	python 2.7x
use: 
	This program is designed to record a wav file of your voice
packages required:
	pyaudio
	wave
notes:
	***THIS PROGRAM IS NOT WORKING ON FLASK, USE FOR STUB PURPOSES AND DEVELOPMENT IN FUTURE.***
"""


import pyaudio
import wave

# global variables
RECORD_SECONDS = 5


def record():
	"""
	This program was developed in total to see if it will record on flask.  Although we are able to run 
	locally, pythonanywhere does not have the pyaudio package required to run this program.

	"""

	# format variables to correctly get wav files
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024
	WAVE_OUTPUT_FILENAME = "file.wav"
	
	# initialize the pyaudio package
	audio = pyaudio.PyAudio()
	 
	# start recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
		rate=RATE, input=True,
		frames_per_buffer=CHUNK)

	# simple print to tell user 
	print("recording...")
	# init list to help deal with the chucks and frames that come with wav files
	frames = []
	 
	# start piecing together the audio as it comes in
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	print("finished recording")
	 
	 
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	 
	# generate the wav file
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

if __name__ == "__main__":
	record()