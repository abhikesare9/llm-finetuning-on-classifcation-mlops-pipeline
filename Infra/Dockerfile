# Step 1: Use an official Python runtime as the base image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the working directory
COPY requirements.txt /app/

# Step 4: Install Python dependencies
RUN pip  install accelerate peft bitsandbytes transformers trl 

# Step 5: Copy the FastAPI application code into the container
COPY app.py/ /app/
COPY pubhealthcustommodel /app/

# Step 6: Expose port 8000 (the default FastAPI port)
EXPOSE 8000

# Step 7: Define the command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
