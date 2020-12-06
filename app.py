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

app = Flask(__name__)
app.secret_key = db.flask_key

stripe_keys = {
  'secret_key': db.SECRET_KEY,
  'publishable_key': db.PUBLISHABLE_KEY
}

stripe.api_key = stripe_keys['secret_key']

def check_login():
    if 'mail' in session and 'pwd' in session and 'login' in session:
        if session['login'] == 'True':
            return True 
    return False

def check_premium():
    if check_login():
        data = db.serch_fromMail(session['mail'])#SQLからデータを取得
        if data[0][2] == "pro":
            session['ver'] = "pro"
            return True
        else:
            session['ver'] = "free"
    return False

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'warn' not in session:
        session['warn'] = ''

    if(request.method == "POST"):
        session.permanent = True
        session['login'] = 'True'
        if 'mail' in request.form and 'pwd' in request.form:
            data = db.serch_fromMail(request.form["mail"])#SQLからデータを取得
            if data[0][1] == request.form["pwd"]:
                print("correct pwd")
                session['mail'] = request.form["mail"]
                session['pwd'] = request.form["pwd"]
                session['login'] = 'True'
                session['warn'] = ''
                check_premium()
                return redirect(url_for('index'))   
            else:
                session['warn'] = 'unmatch'
                print(session['warn'])
                return redirect(url_for('login'))    
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session['login'] = 'False'
    return redirect(url_for('index'))   

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'warn' not in session:
        session['warn'] = ''
    if(request.method == "POST"):
        if 'mail' in request.form and 'pwd' in request.form and 'pwdconf' in request.form:
            if request.form['pwd'] == request.form['pwdconf']:#confirmの確認
                if db.insert(request.form['mail'],request.form['pwd'],"free"):#メール重複の確認
                    session['mail'] = request.form["mail"]
                    session['pwd'] = request.form["pwd"]
                    session['login'] = 'True'
                    session['warn'] = ''
                    return redirect(url_for('index'))
                else:
                    session['warn'] = 'overlapping'
                    print(session['warn'])
                    return redirect(url_for('register'))
            else:
                session['warn'] = 'pwdmismatch'
                print(session['warn'])
                return redirect(url_for('register'))
        else:
            return redirect(url_for('register'))

    else:
        return render_template("register.html")


@app.route('/regenerate', methods=["GET", "POST"])
def regenerate():
    if request.method == "GET":
        return render_template("regenerate.html")
    
    if request.method == "POST":
        dat = request.form["mail"]
        session['mail'] = dat
        hs = hashlib.md5(dat.encode()).hexdigest()
        url = url_for('changepwd', h = hs)
        url = "https://ropeproject.sakura.ne.jp" + url
        #send mail
        account = "ropeproject@ropeproject.sakura.ne.jp"
        password = "oppython3"
    
        to_email = request.form["mail"]
        from_email = "ropeproject@ropeproject.sakura.ne.jp"
 
        subject = "Please reset your password"
        message = "This email is sent to the person who will be reissuing the RoPE password. Please follow the link below to reissue it.\r\n" + url +"\nPlease destroy this email if you do not recognize it."
        print(message)
        msg = MIMEText(message, "html")
        msg["Subject"] = subject
        msg["To"] = to_email
        msg["From"] = from_email
        server = smtplib.SMTP("ropeproject.sakura.ne.jp", 587)
        server.starttls()
        server.login(account, password)
        server.send_message(msg)
        server.quit()

        return redirect(url_for('index'))

@app.route('/changepwd')
def changepwd():
    if request.method == "GET":
        if 'mail' not in session:
            return redirect(url_for('index'))
        mail = session['mail']
        if request.form["h"] == hashlib.md5(mail.encode()).hexdigest():
            return render_template("changepwd.html")
    
    if request.method == "POST":
        if request.form['pwd'] == request.form['pwdconf']:
            newpwd = request.form['pwd']
            data = db.serch_fromMail(session['mail'])#SQLからデータを取得
            version = data[0][2]

            db.delete(session['mail'])
            db.insert(session['mail'],newpwd,version)
            return redirect(url_for('login'))

        else:
            session['warn'] = 'pwdmismatch'
            return redirect(url_for('changepwd'))

   
#Stripe
@app.route('/charge', methods=['POST'])
def charge():
    amount = 500
    customer = stripe.Customer.create(
        email=session['mail'],
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('payed.html', amount=amount)


@app.route('/charge')
def payed():
   return render_template("payed.html")

#PWA
@app.route("/manifest.json")
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

@app.route('/favicon.ico')
def favicon():
   return app.send_static_file('favicon.png')


#main
@app.route("/",methods=["GET","POST"]) 
def index():
    return render_template("index.html",key=stripe_keys['publishable_key'])

@app.route("/index.html")
def index_sub():
    return render_template("index.html",key=stripe_keys['publishable_key'])


@app.route("/craft.html", methods=['GET']) 
def craft():
    if check_login():
        if check_premium():
            Basic = ['Basic',[['BB','BasicBlock','True'],
                                ['BB1','BasicBlock','True'],
                                ['BB2','BasicBlock','True'],
                                ['BasicBlockHeavy','Heavy Block','True'],
                                ['EdgeBlock1','Edge 1','True'],
                                ['EdgeBlock2','Edge 2','True'],
                                ['HalfBlock','Edge 3','True'],
                                ['BasicBlock-1','Advance Block','True'],
                                ['BasicBlock-2','Advance Block','True'],
                                ['BasicBlock-3','Advance Block','True']]]
        
            Wheel = ['Wheel',[['TB','Wheel big','True'],
                            ['TM','Wheel mini','True'],
                            ['BallTire','Ball Wheel','True'],
                            ['Axle','Axle','True']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True'],
                        ['SB','Servo large','True'],
                        ['SM','Servo mini','True']]]

            Sensor = ['Sensor',[['CS','Color Sensor','True'],['RF','RangeFinder','True']]]


        else:   
            Basic = ['Basic',[['BB','BasicBlock','True'],
                                ['BB1','BasicBlock','True'],
                                ['BB2','BasicBlock','True'],
                                ['BasicBlockHeavy','Heavy Block','True'],
                                ['EdgeBlock1','Edge 1','True'],
                                ['EdgeBlock2','Edge 2','True'],
                                ['HalfBlock','Edge 3','True'],
                                ['BasicBlock-1','Advance Block','True'],
                                ['BasicBlock-2','Advance Block','True'],
                                ['BasicBlock-3','Advance Block','True']]]
        
            Wheel = ['Wheel',[['TB','Wheel big','True'],
                            ['TM','Wheel mini','True'],
                            ['BallTire','Ball Wheel','True'],
                            ['Axle','Axle','True'],
                            ['Bearing','Bearing','True']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True'],
                        ['SB','Servo large','True'],
                        ['SM','Servo mini','True']]]

            Sensor = ['Sensor',[['CS','Color Sensor','False'],['RF','RangeFinder','True']]]

        parts = [Basic,Wheel,Motor,Sensor]
        return render_template("craft.html",parts=parts)
    else:
        return redirect(url_for('login'))    
@app.route("/mission.html", methods=['POST', 'GET']) 
def mission():
    if check_login():
        return render_template("mission.html")
    else:
        return redirect(url_for('login'))    

@app.route("/missionSelect.html", methods=['POST', 'GET']) 
def missionSelect():
    if check_login():
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
    if check_login():
        return render_template("program.html")
    else:
        return redirect(url_for('login'))    



if __name__ == "__main__":
    app.run(debug=True ,threaded=True)
