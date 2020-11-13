from flask import  request,session,redirect,render_template,send_from_directory,Flask,url_for
from flask import *
import flask_wtf
import wtforms
import db
from datetime import timedelta

app = Flask(__name__)
app.secret_key = b'haissaiviavbdaivb'


def check_login():
    if 'mail' in session and 'pwd' in session and 'login' in session:
        if session['login'] == 'True':
            return True 
    return False

def check_premium():
    if check_login():
        data = db.serch_fromMail(session['mail'])#SQLからデータを取得
        if data[0][2] == "pro":
            return True
    return False

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'warn' not in session:
        session['warn'] = ''

    if(request.method == "POST"):
        if 'mail' in request.form and 'pwd' in request.form:
            data = db.serch_fromMail(request.form["mail"])#SQLからデータを取得
            print(data[0][0])
            if data[0][1] == request.form["pwd"]:
                print("correct pwd")
                session['mail'] = request.form["mail"]
                session['pwd'] = request.form["pwd"]
                session['login'] = 'True'
                print(data[0][0])
                if 'warn' in session:
                    session['warn'] = 'null'
                
                print(session['warn'])
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
                    if 'warn' in session:
                        session['warn'] = 'null'
                    print(session['warn'])
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
    if check_login():
        state = "login"
    else:
        state="logout"

    return render_template("index.html",state=state)

@app.route("/index.html")
def index_sub():
    if check_login():
        state = "login"
    else:
        state="logout"

    return render_template("index.html",state=state)


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
        return render_template("craft.html",parts=parts)
    else:
        return redirect('login')
@app.route("/mission.html", methods=['POST', 'GET']) 
def mission():
    if check_login():
        return render_template("mission.html")
    else:
        return redirect('login')

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
        return redirect('login')


@app.route("/program.html", methods=['POST', 'GET']) 
def program():
    if check_login():
        return render_template("program.html")
    else:
        return redirect('login')



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True ,threaded=True)
