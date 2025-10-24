from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import random
import os
import json
import logging
import yaml
from pathlib import Path
import time

# Import our custom logger
from logger_config import get_logger

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get structured logger
app_logger = get_logger()

# Load configuration
def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

config = load_config()
transport_config = config.get('default', {}).get('transport', {})

app = FastAPI(title="Transport Request API", version="1.0.0")

# CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransportRequest(BaseModel):
    deliveryNoteNumber: str
    truckLicensePlates: str
    trailerLicensePlates: str
    carrierCountry: str
    carrierTaxCode: str
    carrierFullName: str
    borderCrossing: str
    borderCrossingDate: str  # ISO date string

    @field_validator('deliveryNoteNumber', 'truckLicensePlates', 'carrierCountry', 'carrierTaxCode', 'carrierFullName', 'borderCrossing')
    @classmethod
    def validate_non_empty_string(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v.strip()

@app.post("/api/submit")
async def submit_transport_request(
    request: Request,
    data: str = Form(...),  # JSON as form field (not file!)
    attachment: Optional[UploadFile] = File(None)
):
    """
    Accepts JSON data (as form field) and optional file. Returns unique request ID.
    """
    start_time = time.time()
    user_ip = request.client.host if request.client else "unknown"
    
    logger.info("=== NEW SUBMIT REQUEST ===")
    logger.info(f"Received data: {data}")
    logger.info(f"Attachment: {attachment.filename if attachment else 'None'}")
    
    # Generate unique request ID first for logging
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    rand = random.randint(100, 999)
    request_id = f"REQ-{now}-{rand}"
    
    try:
        # Parse JSON data
        data_dict = json.loads(data)
        logger.info(f"Parsed JSON: {data_dict}")
        req = TransportRequest(**data_dict)
        logger.info("Data validation successful")
        logger.info(f"Generated request ID: {request_id}")
        
        # Log form submission attempt
        app_logger.log_form_submit(
            form_data=data_dict,
            attachment_name=attachment.filename if attachment else None,
            status="PROCESSING",
            request_id=request_id,
            user_ip=user_ip
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        
        # Log failed submission
        app_logger.log_form_submit(
            form_data={"raw_data": data},
            status="ERROR",
            error_message=f"JSON decode error: {e}",
            request_id=request_id,
            user_ip=user_ip
        )
        
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
        
    except Exception as e:
        logger.error(f"Data validation error: {e}")
        
        # Log validation error
        try:
            parsed_data = json.loads(data)
        except:
            parsed_data = {"raw_data": data}
            
        app_logger.log_form_submit(
            form_data=parsed_data,
            attachment_name=attachment.filename if attachment else None,
            status="ERROR",
            error_message=f"Data validation error: {e}",
            request_id=request_id,
            user_ip=user_ip
        )
        
        raise HTTPException(status_code=400, detail=f"Invalid data: {e}")

    # Save attachment with new name if exists
    attachment_saved = False
    if attachment and attachment.filename:
        ext = os.path.splitext(attachment.filename)[1]
        new_filename = f"attachment_{request_id}{ext}"
        
        # Get attachments folder from config (relative to backend folder)
        attachments_folder = transport_config.get('local_attachments_folder', './attachments')
        backend_dir = Path(__file__).parent
        attachments_path = backend_dir / attachments_folder.lstrip('./')
        
        # Create attachments directory if it doesn't exist
        attachments_path.mkdir(exist_ok=True)
        
        # Save file locally
        file_path = attachments_path / new_filename
        content = await attachment.read()
        with open(file_path, "wb") as f:
            f.write(content)
        attachment_saved = True
        
        logger.info(f"Attachment saved: {file_path} ({len(content)} bytes)")
        
        # TODO: Upload to SharePoint here
        sharepoint_path = transport_config.get('sharepoint_attachments_folder', '/Shared Documents/Attachments')
        logger.info(f"TODO: Upload to SharePoint: {sharepoint_path}/{new_filename}")
    else:
        logger.info("No attachment received")

    # Log received data summary
    logger.info(f"Request processed successfully:")
    logger.info(f"  - Request ID: {request_id}")
    logger.info(f"  - Delivery Note: {data_dict.get('deliveryNoteNumber')}")
    logger.info(f"  - Carrier: {data_dict.get('carrierFullName')}")
    logger.info(f"  - Border Crossing: {data_dict.get('borderCrossing')}")
    logger.info(f"  - Attachment: {'Yes' if attachment_saved else 'No'}")
    
    # Save data to Excel
    excel_saved = save_to_excel(request_id, data_dict, attachment_saved)
    
    # Calculate processing time
    processing_time = int((time.time() - start_time) * 1000)  # milliseconds
    
    # Log successful completion
    app_logger.log_form_submit(
        form_data=data_dict,
        attachment_name=attachment.filename if attachment else None,
        status="SUCCESS",
        request_id=request_id,
        user_ip=user_ip
    )
    
    response_data = {
        "success": True,
        "request_id": request_id,
        "attachment_saved": attachment_saved,
        "excel_saved": excel_saved,
        "processing_time_ms": processing_time,
        "data_received": data_dict
    }
    
    logger.info("=== REQUEST COMPLETED ===")
    return JSONResponse(response_data)

def save_to_excel(request_id: str, data: dict, has_attachment: bool) -> bool:
    """Save transport request data to Excel file"""
    try:
        # Get Excel file path from config
        excel_file = transport_config.get('local_excel_file', './data/transport_requests.xlsx')
        backend_dir = Path(__file__).parent
        excel_path = backend_dir / excel_file.lstrip('./')
        
        # Create data directory if it doesn't exist
        excel_path.parent.mkdir(exist_ok=True)
        
        # Prepare row data
        row_data = {
            'Request_ID': request_id,
            'Timestamp': datetime.now().isoformat(),
            'Delivery_Note_Number': data.get('deliveryNoteNumber', ''),
            'Truck_License_Plates': data.get('truckLicensePlates', ''),
            'Trailer_License_Plates': data.get('trailerLicensePlates', ''),
            'Carrier_Country': data.get('carrierCountry', ''),
            'Carrier_Tax_Code': data.get('carrierTaxCode', ''),
            'Carrier_Full_Name': data.get('carrierFullName', ''),
            'Border_Crossing': data.get('borderCrossing', ''),
            'Border_Crossing_Date': data.get('borderCrossingDate', ''),
            'Has_Attachment': 'Yes' if has_attachment else 'No'
        }
        
        logger.info(f"Saving to Excel: {excel_path}")
        logger.info(f"Row data: {row_data}")
        
        # TODO: Implement Excel writing (openpyxl or pandas)
        # For now, save as JSON
        json_path = excel_path.with_suffix('.json')
        
        # Load existing data or create new
        existing_data = []
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        
        # Add new row
        existing_data.append(row_data)
        
        # Save updated data
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data saved to: {json_path}")
        
        # TODO: Upload to SharePoint Excel
        sharepoint_excel = transport_config.get('sharepoint_excel_path', '/Shared Documents/transport_requests.xlsx')
        logger.info(f"TODO: Upload to SharePoint Excel: {sharepoint_excel}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error saving to Excel: {e}")
        return False

@app.get("/")
def root():
    logger.info("Health check endpoint accessed")
    return {"message": "Transport backend running", "status": "healthy"}

@app.get("/api/health")
def health():
    logger.info("API health check accessed")
    return {"status": "healthy", "service": "transport-api"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
