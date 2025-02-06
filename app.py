from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
import httpx
import math 

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

NUMBERS_API_URL = "http://numbersapi.com"

def is_prime(n: int) -> bool: 
	"""Check if a number is prime."""
	if n < 2:
		return False
	for i in range(2, int(math.sqrt(n)) + 1): 
		if n % i == 0: 
			return False
	return True 
	
def is_perfect(n: int) -> bool: 
	"""Check if a number is a perfect number."""
	if n < 1: 
		return False 
	return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool: 
	"""Check if a number is an Armstrong (narcissistic) number."""
	digits = [int(d) for d in str(n)]
	power = len(digits)
	return sum(d ** power for d in digits) == n

def get_fun_fact(n: int) -> str: 
	"""Fetch a fun fact from the Numbers API."""
	try: 
		response = httpx.get(f"{NUMBERS_API_URL}/{n}/math", timeout=5)
		if response.status_code == 200: 
			return response.text
		return f"No fun fact available for {n}."
	except Exception: 
		return f"Could not fetch a fun fact for {n}."

def classify_number(n: int) -> dict: 
	"""Classify the  number and return its properties."""
	properties = ["even" if n % 2 == 0 else "odd"]

	if is_armstrong(n):
		properties.insert(0, "armstrong")

	return {
		"number": n, 
		"is_prime": is_prime(n), 
		"properties": properties, 
		"digit_sum": sum(int(d) for d in str(n)), 
		"fun_fact": get_fun_fact(n) 
	}

@app.get("/api/classify-number") 
async def classify_number_api(number: int = Query(..., description="The number to classify")):
	"""API endpoint to classify numbers."""
	try: 
		return classify_number(number)
	except Exception as e: 
		raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/classify-number/{number}")
async def classify_number_path(number: int): 
	"""Alternate API endpoint that allows numbers in the  URL path."""
	try: 
		return classify_number(number)
	except Exception as e: 
		raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/classify-number", response_model=dict)
async def invalid_number(number: str = Query(..., description="Invalid number input")):
	"""Handles invalid input formats."""
	return {"number": number, "error": True}
