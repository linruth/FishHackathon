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

	return redirect('/thankyou');

@app.route('/thankyou')
def thankyou():
	return render_template("thankyou.html")

def filter_animal(choice, animal):
	if choice == "All":
		return True
	elif choice == "No" and animal == "None":
		return True
	elif choice == "Yes" and animal != "None":
		return True
	else:
		return False

def filter_depth(choice, depth):
	if choice == "All":
		return True
	elif choice == "Shore" and depth == "Shore":
		return True
	elif choice == "Ocean floor" and depth == "Ocean floor":
		return True
	elif choice == "Floating" and depth == "Floating":
		return True
	else:
		return False

def filter_recovered(choice, recovered):
	if choice == "All":
		return True
	elif choice == "Yes" and recovered == "Yes":
		return True
	elif choice == "No" and recovered == "No":
		return True
	else:
		return False

def filter_material(choice, recovered):
	if choice == "All":
		return True
	elif choice == "Synthetic" and recovered == "Synthetic":
		return True
	elif choice == "Mesh" and recovered == "Mesh":
		return True
	else:
		return False

@app.route('/display', methods=['GET', 'POST'])
def display():
	
	item_choice = request.form["item"]
	animal_choice = request.form["animal"]
	depth_choice = request.form["depth"]
	recovered_choice = request.form["isRecovered"]
	material_choice = request.form["material"]

	return_list = []
	results = firebase.get('/', None)
	count = 1
	for id in results.keys():

		if (filter_recovered(recovered_choice, results[id]["Recovered"]) and filter_material(material_choice, results[id]["Material"]) and filter_animal(animal_choice, results[id]["Animals"]) and results[id]["Item"] == item_choice and filter_depth(depth_choice, results[id]["Depth"])):
			local_list = []
			local_list.append(count)
			local_list.append(results[id]["Item"])
			local_list.append(results[id]["Animals"])
			local_list.append(results[id]["Recovered"])
			local_list.append(results[id]["Depth"])
			local_list.append(results[id]["Lat"])
			local_list.append(results[id]["Lon"])

			return_list.append(local_list)
			count = count + 1
	return render_template("display_entries.html", return_list=return_list)

@app.route('/find', methods=['GET'])
def find():
	return render_template("findindex.html")

if __name__ == '__main__':
    app.run()
