#our web app framework!

#you could also generate a skeleton from scratch via
#http://flask-appbuilder.readthedocs.io/en/latest/installation.html

#Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the
#HTML escaping on your own to keep the application secure. Because of that Flask configures the Jinja2 template engine 
#for you automatically.
#requests are objects that flask handles (get set post, etc)
from flask import Flask, render_template,request
#scientific computing library for saving, reading, and resizing images
from scipy.misc import imsave, imread, imresize
#for matrix math
import numpy as np
#for importing our keras model
import keras.models
#for regular expressions, saves time dealing with string data
import re
# for converting base64 
import base64
# for imagae processing
import imageio
#system level operations (like loading files)
import sys 
#for reading operating system data
import os
#tell our app where our saved model is
sys.path.append(os.path.abspath("./model"))
from load import * 

from PIL import Image

#initalize our flask app
app = Flask(__name__)
#global vars for easy reusability
global model, graph
#initialize these variables
model, graph = init()

#decoding an image from base64 into raw representation
def convertImage(imgData1):
	#print(type(base64.b64decode(imgData1)))
	#print(base64.decodebytes(imgData1))
	#imgstr = re.search(r'base64,(.*)',imgData1).group(1)
	#print(imgstr)
	imgstr = base64.b64decode(imgData1)
	with open('output.png','wb') as output:
		output.write(imgstr)
	

@app.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("index.html")

@app.route('/predict/',methods=['GET','POST'])
def predict():
	#whenever the predict method is called, we're going
	#to input the user drawn character as an image into the model
	#perform inference, and return the classification
	#get the raw data format of the image
	imgstring = request.get_data()
	# size of the image differs from image to image
	print("Länge: ", sys.getsizeof(imgstring))
	imgData = re.sub('^data:image/.+;base64,', '', imgstring.decode('utf-8'))
	#print(type(imgData))
	#encode it into a suitable format
	convertImage(imgData)
	#print("debug")
	#read the image into memory
	x = imread('output.png',mode='L')
	#y = Image.open('output.png')
	#print(type(y))
	#print(y.size)
	#y1 = y.resize((28,28))
	#print(type(y1))
	#print(y1.size)
	
	#compute a bit-wise inversion so black becomes white and vice versa
	x = np.invert(x)

	#make it the right size
	x = imresize(x,(28,28))
	#imshow(x)
	#print(type(x))
	
	#x = np.array(y1)
	#print(x.shape)
	
	#convert to a 4D tensor to feed into our model
	x = x.reshape(1,28,28,1)
	#print("debug2")
	#in our computation graph
	with graph.as_default():
		#perform the prediction
		out = model.predict(x)
		print(out)
		print(np.argmax(out,axis=1))
		#print("debug3")
		#convert the response to a string
		response = np.array_str(np.argmax(out,axis=1))
		return response	
	

if __name__ == "__main__":
	#decide what port to run the app in
	port = int(os.environ.get('PORT', 5000))
	#run the app locally on the givn port
	app.run(host='0.0.0.0', port=port)
	#optional if we want to run in debugging mode
	#app.run(debug=True)
