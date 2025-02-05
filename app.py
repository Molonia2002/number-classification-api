from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
import os
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
	power = len(digits) 
	return sum(d ** power for d in digits) == n

def digit_sum(n): 
	return sum(int(d) for d in str(n))
 

# Function to calculate the sum of digits
def get_fun_fact(n):
	try:  
		response = requests.get(f"http://numberapi.com/{n}/math?json")
		if response.status_code == 200:
			return response.json().get("text", "No fun fact available.")
		return "No fun available."
	except Exception: 
		return "Error fetching fun fact."

@app.route("/")
def home(): 
	return "Hello, your Flask API is running on Render!"

# API endpoint 
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
	number = request.args.get('number')
		
	if not number or not number.isdigit():
		return jsonify({"error": "Invalid input. Please provide a valid number."}), 400
 
	number = int(number)

	# Determine properties 
	properties = []
	if is_armstrong(number):
		properties.append("armstrong")
	if number % 2 == 0:
		properties.append("odd")
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
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
