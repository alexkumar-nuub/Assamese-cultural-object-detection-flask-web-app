import predict as prdct

from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app=Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return render_template('index.html')

@app.route('/api/pred/', methods=['GET', 'POST'])
def pred():
    isUrl = request.form['isUrl']
    file = request.files['file']
    if os.path.isfile(f"./outputs/temp") is True:
        os.remove(f"./outputs/temp")
    file.save('./outputs/temp')
    capResult = prdct.pred('./outputs/temp')
    return jsonify(img_url="True", response = "00",
                   capResult=capResult)

@app.route('/',methods=['POST'])
def predict():
    return ('', 204)

@app.route('/outputs/<path:path>')
def send_outputs(path):
    return send_from_directory('outputs', path)
        
if __name__ == '__main__':
    app.run(port=3000,debug=True)