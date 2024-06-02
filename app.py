from functools import wraps
from flask import Flask, jsonify, make_response, request, render_template
import jwt
import datetime
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notasecuredkey'

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token')
        print("Token:", token)
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # # Decode without verifying the signature to inspect payload
            # payload = base64_url_decode(token.split('.')[1] + '==').decode('utf-8')
            # print("Payload:", payload)
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print("Decoded data:", data)
        except Exception as e:
            print("Error decoding token:", e)
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    return decorator

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.form['password'] == 'admin':
        payload = {
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    
    return make_response('Could not verify', 401)

@app.route('/protected')
@token_required
def protected():
    return 'This is only available for users with a valid token.'

@app.route('/unprotected')
def unprotected():
    return 'This is available for everyone!'

if __name__ == '__main__':
    app.run(debug=True)
