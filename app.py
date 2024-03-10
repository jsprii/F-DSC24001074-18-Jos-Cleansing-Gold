import re
import sqlite3
import pandas as pd
import os
from cleansing_slang import clean_slang
from cleansing_abusive import clean_abusive
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from, LazyJSONEncoder, LazyString

import re
import pandas as pd

from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)

app.json_provider_class = LazyJSONEncoder
app.json = LazyJSONEncoder(app)
 

swagger_template = dict(
    info={
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
        },
    host=LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                    config=swagger_config)

#Load data cleansing slang dan abusive
conn = sqlite3.connect('simple_apiv3/data/slang.db')
df_slang = pd.read_sql('''SELECT * FROM slangwords''', conn)
conn.close()
conn2 = sqlite3.connect('simple_apiv3/data/abusive.db')
df_abusive = pd.read_sql('''SELECT * FROM abusivewords''', conn2)
conn2.close()

#Extend cleansing
def clean_text(text):
    if isinstance(text, float):
        text = str(text)
        
    cleaned_text = clean_slang(re.sub(r'\\x..', '', text), df_slang) #Menghapus dari database untuk df_slang
    cleaned_text = clean_abusive(re.sub(r'\\x..', '', cleaned_text), df_abusive) #Menghapus dari database untuk df_abusive
    cleaned_text = re.sub(r'\d', '', cleaned_text) #Menghapus angka dari teks
    cleaned_text = re.sub(r'RT USER', '', cleaned_text) #Menghapus "RT USER"
    cleaned_text = re.sub(r'\\\\n|\\n', '', cleaned_text) #Menghapus kata \\n dan \n
    cleaned_text = re.sub(r'[^\w\s,.?!]', '', cleaned_text) #Menghapus karakter selain huruf, angka, spasi, koma, titik, tanda tanya, dan tanda seru
    cleaned_text = re.sub(r'\bUSER\b', '', cleaned_text) #Menghapus kata "USER" 
    cleaned_text = re.sub(r'(\?{2,})', '?', cleaned_text) #Menghapus karakter "?" lebih dari 2 berturut-turut menjadi 1 saja
    cleaned_text = re.sub(r'(\,{2,})', '', cleaned_text) #Menghapus karakter "," lebih dari 2 berturut-turut menjadi 1 saja
    cleaned_text = re.sub(r'(\.{2,})', '.', cleaned_text) #Menghapus karakter "." lebih dari 2 berturut-turut menjadi 1 saja
    cleaned_text = re.sub(r'(\!{2,})', '!', cleaned_text) #Menghapus karakter "!" lebih dari 2 berturut-turut menjadi 1 saja
    cleaned_text = re.sub(r'[ð½]', '', cleaned_text) #Menghapus karakter "ð½"
    cleaned_text = re.sub(r'(?<=^)\.', '', cleaned_text) #Menghapus "." di kata awal
    cleaned_text = re.sub(r'\s{2,}', '', cleaned_text) #Menghapus spasi lebih dari 2

    return cleaned_text


#Halaman Awal
@app.route('/')
def hello():
    return "Hi! Selamat Datang 👋"

#Text Input
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    cleaned_text = clean_text(text)


    json_response = {
        'status_code': 200,
        'description': "Text Cleaned",
        'data': cleaned_text
    }

    response_data = jsonify(json_response)
    return response_data

#File Input ke folder
UPLOAD_FOLDER = 'simple_apiv3/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#File input
@swag_from("docs/data.yml", methods=['POST'])
@app.route("/uploadfiles", methods=['POST'])
def uploadFiles():
      # Save file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
           uploaded_file.save(file_path)
          # Read File
           df = pd.read_csv(file_path,encoding="ISO-8859-1", sep='/Next/')
           first_column = df.iloc[:,0].tolist()
           # Cleansing
           cleaned_text=[clean_text(str(value)) for value in first_column]
      return jsonify(cleaned_text)

if __name__ == '__main__':
    app.run(debug=True)