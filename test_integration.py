"""
Integration tests for the complete Transport Request system

These tests verify the entire flow from frontend to backend including:
- Form submission with file uploads
- Data persistence
- Docker containerization
- API endpoints integration

Run with:
    pytest test_integration.py -v
"""

import pytest
import requests
import json
import time
import subprocess
import os
from pathlib import Path


class TestSystemIntegration:
    """Test the complete system integration"""
    
    @pytest.fixture(scope="class")
    def backend_url(self):
        """Backend URL for testing"""
        return "http://localhost:8000"
    
    @pytest.fixture(scope="class")
    def frontend_url(self):
        """Frontend URL for testing"""
        return "http://localhost:3000"
    
    def test_backend_health_check(self, backend_url):
        """Test that backend is running and healthy"""
        try:
            response = requests.get(f"{backend_url}/", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["message"] == "Transport backend running"
        except requests.ConnectionError:
            pytest.skip("Backend not running - start with: python backend/fastapi_app.py")
    
    def test_api_health_endpoint(self, backend_url):
        """Test API health endpoint"""
        try:
            response = requests.get(f"{backend_url}/api/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
        except requests.ConnectionError:
            pytest.skip("Backend not running")
    
    def test_submit_form_data_only(self, backend_url):
        """Test submitting form data without file attachment"""
        form_data = {
            "deliveryNoteNumber": "INT-TEST-001",
            "truckLicensePlates": "IT123AB",
            "trailerLicensePlates": "IT456CD",
            "carrierCountry": "Italy",
            "carrierTaxCode": "IT12345678901",
            "carrierFullName": "Integration Test Transport",
            "borderCrossing": "Nadlac",
            "borderCrossingDate": "2025-10-30"
        }
        
        try:
            response = requests.post(
                f"{backend_url}/api/submit",
                data={"data": json.dumps(form_data)},
                timeout=10
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "request_id" in data
            assert data["request_id"].startswith("REQ-")
            assert data["attachment_saved"] is False
            assert data["excel_saved"] is True
            
        except requests.ConnectionError:
            pytest.skip("Backend not running")
    
    def test_submit_form_with_file(self, backend_url):
        """Test submitting form data with file attachment"""
        form_data = {
            "deliveryNoteNumber": "INT-TEST-002",
            "truckLicensePlates": "DE789XY",
            "trailerLicensePlates": "DE012ZW",
            "carrierCountry": "Germany",
            "carrierTaxCode": "DE123456789",
            "carrierFullName": "German Test Transport GmbH",
            "borderCrossing": "Nadlac",
            "borderCrossingDate": "2025-10-31"
        }
        
        # Create a test file
        test_file_content = b"Integration test PDF content - this is a test document for file upload."
        
        try:
            response = requests.post(
                f"{backend_url}/api/submit",
                data={"data": json.dumps(form_data)},
                files={"attachment": ("integration_test.pdf", test_file_content, "application/pdf")},
                timeout=10
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["attachment_saved"] is True
            assert data["excel_saved"] is True
            
            # Verify file was saved
            request_id = data["request_id"]
            expected_file_path = Path("backend/attachments") / f"{request_id}_integration_test.pdf"
            assert expected_file_path.exists()
            
            # Verify file content
            with open(expected_file_path, 'rb') as f:
                saved_content = f.read()
                assert saved_content == test_file_content
                
        except requests.ConnectionError:
            pytest.skip("Backend not running")
    
    def test_invalid_form_data(self, backend_url):
        """Test handling of invalid form data"""
        invalid_data = {
            "deliveryNoteNumber": "",  # Empty required field
            "invalidField": "should not be accepted"
        }
        
        try:
            response = requests.post(
                f"{backend_url}/api/submit",
                data={"data": json.dumps(invalid_data)},
                timeout=5
            )
            
            assert response.status_code == 400
            data = response.json()
            assert "Invalid data" in data["detail"]
            
        except requests.ConnectionError:
            pytest.skip("Backend not running")
    
    def test_malformed_json(self, backend_url):
        """Test handling of malformed JSON"""
        try:
            response = requests.post(
                f"{backend_url}/api/submit",
                data={"data": "invalid json"},
                timeout=5
            )
            
            assert response.status_code == 400
            data = response.json()
            assert "Invalid JSON" in data["detail"]
            
        except requests.ConnectionError:
            pytest.skip("Backend not running")
    
    def test_data_persistence(self, backend_url):
        """Test that submitted data is properly saved"""
        form_data = {
            "deliveryNoteNumber": "PERSIST-TEST-001",
            "truckLicensePlates": "PS123TE",
            "trailerLicensePlates": "PS456ST",
            "carrierCountry": "Poland",
            "carrierTaxCode": "PL9876543210",
            "carrierFullName": "Persistence Test Transport",
            "borderCrossing": "Nadlac",
            "borderCrossingDate": "2025-11-01"
        }
        
        try:
            response = requests.post(
                f"{backend_url}/api/submit",
                data={"data": json.dumps(form_data)},
                timeout=10
            )
            
            assert response.status_code == 200
            data = response.json()
            request_id = data["request_id"]
            
            # Check if data file exists and contains our data
            data_file_path = Path("backend/data/transport_requests.json")
            assert data_file_path.exists()
            
            with open(data_file_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                
            # Find our submitted request
            our_request = None
            for request in saved_data:
                if request.get("Request_ID") == request_id:
                    our_request = request
                    break
            
            assert our_request is not None
            assert our_request["Delivery_Note_Number"] == "PERSIST-TEST-001"
            assert our_request["Carrier_Full_Name"] == "Persistence Test Transport"
            
        except requests.ConnectionError:
            pytest.skip("Backend not running")


class TestDockerIntegration:
    """Test Docker containerization"""
    
    def test_docker_compose_config_valid(self):
        """Test that docker-compose.yaml is valid"""
        docker_compose_path = Path("docker-compose.yaml")
        assert docker_compose_path.exists()
        
        # Try to validate docker-compose file
        try:
            result = subprocess.run(
                ["docker-compose", "config"],
                cwd=".",
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0, f"Docker compose config invalid: {result.stderr}"
        except subprocess.TimeoutExpired:
            pytest.skip("Docker compose validation timed out")
        except FileNotFoundError:
            pytest.skip("Docker compose not installed")
    
    def test_backend_dockerfile_exists(self):
        """Test backend Dockerfile exists and is valid"""
        dockerfile_path = Path("backend/Dockerfile")
        assert dockerfile_path.exists()
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
            assert "FROM python:" in content
            assert "COPY requirements.txt" in content
            assert "pip install" in content
            assert "CMD" in content or "ENTRYPOINT" in content
    
    def test_frontend_dockerfile_exists(self):
        """Test frontend Dockerfile exists and is valid"""
        dockerfile_path = Path("frontend/Dockerfile")
        assert dockerfile_path.exists()
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
            assert "FROM node:" in content
            assert "package.json" in content
            assert "npm" in content


class TestConfigurationIntegration:
    """Test configuration system integration"""
    
    def test_config_file_exists(self):
        """Test that config.yaml exists and is valid"""
        config_path = Path("backend/config.yaml")
        assert config_path.exists()
        
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        assert "default" in config
        assert "transport" in config["default"]
        assert "local_attachments_folder" in config["default"]["transport"]
        assert "local_excel_file" in config["default"]["transport"]
    
    def test_attachment_directory_creation(self):
        """Test that attachment directory is created when needed"""
        import yaml
        
        config_path = Path("backend/config.yaml")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        attachments_folder = config["default"]["transport"]["local_attachments_folder"]
        attachments_path = Path("backend") / attachments_folder
        
        # Directory should exist or be creatable
        if not attachments_path.exists():
            attachments_path.mkdir(parents=True, exist_ok=True)
        
        assert attachments_path.exists()
        assert attachments_path.is_dir()


class TestPerformanceIntegration:
    """Test system performance characteristics"""
    
    def test_api_response_time(self, backend_url="http://localhost:8000"):
        """Test API response time is reasonable"""
        form_data = {
            "deliveryNoteNumber": "PERF-TEST-001",
            "truckLicensePlates": "PF123RM",
            "trailerLicensePlates": "PF456NC",
            "carrierCountry": "France",
            "carrierTaxCode": "FR12345678901",
            "carrierFullName": "Performance Test Transport",
            "borderCrossing": "Nadlac",
            "borderCrossingDate": "2025-11-05"
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{backend_url}/api/submit",
                data={"data": json.dumps(form_data)},
                timeout=10
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response.status_code == 200
            assert response_time < 5.0  # Should respond within 5 seconds
            
        except requests.ConnectionError:
            pytest.skip("Backend not running")
    
    def test_concurrent_requests(self, backend_url="http://localhost:8000"):
        """Test handling of multiple concurrent requests"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request(request_id):
            form_data = {
                "deliveryNoteNumber": f"CONCURRENT-{request_id}",
                "truckLicensePlates": f"C{request_id:02d}123",
                "trailerLicensePlates": f"C{request_id:02d}456",
                "carrierCountry": "Spain",
                "carrierTaxCode": "ES12345678901",
                "carrierFullName": f"Concurrent Test {request_id}",
                "borderCrossing": "Nadlac",
                "borderCrossingDate": "2025-11-10"
            }
            
            try:
                response = requests.post(
                    f"{backend_url}/api/submit",
                    data={"data": json.dumps(form_data)},
                    timeout=10
                )
                results.put((request_id, response.status_code, response.json()))
            except Exception as e:
                results.put((request_id, None, str(e)))
        
        try:
            # Create 5 concurrent requests
            threads = []
            for i in range(5):
                thread = threading.Thread(target=make_request, args=(i,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join(timeout=15)
            
            # Check results
            successful_requests = 0
            while not results.empty():
                request_id, status_code, response_data = results.get()
                if status_code == 200:
                    successful_requests += 1
                    assert response_data.get("success") is True
            
            assert successful_requests >= 3  # At least 3 out of 5 should succeed
            
        except requests.ConnectionError:
            pytest.skip("Backend not running")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])