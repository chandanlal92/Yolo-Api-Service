# YOLO API Service

This project provides an API service that uses a YOLO (You Only Look Once) model to detect objects in an image and draw bounding boxes around them. The API accepts an S3 bucket_name of the image where it is stored and Object_Name of Image, processes the image using the YOLO model, and returns the image with bounding boxes.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Software](#running-the-software)
  - [Locally](#locally)
  - [Using Docker](#using-docker)
  - [Using Kubernetes](#using-kubernetes)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Accepts an image URL from an S3 bucket.
- Uses a YOLO model to detect objects in the image.
- Draws bounding boxes around detected objects.
- Returns the processed image as a downloadable file.

## Prerequisites

- Python 3.9+
- Docker
- Docker Desktop (for Kubernetes deployment)
- AWS CLI (optional, for S3 integration)
- kubectl (for Kubernetes deployment)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/yolo-api-service.git
   cd yolo-api-service
2. Create a virtual environment (recommended):
   ```sh
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
   ```sh

3. Install Python Dependencies
    ```sh
    pip install -r requirements.txt
    ```sh
4. Set up AWS credentials (if using S3): 
    Create a .env file in the root directory:
    ```sh
    AWS_ACCESS_KEY_ID=your-access-key-id
    AWS_SECRET_ACCESS_KEY=your-secret-access-key
    ```sh
## Running the Software

1. Running the Application Locally
   ```sh
    python -m uvicorn main:app --reload
   ```sh

   The API will be available at http://localhost:5000.
2. Using Docker
   1. Build the Docker image:
   ```sh
    docker build -t yolo-api-service:1.0 .
   ```sh

   2. Run the Docker container:
    ```sh
    docker run -p 5000:5000 yolo-api-service:1.0
    ```sh
   3. Access the API:
    The API will be available at http://localhost:5000.
3. Using Kubernetes
   1. Create a Kubernetes secret for AWS credentials:
    ```sh
        kubectl create secret generic aws-credentials \
        --from-literal=aws-access-key-id=your-access-key-id \
        --from-literal=aws-secret-access-key=your-secret-access-key
    ```sh

   2. Apply the Kubernetes deployment:
    ```sh
        kubectl apply -f deployment.yaml
    ```sh
     
    3. Access the API:
      Minikube:
        ```sh
           minikube service yolo-api-service
        ```sh

## Testing
    Run Unit and Integration Tests  
    1. Install testing dependencies (if not already installed):
    ```sh
          pip install pytest requests
    ```sh
    2. Run all tests:
    ```sh
          python -m pytest tests/
    ```sh
    3. Run tests with coverage:
    ```sh
        pip install pytest-cov
        python -m pytest --cov=app tests/
    ```sh

## Example Test Command

    ```sh
            curl -X POST http://localhost:5000/process-image \
            -H "Content-Type: application/json" \
            -d '{
                "bucket_name": "test-bucket",
                "object_key": "test-image.jpg"
            }'
    ```sh

## API End Points

    API Endpoints
    POST /process-image
    Process an image from an S3 bucket and return the image with bounding boxes.

    Request Body:
    ```sh
    {
    "bucket_name": "your-bucket-name",
    "object_key": "path/to/your/image.jpg"
        }
    ```sh

## Deployment
1. Docker
   Build and push the Docker image:
    ```sh
    docker build -t your-dockerhub-username/yolo-api-service:1.0 .
    docker push your-dockerhub-username/yolo-api-service:1.0
    ```sh
2. Deploy to Kubernetes:
    ```sh
    kubectl apply -f deployment.yaml
    ```sh
## Contributing

Contributing
    Contributions are welcome! Please follow these steps:

    Fork the repository.

    Create a feature branch (git checkout -b feature/YourFeature).

    Commit changes (git commit -m 'Add YourFeature').

    Push to the branch (git push origin feature/YourFeature).

    Open a Pull Request.

## License

This project is licensed under the MIT License. 