# 🧪 Testing Documentation

## 📊 **Current Test Status**
- **Backend**: ✅ 20/20 tests passing (100%)
- **Frontend**: ✅ 21/21 tests passing (100%)
- **Total**: ✅ 41/41 tests passing (100%)

## 🚀 **Development Server Setup**

### Prerequisites
- Python 3.12+ with virtual environment
- Node.js 18+ with npm
- Project dependencies installed (see Setup below)

### Setup (First Time)
```bash
# Navigate to project directory
cd path/to/uit-ro-transport-request

# Install Python virtualenv and create environment
py -m pip install --user virtualenv
py -m venv env

# Activate environment (Windows)
.\env\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Start Backend (FastAPI)
```powershell
# Windows PowerShell - from project root
cd "path\to\uit-ro-transport-request"
& ".\env\Scripts\python.exe" "backend\fastapi_app.py"

# Or from backend folder
cd "path\to\uit-ro-transport-request\backend"
& "..\env\Scripts\python.exe" fastapi_app.py
```

### Start Frontend (Vite)
```powershell
# Windows PowerShell
cd "path\to\uit-ro-transport-request\frontend"
npm run dev
```

### Access Application
- **Frontend**: http://localhost:3001/
- **Backend API**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs

## 🧪 **Testing Commands**

### Run All Tests
```bash
# Backend tests
cd backend && python -m pytest test_fastapi_app.py -v

# Frontend tests
cd frontend && npm test

# All tests (Linux/Mac)
./run_tests.sh all

# All tests (Windows)
.\run_tests.ps1 all
```

### With Coverage
```bash
# Backend with coverage
cd backend && python -m pytest test_fastapi_app.py --cov=. --cov-report=html

# Frontend with coverage
cd frontend && npm test -- --coverage
```

## 🏗️ **Test Infrastructure**

### Backend (Python/FastAPI)
- **Framework**: pytest + httpx
- **Location**: `backend/test_fastapi_app.py`
- **Coverage**: 91% code coverage
- **Features**:
  - API endpoint testing
  - Data validation tests
  - File upload/handling
  - Error handling
  - Request ID generation

### Frontend (React/Jest)
- **Framework**: Jest + React Testing Library
- **Locations**:
  - `frontend/src/components/FileUpload/FileUpload.test.jsx`
  - `frontend/src/components/TransportForm/TransportForm.test.jsx`
- **Features**:
  - Component rendering tests
  - User interaction simulation
  - Form validation testing
  - File upload UI testing

### Integration Tests
- **Location**: `test_integration.py`
- **Purpose**: End-to-end workflow testing
- **Requirements**: Running backend + frontend

## 📋 **Test Categories**

### Backend Tests (20 tests)
1. **Health Endpoints** - API availability
2. **Transport Request Model** - Data validation
3. **Submit Endpoint** - Form submission handling
4. **File Handling** - Upload and storage
5. **Data Persistence** - JSON/Excel saving
6. **Request ID Generation** - Unique ID creation
7. **Error Handling** - Exception management

### Frontend Tests (21 tests)
1. **FileUpload Component** (13 tests)
   - Rendering and UI
   - File type validation
   - Size limit display
   - Input interaction
2. **TransportForm Component** (8 tests)
   - Form rendering
   - Field validation
   - Submit behavior
   - LocalizationProvider integration

## 🔧 **Configuration Files**

### Backend
- `pytest.ini` - pytest configuration
- `backend/test_fastapi_app.py` - test suite

### Frontend
- `frontend/package.json` - Jest configuration
- `frontend/src/setupTests.js` - test environment setup
- `frontend/.eslintrc.json` - ESLint with Jest support

## 📈 **Quality Metrics**

### Coverage Targets
- Backend: ✅ 91% (target: 80%+)
- Frontend: ✅ Good component coverage
- Critical paths: ✅ 100% covered

### Performance
- Backend tests: ~1.3s execution time
- Frontend tests: ~8-10s execution time
- Total: Under 15 seconds

## 🛠️ **Troubleshooting**

### Common Issues
1. **"jest is not defined"** → Fixed with `/* eslint-env jest */`
2. **act() warnings** → Normal for MUI components
3. **Backend ValidationError** → Fixed with proper Pydantic validators

### Test Failures
- Check if backend is running for integration tests
- Verify npm dependencies are installed
- Ensure Python virtual environment is activated

## ✅ **Ready for Production**
- All tests passing
- ESLint errors resolved
- Comprehensive coverage
- CI/CD ready configuration