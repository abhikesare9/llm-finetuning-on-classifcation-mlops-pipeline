import torch
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration, TrainingArguments, Trainer
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# Step 1: Initialize the FastAPI app
app = FastAPI()

# Step 2: Load the RAG tokenizer and retriever
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq",trust_remote_code=True)
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)

# Step 3: Load the RAG model for token generation
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

# Step 4: Define the input format for the API
class ClaimInput(BaseModel):
    claim: str
    main_text: str

# Step 5: Load dataset and create knowledge base
# Assuming you have a dataset in CSV format with 'main_text' and 'claim' columns
df = pd.read_csv('../raw_data/PUBHEALTH/merged.csv')  # Your dataset path
knowledge_base = df['main_text'].tolist()

# Index the knowledge base
retriever.index_knowledge_documents(knowledge_base)

# Step 6: Define the endpoint for the chatbot
@app.post("/chatbot/")
async def get_claim_response(input_data: ClaimInput):
    # Tokenize inputs
    inputs = tokenizer(input_data.claim, return_tensors="pt")

    # Generate response
    with torch.no_grad():
        generated = model.generate(input_ids=inputs['input_ids'], num_beams=2, max_length=200)

    # Decode the response
    output_text = tokenizer.decode(generated[0], skip_special_tokens=True)
    return {"response": output_text}

# Step 7: Fine-tuning (optional)
def fine_tune_rag(dataset):
    # Set training arguments
    training_args = TrainingArguments(
        output_dir='./results',         
        num_train_epochs=3,              
        per_device_train_batch_size=2,  
        save_steps=10_000,               
        save_total_limit=2,              
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model,                         
        args=training_args,                  
        train_dataset=dataset,  # Your dataset here
    )

    # Fine-tune the model
    trainer.train()

# Step 8: Run the FastAPI app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
