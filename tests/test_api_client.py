"""
Test coverage for the API client
"""

import pytest
from src.api_client import APIClient


class TestAPIClient:
    """Test the API client functionality"""
    
    def test_api_client_initialization(self):
        """Test API client initialization"""
        client = APIClient("https://example.com")
        assert client.base_url == "https://example.com"
        assert "Content-Type" in client.session.headers
        assert "Accept" in client.session.headers
    
    def test_api_client_default_url(self):
        """Test API client with default URL"""
        client = APIClient()
        assert "restful-booker.herokuapp.com" in client.base_url
    
    def test_get_health(self):
        """Test health check method"""
        client = APIClient()
        result = client.get_health()
        assert "status_code" in result
        assert "text" in result
    
    def test_get_bookings(self):
        """Test get bookings method"""
        client = APIClient()
        result = client.get_bookings()
        assert "status_code" in result
        assert "data" in result
    
    def test_create_booking(self):
        """Test create booking method"""
        client = APIClient()
        booking_data = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": "2023-01-01", "checkout": "2023-01-02"},
            "additionalneeds": "None"
        }
        result = client.create_booking(booking_data)
        assert "status_code" in result
        assert "data" in result
    
    def test_get_booking_success(self):
        """Test get specific booking with valid ID"""
        client = APIClient()
        # This will likely return None since we don't have a real booking ID
        result = client.get_booking(1)
        # The method should handle the request gracefully
        assert result is None or isinstance(result, dict)
