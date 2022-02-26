import flask
import os
import threading    #god save the queen or something why do people hate threadss
import json
import types
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
#os.environ["FLASK_ENV"] = "production"

TESTING = False
SOLO = False

homedir = os.path.expanduser("~")
with open(homedir + "/stemplayerplayer_config.json") as json_file:
        tempjson = json.load(json_file)
        UPLOAD_FOLDER = tempjson['SPP_HOME']
ALLOWED_EXTENSIONS = {'mp3','wav','flac'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#startstop_bridge = 1
globalthread = types.SimpleNamespace()

# this was absolutely copied
class ThreadingExample(object):
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        thread = globalthread

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            app.run(port=1337)

def start_bridge(startstop_bridge):
    print(startstop_bridge)
    global globalthread
    if startstop_bridge==1:
        #startstop_bridge=0
        #app.config
        example = ThreadingExample()
        print("bridge started!\n")
    elif startstop_bridge==0:
        #startstop_bridge=1
        globalthread._running = False
        print("bridge stopped!")
    #return startstop_bridge

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/stembridge_upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.form['folder'])
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file specified')
            return redirect(request.url)
        file = request.files['file']
        folder = request.form['folder']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '' or folder is None:
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], folder)):
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder))
            if folder:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], folder, filename))
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "success"
        else: return "fail"
    if TESTING is True:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=text name=folder>
          <input type=submit value=Upload>
        </form>
        '''
    else: return "enabled"

#test variable
if SOLO is True:
    app.run(port=1337)
