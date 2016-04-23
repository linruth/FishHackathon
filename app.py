from xml.etree.ElementTree import fromstring
from firebase import firebase

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
	print lon

	route = "/" + id
	firebase.put(route, "Item", item)
	firebase.put(route, "Animals", animal)
	firebase.put(route, "Depth", depth)
	firebase.put(route, "Recovered", recovered)
	firebase.put(route, "Material", material)
	firebase.put(route, "Lat", lat)
	firebase.put(route, "Lon", lon)

	return redirect('/');


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
