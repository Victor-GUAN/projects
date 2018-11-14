
"""
Created on Tue Mar 28 01:00:11 2017

@author: Minghui GUAN
"""

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
    mydata['msg'] = "Hello Javascript."
    print mydata
    return jsonify(result=mydata)
def hello_world():  
    return 'Hello world!'  
    
if __name__ == '__main__':
    app.run(port="80")
     
'''app = Flask(__name__)  
     
@app.route('/',methods=['GET','POST'])  
def hello_world():  
    return 'Hello world!'  
      
if __name__ == '__main__':
    app.run()'''
