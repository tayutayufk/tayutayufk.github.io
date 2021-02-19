from flask import  request,session,redirect,render_template,send_from_directory,Flask,url_for,make_response,jsonify
from flask import *
import db
import datetime
import os
import stripe

from email.mime.text import MIMEText
import smtplib

import hashlib

import urllib.parse
import json
import base64
from datetime import datetime as dt
import random

app = Flask(__name__)
app.secret_key = db.flask_key

stripe.api_key = db.SECRET_KEY



def init_session():
    session['login'] = 'False'
    session['mail'] = ''
    session['pwd'] = ''
    session['ver'] = 'pro'
    session['warn'] = ''
    session['stage'] = 'maze'
    return

def check_premium():
    if session['login'] == 'True':
        data = db.search_fromMail(session['mail'])
        if data[0][2] == "pro":
            session['ver'] = "pro"
            return True
        else:
            session['ver'] = "free"
    return False

def check_hash(h):
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y/%m/%d')
    seed =  tstr[:-3] + 'RoPE'
    ser_hash = hashlib.sha256(seed.encode()).hexdigest()
    if ser_hash == h:
        init_session()
        session['login'] = 'True'
        session['ver'] = 'pro'
        ##server side 
        tdatetime = dt.now()
        tstr = tdatetime.strftime('%Y/%m/%d')
        usname = tstr + 'itch' + str(random.randint(1,10000000))
        pwd = ser_hash = hashlib.sha256(usname.encode()).hexdigest()
        db.insert(usname,pwd,session['ver'])

        ##
        return True
    else:
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
        init_session()
        seed = db.google_id + id_token['email']
        pwd = hashlib.md5(seed.encode()).hexdigest()
        if db.insert(id_token['email'],pwd,session['ver']):
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
@app.route('/payment')
def payment():
    if session['login'] == 'False':
        return redirect(url_for('login'))

    if session['ver'] == "free":
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price':'price_1I9nkSKTMlPLG6E8diP0odDO',
                'quantity':1,
            }],
            mode='payment',
            success_url= url_for('payed',_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = url_for('index',_external=True),
        )
        session['StripeID'] = checkout_session['id']
        return render_template(
            "payment.html",
            checkout_session_id = checkout_session['id'],
            checkout_public_key = db.PUBLISHABLE_KEY
            )
    else:
        return redirect(url_for('index'))


@app.route('/payed')
def payed():
    if 'session_id' not in request.args:
        return redirect(url_for('index'))
    pay_id = request.args.get('session_id')
    if 'StripeID' in session:
        if session['StripeID'] == pay_id:
            db.upgrade(session['mail'])
            session['ver'] = "pro"
            return render_template("payed.html")
    return redirect(url_for('index'))

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

@app.route("/.well-known/assetlinks.json")
def assetlinks():
    return app.send_static_file('assetlinks.json')

#main
@app.route("/",methods=["GET","POST"]) 
def index():
    if 'login' not in session:
        init_session()

    
    if 'from' in request.args:
        fromsite = request.args.get('from')
        #from itch
        if fromsite == 'itch':
            session['login'] = 'True'

            tdatetime = dt.now()
            tstr = tdatetime.strftime('%Y/%m/%d')
            usname = tstr + 'itch' + str(random.randint(1,10000000))
            pwd = ser_hash = hashlib.sha256(usname.encode()).hexdigest()
            db.insert(usname,pwd,session['ver'])
            return render_template("index.html")

        if fromsite == 'android' and 'h' in request.args:
            h = request.args.get('h')
            check_hash(h)
            return render_template("index.html")
    

    #session['login'] = 'True'
    #session['ver'] = 'free'
    return render_template("index.html")

@app.route("/index.html")
def index_sub():
    if 'login' not in session:
        init_session()

    
    if 'from' in request.args:
        fromsite = request.args.get('from')
        #from itch
        if fromsite == 'itch':
            session['login'] = 'True'

            tdatetime = dt.now()
            tstr = tdatetime.strftime('%Y/%m/%d')
            usname = tstr + 'itch' + str(random.randint(1,10000000))
            pwd = ser_hash = hashlib.sha256(usname.encode()).hexdigest()
            db.insert(usname,pwd,session['ver'])
            return render_template("index.html")
    
        if fromsite == 'android' and 'h' in request.args:
            h = request.args.get('h')
            check_hash(h)
            return render_template("index.html")

    #session['login'] = 'True'
    #session['ver'] = 'free'
    return render_template("index.html")

@app.route("/craft.html", methods=['GET']) 
def craft():

    #if 'login' not in session:
    #    init_session()
    #    return redirect(url_for('login'))
    if 'login' in session:
        if session['ver'] == 'free':
            Basic = ['Basic',[['BB','BasicBlock','True'],
                                ['BB1','BasicBlock','True'],
                                ['BB2','BasicBlock','True'],
                                ['BasicBlockHeavy','Heavy Block','True']]]
            
            Advance = ['Advance',[['EdgeBlock1','Edge 1','True'],
                                ['EdgeBlock2','Edge 2','True'],
                                ['HalfBlock','Edge 3','True'],
                                ['BasicBlock-1','Advance Block','False'],
                                ['BasicBlock-2','Advance Block','False'],
                                ['BasicBlock-3','Advance Block','False']]]
        
            Wheel = ['Wheel',[['Tire_big2','Wheel L','False'],
                            ['TB','Wheel M','True'],
                            ['TM','Wheel S','True'],
                            ['BallTire','Ball Wheel','True'],
                            ['Axle','Axle','True'],
                            ['Bearing','Bearing','False'],
                            ['Bearing_Locked','Fixed axle','False']]]

            Motor = ['Motor',[['MB','Motor big','False'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True'],
                        ['Thruster','Thruster','True'],
                        ['Servomotor_big','Servo large','False'],
                        ['Servomotor_mini','Servo mini','False'],
                        ['Solenoid_mini','Solenoid mini','False']]]

            Sensor = ['Sensor',[['CS','Color Sensor','True'],['RF','RangeFinder','False'],['Gyro','Gyro','False']]]
        elif session['ver'] == 'pro':
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
        
            Wheel = ['Wheel',[['Tire_big2','Wheel L','True'],
                            ['TB','Wheel M','True'],
                            ['TM','Wheel S','True'],
                            ['BallTire','Ball Wheel','True'],
                            ['Axle','Axle','True'],
                            ['Bearing','Bearing','True'],
                            ['Bearing_Locked','Fixed axle','True']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True'],
                        ['Thruster','Thruster','True'],
                        ['Servomotor_big','Servo large','True'],
                        ['Servomotor_mini','Servo mini','True'],
                        ['Solenoid_mini','Solenoid mini','True']]]

            Sensor = ['Sensor',[['CS','Color Sensor','True'],['RF','RangeFinder','True'],['Gyro','Gyro','True']]]

        parts = [Basic,Advance,Wheel,Motor,Sensor]
        return render_template("craft.html",parts=parts)
@app.route("/mission.html", methods=['POST', 'GET']) 
def mission():

    #if 'login' not in session:
    #    init_session()
    #    return redirect(url_for('login'))

    if request.method == "GET":
        return render_template("mission.html")
        #if session['login'] == 'True':
        #    return render_template("mission.html")
        #else:
        #    return redirect(url_for('login'))    
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
    #if 'login' not in session:
    #    init_session()
    #    return redirect(url_for('login'))
    if 'login' in session:
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



@app.route("/program.html", methods=['POST', 'GET']) 
def program():
    return render_template("program.html")
    #if session['login'] == 'True':
    #    return render_template("program.html")
    #else:
    #    return redirect(url_for('login'))    



if __name__ == "__main__":
    app.run( debug=True ,threaded=True)
