# Use Ubuntu 20.04 as the base image
FROM python:3.9

# Set the working directory in the container

WORKDIR /app


# Copy the requirements file into the container
COPY requirements.txt .
COPY .env /app/.env

# Install Python and system dependencies
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 && rm -rf /var/lib/apt/lists/*



RUN pip install --no-cache-dir -r requirements.txt


# Copy the application code into the container
COPY . .


# Expose the port the app runs on
EXPOSE 5000

# Set environment variables for AWS credentials
# ENV LD_LIBRARY_PATH=/usr/local/lib
# ENV AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY
# ENV AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID

# Command to run the application
CMD ["python", "Object_detection_api.py"]