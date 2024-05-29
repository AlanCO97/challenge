from unittest.mock import patch

def test_bulk_passengers_create_success(test_client):
    passengers_data = [
        {"name": "John Doe", "email": "john.doe@example.com"},
        {"name": "Jane Smith", "email": "jane.smith@example.com"}
    ]

    # Mock de la función publish_message
    with patch("api.passenger.publish_message") as mock_publish:
        response = test_client.post("api/passengers/bulk", json=passengers_data)
        assert response.status_code == 200

        db_passengers = response.json()
        assert len(db_passengers) == 2

        assert mock_publish.call_count == len(db_passengers)

def test_bulk_passengers_create_failure(test_client):
    invalid_passengers_data = [
        {"name": "John Doe"},
        {"name": "Jane Smith", "email": "john.doe@example.com"}
    ]

    response = test_client.post("api/passengers/bulk", json=invalid_passengers_data)
    
    assert response.status_code == 422

def test_bulk_create_service_error(test_client):
    passengers_data = [
        {"name": "John Doe", "email": "john.doe@example.com"},
        {"name": "Jane Smith", "email": "jane.smith@example.com"}
    ]

    with patch("services.passenger.PassengerService.bulk_create", return_value=None):
        response = test_client.post("api/passengers/bulk", json=passengers_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "not saved"}