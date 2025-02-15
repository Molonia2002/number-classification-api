from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import requests
from starlette.responses import JSONResponse

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: list[str]
    digit_sum: int
    fun_fact: str


class ErrorResponse(BaseModel):
    number: str
    error: bool


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
    digits = [int(d) for d in str(abs(n))]
    power = len(digits)
    return sum(d ** power for d in digits) == abs(n)


def fetch_fun_fact(n: int) -> str:
    """Fetch a fun fact about the number from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException:
        pass
    return f"{n} is an interesting number!"


def classify_number(n: int) -> dict:
    """Classify the number and return its properties."""
    properties = ["even" if n % 2 == 0 else "odd"]

    if is_prime(n):
        properties.append("prime")
    if is_perfect(n):
        properties.append("perfect")
    if is_armstrong(n):
        properties.append("armstrong")

    digit_sum = sum(int(d) for d in str(abs(n)))

    return {
        "number": n,
        "is_prime": is_prime(n),
        "is_perfect": bool(is_perfect(n)),  # Ensure boolean type
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fetch_fun_fact(n)
    }


@app.get("/api/classify-number", response_model=NumberResponse)
async def classify_number_api(number: str = Query(..., description="The number to classify")):
    """API endpoint to classify numbers."""
    if not number.lstrip("-").isdigit():  # Check for invalid input
        return JSONResponse(
            status_code=400,
            content={"number": "alphabet", "error": True}  # **EXACT required JSON format**
        )

    return classify_number(int(number))


@app.get("/api/classify-number/{number}", response_model=NumberResponse)
async def classify_number_path(number: str):
    """Alternate API endpoint that allows numbers in the URL path."""
    if not number.lstrip("-").isdigit():  # Check for invalid input
        return JSONResponse(
            status_code=400,
            content={"number": "alphabet", "error": True}  # **EXACT required JSON format**
        )

    return classify_number(int(number))
