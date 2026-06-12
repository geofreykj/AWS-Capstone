# AWS Bedrock RAG Application

## Overview

This project is a Retrieval-Augmented Generation (RAG) application built using AWS services and deployed on Amazon ECS. The application allows users to upload PDF and Markdown documents, stores them in Amazon S3, generates embeddings using Amazon Bedrock, stores vector embeddings in ChromaDB, and enables users to ask questions about the uploaded documents through a chat interface.

The project demonstrates the integration of multiple AWS services to build an end-to-end Generative AI solution.

---

## Architecture

### Components

* **Streamlit** – User Interface
* **Amazon ECS (Fargate)** – Application Hosting
* **Amazon ECR** – Docker Image Registry
* **Amazon S3** – Document Storage
* **Amazon Bedrock** – Embeddings and LLM Inference
* **ChromaDB** – Vector Database
* **CloudWatch Logs** – Application Logging

### Workflow

#### Document Ingestion

1. User uploads a PDF or Markdown document.
2. Document is stored in Amazon S3.
3. Application retrieves the document from S3.
4. Text is extracted from the document.
5. Text is split into smaller chunks.
6. Embeddings are generated using Amazon Bedrock.
7. Embeddings and metadata are stored in ChromaDB.

#### Question Answering

1. User submits a question.
2. Question embedding is generated using Amazon Bedrock.
3. ChromaDB performs semantic similarity search.
4. Relevant document chunks are retrieved.
5. Retrieved context and user question are sent to the LLM through Amazon Bedrock.
6. The generated response is displayed to the user.

---

## AWS Services Used

### Amazon S3

Stores uploaded documents and serves as the source for document ingestion.

### Amazon Bedrock

Used for:

* Text Embedding Generation
* Large Language Model Inference
* Retrieval-Augmented Generation Workflow

### Amazon ECS (Fargate)

Hosts the containerized Streamlit application.

### Amazon ECR

Stores and manages Docker images used by ECS.

### CloudWatch Logs

Captures application and container logs for monitoring and troubleshooting.

---

## Project Structure

```text
project-root/
│
├── app.py
│
├── services/
│   ├── s3_service.py
│   ├── ingestion_service.py
│   ├── bedrock_service.py
│   └── chroma_service.py
│
├── utils/
│   └── chunker.py
│
├── terraform/
│   ├── main.tf
│   ├── provider.tf
│   └── outputs.tf
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Features

### Document Upload

* Upload PDF files
* Upload Markdown files
* Store documents in Amazon S3

### Document Processing

* Text Extraction
* Text Chunking
* Embedding Generation
* Vector Storage

### Chat Interface

* Semantic Search
* Context Retrieval
* LLM-Based Answer Generation

---

## Deployment Workflow

### Local Development

1. Clone the repository
2. Create a Python virtual environment
3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure AWS credentials

```bash
aws configure
```

5. Run the application

```bash
streamlit run app.py
```

---

### Docker

Build the image:

```bash
docker build -t rag-capstone .
```

Run locally:

```bash
docker run -p 8501:8501 rag-capstone
```

---

### Amazon ECR

Tag image:

```bash
docker tag rag-capstone:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/rag-capstone:latest
```

Push image:

```bash
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/rag-capstone:latest
```

---

### Amazon ECS

Infrastructure is provisioned using Terraform.

Deploy:

```bash
terraform init
terraform plan
terraform apply
```

Once deployed, access the application through the ECS task public IP.

---

## Environment Variables

```env
AWS_REGION=us-east-1
BUCKET_NAME=<your-bucket-name>
MODEL_ID=<bedrock-model-id>
```

---

## Technologies Used

* Python
* Streamlit
* Boto3
* Amazon Bedrock
* Amazon S3
* Amazon ECS Fargate
* Amazon ECR
* ChromaDB
* Terraform
* Docker

---

## Future Improvements

* Persistent vector database storage
* Authentication and authorization
* Multi-user document management
* Metadata filtering
* Automated ingestion pipeline
* Load balancer and custom domain
* CI/CD pipeline

---

## Learning Outcomes

This project demonstrates:

* AWS service integration
* Containerized application deployment
* Retrieval-Augmented Generation (RAG)
* Vector database implementation
* Infrastructure as Code using Terraform
* Amazon Bedrock integration for Generative AI applications

---

## Author

AWS Capstone Project

Built as part of the AWS Generative AI Training Program.
