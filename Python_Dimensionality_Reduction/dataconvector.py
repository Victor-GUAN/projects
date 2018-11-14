
"""
Created on Tue Mar 28 01:00:11 2017

@author: Minghui GUAN
"""

'''import json                  # Python build-in function
from flask import jsonify    # Flask build-in function
from flask import Flask
from flask import request
app = Flask()
@app.route('/dataconvector')
def dataConvector():
    mydata = json.loads(request.args.get('mykey'))
    mydata['msg'] = "Hello Javascript."
    return jsonify(result=mydata)'''
    
from flask import Flask  
      
app = Flask(__name__)  
     
@app.route('/',methods=['GET','POST'])  
def hello_world():  
    return 'Hello world!'  
      
if __name__ == '__main__':
    app.run()