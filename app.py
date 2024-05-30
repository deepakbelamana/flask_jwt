import datetime
from flask import Flask,jsonify,session,render_template,request
import jwt

app=Flask(__name__)
app.config['SECURITY_KEY']='16b6e8fb778e418789a0e9ab90e0da9c'
app.secret_key='16b6e8fb778e418789a0e9ab90e0da9c'

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else: 
        return 'logged in currently'

@app.route('/login',methods=['post'])
def login():
    if request.form['username'] and request.form['password'] == 'amadmin':
        session['logged_in']=True
        token=jwt.encode({
            'username': request.form['username'],
            'expiration': str(datetime.datetime.now()+datetime.timedelta(seconds=120))},app.secret_key)
        return jsonify({'token':token})
    else: 
        return 'invalid credentials'
    
if(__name__=='__main__'):
    app.run(debug=True)