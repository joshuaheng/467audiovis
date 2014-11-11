from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import urllib2
import json
import ast
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    url = request.json['url']
    print url
    if request.method == 'POST':
        print "Hello world! this is a HTTP POST"
        req = urllib2.Request('http://api.soundcloud.com/resolve.json?url='+url+'&client_id=1a7c545524e6ae578d151a9096b051d4')
        res = urllib2.urlopen(req)
        #convert curl response from string to json object
        #result is the resolved track information
        result = json.loads(res.read())
        trackid = result['id']
        #execute curl search to get all comments for this trackid
        req = urllib2.Request("http://api.soundcloud.com/tracks/"+str(trackid)+"/comments.json?client_id=1a7c545524e6ae578d151a9096b051d4")
        res = urllib2.urlopen(req)
        comments = res.read()
        #list of all comments object for a given song
        comments = ast.literal_eval(comments)
        return jsonify(result=comments)
    else:
        print "Hello world! this is a HTTP GET"
        return "search done"

if __name__ == '__main__':
    app.debug = True
    app.run()