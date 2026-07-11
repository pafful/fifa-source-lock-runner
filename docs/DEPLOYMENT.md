# Deployment Guide

## Local Development

### Prerequisites

- Python 3.12+
- Playwright browser runtime
- Optional: Docker and Docker Compose

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### Run the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker

The repository includes a Dockerfile for containerizing the FastAPI service.

### Build

```bash
docker build -t fifa-source-lock-runner:latest .
```

### Run

```bash
docker run --rm -p 8000:8000 fifa-source-lock-runner:latest
```

## Docker Compose

A sample Compose file can be used for local orchestration:

```yaml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      PYTHONUNBUFFERED: "1"
```

Run with:

```bash
docker compose up --build
```

## AWS ECR

To publish the image to Amazon ECR:

```bash
aws ecr create-repository --repository-name fifa-source-lock-runner
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
docker tag fifa-source-lock-runner:latest <account-id>.dkr.ecr.<region>.amazonaws.com/fifa-source-lock-runner:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/fifa-source-lock-runner:latest
```

## Kubernetes Deployment

Example manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fifa-source-lock-runner
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fifa-source-lock-runner
  template:
    metadata:
      labels:
        app: fifa-source-lock-runner
    spec:
      containers:
        - name: app
          image: <your-image>
          ports:
            - containerPort: 8000
          env:
            - name: PYTHONUNBUFFERED
              value: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: fifa-source-lock-runner
spec:
  selector:
    app: fifa-source-lock-runner
  ports:
    - port: 80
      targetPort: 8000
```

## GitHub Actions CI/CD

A workflow can be added under .github/workflows to run linting, tests, and container builds.

Example high-level stages:

1. Checkout repository.
2. Set up Python.
3. Install dependencies.
4. Run tests.
5. Build Docker image.
6. Push to ECR or a container registry.

## Production Considerations

- Add authentication and authorization.
- Mount persistent storage for data/ outputs.
- Use managed secrets instead of plain environment variables.
- Place the service behind a load balancer or ingress controller.
