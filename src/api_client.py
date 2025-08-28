"""
Simple API client for testing coverage
"""

import requests
from typing import Dict, Any, Optional


class APIClient:
    """Simple API client for the Restful Booker API"""
    
    def __init__(self, base_url: str = "https://restful-booker.herokuapp.com/"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def get_health(self) -> Dict[str, Any]:
        """Get API health status"""
        response = self.session.get(f"{self.base_url}/ping")
        return {"status_code": response.status_code, "text": response.text}
    
    def get_bookings(self) -> Dict[str, Any]:
        """Get all bookings"""
        response = self.session.get(f"{self.base_url}/booking")
        return {"status_code": response.status_code, "data": response.json()}
    
    def create_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new booking"""
        response = self.session.post(f"{self.base_url}/booking", json=booking_data)
        return {"status_code": response.status_code, "data": response.json()}
    
    def get_booking(self, booking_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific booking by ID"""
        try:
            response = self.session.get(f"{self.base_url}/booking/{booking_id}")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None
