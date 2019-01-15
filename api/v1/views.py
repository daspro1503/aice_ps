from flask import Flask,jsonify,request,Response
import models
import jwt
import datetime
from functools import wraps
app=Flask(__name__) 
test=models.ireporter()
app.config['SECRET_KEY']='Api2019'
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=request.args.get('token')
        if not token:
            return jsonify({'message':'Token is missing!'}),403
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Token is invalid'}),403
        return f(args,**kwargs)
    return decorated
@app.route('/api/v1/login',methods=['POST'])  
def login():
    auth=request.authorization
    if auth and auth.password=='password':
        token = jwt.encode({'user':auth.username,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})

    return jsonify({"status":"401","Data":"Phone number already registered please use another phone number"}),401
@app.route('/api/v1/signup', methods = ['POST'])
def sign_up():
    request_data=request.get_json()
    if not request.json :
        return "Enter parameters in acceptable json format and try again",403
    else:
        reply=test.signup(request_data['firstname'],request_data['lastname'],request_data['othername'],request_data['email'],request_data['phonenumber'],request_data['username'],request_data['password'])       
        
        return reply

@app.route('/api/v1/red-flag', methods = ['POST'])
def create_red_flag():
    request_data=request.get_json()
    if not request.json :
        return "Enter parameters in acceptable json format and try again",403
    else:
        reply=test.create_incident(request_data['CreatedBy'],request_data['i_type'],request_data['location'],request_data['images'],request_data['videos'],request_data['comment'])       
        
        
        return jsonify({'data':reply})    

@app.route('/api/v1/all_red-flags', methods = ['GET'])
@token_required
def get_all_redflags():
    request_data=request.get_json()
    if not request.json :
        return "Enter parameters in acceptable json format and try again",403
    else:
        reply=test.get_all(request_data['CreatedBy'])       
        
        #response=Response("d",201,mimetype="application/json")
        return jsonify({'data':reply})        
      
@app.route('/api/v1/edit_location/<int:id>', methods = ['PATCH'])
def edit_location(id):
    
    request_data=request.get_json()
    if not request.json :
        return "Enter parameters in acceptable json format and try again",403
    else:
        reply=test.patch_record(id,"location",request_data['value'])       
        
        #response=Response("d",201,mimetype="application/json")
        return jsonify({'data':reply})   
@app.route('/api/v1/edit_comment/<int:id>', methods = ['PATCH'])
@token_required
def edit_comment(id):
    
    request_data=request.get_json()
    if not request.json :
        return "Enter parameters in acceptable json format and try again",403
    else:
        reply=test.patch_record(id,"comment",request_data['value'])       
        
       
        return jsonify({'data':reply})  
@app.route('/api/v1/edit_images/<int:id>', methods = ['PATCH'])
def edit_images(id):
    
    request_data=request.get_json()
    if not request.json :
        return "Enter parameters in acceptable json format and try again",403
    else:
        reply=test.patch_record(id,"images",request_data['value'])       
        
        
        return jsonify({'data':reply})
@app.route('/api/v1/edit_videos/<int:id>', methods = ['PATCH'])
def edit_videos(id):
    
    request_data=request.get_json()
    if not request.json :
        return "Enter parameters in acceptable json format and try again",403
    else:
        reply=test.patch_record(id,"videos",request_data['value'])       
        
        #response=Response("d",201,mimetype="application/json")
        return jsonify({'data':reply})  
@app.route('/api/v1/delete_redflag/<int:id>', methods = ['DELETE'])
def delete_record(id):
    
    request_data=request.get_json()
    if not request.json :
        return "Enter parameters in acceptable json format and try again",403
    else:
        reply=test.delete_record(id)       
        
        #response=Response("d",201,mimetype="application/json")
        return jsonify({'data':reply})  

if __name__=='__main__':
    app.run(debug=True)