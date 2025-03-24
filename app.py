from flask import Flask,render_template,request,redirect
from prediction_pipline import preprocessing,vectorizer,get_Prediction

# Initialize Flask application
app = Flask(__name__)

# Global variables to hold reviews and sentiment counts
data = dict()
reviews=[]
positive = 0
negative = 0

# Route for the index page (GET request)
@app.route("/")
def index():
    data['reviews']=reviews
    data['positive'] = positive
    data['negative'] = negative

    return render_template('index.html',data=data)

# Route to handle review submission 
@app.route("/",methods=['post'])
def my_post():
    text = request.form['text']
    preprosessed_txt = preprocessing(text)
    vectorized_txt = vectorizer(preprosessed_txt)
    prediction = get_Prediction(vectorized_txt)

    if prediction == 'negative':
        global negative
        negative +=1
    else:
        global positive
        positive +=1
    reviews.insert(0,text)
    return redirect(request.url)

if __name__ =="__mail__":
    app.run()