from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)


import requests 

app = Flask(__name__) 
CORS(app) #Enable CORS for all routes 

# Function to check if a number is a perfect number 
def is_prime(n):
	if n < 2: 
		return False
	for i in range(2, int(n**0.5) + 1):
		if n % i == 0:
			return False 
	return True

def is_perfect(n): 
	if n < 2: 
		return False 
	divisors = [i for i in range(1, n) if n % i == 0]
	return sum(divisors) == n

# Function to check if a number is an Armstrong number 
def is_armstrong(n): 
	digits = [int(d) for d in str(n)]
	num_digits = len(digits) 
	return sum(d ** num_digits for d in digits) == n

def digit_sum(n): 
	return sum(int(d) for d in str(n))
 

# Function to calculate the sum of digits
def get_fun_fact(n): 
	url = f"http://numberapi.com/{n}/math"
	response = requests.get(url)
	return response.text if response.status_code == 200 else "No fun available."

# API endpoint 
@app.route('/api/classify-number', methods=['GET'])
def classify_number(): 
	number = request.args.get('number')
	
	# Input validation 
	if not number or not number.lstrip('_').isdigit():
		return jsonify({
			"number": number if number else "null",
			"error": True 
	}), 400

	

	number = int(number) 

	# Determine properties 
	properties = []
	if is_armstrong(number):
		properties.append("armstrong")
	if number % 2 == 0:
		properties.append("even")
	else: 
		properties.append("odd")
 

	# Prepare response 
	response = {
		"number": number,
		"is_prime": is_prime(number),
		"is_perfect": is_perfect(number), 
		"properties": properties,
		"digit_sum": digit_sum(number),
		"fun_fact": get_fun_fact(number)
	}

	return jsonify(response), 200

# Run the app
if __name__ == '__main__': 
	
	serve(app, host='0.0.0.0', port=8000)
