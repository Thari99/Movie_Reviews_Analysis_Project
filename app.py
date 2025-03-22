from flask import Flask,render_template,request,redirect
from prediction_pipline import preprocessing,vectorizer,get_Prediction

app = Flask(__name__)

data = dict()
reviews=[]
positive = 0
negative = 0

@app.route("/")
def index():
    data['reviews']=reviews
    data['positive'] = positive
    data['negative'] = negative

    return render_template('index.html',data=data)

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