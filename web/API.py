import json
from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_cors import CORS

import json
import operator
import numpy as np
import pickle, string, re
from pyvi import ViTokenizer, ViPosTagger
from keras.models import Model
from keras.models import load_model
from keras.preprocessing.text import *
from keras.preprocessing.sequence import *

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

MODEL = ""

listLabel = 'FOOD#STYLE&OPTIONS,FOOD#PRICES,FOOD#QUALITY,DRINKS#STYLE&OPTIONS,DRINKS#QUALITY,DRINKS#PRICES,RESTAURANT#GENERAL,RESTAURANT#MISCELLANEOUS,RESTAURANT#PRICES,LOCATION#GENERAL,SERVICE#GENERAL,AMBIENCE#GENERAL'
categories = listLabel.split(',')
maxLength = 548

@app.route('/setmodel', methods=['POST'])

def normalText(sent):
    sent = str(sent).replace('_',' ').replace('/',' trên ')
    sent = re.sub('-{2,}','',sent)
    sent = re.sub('\\s+',' ', sent)
    patPrice = r'([0-9]+k?(\s?-\s?)[0-9]+\s?(k|K))|([0-9]+(.|,)?[0-9]+\s?(triệu|ngàn|trăm|k|K|))|([0-9]+(.[0-9]+)?Ä‘)|([0-9]+k)'
    patURL = r"(?:http://|www.)[^\"]+"
    sent = re.sub(patURL,'website',sent)
    sent = re.sub(patPrice, ' giá_tiền ', sent)
    sent = re.sub('\.+','.',sent)
    sent = re.sub('(hagtag\\s+)+',' hagtag ',sent)
    sent = re.sub('\\s+',' ',sent)
    return sent

def deleteIcon(text):
    text = text.lower()
    s = ''
    pattern = r"[a-zA-ZaăâbcdđeêghiklmnoôơpqrstuưvxyàằầbcdđèềghìklmnòồờpqrstùừvxỳáắấbcdđéếghíklmnóốớpqrstúứvxýảẳẩbcdđẻểghỉklmnỏổởpqrstủửvxỷạặậbcdđẹệghịklmnọộợpqrstụựvxỵãẵẫbcdđẽễghĩklmnõỗỡpqrstũữvxỹAĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXYÀẰẦBCDĐÈỀGHÌKLMNÒỒỜPQRSTÙỪVXỲÁẮẤBCDĐÉẾGHÍKLMNÓỐỚPQRSTÚỨVXÝẠẶẬBCDĐẸỆGHỊKLMNỌỘỢPQRSTỤỰVXỴẢẲẨBCDĐẺỂGHỈKLMNỎỔỞPQRSTỦỬVXỶÃẴẪBCDĐẼỄGHĨKLMNÕỖỠPQRSTŨỮVXỸ,._]"
    
    for char in text:
        if char !=' ':
            if len(re.findall(pattern, char)) != 0:
                s+=char
            elif char == '_':
                s+=char
        else:
            s+=char
    s = re.sub('\\s+',' ',s)
    return s.strip()


def clean_doc(doc):
    for punc in string.punctuation:
        doc = doc.replace(punc,' '+ punc + ' ')
    doc = normalText(doc)
    doc = deleteIcon(doc)
    doc = ViTokenizer.tokenize(doc)
    doc = doc.lower()
    doc = re.sub(r"\?", " \? ", doc)
    doc = re.sub(r"[0-9]+", " num ", doc)
    for punc in string.punctuation:
        if punc not in "_":
            doc = doc.replace(punc,' ')
    doc = re.sub('\\s+',' ',doc)
    return doc

def setter():
    global MODEL
    if request.method == "POST":
        try:
            MODEL = request.get_json()['Model']
        except:
            return 'error'
    return 'ok'

def sentiment_analysis(sentence):
    # code cua m bo vo day
    #print(sentence)
    return jsonify(sentence)
app.add_url_rule('/sentiment-analysis/<string:sentence>', 'sentiment_analysis', sentiment_analysis)

def index():
    return "ok"
app.add_url_rule('/', 'index', index)

app.run(host='localhost', port=8080, debug=True) 