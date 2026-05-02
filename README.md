# SmartHome IoT Test Automation Suite

An end-to-end SDET / QA Automation project that simulates a smart home IoT ecosystem inspired by modern smart appliance platforms.

This project includes a Flask mock backend, SQLite database, smart appliance APIs, a lightweight web dashboard, and an automation framework covering API, UI, database, boundary, negative, smoke, and audit log validation.

---

## Project Overview

The project simulates four smart appliances:

- Smart AC
- Smart TV
- Smart Refrigerator
- Washing Machine

The automation suite validates real-world smart appliance workflows such as login, device listing, appliance control, temperature and volume validation, washing machine cycle updates, database verification, UI validation, and audit log creation.

---

## Real-World Problem

Smart home platforms allow users to control appliances remotely through mobile or web applications. In such systems, companies need to verify that:

- Users can securely log in.
- Only authorized users can access devices.
- Smart appliances respond correctly to commands.
- Invalid inputs are rejected properly.
- API responses match database updates.
- UI reflects the latest device state.
- Every successful action is tracked through audit logs.
- Regression tests run automatically after code changes.

This project solves that testing problem by building a complete automation suite for a simulated smart appliance ecosystem.

---

## Tech Stack

| Area | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| API Testing | Pytest, Requests |
| UI Automation | Playwright, Pytest |
| DB Validation | SQLite queries |
| Reporting | Pytest HTML |
| CI/CD | GitHub Actions |
| Frontend | HTML, CSS, JavaScript |
| Version Control | Git, GitHub |

---

## Features

### Backend Features

- Flask-based mock smart home backend
- SQLite database integration
- User login API
- Token-protected device APIs
- Smart appliance control APIs
- Device-specific business validation
- Audit log creation for successful device actions
- Health check API

### Automation Features

- API automation using Pytest and Requests
- UI automation using Playwright and Pytest
- Database validation using SQLite queries
- Boundary Value Analysis using Pytest parametrization
- Negative testing
- Smoke testing
- Audit log validation
- HTML test report generation
- GitHub Actions CI/CD pipeline

---

## Smart Devices Covered

| Device | Validations Covered |
|---|---|
| Smart AC | Power ON/OFF, temperature range 16°C–30°C, mode validation |
| Smart TV | Power ON/OFF, volume range 0–100, input mode validation |
| Smart Refrigerator | Fridge temperature 1°C–8°C, freezer temperature -24°C to -15°C |
| Washing Machine | Cycle control, water level range 1–5 |

---

## Project Architecture

```text
SmartHome IoT Test Automation Suite
│
├── Backend
│   ├── Flask APIs
│   ├── SQLite Database
│   ├── Authentication
│   ├── Device Control Logic
│   └── Audit Logs
│
├── Frontend
│   ├── Login Page
│   ├── Dashboard Page
│   └── Smart Device Controls
│
└── Automation
    ├── API Tests
    ├── UI Tests
    ├── DB Validation Tests
    ├── Boundary Tests
    ├── Negative Tests
    └── HTML Reports
```

---

## Folder Structure

```text
smarthome-iot-test-suite/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── seed.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── device_routes.py
│   │   └── audit_routes.py
│   └── services/
│       ├── auth_service.py
│       ├── device_service.py
│       └── audit_service.py
│
├── frontend/
│   ├── login.html
│   ├── dashboard.html
│   └── app.js
│
├── automation/
│   ├── api_tests/
│   │   ├── test_auth_api.py
│   │   ├── test_device_api.py
│   │   └── test_boundary_api.py
│   │
│   ├── db_tests/
│   │   └── test_device_db_validation.py
│   │
│   ├── ui_tests/
│   │   ├── pages/
│   │   │   ├── login_page.py
│   │   │   └── dashboard_page.py
│   │   ├── test_login_ui.py
│   │   └── test_dashboard_ui.py
│   │
│   ├── utils/
│   │   ├── api_client.py
│   │   └── db_client.py
│   │
│   └── conftest.py
│
├── reports/
│   └── html/
│       └── full_test_report.html
│
├── .github/
│   └── workflows/
│       └── qa-tests.yml
│
├── README.md
├── TEST_STRATEGY.md
├── BUG_REPORT_SAMPLE.md
├── requirements.txt
├── pytest.ini
└── .gitignore
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Backend and DB health check |
| POST | `/api/auth/login` | User login |
| GET | `/api/devices` | Get all smart devices |
| GET | `/api/devices/<id>` | Get device details |
| PATCH | `/api/devices/<id>/power` | Update device power |
| PATCH | `/api/devices/<id>/temperature` | Update AC/Refrigerator temperature |
| PATCH | `/api/devices/<id>/volume` | Update TV volume |
| PATCH | `/api/devices/<id>/mode` | Update device mode |
| PATCH | `/api/devices/<id>/cycle` | Update washing machine cycle |
| GET | `/api/audit-logs` | View audit logs |

---

## API Flow

```text
Client / Postman / Test Script
        ↓
Flask Route
        ↓
Service Layer
        ↓
SQLite Database
        ↓
JSON Response
```

Example:

```text
PATCH /api/devices/1/temperature
        ↓
Validate token
        ↓
Check device exists
        ↓
Validate AC temperature range: 16°C to 30°C
        ↓
Update SQLite database
        ↓
Create audit log
        ↓
Return JSON response
```

---

## Test Coverage

Total automated tests: **43**

| Test Type | Count |
|---|---:|
| API Tests | 32 |
| Database Validation Tests | 4 |
| UI Automation Tests | 7 |
| Total | 43 |

---

## Testing Types Covered

- API Testing
- UI Automation Testing
- Database Validation Testing
- Boundary Value Analysis
- Negative Testing
- Smoke Testing
- Audit Log Validation
- Token Authentication Testing

---

## Boundary Value Test Coverage

| Module | Valid Range | Invalid Values Tested |
|---|---|---|
| AC Temperature | 16°C to 30°C | 15, 31 |
| TV Volume | 0 to 100 | -1, 101 |
| Refrigerator Temperature | 1°C to 8°C | 0, 9 |
| Washing Machine Water Level | 1 to 5 | 0, 6 |

---

## Sample Test Scenarios

### Authentication

- Login with valid credentials
- Login with invalid password
- Login with missing email/password

### Device API

- Get all devices with valid token
- Reject device API access without token
- Get device detail by ID
- Return 404 for invalid device ID

### Smart AC

- Turn AC ON/OFF
- Update AC temperature with valid value
- Reject AC temperature below 16°C
- Reject AC temperature above 30°C

### Smart TV

- Update TV volume with valid value
- Reject TV volume below 0
- Reject TV volume above 100

### Smart Refrigerator

- Update fridge temperature
- Update freezer temperature
- Reject invalid fridge temperature

### Washing Machine

- Start washing cycle
- Update water level
- Reject invalid water level

### Database Validation

- Verify AC temperature update in database
- Verify TV volume update in database
- Verify washing machine water level update in database
- Verify audit log creation after device action

### UI Automation

- Validate successful login
- Validate invalid login error
- Validate dashboard displays 4 devices
- Update AC temperature from UI
- Validate invalid AC temperature error from UI
- Update TV volume from UI
- Validate logout flow

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/AnshUpadhyay30/smarthome-iot-test-automation-suite.git
cd smarthome-iot-test-automation-suite
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate virtual environment

For macOS/Linux:

```bash
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 5. Seed the database

```bash
cd backend
python seed.py
```

### 6. Start Flask backend

```bash
python app.py
```

Backend will run at:

```text
http://127.0.0.1:5000
```

### 7. Open frontend dashboard

Open this file in browser:

```text
frontend/login.html
```

Demo credentials:

```text
Email: admin@test.com
Password: admin123
```

### 8. Run all tests

Open a new terminal from project root:

```bash
source .venv/bin/activate
pytest -v
```

### 9. Generate HTML test report

```bash
pytest -v --html=reports/html/full_test_report.html --self-contained-html
```

Open report:

```bash
open reports/html/full_test_report.html
```

---

## Run Specific Test Suites

Run smoke tests:

```bash
pytest -m smoke -v
```

Run boundary tests:

```bash
pytest -m boundary -v
```

Run database validation tests:

```bash
pytest -m db -v
```

Run UI automation tests:

```bash
pytest -m ui -v
```

---

## HTML Test Report

The project generates a Pytest HTML report showing:

- Test case names
- Pass/fail status
- Execution time
- Environment details
- Test summary

Report path:

```text
reports/html/full_test_report.html
```

---

## GitHub Actions CI/CD

This project includes a GitHub Actions workflow that runs automated tests on every push and pull request to the main branch.

Workflow file:

```text
.github/workflows/qa-tests.yml
```

CI pipeline steps:

```text
Checkout code
        ↓
Set up Python
        ↓
Install dependencies
        ↓
Install Playwright Chromium
        ↓
Seed database
        ↓
Start Flask backend
        ↓
Run automated tests
        ↓
Generate HTML report
        ↓
Upload report artifact
```

---

## Example Commands

Check backend health:

```bash
curl http://127.0.0.1:5000/health
```

Login API:

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"admin@test.com","password":"admin123"}'
```

Get devices:

```bash
curl http://127.0.0.1:5000/api/devices \
-H "Authorization: Bearer mock-token-1"
```

Update AC temperature:

```bash
curl -X PATCH http://127.0.0.1:5000/api/devices/1/temperature \
-H "Content-Type: application/json" \
-H "Authorization: Bearer mock-token-1" \
-d '{"temperature":22}'
```

Get audit logs:

```bash
curl http://127.0.0.1:5000/api/audit-logs \
-H "Authorization: Bearer mock-token-1"
```

---

## Project Highlights

- Built a complete mock smart home IoT backend using Flask and SQLite.
- Automated 43 test cases across API, UI, database, boundary, negative, smoke, and audit log scenarios.
- Implemented Playwright UI automation using Page Object Model.
- Added database validation to verify API/UI actions at persistence level.
- Applied Boundary Value Analysis for device-specific business rules.
- Generated HTML test reports using pytest-html.
- Configured GitHub Actions CI/CD pipeline for automated test execution.

---

## Resume Summary

Built an end-to-end SmartHome IoT Test Automation Suite with Flask, SQLite, Pytest, Requests, Playwright, database validation, HTML reporting, and GitHub Actions CI/CD. Automated 43 test cases covering API, UI, boundary value, negative, smoke, database, and audit log validation scenarios.

---

## Interview Explanation

I built a SmartHome IoT Test Automation Suite inspired by smart appliance platforms. The system simulates AC, TV, refrigerator, and washing machine workflows using a Flask backend and SQLite database. I created APIs for login, device listing, device control, and audit logs. Then I built an automation framework using Pytest, Requests, Playwright, and SQL validation. The suite covers API testing, UI automation, database validation, boundary value analysis, negative testing, smoke testing, audit logs, HTML reporting, and CI/CD execution using GitHub Actions.

---

## Author

**Ansh Upadhyay**

SDET / QA Automation / Python Automation Project