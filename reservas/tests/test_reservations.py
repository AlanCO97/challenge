from unittest.mock import patch

from schemas.passengers import Passenger
from schemas.reservations import Reservation

# CREATE

def test_create_reservation_success(test_client):
    reservation_data = {
        "name": "Test Reservation",
        "passenger": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
    }

    # Ajusta la ruta al método publish_message según donde esté definido
    with patch("api.reservation.publish_message") as mock_publish:
        response = test_client.post("api/reservations", json=reservation_data)
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["name"] == reservation_data["name"]
        assert response_data["passenger"]["name"] == reservation_data["passenger"]["name"]
        assert response_data["passenger"]["email"] == reservation_data["passenger"]["email"]

        mock_publish.assert_called_once_with("passenger_created", {
            "id": response_data["passenger"]["id"],
            "name": reservation_data["passenger"]["name"],
            "email": reservation_data["passenger"]["email"]
        })


def test_create_reservation_fail(test_client):
    reservation_data = {
        "name": "Test Reservation",
        "passenger": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
    }

    with patch("services.reservation.ReservationService.create", return_value=None):
        response = test_client.post("api/reservations", json=reservation_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "not saved"}

# BULK

def test_bulk_create_success(test_client):
    reservations_data = [
        {"name": "Reservation 1", "passenger": {"name": "John Doe", "email": "john.doe@example.com"}},
        {"name": "Reservation 2", "passenger": {"name": "Jane Smith", "email": "jane.smith@example.com"}}
    ]

    # Mock de la función publish_message
    with patch("api.reservation.publish_message") as mock_publish:
        response = test_client.post("api/reservations/bulk", json=reservations_data)
        assert response.status_code == 200

        db_reservations = response.json()
        assert len(db_reservations) == 2

        assert mock_publish.call_count == len(db_reservations)

def test_bulk_create_failure(test_client):
    invalid_reservations_data = [
        {"name": "Reservation 1", "passenger": {"name": "John Doe"}},
        {"name": "Reservation 2", "passenger": {"name": "Jane Smith", "email": "john.doe@example.com"}}
    ]

    response = test_client.post("api/reservations/bulk", json=invalid_reservations_data)
    
    assert response.status_code == 422

def test_bulk_create_service_error(test_client):
    reservations_data = [
        {"name": "Reservation 1", "passenger": {"name": "John Doe", "email": "john.doe@example.com"}},
        {"name": "Reservation 2", "passenger": {"name": "Jane Smith", "email": "jane.smith@example.com"}}
    ]

    with patch("services.reservation.ReservationService.bulk_create", return_value=None):
        response = test_client.post("api/reservations/bulk", json=reservations_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "not saved"}

# GET ALL
def test_get_reservation_success(test_client):
    fake_reservations = [
        {"id": 1, "name": "Reservation 1", "passenger": {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}},
        {"id": 2, "name": "Reservation 2", "passenger": {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"}}
    ]

    with patch("services.reservation.ReservationService.get_all") as mock_get_all:
        mock_get_all.return_value = fake_reservations

        response = test_client.get("/api/reservations")
        assert response.status_code == 200

        db_reservations = response.json()
        assert len(db_reservations) == len(fake_reservations)
        for i, db_reservation in enumerate(db_reservations):
            assert db_reservation["id"] == fake_reservations[i]["id"]
            assert db_reservation["name"] == fake_reservations[i]["name"]
            assert db_reservation["passenger"]["id"] == fake_reservations[i]["passenger"]["id"]
            assert db_reservation["passenger"]["name"] == fake_reservations[i]["passenger"]["name"]
            assert db_reservation["passenger"]["email"] == fake_reservations[i]["passenger"]["email"]

def test_get_reservation_empty(test_client):
    with patch("services.reservation.ReservationService.get_all") as mock_get_all:
        mock_get_all.return_value = []

        response = test_client.get("/api/reservations")
        assert response.status_code == 200

        assert response.json() == []

# GET BY ID
def test_get_reservation_by_id_success(test_client):
    reservation_id = 1
    fake_reservation = {"id": reservation_id, "name": "Test Reservation", "passenger": {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}}

    with patch("services.reservation.ReservationService.get_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = fake_reservation

        response = test_client.get(f"api/reservations/{reservation_id}")
        assert response.status_code == 200

        db_reservation = response.json()
        assert db_reservation["id"] == reservation_id
        assert db_reservation["name"] == fake_reservation["name"]
        assert db_reservation["passenger"]["id"] == fake_reservation["passenger"]["id"]
        assert db_reservation["passenger"]["name"] == fake_reservation["passenger"]["name"]
        assert db_reservation["passenger"]["email"] == fake_reservation["passenger"]["email"]

def test_get_reservation_by_id_not_found(test_client):
    invalid_reservation_id = 1000

    with patch("services.reservation.ReservationService.get_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = None

        response = test_client.get(f"api/reservations/{invalid_reservation_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "not found"

# UPDATE
def test_update_reservation_success(test_client):

    reservation_id = 1
    reservation_update_data = {
        "name": "Updated Reservation",
        "id": reservation_id, 
        "passenger": {
            "id": 1,
            "name": "Updated Passenger", 
            "email": "updated.passenger@example.com"
            }
    }

    # Mock de la función de servicio de reserva para devolver una reserva actualizada
    with patch("services.reservation.ReservationService.update") as mock_update:
        with patch("api.reservation.publish_message") as mock_publish:

            updated_reservation_data = Reservation(name=reservation_update_data["name"],
                                                created_at=None,
                                                id=reservation_id,
                                                passenger=Passenger(**reservation_update_data["passenger"]))

            

            mock_update.return_value = updated_reservation_data

            response = test_client.put(f"api/reservations/{reservation_id}", json=reservation_update_data)
            assert response.status_code == 200

            updated_reservation = response.json()
            assert updated_reservation["id"] == reservation_id
            assert updated_reservation["name"] == reservation_update_data["name"]
            assert updated_reservation["passenger"]["name"] == reservation_update_data["passenger"]["name"]
            assert updated_reservation["passenger"]["email"] == reservation_update_data["passenger"]["email"]
            mock_publish.assert_called_once_with("passenger_updated", {
            "id": updated_reservation["passenger"]["id"],
            "name": updated_reservation["passenger"]["name"],
            "email": updated_reservation["passenger"]["email"]
        })

def test_update_reservation_not_found(test_client):
    invalid_reservation_id = 1000
    reservation_update_data = {
        "name": "Updated Reservation",
        "id": invalid_reservation_id, 
        "passenger": {
            "id": 1,
            "name": "Updated Passenger", 
            "email": "updated.passenger@example.com"
            }
    }

    with patch("services.reservation.ReservationService.update") as mock_update:
        with patch("api.reservation.publish_message") as mock_publish:
            mock_update.side_effect = ValueError("Reservation not found")

            response = test_client.put(f"api/reservations/{invalid_reservation_id}", json=reservation_update_data)
            assert response.status_code == 404
            assert response.json()["detail"] == "Reservation not found"

            assert mock_publish.called == False

def create_reservation(test_client) -> tuple[int, int]:
    reservation_data = {
        "name": "Test Reservation",
        "passenger": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
    }
    with patch("api.reservation.publish_message", return_value=None):
        response = test_client.post("api/reservations", json=reservation_data)
        response_data = response.json()
        return response_data["id"], response_data["passenger"]["id"]

def get_all_reservations(test_client) -> int:
    response = test_client.get("/api/reservations")
    db_reservations = response.json()
    return len(db_reservations)

# DELETE
# Prueba para la eliminación exitosa con eliminación del pasajero
def test_delete_reservation_success_with_passenger_delete(test_client):
    reservation_id, passenger_id = create_reservation(test_client)
    with patch("api.reservation.publish_message", return_value=None) as mock_publish:
        response = test_client.delete(f"/api/reservations/{reservation_id}")

        assert response.status_code == 200
        assert response.json() == {"message": "Reservation deleted successfully"}
        mock_publish.assert_called_once_with("passenger_deleted", {"id": passenger_id})
        reservation_num = get_all_reservations(test_client)
        assert reservation_num == 0

def test_delete_reservation_not_found(test_client):
    reservation_id = 1
    with patch("services.reservation.ReservationService.delete") as mock_update:
        with patch("api.reservation.publish_message") as mock_publish:
            mock_update.side_effect = ValueError("Reservation not found")

            response = test_client.delete(f"api/reservations/{reservation_id}")
            assert response.status_code == 404
            assert response.json()["detail"] == "Reservation not found"

            assert mock_publish.called == False