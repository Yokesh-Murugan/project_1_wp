import numpy as np 
from flask import Flask, request, jsonify, render_template 
import pickle 
#importing the inputScript file used to analyze the URL 
import inputScript

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "<bLx-wd7zyRvcRj2fC_eiUwXHaiknCIw7ZQaB5d4pAKcF>"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
#load model 
app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl', 'rb'))


#Redirects to the page to give the user iput URL. 
@app.route('/')
@app.route('/predict')
def predict(): 
	return render_template('Final.html') 

#Fetches the URL given by the URL and passes to inputScript
@app.route('/y_predict', methods=['POST'])
def y_predict(): 

	url = request.form['URL']
	checkprediction = inputScript.main(url)
	prediction = model.predict(checkprediction)
	print(prediction)
	output=prediction[0]
	if(output==1): 
		pred="Your are safe!! This is a Legitimate Website."
	else:
		pred="You are on the wrong site. Be cautious!"
	return render_template('final.html', prediction_text='{}'.format(pred), url=url)
	
@app.route('/predict_api', methods=['POST'])
def predict_api():

	# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6a9f6b1c-79ce-46bc-a11f-c2d694e7d71d/predictions?version=2022-11-10', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
	output = prediction[0]
	return jsonify(output)

if  __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)