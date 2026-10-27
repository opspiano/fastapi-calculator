import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import operations

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI(title="FastAPI Calculator")

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

class CalculationResponse(BaseModel):
    result: float

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>FastAPI Calculator</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f7fafc; }
            .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 340px; }
            h2 { margin-top: 0; color: #2d3748; text-align: center; }
            .form-group { margin-bottom: 1rem; }
            label { display: block; margin-bottom: 0.3rem; color: #4a5568; font-size: 0.9rem; }
            input, select, button { width: 100%; padding: 0.6rem; border-radius: 4px; border: 1px solid #cbd5e0; box-sizing: border-box; font-size: 1rem; }
            button { background-color: #3182ce; color: white; border: none; cursor: pointer; font-weight: bold; margin-top: 0.5rem; }
            button:hover { background-color: #2b6cb0; }
            #result { margin-top: 1.2rem; padding: 0.8rem; background-color: #edf2f7; border-radius: 4px; text-align: center; font-weight: bold; color: #2d3748; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Web Calculator</h2>
            <div class="form-group">
                <label for="num1">First Number</label>
                <input type="number" id="num1" step="any" placeholder="Enter first number">
            </div>
            <div class="form-group">
                <label for="operation">Operation</label>
                <select id="operation">
                    <option value="add">Add (+)</option>
                    <option value="subtract">Subtract (-)</option>
                    <option value="multiply">Multiply (×)</option>
                    <option value="divide">Divide (÷)</option>
                </select>
            </div>
            <div class="form-group">
                <label for="num2">Second Number</label>
                <input type="number" id="num2" step="any" placeholder="Enter second number">
            </div>
            <button id="calc-btn" onclick="calculate()">Calculate</button>
            <div id="result">Result will appear here</div>
        </div>
        <script>
            async function calculate() {
                const num1 = parseFloat(document.getElementById('num1').value);
                const num2 = parseFloat(document.getElementById('num2').value);
                const operation = document.getElementById('operation').value;
                const resultDiv = document.getElementById('result');

                if (isNaN(num1) || isNaN(num2)) {
                    resultDiv.innerText = "Error: Please enter valid numbers.";
                    return;
                }

                try {
                    const res = await fetch('/calculate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ num1, num2, operation })
                    });
                    const data = await res.json();
                    if (!res.ok) {
                        resultDiv.innerText = "Error: " + data.detail;
                    } else {
                        resultDiv.innerText = "Result: " + data.result;
                    }
                } catch (err) {
                    resultDiv.innerText = "Network Error: " + err;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/calculate", response_model=CalculationResponse)
def calculate_api(req: CalculationRequest):
    logging.info(f"API Request: {req.operation} with operands {req.num1}, {req.num2}")
    try:
        if req.operation == "add":
            res = operations.add(req.num1, req.num2)
        elif req.operation == "subtract":
            res = operations.subtract(req.num1, req.num2)
        elif req.operation == "multiply":
            res = operations.multiply(req.num1, req.num2)
        elif req.operation == "divide":
            res = operations.divide(req.num1, req.num2)
        else:
            raise HTTPException(status_code=400, detail="Unsupported operation.")
        return CalculationResponse(result=res)
    except ZeroDivisionError as e:
        raise HTTPException(status_code=400, detail=str(e))
