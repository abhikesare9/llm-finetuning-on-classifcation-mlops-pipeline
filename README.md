# ML Pipeline and Deployment Overview

This repository contains the necessary components for building, training, and deploying a machine learning model, using a variety of tools and technologies to ensure a streamlined process. Below is a high-level breakdown of each component:

## Project Structure Overview

1. **Data Preparation Pipeline**  
   The data preparation pipeline is responsible for:
   - Downloading datasets.
   - Selecting and preparing the required features for model training.

2. **Feature Engineering Pipeline**  
   - Converts labels to appropriate encodings required by the model for training.

3. **Training Pipeline**  
   - Manages the model training process.
   - Uses defined hyperparameters.
   - Saves the trained model for deployment.

4. **Deployment Pipeline**  
   - **Terraform** is used to create the EKS cluster and the associated VPC.
   - **Helm charts** are used to deploy the Docker image to the EKS cluster.
   - **JenkinsFile** is responsible for building docker image and deploy to EKS cluster through helm chart.

## Code Quality and Static Analysis

- **SonarQube**  
  SonarQube is set up using **Ansible** and will be used for static code testing and ensuring code quality throughout the development cycle.

## Model Monitoring and Drift Detection

- **Prometheus and Grafana**  
  - Deployed using **Helm charts** to monitor model performance in real-time.
  
- **Data Drift and Model Drift Monitoring**  
  - We can integrate **Amazon SageMaker**, **Vertex AI**, or **Evidently AI** modules to detect and monitor issues like data drift and model drift.

## Utility Functions

- **Logger and ConfigParser**  
  - A singleton logger is implemented for logging.
  - A configuration parser is included to manage and read config parameters efficiently.

## Model Deployment

- The trained model will be pushed to **Hugging Face** for future reference and sharing.

## Improving Model Accuracy

- **Data Cleaning**: Improving data quality can significantly boost model performance.
- **RAG (Retrieval-Augmented Generation)**: Implementing an RAG system is suggested for further model accuracy improvements.

## Directory Structure

- The **`training`** folder contains the Jupyter notebooks used during model training.
