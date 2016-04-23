from xml.etree.ElementTree import fromstring

from flask import Flask, render_template, request,json,jsonify, redirect
import urllib

app = Flask(__name__)

@app.route('/')
def hello_world():
    print("hello");
    #return render_template("index.html");


if __name__ == '__main__':
    app.run()