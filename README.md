# Python Pytest - API & UI Testing Suite

[![Tests](https://github.com/yourusername/python-pytest/workflows/CI/badge.svg)](https://github.com/yourusername/python-pytest/actions)
[![Coverage](https://img.shields.io/badge/coverage-88%25-brightgreen)](https://github.com/yourusername/python-pytest)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-8.4.1+-green.svg)](https://docs.pytest.org/)
[![Selenium](https://img.shields.io/badge/selenium-4.35.0+-orange.svg)](https://selenium-python.readthedocs.io/)

A comprehensive, fast pytest-based test suite covering both API testing for the [Restful Booker API](https://restful-booker.herokuapp.com/apidoc/index.html) and UI testing for the [Sauce Demo](https://www.saucedemo.com/) application. This project focuses on simplicity and speed without the overhead of BDD frameworks.

## 🚀 Features

### API Testing
- **Fast & Lightweight**: Pure pytest with no BDD overhead
- **Comprehensive Coverage**: Tests all major API endpoints (CRUD operations)
- **Schema Validation**: JSON schema validation using jsonschema
- **Error Handling**: Tests both positive and negative scenarios
- **Environment Configurable**: Easy to switch between local Docker and production API

### UI Testing
- **Modern Selenium**: Selenium 4.35+ with webdriver-manager for automatic driver management
- **Test Isolation**: Function-scoped fixtures with proper browser cleanup
- **Stable Selectors**: Data-test attributes for reliable element identification
- **Cross-browser Ready**: Chrome with headless mode for CI/CD
- **Performance Monitoring**: Built-in performance testing capabilities

## 📊 Project Status

| Badge | Description | Status |
|-------|-------------|---------|
| ![Tests](https://github.com/yourusername/python-pytest/workflows/CI/badge.svg) | GitHub Actions CI/CD | ![GitHub Actions](https://img.shields.io/badge/status-passing-brightgreen) |
| ![Coverage](https://img.shields.io/badge/coverage-88%25-brightgreen) | Test Coverage | ![Coverage](https://img.shields.io/badge/status-88%25-brightgreen) |
| ![Python](https://img.shields.io/badge/python-3.8+-blue.svg) | Python Version | ![Python](https://img.shields.io/badge/status-3.8+-blue) |
| ![Pytest](https://img.shields.io/badge/pytest-8.4.1+-green.svg) | Testing Framework | ![Pytest](https://img.shields.io/badge/status-8.4.1+-green) |

## 🏗️ Project Structure

```
python-pytest/
├── src/
│   ├── __init__.py          # Package initialization
│   └── api_client.py        # API client library
├── tests/
│   ├── test_api.py          # Main API test suite
│   ├── test_api_client.py   # API client tests
│   ├── test_ui.py           # UI/Selenium test suite
│   └── conftest.py          # Pytest configuration
├── schemas/
│   ├── booking_schema.json  # JSON schema for booking validation
│   └── booking_id_schema.json
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## 🧪 Test Coverage

### API Testing Coverage
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

### UI Testing Coverage
The UI test suite covers the following scenarios on [Sauce Demo](https://www.saucedemo.com/):

- **Valid Login** - Successful authentication with standard credentials
- **Invalid Login** - Error handling for incorrect credentials
- **Locked User** - Handling of locked-out user accounts
- **User Logout** - Complete logout flow and session cleanup
- **Performance Testing** - Page load performance monitoring
- **Inventory Display** - Product page functionality and element verification

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

### Run all tests (API + UI)
```bash
python -m pytest tests/ -v
```

### Run specific test suites
```bash
# API tests only
python -m pytest tests/test_api.py -v

# UI tests only  
python -m pytest tests/test_ui.py -v

# API client tests only
python -m pytest tests/test_api_client.py -v
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

## 🔄 Updating Coverage Badge

The coverage badge shows the current test coverage percentage. To update it:

1. **Run coverage locally**:
   ```bash
   python -m pytest tests/ --cov=tests
   ```

2. **Update the badge URL** in README.md:
   ```markdown
   [![Coverage](https://img.shields.io/badge/coverage-XX%25-brightgreen)](https://github.com/yourusername/python-pytest)
   ```

3. **For automated updates**, the GitHub Actions workflow will generate coverage reports and you can manually update the badge based on the results.

## 📊 Test Results Example

```
============================================ test session starts ============================================
platform win32 -- Python 3.13.2, pytest-8.4.1, pluggy-1.6.0
collected 22 items

tests/test_api.py::TestAPI::test_health_check PASSED                   [  4%]
tests/test_api.py::TestAPI::test_create_booking PASSED                 [  9%]
tests/test_api.py::TestAPI::test_get_booking PASSED                    [ 13%]
tests/test_api.py::TestAPI::test_get_all_bookings PASSED               [ 18%]
tests/test_api.py::TestAPI::test_get_bookings_with_filters PASSED      [ 22%]
tests/test_api.py::TestAPI::test_update_booking PASSED                 [ 27%]
tests/test_api.py::TestAPI::test_partial_update_booking PASSED         [ 31%]
tests/test_api.py::TestAPI::test_delete_booking PASSED                 [ 36%]
tests/test_api.py::TestAPI::test_invalid_booking_id PASSED             [ 40%]
tests/test_api.py::TestAPI::test_invalid_auth_credentials PASSED       [ 45%]
tests/test_api_client.py::TestAPIClient::test_api_client_initialization PASSED [ 50%]
tests/test_api_client.py::TestAPIClient::test_api_client_default_url PASSED [ 54%]
tests/test_api_client.py::TestAPIClient::test_get_health PASSED        [ 59%]
tests/test_api_client.py::TestAPIClient::test_get_bookings PASSED      [ 63%]
tests/test_api_client.py::TestAPIClient::test_create_booking PASSED    [ 68%]
tests/test_api_client.py::TestAPIClient::test_get_booking_success PASSED [ 72%]
tests/test_ui.py::TestLogin::test_valid_login PASSED                   [ 77%]
tests/test_ui.py::TestLogin::test_invalid_login PASSED                 [ 81%]
tests/test_ui.py::TestLogin::test_locked_out_user PASSED               [ 86%]
tests/test_ui.py::TestLogin::test_logout PASSED                        [ 90%]
tests/test_ui.py::TestLogin::test_page_load_performance XFAIL           [ 95%]
tests/test_ui.py::TestInventory::test_inventory_items_displayed PASSED [100%]

============================================ 21 passed, 1 xfailed in 57.95s ============================================
```

## 🔧 Dependencies

### Core Testing
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting

### API Testing
- **requests**: HTTP library for API calls
- **jsonschema**: JSON schema validation

### UI Testing
- **selenium**: Web browser automation
- **webdriver-manager**: Automatic browser driver management

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
