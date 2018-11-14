
"""
Created on Tue Mar 28 01:00:11 2017

@author: Minghui GUAN
"""
import base64
import json                  # Python build-in function
from flask import jsonify    # Flask build-in function
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/Flask/dataconvert',methods=['GET','POST'])
def dataconvert():
    mydata = json.loads(request.args.get('mykey'))
	
	with open(mydata['msg'], "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
	
    mydata['msg'] = encoded_string
	
    return jsonify(result=mydata) 
    
if __name__ == '__main__':
    app.run(port="80")
