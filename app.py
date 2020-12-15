from flask import  request,session,redirect,render_template,send_from_directory,Flask,url_for,make_response
from flask import *
import flask_wtf
import wtforms
import db
import datetime
import os
import stripe

from email.mime.text import MIMEText
import smtplib

import hashlib
from email.mime.text import MIMEText

import urllib.parse
import json
import base64


app = Flask(__name__)
app.secret_key = db.flask_key

stripe_keys = {
  'secret_key': db.SECRET_KEY,
  'publishable_key': db.PUBLISHABLE_KEY
}

stripe.api_key = stripe_keys['secret_key']

def init_session():
    session['login'] = 'False'
    session['mail'] = ''
    session['pwd'] = ''
    session['ver'] = 'free'
    session['warn'] = ''
    session['stage'] = 'basic'

def check_premium():
    if session['login'] == 'True':
        data = db.search_fromMail(session['mail'])#SQLからデータを取得
        if data[0][2] == "pro":
            session['ver'] = "pro"
            return True
        else:
            session['ver'] = "free"
    return False

def send_mail(to_email,subject,message):
    #send mail
    account = "ropeproject@ropeproject.sakura.ne.jp"
    password = db.mail_pass
    from_email = "ropeproject@ropeproject.sakura.ne.jp"
         
    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email
    server = smtplib.SMTP("ropeproject.sakura.ne.jp", 587)
    server.starttls()
    server.login(account, password)
    server.send_message(msg)
    server.quit()
    return

@app.route("/login", methods=["GET", "POST"])
def login():
    state = "asd"
    redirect_url = request.host_url[:-1] + url_for('check')
    return redirect('https://accounts.google.com/o/oauth2/auth?{}'.format(urllib.parse.urlencode({
        'client_id': db.google_id,
        'scope': 'email',
        'redirect_uri': redirect_url,
        'state': state,
        'openid.realm': request.host_url,
        'response_type': 'code'
    })))
    
    """
    if request.method == "POST":
        if 'mail' in request.form and 'pwd' in request.form:
            data = db.serch_fromMail(request.form["mail"])#SQLからデータを取得
            if len(data) == 0:
                session['warn'] = 'unmatch'
                return redirect(url_for('login'))    
            if data[0][1] == request.form["pwd"]:
                init_session()
                session['mail'] = request.form["mail"]
                session['pwd'] = request.form["pwd"]
                session['login'] = 'True'
                check_premium()
                return redirect(url_for('index'))   
            else:
                session['warn'] = 'unmatch'
                return redirect(url_for('login'))    
    else:
        session['login'] = 'False'
        return render_template("login.html")
    """

@app.route('/login/check')
def check():
    if request.args.get('state') != "asd":
        return 'invalid state'
    redirect_url = request.host_url[:-1] + url_for('check')
    dat = urllib.request.urlopen('https://www.googleapis.com/oauth2/v4/token', urllib.parse.urlencode({
        'code': request.args.get('code'),
        'client_id': db.google_id,
        'client_secret': db.google_sec,
        'redirect_uri': redirect_url,
        'grant_type': 'authorization_code'
    }).encode('ascii')).read()

    dat = json.loads(dat.decode('ascii'))

    id_token = dat['id_token'].split('.')[1]
    id_token = id_token + '=' * (4 - len(id_token)%4)
    id_token = base64.b64decode(id_token, '-_')
    id_token = json.loads(id_token.decode('ascii'))

    data = db.search_fromMail(id_token['email'])
    if len(data) == 0:
        seed = db.google_id + id_token['email']
        pwd = hashlib.md5(seed.encode()).hexdigest()
        if db.insert(id_token['email'],pwd,"free"):
            init_session()
            session['mail'] = id_token['email']
            session['pwd'] = pwd
            session['login'] = 'True'
    else:
        init_session()
        session['mail'] = id_token['email']
        session['pwd'] = data[0][1]
        session['login'] = 'True'
        session['ver'] = data[0][2]

    return redirect(url_for('index'))   

@app.route('/logout')
def logout():
    init_session()
    return redirect(url_for('index'))   

#Stripe
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 500,
                        #'receipt_email': session['mail'],
                        'product_data': {
                            'name': 'RoPE',
                            'images': [request.host_url[:-1] + '/static/img/white.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.host_url[:-1] + url_for('index'),
            cancel_url=request.host_url[:-1] + url_for('index'),
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403
    
@app.route('/payed')
def payed():
   return render_template("payed.html")

#PWA
@app.route("/manifest.json")
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/service-worker.js',methods=['GET'])
def sw():
    return app.send_static_file('service-worker.js')

@app.route('/favicon.ico')
def favicon():
   return app.send_static_file('favicon.png')


#main
@app.route("/",methods=["GET","POST"]) 
def index():
    if 'login' not in session:
        init_session()
    return render_template("index.html",key=stripe_keys['publishable_key'])

@app.route("/index.html")
def index_sub():
    if 'login' not in session:
        init_session()
    return render_template("index.html",key=stripe_keys['publishable_key'])


@app.route("/craft.html", methods=['GET']) 
def craft():
    if session['login'] == 'True':
        if session['stage'] == 'basic':
            Basic = ['Basic',[['BB','BasicBlock','True'],
                                ['BB1','BasicBlock','True'],
                                ['BB2','BasicBlock','True'],
                                ['BasicBlockHeavy','Heavy Block','False']]]
            
            Advance = ['Advance',[['EdgeBlock1','Edge 1','False'],
                                ['EdgeBlock2','Edge 2','False'],
                                ['HalfBlock','Edge 3','False'],
                                ['BasicBlock-1','Advance Block','False'],
                                ['BasicBlock-2','Advance Block','False'],
                                ['BasicBlock-3','Advance Block','False']]]
        
            Wheel = ['Wheel',[['TB','Wheel big','True'],
                            ['TM','Wheel mini','True'],
                            ['BallTire','Ball Wheel','True'],
                            ['Axle','Axle','False'],
                            ['Bearing','Bearing','False'],
                            ['Bearing_Locked','Fixed axle','False']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True'],
                        ['SB','Servo large','False'],
                        ['SM','Servo mini','False'],
                        ['Solenoid_mini','Solenoid mini','False']]]

            Sensor = ['Sensor',[['CS','Color Sensor','False'],['RF','RangeFinder','False']]]

        elif session['stage'] == "line_trace":
            Basic = ['Basic',[['BB','BasicBlock','True'],
                                ['BB1','BasicBlock','True'],
                                ['BB2','BasicBlock','True'],
                                ['BasicBlockHeavy','Heavy Block','False']]]
            
            Advance = ['Advance',[['EdgeBlock1','Edge 1','True'],
                                ['EdgeBlock2','Edge 2','True'],
                                ['HalfBlock','Edge 3','True'],
                                ['BasicBlock-1','Advance Block','False'],
                                ['BasicBlock-2','Advance Block','False'],
                                ['BasicBlock-3','Advance Block','False']]]
        
            Wheel = ['Wheel',[['TB','Wheel big','True'],
                            ['TM','Wheel mini','True'],
                            ['BallTire','Ball Wheel','True'],
                            ['Axle','Axle','True'],
                            ['Bearing','Bearing','False'],
                            ['Bearing_Locked','Fixed axle','False']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True'],
                        ['SB','Servo large','True'],
                        ['SM','Servo mini','True'],
                        ['Solenoid_mini','Solenoid mini','False']]]

            Sensor = ['Sensor',[['CS','Color Sensor','True'],['RF','RangeFinder','False']]]

        elif session['stage'] == "maze":
            Basic = ['Basic',[['BB','BasicBlock','True'],
                                ['BB1','BasicBlock','True'],
                                ['BB2','BasicBlock','True'],
                                ['BasicBlockHeavy','Heavy Block','True']]]
            
            Advance = ['Advance',[['EdgeBlock1','Edge 1','True'],
                                ['EdgeBlock2','Edge 2','True'],
                                ['HalfBlock','Edge 3','True'],
                                ['BasicBlock-1','Advance Block','True'],
                                ['BasicBlock-2','Advance Block','True'],
                                ['BasicBlock-3','Advance Block','True']]]
        
            Wheel = ['Wheel',[['TB','Wheel big','True'],
                            ['TM','Wheel mini','True'],
                            ['BallTire','Ball Wheel','True'],
                            ['Axle','Axle','True'],
                            ['Bearing','Bearing','True'],
                            ['Bearing_Locked','Fixed axle','True']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True'],
                        ['SB','Servo large','True'],
                        ['SM','Servo mini','True'],
                        ['Solenoid_mini','Solenoid mini','False']]]

            Sensor = ['Sensor',[['CS','Color Sensor','True'],['RF','RangeFinder','True']]]

        else:   
            Basic = ['Basic',[['BB','BasicBlock','True'],
                                ['BB1','BasicBlock','True'],
                                ['BB2','BasicBlock','True'],
                                ['BasicBlockHeavy','Heavy Block','True']]]
            
            Advance = ['Advance',[['EdgeBlock1','Edge 1','True'],
                                ['EdgeBlock2','Edge 2','True'],
                                ['HalfBlock','Edge 3','True'],
                                ['BasicBlock-1','Advance Block','True'],
                                ['BasicBlock-2','Advance Block','True'],
                                ['BasicBlock-3','Advance Block','True']]]
        
            Wheel = ['Wheel',[['TB','Wheel big','True'],
                            ['TM','Wheel mini','True'],
                            ['BallTire','Ball Wheel','True'],
                            ['Axle','Axle','True'],
                            ['Bearing','Bearing','True'],
                            ['Bearing_Locked','Fixed axle','True']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True'],
                        ['SB','Servo large','True'],
                        ['SM','Servo mini','True'],
                        ['Solenoid_mini','Solenoid mini','True']]]

            Sensor = ['Sensor',[['CS','Color Sensor','True'],['RF','RangeFinder','True']]]

        parts = [Basic,Advance,Wheel,Motor,Sensor]
        return render_template("craft.html",parts=parts)
    else:
        return redirect(url_for('login'))    
@app.route("/mission.html", methods=['POST', 'GET']) 
def mission():
    if request.method == "GET":
        if session['login'] == 'True':
            return render_template("mission.html")
        else:
            return redirect(url_for('login'))    
    else:
        if 'clear' in request.form:
            if request.form['clear'] == 'basic':
                session['stage'] = request.form['clear']
            elif request.form['clear'] == 'line_trace' and session['stage'] == 'basic':
                session['stage'] = request.form['clear']
            elif request.form['clear'] == 'maze' and session['stage'] == 'line_trace':
                session['stage'] = request.form['clear']

        return redirect(url_for('index'))
            
@app.route("/missionSelect.html", methods=['POST', 'GET']) 
def missionSelect():
    if session['login'] == 'True':
        missions = []
        Basic = ['basic_','Basic',[
            '<p>Go through the checkpoint.</p>',
            '<p>Go through the checkpoint.</p>',
            '<p>Go through the checkpoint.</p>',
            '<p>Go through the checkpoint.</p>'
        ]]
        LineTracking = ['line_tracking_','Line Tracking',[
            '<p>Stop above the <strong>first</strong> line!</p>',
            '<p>Stop above the <strong>second</strong> line!</p>',
            '<p>Stop above the <strong>8th</strong> line!</p>',
            '<p>Go through checkpoint.<strong>THIS COURSE CHANGE AT RANDOM.</strong></p>',
            '<p>Go through checkpoint.<strong>THIS COURSE CHANGE AT RANDOM.</strong></p>',
            '<p>This mission is time attack.You need go through goal as fast as possible. <strong>Make good use of the markings.</strong></p>'
        ]]
        Maze = ['maze_','Maze',[
            '<p>Go through the checkpoint. This wall will destroy your robot.</p>',
            '<p>Go through checkpoint.<strong>THIS COURSE CHANGE AT RANDOM.</strong></p>',
            '<p>Go through checkpoint.<strong>THIS COURSE CHANGE AT RANDOM.</strong></p>',
            '<p>Go through checkpoint.<strong>THIS COURSE CHANGE AT RANDOM.</strong></p>',
            '<p>Go through checkpoint.<strong>THIS COURSE CHANGE AT RANDOM.</strong></p>',
            '<p>Go through checkpoint.</p><strong>You probably notice that you cannot use the method you use before.</strong></p>',
            '<p>Go through checkpoint.</p>',
            '<p>Go through checkpoint.</p>',
            '<p>Go through checkpoint.</p>',
        ]]
        missions.append(Basic)
        missions.append(LineTracking)
        missions.append(Maze)
        return render_template("missionSelect.html",missions = missions)
    else:
        return redirect(url_for('login'))    


@app.route("/program.html", methods=['POST', 'GET']) 
def program():
    if session['login'] == 'True':
        return render_template("program.html")
    else:
        return redirect(url_for('login'))    



if __name__ == "__main__":
    app.run(debug=True ,threaded=True)
