from flask import  request,session,redirect,render_template,send_from_directory,Flask,url_for
from flask import *
import flask_wtf
import wtforms
import db
from datetime import timedelta

app = Flask(__name__)
app.secret_key = b'haissaiviavbdaivb'
session_sub = {'mail':'','pwd':'','login':'','warn':''}

def check_login():
    if session_sub['login'] == 'True':
        return True 
    return False

def check_premium():
    if check_login():
        data = db.serch_fromMail(session_sub['mail'])#SQLからデータを取得
        if data[0][2] == "pro":
            return True
    return False

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'warn' not in session_sub:
        session_sub['warn'] = ''

    if(request.method == "POST"):
        session_sub['login'] = 'True'
        if 'mail' in request.form and 'pwd' in request.form:
            data = db.serch_fromMail(request.form["mail"])#SQLからデータを取得
            print(data[0][0])
            if data[0][1] == request.form["pwd"]:
                print("correct pwd")
                session_sub['mail'] = request.form["mail"]
                session_sub['pwd'] = request.form["pwd"]
                session_sub['login'] = 'True'
                print(data[0][0])
                session_sub['warn'] = ''
                return redirect(url_for('index',session_sub=session_sub))   
            else:
                session_sub['warn'] = 'unmatch'
                print(session_sub['warn'])
                return redirect(url_for('login',session_sub=session_sub))    
    else:
        return render_template("login.html",session_sub=session_sub)

@app.route('/logout')
def logout():
    session_sub['login'] = 'False'
    return redirect(url_for('index',session_sub=session_sub))   

@app.route('/register', methods=["GET", "POST"])
def register():
    if 'warn' not in session_sub:
        session_sub['warn'] = ''
    if(request.method == "POST"):
        if 'mail' in request.form and 'pwd' in request.form and 'pwdconf' in request.form:
            if request.form['pwd'] == request.form['pwdconf']:#confirmの確認
                if db.insert(request.form['mail'],request.form['pwd'],"free"):#メール重複の確認
                    session_sub['mail'] = request.form["mail"]
                    session_sub['pwd'] = request.form["pwd"]
                    session_sub['login'] = 'True'
                    session_sub['warn'] = ''
                    return redirect(url_for('index',session_sub=session_sub))
                else:
                    session_sub['warn'] = 'overlapping'
                    print(session_sub['warn'])
                    return redirect(url_for('register',session_sub=session_sub))
            else:
                session_sub['warn'] = 'pwdmismatch'
                print(session_sub['warn'])
                return redirect(url_for('register',session_sub=session_sub))
        else:
            return redirect(url_for('register',session_sub=session_sub))

    else:
        return render_template("register.html",session_sub=session_sub)

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
    return render_template("index.html",session_sub=session_sub)

@app.route("/index.html")
def index_sub():
    return render_template("index.html",session_sub=session_sub)


@app.route("/craft.html", methods=['GET']) 
def craft():
    if check_login():
        if check_premium():
            Basic = ['Basic',[['BB','BasicBlock','True'],
                    ['BB1','BasicBlock','True'],
                    ['BB2','BasicBlock','True']]]
        
            Wheel = ['Wheel',[['TB','Wheel big','True'],['TM','Wheel mini','True'],['BT','Ball Wheel','True']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True']]]
            Sensor = ['Sensor',[['CS','Color Sensor','True'],['RF','RangeFinder','True']]]


        else:   
            Basic = ['Basic',[['BB','BasicBlock','True'],
                        ['BB1','BasicBlock','True'],
                        ['BB2','BasicBlock','True']]]
        
            Wheel = ['Wheel',[['TB','Wheel big','True'],['TM','Wheel mini','True'],['BT','Ball Wheel','True']]]

            Motor = ['Motor',[['MB','Motor big','True'],
                        ['MN','Motor','True'],
                        ['MM','Motor mini','True']]]
            Sensor = ['Sensor',[['CS','Color Sensor','False'],['RF','RangeFinder','True']]]

        parts = [Basic,Wheel,Motor,Sensor]
        return render_template("craft.html",parts=parts,session_sub=session_sub)
    else:
        return redirect(url_for('login',session_sub=session_sub))    
@app.route("/mission.html", methods=['POST', 'GET']) 
def mission():
    if check_login():
        return render_template("mission.html",session_sub=session_sub)
    else:
        return redirect(url_for('login',session_sub=session_sub))    

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
        return redirect(url_for('login',session_sub=session_sub))    


@app.route("/program.html", methods=['POST', 'GET']) 
def program():
    if check_login():
        return render_template("program.html")
    else:
        return redirect(url_for('login',session_sub=session_sub))    



if __name__ == "__main__":
    app.run(debug=True ,threaded=True)
