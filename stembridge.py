import flask
import os
import threading    #god save the queen or something why do people hate threads
import types
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
os.environ["FLASK_ENV"] = "production"

UPLOAD_FOLDER = "C:\stemplayer\\"
ALLOWED_EXTENSIONS = {'mp3','wav','flac'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
startstop = 1
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

def start_bridge():
    global globalthread
    global startstop
    if startstop==1:
        startstop=0
        app.config
        example = ThreadingExample()
        print("bridge started!\n")
    elif startstop==0:
        startstop=1
        globalthread._running = False
        print("bridge stopped!")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/stembridge_upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('download_file', name=filename))
            return "success"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
