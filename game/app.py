from flask import  *
app = Flask(__name__)  # アプリの設定


@app.route("/manifest.json")
def manifest():
    return send_from_directory("static","manifest.json")

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

@app.route("/",methods=["GET","POST"])  # どのページで実行する関数か設定
def m():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/craft.html", methods=['POST', 'GET']) 
def craft():
    return render_template('craft.html')

@app.route("/mission.html", methods=['POST', 'GET']) 
def mission():
    return render_template('mission.html')

@app.route("/missionSelect.html", methods=['POST', 'GET']) 
def missionSelect():
    return render_template('missionSelect.html')


@app.route("/program.html", methods=['POST', 'GET']) 
def program():
    return render_template('program.html')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)