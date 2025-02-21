import pytest
def test_process_image_endpoint(client):
    """Test the /process-image endpoint."""
    # Mock the request payload
    payload = {
        "bucket_name": "test-yolo-chandan",
        "object_key": "Test_Dog.jpeg"
    }

    # Send a POST request to the endpoint
    response = client.post("/process-image", json=payload)

    # Check the response status code
    assert response.status_code == 200

    # Check the response content type
    assert response.content_type == "image/jpeg"

def test_process_image_endpoint_missing_parameters(client):
    """Test the /process-image endpoint with missing parameters."""
    # Send a POST request without required parameters
    response = client.post("/process-image", json={})

    # Check the response status code and error message
    assert response.status_code == 400
    assert "bucket_name and object_key are required" in response.json["error"]