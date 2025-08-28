# Python Pytest - Restful Booker API Testing

A streamlined, fast pytest-based test suite for the [Restful Booker API](https://restful-booker.herokuapp.com/apidoc/index.html). This project focuses on simplicity and speed without the overhead of BDD frameworks.

## 🚀 Features

- **Fast & Lightweight**: Pure pytest with no BDD overhead
- **Comprehensive Coverage**: Tests all major API endpoints (CRUD operations)
- **Schema Validation**: JSON schema validation using jsonschema
- **Error Handling**: Tests both positive and negative scenarios
- **Environment Configurable**: Easy to switch between local Docker and production API

## 🏗️ Project Structure

```
python-pytest/
├── tests/
│   ├── test_api.py          # Main API test suite
│   └── conftest.py          # Pytest configuration
├── schemas/
│   ├── booking_schema.json  # JSON schema for booking validation
│   └── booking_id_schema.json
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## 🧪 Test Coverage

The test suite covers the following API endpoints:

- **Health Check** (`/ping`) - API status verification
- **Create Booking** (`POST /booking`) - New booking creation
- **Get All Bookings** (`GET /booking`) - List all booking IDs
- **Get Specific Booking** (`GET /booking/{id}`) - Retrieve booking details
- **Filtered Search** (`GET /booking?firstname=X&lastname=Y`) - Search with parameters
- **Update Booking** (`PUT /booking/{id}`) - Full booking update
- **Partial Update** (`PATCH /booking/{id}`) - Partial field updates
- **Delete Booking** (`DELETE /booking/{id}`) - Remove booking
- **Authentication** (`POST /auth`) - Token generation and validation
- **Error Scenarios** - Invalid IDs, authentication failures

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd python-pytest
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running Tests

### Run all tests
```bash
python -m pytest tests/ -v
```

### Run specific test file
```bash
python -m pytest tests/test_api.py -v
```

### Run with coverage
```bash
# Simple coverage report
python -m pytest tests/ --cov=tests

# Detailed HTML coverage report
python -m pytest tests/ --cov=tests --cov-report=html
```

### Run specific test method
```bash
python -m pytest tests/test_api.py::TestAPI::test_create_booking -v
```

## ⚙️ Configuration

### Environment Variables

- `BASE_URL`: API base URL (defaults to production API)
  ```bash
  export BASE_URL=http://localhost:3001/  # For local Docker
  export BASE_URL=https://restful-booker.herokuapp.com/  # For production
  ```

- `API_USERNAME`: Username for authentication (defaults to "admin")
  ```bash
  export API_USERNAME=your_username
  ```

- `API_PASSWORD`: Password for authentication (defaults to "password123")
  ```bash
  export API_PASSWORD=your_password
  ```

### Local Development with Docker

To test against a local Docker instance:

1. **Pull the Docker image**
   ```bash
   docker pull mwinteringham/restfulbooker:latest
   ```

2. **Run the container**
   ```bash
   docker run -d -p 3001:3001 mwinteringham/restfulbooker:latest
   ```

3. **Set environment variable**
   ```bash
   export BASE_URL=http://localhost:3001/
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/ -v
   ```

## 📊 Test Results Example

```
============================================ test session starts ============================================
platform win32 -- Python 3.13.2, pytest-8.4.1, pluggy-1.6.0
collected 10 items

tests/test_api.py::TestAPI::test_health_check PASSED                    [ 10%]
tests/test_api.py::TestAPI::test_create_booking PASSED                 [ 20%]
tests/test_api.py::TestAPI::test_get_booking PASSED                    [ 30%]
tests/test_api.py::TestAPI::test_get_all_bookings PASSED               [ 40%]
tests/test_api.py::TestAPI::test_get_bookings_with_filters PASSED      [ 50%]
tests/test_api.py::TestAPI::test_update_booking PASSED                 [ 60%]
tests/test_api.py::TestAPI::test_partial_update_booking PASSED         [ 70%]
tests/test_api.py::TestAPI::test_delete_booking PASSED                 [ 80%]
tests/test_api.py::TestAPI::test_invalid_booking_id PASSED             [ 90%]
tests/test_api.py::TestAPI::test_invalid_auth_credentials PASSED       [100%]

============================================= 10 passed in 10.51s =============================================
```

## 🔧 Dependencies

- **pytest**: Testing framework
- **requests**: HTTP library for API calls
- **jsonschema**: JSON schema validation

## 📝 Code Quality

The project uses:
- **Type hints** for better code clarity
- **Pytest fixtures** for test setup and teardown
- **Class-based organization** for better test structure
- **Comprehensive assertions** with descriptive error messages
- **Proper timeout handling** for network requests

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📚 Resources

- [Restful Booker API Documentation](https://restful-booker.herokuapp.com/apidoc/index.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Requests Library](https://requests.readthedocs.io/)
- [JSON Schema](https://json-schema.org/)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
