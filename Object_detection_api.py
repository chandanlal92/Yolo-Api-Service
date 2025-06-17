from flask import Flask, request, jsonify, send_file
import boto3
from ultralytics import YOLO
import cv2
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv("/app/.env")


app = Flask(__name__)

# Load YOLO model
model = YOLO("yolov8n.pt")  # You can use any YOLO model here

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def download_image_from_s3(bucket_name, object_key):
    """Download an image from S3."""
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response["Body"].read()
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    return image


def draw_bounding_boxes(image, results):
    """Draw bounding boxes on the image using YOLO results."""
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = box.conf[0].item()
            cls_id = int(box.cls[0].item())
            label = f"{model.names[cls_id]} {confidence:.2f}"
            color = (0, 255, 0)  # Green color for bounding boxes
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                image,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2,
            )
    return image


@app.route("/process-image", methods=["POST"])
def process_image():
    """
    API endpoint to process an image from S3 and
    return the image with bounding boxes.
    """
    data = request.json
    bucket_name = data.get("bucket_name")
    object_key = data.get("object_key")

    if not bucket_name or not object_key:
        return jsonify(
            {"error": "bucket_name and object_key are required"}
        ), 400

    try:
        # Download image from S3
        image = download_image_from_s3(bucket_name, object_key)

        # Run YOLO model on the image
        results = model(image)

        # Draw bounding boxes on the image
        output_image = draw_bounding_boxes(image, results)

        # Save the output image temporarily
        output_path = "output_image.jpg"
        cv2.imwrite(output_path, output_image)

        # Return the output image as a downloadable file
        return send_file(
            output_path,
            mimetype="image/jpeg",
            as_attachment=True,
            download_name="output_image.jpg",
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "API is working!"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
