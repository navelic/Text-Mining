from flask import Flask, render_template, request
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.probability import FreqDist
from nltk.tokenize import blankline_tokenize
from plotly.offline import plot
from plotly.graph_objs import Bar
from flask import Markup
app=Flask(__name__)
@app.route('/send')
def sum():
    return render_template("test.html")

@app.route('/send', methods=['POST'])
def some():
    cont = request.form['cont']
    cont_tokens=word_tokenize(cont)
   
    punctuation=re.compile(r'[-.?!,:;()|0-9]')
    post_punc=[]
    for i in cont_tokens:
        j=punctuation.sub("",i)
        if(len(j)>0):
            post_punc.append(j)
    stop_words = stopwords.words('english')
    post_punc1=[word for word in post_punc if word not in stop_words]
    size=len(post_punc1)
    
    pst=PorterStemmer()
    post_punc_stem=[]
    for i in post_punc1:
        post_punc_stem.append(pst.stem(i))
    blank1=blankline_tokenize(cont)
    lb=len(blank1)
    fdist=FreqDist()
    for i in post_punc_stem:
        fdist[i.lower()]+=1
        df=pd.DataFrame(list(fdist.items()),columns=["Word","Absolute Frequency"])
        df['Relative Frequency']=df["Absolute Frequency"]/size
    df1=df.sort_values(by ='Absolute Frequency' , ascending =False)
    df1=df1.head()
    f1=plot([Bar(x=df1["Word"],y=df1["Absolute Frequency"])],output_type='div')
 
    f2=plot([Bar(x=df["Word"],y=df["Absolute Frequency"])],output_type='div')
    
    return render_template("index.html",df=df.to_html(classes="table table-striped"),f1=Markup(f1),f2=Markup(f2),blank1=lb)

if __name__=="__main__":
    app.run()
    
