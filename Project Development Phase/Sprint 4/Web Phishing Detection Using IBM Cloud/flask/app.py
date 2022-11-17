import numpy as np
from flask import Flask, render_template, request, redirect, jsonify
from markupsafe import escape

import inputScript  
import requests

app = Flask(__name__)


API_KEY = "9ZgwCALvmlWQ1gMn-1P0H05YWQ9QnxVfBQRBH7mqDXZ5"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}




@app.route('/')
def predict():
    return render_template("final2.html")


@app.route('/predict',methods=["POST"])
def y_predict():
    url = request.form['url']
    check_predic = inputScript.main(url)
    
    payload_scoring = {"input_data": [{"field": [["UsingIP", "LongURL", "ShortURL", "Symbol@", "Redirecting//", "PrefixSuffix-", "SubDomains", "HTTPS","DomainRegLen", "Favicon", "NonStdPort", "HTTPSDomainURL", "RequestURL", "AnchorURL", "LinksInScriptTags",
    "ServerFormHandler", "InfoEmail", "AbnormalURL", "WebsiteForwarding", "StatusBarCust", "DisableRightClick","UsingPopupWindow", "IframeRedirection", "AgeofDomain", "DNSRecording", "WebsiteTraffic", "PageRank",
    "GoogleIndex", "LinksPointingToPage", "StatsReport"]], "values": [[1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 0, 1, 1, 1, 1, -1, -1, -1, -1, 1, 0, 1]]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6db6587e-44b1-4ab1-b4ac-0af6e2e5b883/predictions?version=2022-11-15',json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    prediction=(response_scoring.json())
   


   
    predic=prediction['predictions'][0]['values'][0][0]

    
    if(predic==-1):
        pred = "You are safe!! This is a Legimate Website :)"
    elif(predic==1):
        pred = "You are in a phishing site. Dont Trust :("
    else:
        pred = "You are in a suspecious site. Be Cautious ;("

    return render_template("final2.html", pred_text = '{}'.format(pred), url = url)


"""@app.route('/predict_api', methods = ['POST'])
def predict_api():

    data = request.get_json(force = True)
    predic = model.y_predict([np.array(list(data.values()))])
    result = predic[0]
    return jsonify(result)"""

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
