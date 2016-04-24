from xml.etree.ElementTree import fromstring
from firebase import firebase
from imgurpython import ImgurClient

from flask import Flask, render_template, request,json,jsonify, redirect
import urllib

import random
import string




app = Flask(__name__)
firebase = firebase.FirebaseApplication("https://boiling-torch-8247.firebaseio.com/#-KG09txqVpTw6jUmqcas|c3c8dd314bcafecb0cf13741fe2b0825", None)

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

@app.route('/')
def hello_world():
    print("hello");
    return render_template("index2.html");


@app.route('/add', methods=['POST'])
def add():
	id = id_generator()
	route = "/" + id
	result = firebase.get(route, None)
	while result != None:
		id = id_generator()
		route = "/" + id
		result = firebase.get(route, None)
	item = request.form["item"]
	animal = request.form["animal"]
	depth = request.form["depth"]
	recovered = request.form["isRecovered"]
	material = request.form["material"]
	lat = request.form["lat"]
	lon = request.form["lon"]
	photo = request.form["photo"]
	print lon
	print photo

	route = "/" + id
	firebase.put(route, "Item", item)
	firebase.put(route, "Animals", animal)
	firebase.put(route, "Depth", depth)
	firebase.put(route, "Recovered", recovered)
	firebase.put(route, "Material", material)
	firebase.put(route, "Lat", lat)
	firebase.put(route, "Lon", lon)
	firebase.put(route, "Photo", photo)

	return redirect('/');

@app.route('/thankyou')
def thankyou():
	return render_template("thankyou.html")



# @app.route('/image_upload', methods=['POST'])
# def upload_file():
# 	item = request.form["my_image"];
# 	print (item);
# 	return render_template("/")
#     # upload_result = None
#     # thumbnail_url1 = None
#     # print("before post");
#     # if request.method == 'POST':
#     # 	print("after post")
#     #     file = request.files['my_image']
#     #     print("request files")
#     #     if file:
#     #     	print("enter if")
#     #     	upload_result = upload(file)
#     #     	thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format = "jpg", crop = "fill", width = 100, height = 100)
#     #     	print(public_id)
    
#     #return render_template('/')



# @app.route('/uploadpage')
# def you():
# 	return render_template("imageform.html")











@app.route('/display', methods=['GET'])
def display():
	item = "Net"
	recovered = False
	return_list = []
	results = firebase.get('/', None)

	for id in results.keys():
		if (results[id]["Item"] == item) and (results[id]["Recovered"] == recovered):
			local_list = []
			local_list.append(results[id]["Item"])
			local_list.append(results[id]["Animals"])
			local_list.append(results[id]["Recovered"])
			return_list.append(local_list)
	return render_template("display_entries.html", return_list=return_list)

if __name__ == '__main__':
    app.run()
