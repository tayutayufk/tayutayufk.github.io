from flask import  request,session,redirect,render_template,send_from_directory,Flask
from flask import *
import flask_wtf
import wtforms

app = Flask(__name__)
app.secret_key = b'haissaiviavbdaivb'

def check_login():
    if 'login' in session:
        if session['login'] == 'True':
            return True 
    return False

@app.route("/login", methods=["GET", "POST"])
def login():
    
    if(request.method == "POST"):
        if 'mail' in request.form and 'pwd' in request.form:
            session['mail'] = request.form["mail"]
            session['pwd'] = request.form["pwd"]
            session['login'] = 'True'
            print(session['mail'] + " was login!")

        print(session['login'])
        return redirect('/')
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session['login'] = 'False'
    return redirect('/')


#PWA
@app.route("/manifest.json")
def manifest():
    return send_from_directory("static","manifest.json")

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

@app.route('/favicon.png')
def favicon():
   return app.send_static_file('icon.png')


#main
@app.route("/",methods=["GET","POST"]) 
def m():
    if check_login():
        state = "login"
    else:
        state="logout"

    return render_template("index.html",state=state)

@app.route("/index.html")
def index():
    if check_login():
        state = "login"
    else:
        state="logout"

    return render_template("index.html",state=state)

@app.route("/craft.html", methods=['POST', 'GET']) 
def craft():
    if check_login():
        parts = {}
        Basic = [['BB','BasicBlock'],
                    ['BB1','BasicBlock'],
                    ['BB2','BasicBlock']]
        
        Wheel = [['TB','Wheel big'],['TM','Wheel mini'],['BT','Ball Wheel']]

        Motor = [['MB','Motor big'],
                ['MN','Motor'],
                ['MM','Motor mini']]
        Sensor = [['CS','Color Sensor'],['RF','RangeFinder']]

        parts['Basic'] = Basic
        parts['Wheel'] = Wheel
        parts['Motor'] = Motor
        parts['Sensor'] = Sensor
        return render_template("craft.html",parts=parts)
    else:
        return redirect('/login')

@app.route("/mission.html", methods=['POST', 'GET']) 
def mission():
    if check_login():
        return render_template("mission.html")
    else:
        return redirect('/login')

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
        return redirect('/login')


@app.route("/program.html", methods=['POST', 'GET']) 
def program():
    if check_login():
        return render_template("program.html")
    else:
        return redirect('login')



if __name__ == "__main__":
    app.run(debug=True)