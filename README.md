# 🚚 Transport Request Management System

> Modern web application for managing transport requests with file attachments and data validation.

## 📋 **Overview**

This application provides a comprehensive solution for managing transport requests with the following features:

- **Frontend**: Modern React application with Material-UI components
- **Backend**: FastAPI with automatic data validation and Excel export
- **File Handling**: Secure file upload with attachment management
- **Data Export**: Automatic Excel and JSON data persistence
- **Testing**: Comprehensive test coverage (41/41 tests passing)

## 🚀 **Quick Start**

### Prerequisites
- Python 3.12+ with virtual environment
- Node.js 18+ with npm
- Terminal (PowerShell on Windows, bash on Linux/Mac)

### Setup
1. Clone or download the project
2. Navigate to project directory: `cd uit-ro-transport-request`
3. **Install Backend Dependencies:**
   ```bash
   # Install virtualenv (if not already installed)
   py -m pip install --user virtualenv
   
   # Create virtual environment
   py -m venv env
   
   # Activate virtual environment
   # Windows
   .\env\Scripts\activate
   
   # Linux/Mac  
   source env/bin/activate
   
   # Upgrade pip and install Python packages
   py -m pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```
4. **Install Frontend Dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### 1. Start Backend (FastAPI)

**Windows (PowerShell):**
```powershell
# Navigate to project root
cd "path\to\uit-ro-transport-request"

# Start backend server
& ".\env\Scripts\python.exe" "backend\fastapi_app.py"
```

**Linux/Mac (bash):**
```bash
# Navigate to project root
cd path/to/uit-ro-transport-request

# Start backend server
./env/bin/python backend/fastapi_app.py
```

### 2. Start Frontend (Vite)

**Windows (PowerShell):**
```powershell
# Navigate to frontend folder
cd "path\to\uit-ro-transport-request\frontend"

# Start development server
npm run dev
```

**Linux/Mac (bash):**
```bash
# Navigate to frontend folder
cd path/to/uit-ro-transport-request/frontend

# Start development server
npm run dev
```

### 3. Access Application
- **Application UI**: http://localhost:3001/
- **Backend API**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs

## 🏗️ **Architecture**

```
┌─────────────────┐    HTTP/JSON    ┌──────────────────┐
│   Frontend      │ ───────────────▶ │    Backend       │
│   (React/Vite)  │                 │   (FastAPI)      │
│   Port: 3001    │ ◀─────────────── │   Port: 8000     │
└─────────────────┘                 └──────────────────┘
                                             │
                                             ▼
                                    ┌──────────────────┐
                                    │   Data Storage   │
                                    │  • Excel files   │
                                    │  • JSON files    │
                                    │  • Attachments   │
                                    └──────────────────┘
```

## 📁 **Project Structure**

```
uit-ro-transport-request/
├── 📁 env/                               # Python virtual environment
├── 📁 backend/
│   ├── fastapi_app.py                    # Main FastAPI application
│   ├── test_fastapi_app.py               # Backend tests (20 tests)
│   ├── config.yaml                       # Application configuration
│   ├── requirements*.txt                 # Python dependencies
│   ├── data/                             # Data storage (JSON/Excel)
│   └── attachments/                      # Uploaded files
├── 📁 frontend/
│   ├── src/
│   │   ├── App.jsx                       # Main React application
│   │   ├── main.jsx                      # Application entry point
│   │   ├── components/
│   │   │   ├── TransportForm/            # Main form component
│   │   │   ├── FileUpload/               # File upload component
│   │   │   ├── FormField/                # Reusable form fields
│   │   │   └── dropDownCountry.jsx       # Country dropdown
│   │   ├── data/
│   │   │   ├── Countries_List.json       # Country options
│   │   │   └── borderCrossings.json      # Border crossing data
│   │   └── *.test.jsx                    # Frontend tests (21 tests)
│   ├── public/
│   │   ├── favicon.ico                   # Custom favicon
│   │   └── robots.txt                    # SEO configuration
│   └── package.json                      # NPM dependencies
├── 📁 nginx/                             # Docker reverse proxy config
├── 📄 docker-compose.yaml                # Docker orchestration
├── 📄 TESTING.md                         # Testing documentation
├── 📄 DOCKER_README.md                   # Docker setup guide
├── 📄 run_tests.ps1/.sh                  # Test automation scripts
└── 📄 README.md                          # This file
```

## 🔧 **Features**

### Frontend Features
- ✅ **Responsive Design** - Material-UI components
- ✅ **Form Validation** - react-hook-form with Yup validation
- ✅ **File Upload** - Drag & drop with file type validation
- ✅ **Date Picker** - Material-UI date selection
- ✅ **Country Selection** - Dropdown with predefined options
- ✅ **Real-time Validation** - Instant feedback on form fields

### Backend Features
- ✅ **API Documentation** - Automatic OpenAPI/Swagger docs
- ✅ **Data Validation** - Pydantic models with custom validators
- ✅ **File Handling** - Secure upload and storage
- ✅ **Excel Export** - Automatic data export to Excel format
- ✅ **Request Tracking** - Unique ID generation for each request
- ✅ **Error Handling** - Comprehensive error management

### Data Validation
- ✅ **Required Fields** - All mandatory fields validated
- ✅ **Empty String Protection** - Prevents empty string submissions
- ✅ **File Type Validation** - Only allowed file types accepted
- ✅ **Date Validation** - Proper date format enforcement
- ✅ **Country Validation** - Predefined country list

## 🧪 **Testing**

### Test Coverage
- **Backend**: 20/20 tests passing (91% coverage)
- **Frontend**: 21/21 tests passing
- **Total**: 41/41 tests passing (100%)

### Run Tests
```powershell
# Backend tests
cd backend && python -m pytest test_fastapi_app.py -v

# Frontend tests
cd frontend && npm test

# All tests with coverage
.\run_tests.ps1 all
```

## 📊 **Data Export & Logging**

### Generated Files
- **Excel**: `backend/data/transport_requests.xlsx`
- **JSON**: `backend/data/transport_requests.json`
- **Attachments**: `backend/attachments/attachment_[REQUEST_ID].[ext]`

### Logging System

#### 📁 Log Files Location
- **Backend Logs**: `backend/logs/transport_app_YYYYMMDD.jsonl`
- **Frontend Logs**: Browser localStorage (DevTools → Application → Local Storage)

#### 📝 Log Structure

**Backend Log Format (JSON Lines):**
```json
{
  "timestamp": "2025-10-22T10:30:45.123Z",
  "level": "INFO",
  "event": "form_submit",
  "request_id": "REQ-20251022-103045-456",
  "user_ip": "127.0.0.1",
  "form_data": {
    "deliveryNoteNumber": "DN-123456",
    "truckLicensePlates": "ABC-1234",
    "trailerLicensePlates": "XYZ-5678",
    "carrierCountry": "Poland",
    "carrierTaxCode": "1234567890",
    "carrierFullName": "Transport Company Ltd",
    "borderCrossing": "Terespol-Brest",
    "borderCrossingDate": "2025-10-25"
  },
  "attachments": ["file1.pdf", "file2.jpg"],
  "processing_time_ms": 145,
  "status": "SUCCESS"
}
```

**Frontend Log Format (localStorage):**
```json
{
  "timestamp": "2025-10-22T10:30:45.123Z",
  "type": "FORM_SUBMIT",
  "data": {
    "form_values": {...},
    "attachment_count": 2,
    "request_id": "REQ-20251022-103045-456"
  },
  "status": "SUCCESS"
}
```

#### 🔍 Log Events Tracked
- **Form Submissions** - Complete form data and attachments
- **API Requests** - Success/failure status and timing
- **Network Errors** - Connection issues and retries
- **File Uploads** - Attachment names and processing status
- **Validation Errors** - Field-specific validation failures

### Request ID Format
```
REQ-YYYYMMDD-HHMMSS-XXX
Example: REQ-20251021-220148-298
```

## 🐳 **Docker Deployment**

For production deployment with Docker:

```bash
# Build and start all services
docker-compose up --build

# Access application
http://localhost/
```

See [DOCKER_README.md](DOCKER_README.md) for detailed Docker setup.

## 📚 **API Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Application health status |
| `POST` | `/api/submit` | Submit transport request |
| `GET` | `/docs` | API documentation (Swagger) |
| `GET` | `/openapi.json` | OpenAPI schema |

## 🛠️ **Configuration**

### Environment Setup
- **Python Virtual Environment**: `env/`
- **Node Modules**: `frontend/node_modules/`
- **Configuration**: `backend/config.yaml`

### Port Configuration
- **Frontend**: 3001 (Vite dev server)
- **Backend**: 8000 (FastAPI/Uvicorn)
- **Docker**: 80 (Nginx reverse proxy)

## 🔒 **Security**

- ✅ **File Upload Validation** - Type and size restrictions
- ✅ **Data Sanitization** - Input validation and cleaning
- ✅ **CORS Configuration** - Proper cross-origin setup
- ✅ **Request ID Tracking** - Unique request identification

## 📞 **Support**

For questions or issues:
1. Check [TESTING.md](TESTING.md) for testing documentation
2. Review API documentation at http://localhost:8000/docs
3. Check Docker setup in [DOCKER_README.md](DOCKER_README.md)

---
