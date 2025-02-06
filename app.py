import os
import json
import math 
from flask import Flask, request, jsonify

app = Flask(__name__)

def classify_number(n):
	"""Classifies a number and returns its properties."""
	properties ={
		"even": n % 2 == 0,
		"odd": n % 2 != 0, 
		"prime": is_prime(n), 
		"perfect_square": is_perfect_square(n), 
		"divisible_by_3": n % 3 == 0,
		"divisible_by_5": n % 5 == 0,
		"divisible_by_7": n % 7 == 0,
	}
	
	fun_fact = get_fun_fact(n) 
	
	return {
		"number": n, 
		"properties": properties, 
		"fun_fact": fun_fact 
	}

def is_prime(n): 
	"""Returns True if n is a prime number."""
	if n < 2: 
		return False 
	if n in (2, 3): 
		return True 
	if n % 2 == 0 or n % 3 == 0: 
		return False 
	i = 5
	while i * i <= n: 
		if n % i == 0 or n % (i + 2) == 0: 
			return False
		i += 6
	return True 

def is_perfect_square(n): 
	"""Returns True if n is a perfect square."""
	return n >= 0 and int(math.sqrt(n)) ** 2 == n

def get_fun_fact(n): 
	"""Returns a fun fact about the number."""
	if n % 2 == 0:
		return f"{n} is an even number."
	elif n % 5 == 0: 
		return f"{n} is divisible by 5, just like 10 and 15."
	elif is_prime(n): 
		return f"{n} is a prime number."
	else: 
		return f"{n} is a unique number with interesting properties."

@app.route('/api/classify-number/5', methods=['GET'])
def classify_number(number):
	"""Handles API requests and returns number classification."""
	try: 
		number_str = request.args.get("number")


		if number_str is None:
			return jsonify({"error": "Missing 'number' parameter"}), 400

		try:
			number = float(number_str)
			if number.is_integer(): 
				number = int(number)
		except ValueError: 
			return jsonify({"error": "Invalid number format"}), 400


		response = classify_number(number)
		return jsonify(response), 200

	except Exception as e: 
		return jsonify({"error": str(e)}), 500

if __name__ == '__main__': 
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port)
