''' recognition of capybara images based on Fastai image training  '''
from flask import Flask, render_template, jsonify, request, Markup
from fastai.vision import open_image, load_learner #, image2np
from pathlib import Path
import settings                    # global variables
from predictor import PredictMsg   # also uses settings
settings.init()     
app = Flask(__name__, template_folder='view')

export_file_name = 'capy12.pkl'
pathExport = Path('.')
learner = load_learner(pathExport, export_file_name)
classes = ['agouti', 'beaver', 'capybara', 'cat', 'chinchilla', 'degu', 'dog', 
           'guineapig', 'nutria', 'pacarana', 'rabbit', 'squirrel']

sampleUrlHeader = '../static/'
pathPix = Path('static')
numsamples = len(settings.samples)  # filenames of image samples are in settings.py
samplenum = 0           # rotate through sample images (based on modulo)
def getNextSampleFile():    # get next sample image url 
    global samplenum, numsamples
    if samplenum>numsamples-1: samplenum = 0        # or could use modulo
    nextFile = settings.samples[samplenum]
    samplenum += 1
    return nextFile    

@app.route("/")                             # show main page
def homePage():
    return render_template("index.html")

@app.route("/about")                             # show about page
def aboutPage():
    return render_template("about.html")

@app.route('/analyze', methods=['POST'])    # after pressing "analyze" button
def analyzeImage():
    data = request.files['file']
    img = open_image(data)                    
    outputs = learner.predict(img)[2]
    themsg = PredictMsg(classes, outputs)
    return jsonify({'result': str(themsg)})

@app.route("/sample-img", methods=["GET"])  # show sample images
def showSample():
    onefile = getNextSampleFile()
    relurl = sampleUrlHeader + onefile
    img = open_image(pathPix / onefile)
    outputs = learner.predict(img)[2]
    themsg = PredictMsg(classes, outputs) + "  (Refresh page for more samples.)"
    return render_template("sample.html", themsg=Markup(themsg), img_file=relurl)

if __name__ == '__main__':
    #print ("--------restarting")
    #app.debug = True
    app.run(host='0.0.0.0')
