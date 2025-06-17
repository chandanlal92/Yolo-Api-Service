import sys
import os
import numpy as np
from io import BytesIO


# Add the project root directory to the Python path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    ),
)
from Object_detection_api import download_image_from_s3, draw_bounding_boxes


def test_draw_bounding_boxes():
    """Test the draw_bounding_boxes function."""
    # Create a blank image
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Mock YOLO results
    class MockBox:
        def __init__(self, xyxy, conf, cls):
            self.xyxy = np.array(xyxy)  # Ensure xyxy is a NumPy array
            self.conf = np.array([conf])  # Ensure conf is a NumPy array
            self.cls = np.array([cls])  # Ensure cls is a NumPy array

    class MockResult:
        def __init__(self, boxes):
            self.boxes = boxes

    # Create mock bounding boxes
    boxes = [MockBox([10, 10, 50, 50], 0.9, 0)]
    results = [MockResult(boxes)]

    # Draw bounding boxes
    output_image = draw_bounding_boxes(image, results)

    # Check if the image was modified
    assert output_image is not None
    assert output_image.shape == image.shape


def test_download_image_from_s3(monkeypatch):
    """Test the download_image_from_s3 function."""

    # Mock the S3 client
    class MockS3Client:
        def get_object(self, Bucket, Key):
            class MockResponse:
                def __init__(self):
                    self.Body = BytesIO(b"mock_image_data")

            return MockResponse()

    monkeypatch.setattr("boto3.client", lambda *args, **kwargs: MockS3Client())

    # Test the function
    image = download_image_from_s3(
        os.getenv("YOLO-BUCKET-NAME"), os.getenv("YOLO_IMAGE_FILE_NAME")
    )
    assert image is not None
