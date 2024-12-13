import json

import jsonschema
import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com/"
BOOKING_ENDPOINT = "booking/"
AUTH_ENDPOINT = "auth"

# headers for unauthenticated requests (POST, GET)
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# headers for authenticated requests (PUT, PATCH, DELETE)
headers_with_cookie = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cookie": "",
}


@pytest.fixture(scope="session")
def context():
    return {}


@pytest.fixture(scope="session")
def auth_token(context):
    response = requests.post(
        BASE_URL + AUTH_ENDPOINT,
        headers=headers,
        json={"username": "admin", "password": "password123"},
        timeout=5,
    )
    token = response.json()["token"]
    assert token != ""
    assert response.status_code == 200
    context["token"] = token
    headers_with_cookie["Cookie"] = f"token={token}"
    return token


def test_create_booking(context):
    """Creates a booking, stores bookingid and data to context"""
    checkin_date = "2023-01-01"
    checkout_date = "2023-01-02"

    booking_data = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {"checkin": checkin_date, "checkout": checkout_date},
        "additionalneeds": "Breakfast",
    }

    response = requests.post(
        BASE_URL + BOOKING_ENDPOINT, json=booking_data, headers=headers
    )

    assert response.status_code == 200
    response_data = response.json()

    assert "bookingid" in response_data
    booking = response_data["booking"]
    assert booking["firstname"] == booking_data["firstname"]
    assert booking["lastname"] == booking_data["lastname"]
    assert booking["totalprice"] == booking_data["totalprice"]
    assert booking["depositpaid"] == booking_data["depositpaid"]
    assert booking["bookingdates"]["checkin"] == checkin_date
    assert booking["bookingdates"]["checkout"] == checkout_date
    assert booking["additionalneeds"] == booking_data["additionalneeds"]

    # Store the response values for bookingid and booking_data in the context
    context["bookingid"] = response_data["bookingid"]
    context["booking_data"] = booking_data


def test_update_booking(context, auth_token):
    """Updates an existing booking with a new firstname"""
    bookingid = context["bookingid"]
    booking_data = context["booking_data"]

    # Modify the booking data for the update
    updated_booking_data = booking_data.copy()
    updated_booking_data["firstname"] = "Jane"

    response = requests.put(
        f"{BASE_URL}{BOOKING_ENDPOINT}{bookingid}",
        json=updated_booking_data,
        headers=headers_with_cookie,
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["firstname"] == updated_booking_data["firstname"]


def test_get_booking(context):
    """Retrieves the booking and validates booking schema using jsonschema"""
    bookingid = context["bookingid"]

    response = requests.get(f"{BASE_URL}{BOOKING_ENDPOINT}{bookingid}")
    assert response.status_code == 200
    response_data = response.json()

    # Validate the schema of the booking data
    with open("schemas/booking_schema.json", "r") as f:
        schema = json.load(f)
    jsonschema.validate(response_data, schema)
