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


#main
@app.route("/",methods=["GET","POST"]) 
def m():
    if check_login():
        return render_template("index.html")
    else:
        return redirect('/login')

@app.route("/index.html")
def index():
    if check_login():
        return render_template("index.html")
    else:
        return redirect('/login')

@app.route("/craft.html", methods=['POST', 'GET']) 
def craft():
    if check_login():
        return render_template("craft.html")
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
        return render_template("missionSelect.html")
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