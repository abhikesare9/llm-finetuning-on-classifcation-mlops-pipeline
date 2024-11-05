
from fastapi import FastAPI
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import uvicorn
from threading import Thread

# Initialize FastAPI app
app = FastAPI()

# Load model and tokenizer
model_path = "pubhealthcustommodel"  # Replace with your model path or name
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Initialize text classification pipeline
nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Define the classification route
@app.post("/classify/")
def classify_text(text: str):
    result = nlp(text)
    return {"result": result}

# Run the app with Uvicorn in a new thread
def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start the FastAPI app in a new thread
server = Thread(target=run)
server.start()
