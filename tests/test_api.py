import json
import os
import time
from typing import Dict, Any

import jsonschema
import pytest
import requests
from requests.exceptions import RequestException, Timeout

# Configuration
BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com/")
BOOKING_ENDPOINT = "booking/"
AUTH_ENDPOINT = "auth"
HEALTH_ENDPOINT = "ping"

# Authentication credentials - configurable via environment variables
API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "password123")


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry functions on failure with exponential backoff"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (RequestException, Timeout) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                        continue
                    else:
                        raise last_exception
            return None
        return wrapper
    return decorator

# Test data
SAMPLE_BOOKING = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 123,
    "depositpaid": True,
    "bookingdates": {"checkin": "2023-01-01", "checkout": "2023-01-02"},
    "additionalneeds": "Breakfast",
}

UPDATED_BOOKING = {
    "firstname": "Jane",
    "lastname": "Doe",
    "totalprice": 150,
    "depositpaid": False,
    "bookingdates": {"checkin": "2023-01-01", "checkout": "2023-01-03"},
    "additionalneeds": "Breakfast and Dinner",
}

PARTIAL_UPDATE = {
    "firstname": "Jane",
    "totalprice": 200,
}


class TestAPI:
    """Test class for Restful Booker API endpoints"""
    
    @pytest.fixture(scope="class")
    def auth_token(self) -> str:
        """Get authentication token for protected endpoints"""
        response = requests.post(
            f"{BASE_URL}{AUTH_ENDPOINT}",
            headers={"Content-Type": "application/json"},
            json={"username": API_USERNAME, "password": API_PASSWORD},
            timeout=10,
        )
        assert response.status_code == 200, f"Auth failed: {response.text}"
        token = response.json()["token"]
        assert token, "Token is empty"
        return token
    
    @pytest.fixture(scope="class")
    def auth_headers(self, auth_token: str) -> Dict[str, str]:
        """Get headers with authentication token"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={auth_token}",
        }
    
    @pytest.fixture(scope="class")
    def base_headers(self) -> Dict[str, str]:
        """Get base headers for unauthenticated requests"""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    @pytest.fixture(scope="class")
    def created_booking_id(self, base_headers: Dict[str, str]) -> int:
        """Create a test booking and return its ID"""
        response = requests.post(
            f"{BASE_URL}{BOOKING_ENDPOINT}",
            json=SAMPLE_BOOKING,
            headers=base_headers,
            timeout=10,
        )
        assert response.status_code == 200, f"Booking creation failed: {response.text}"
        booking_data = response.json()
        assert "bookingid" in booking_data, "No booking ID in response"
        return booking_data["bookingid"]
    
    def test_health_check(self, base_headers: Dict[str, str]):
        """Test API health endpoint"""
        response = requests.get(
            f"{BASE_URL}{HEALTH_ENDPOINT}",
            headers=base_headers,
            timeout=10,
        )
        assert response.status_code == 201, f"Health check failed: {response.text}"
    
    def test_create_booking(self, base_headers: Dict[str, str]):
        """Test creating a new booking"""
        response = requests.post(
            f"{BASE_URL}{BOOKING_ENDPOINT}",
            json=SAMPLE_BOOKING,
            headers=base_headers,
            timeout=10,
        )
        
        assert response.status_code == 200, f"Booking creation failed: {response.text}"
        response_data = response.json()
        
        # Validate response structure
        assert "bookingid" in response_data, "No booking ID in response"
        assert "booking" in response_data, "No booking data in response"
        
        # Validate booking data
        booking = response_data["booking"]
        assert booking["firstname"] == SAMPLE_BOOKING["firstname"]
        assert booking["lastname"] == SAMPLE_BOOKING["lastname"]
        assert booking["totalprice"] == SAMPLE_BOOKING["totalprice"]
        assert booking["depositpaid"] == SAMPLE_BOOKING["depositpaid"]
        assert booking["bookingdates"]["checkin"] == SAMPLE_BOOKING["bookingdates"]["checkin"]
        assert booking["bookingdates"]["checkout"] == SAMPLE_BOOKING["bookingdates"]["checkout"]
        assert booking["additionalneeds"] == SAMPLE_BOOKING["additionalneeds"]
    
    def test_get_booking(self, base_headers: Dict[str, str], created_booking_id: int):
        """Test retrieving a specific booking"""
        response = requests.get(
            f"{BASE_URL}{BOOKING_ENDPOINT}{created_booking_id}",
            headers=base_headers,
            timeout=10,
        )
        
        assert response.status_code == 200, f"Get booking failed: {response.text}"
        response_data = response.json()
        
        # Validate schema with better error handling
        try:
            with open("schemas/booking_schema.json", "r") as f:
                schema = json.load(f)
            jsonschema.validate(response_data, schema)
        except FileNotFoundError:
            pytest.fail("Schema file not found: schemas/booking_schema.json")
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in schema file: {e}")
        except jsonschema.ValidationError as e:
            pytest.fail(f"Schema validation failed: {e}")
        
        # Validate data matches what we created
        assert response_data["firstname"] == SAMPLE_BOOKING["firstname"]
        assert response_data["lastname"] == SAMPLE_BOOKING["lastname"]
    
    def test_get_all_bookings(self, base_headers: Dict[str, str]):
        """Test retrieving all booking IDs"""
        response = requests.get(
            f"{BASE_URL}{BOOKING_ENDPOINT}",
            headers=base_headers,
            timeout=10,
        )
        
        assert response.status_code == 200, f"Get all bookings failed: {response.text}"
        bookings = response.json()
        
        # Validate response is a list
        assert isinstance(bookings, list), "Response should be a list"
        
        # Validate each booking has an ID
        for booking in bookings:
            assert "bookingid" in booking, "Each booking should have an ID"
    
    def test_get_bookings_with_filters(self, base_headers: Dict[str, str]):
        """Test retrieving bookings with query parameters"""
        params = {
            "firstname": "John",
            "lastname": "Doe",
        }
        
        response = requests.get(
            f"{BASE_URL}{BOOKING_ENDPOINT}",
            params=params,
            headers=base_headers,
            timeout=10,
        )
        
        assert response.status_code == 200, f"Filtered search failed: {response.text}"
        bookings = response.json()
        
        # Should return at least one booking
        assert len(bookings) > 0, "Should find at least one booking with filters"
    
    def test_update_booking(self, auth_headers: Dict[str, str], created_booking_id: int):
        """Test updating an existing booking (full update)"""
        response = requests.put(
            f"{BASE_URL}{BOOKING_ENDPOINT}{created_booking_id}",
            json=UPDATED_BOOKING,
            headers=auth_headers,
            timeout=10,
        )
        
        assert response.status_code == 200, f"Update booking failed: {response.text}"
        response_data = response.json()
        
        # Validate updated data
        assert response_data["firstname"] == UPDATED_BOOKING["firstname"]
        assert response_data["totalprice"] == UPDATED_BOOKING["totalprice"]
        assert response_data["depositpaid"] == UPDATED_BOOKING["depositpaid"]
    
    def test_partial_update_booking(self, auth_headers: Dict[str, str], created_booking_id: int):
        """Test partially updating a booking (PATCH)"""
        response = requests.patch(
            f"{BASE_URL}{BOOKING_ENDPOINT}{created_booking_id}",
            json=PARTIAL_UPDATE,
            headers=auth_headers,
            timeout=10,
        )
        
        assert response.status_code == 200, f"Partial update failed: {response.text}"
        response_data = response.json()
        
        # Validate only specified fields were updated
        assert response_data["firstname"] == PARTIAL_UPDATE["firstname"]
        assert response_data["totalprice"] == PARTIAL_UPDATE["totalprice"]
        
        # Other fields should remain unchanged
        assert response_data["lastname"] == UPDATED_BOOKING["lastname"]
        assert response_data["depositpaid"] == UPDATED_BOOKING["depositpaid"]
    
    def test_delete_booking(self, auth_headers: Dict[str, str], created_booking_id: int):
        """Test deleting a booking"""
        response = requests.delete(
            f"{BASE_URL}{BOOKING_ENDPOINT}{created_booking_id}",
            headers=auth_headers,
            timeout=10,
        )
        
        assert response.status_code == 201, f"Delete booking failed: {response.text}"
        
        # Verify booking is actually deleted
        get_response = requests.get(
            f"{BASE_URL}{BOOKING_ENDPOINT}{created_booking_id}",
            headers={"Accept": "application/json"},
            timeout=10,
        )
        assert get_response.status_code == 404, "Booking should be deleted"
    
    def test_invalid_booking_id(self, base_headers: Dict[str, str]):
        """Test getting a non-existent booking ID"""
        response = requests.get(
            f"{BASE_URL}{BOOKING_ENDPOINT}99999",
            headers=base_headers,
            timeout=10,
        )
        
        assert response.status_code == 404, "Should return 404 for invalid booking ID"
    
    def test_invalid_auth_credentials(self):
        """Test authentication with invalid credentials"""
        response = requests.post(
            f"{BASE_URL}{AUTH_ENDPOINT}",
            headers={"Content-Type": "application/json"},
            json={"username": "invalid", "password": "wrong"},
            timeout=10,
        )
        
        assert response.status_code == 200, "Should return 200 even with invalid credentials"
        # Note: This API returns 200 but with an empty token for invalid credentials
        token = response.json().get("token", "")
        assert not token, "Should not return a valid token for invalid credentials"
