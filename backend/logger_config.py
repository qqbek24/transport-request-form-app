"""
Advanced logging system for Transport Request Management System
Provides structured logging with JSON format and CSV export capabilities
"""

import logging
import json
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import traceback


class StructuredLogger:
    """Advanced logger with JSON and CSV output capabilities"""
    
    def __init__(self, log_dir: str = "logs", app_name: str = "transport_app"):
        # Ensure logs are always relative to backend directory
        backend_dir = Path(__file__).parent
        self.log_dir = backend_dir / log_dir
        self.app_name = app_name
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup structured logger
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Setup file handlers
        self._setup_file_handlers()
        
    def _setup_file_handlers(self):
        """Setup file handlers for different log formats"""
        today = datetime.now().strftime("%Y%m%d")
        
        # JSON log handler
        json_handler = logging.FileHandler(
            self.log_dir / f"{self.app_name}_{today}.jsonl"
        )
        json_handler.setFormatter(self._get_json_formatter())
        self.logger.addHandler(json_handler)
        
        # Console handler for development
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(console_handler)
        
    def _get_json_formatter(self):
        """Custom JSON formatter"""
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                    'level': record.levelname,
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno
                }
                
                # Add extra fields if present
                if hasattr(record, 'extra_data'):
                    log_entry.update(record.extra_data)
                    
                return json.dumps(log_entry, ensure_ascii=False)
                
        return JSONFormatter()
    
    def log_form_submit(
        self, 
        form_data: Dict[str, Any], 
        attachment_name: Optional[str] = None,
        status: str = "SUCCESS",
        error_message: Optional[str] = None,
        request_id: Optional[str] = None,
        user_ip: Optional[str] = None
    ):
        """Log form submission with structured data"""
        
        log_data = {
            'event_type': 'FORM_SUBMIT',
            'request_id': request_id,
            'user_ip': user_ip,
            'form_data': {
                'delivery_note': form_data.get('deliveryNoteNumber', ''),
                'truck_plates': form_data.get('truckLicensePlates', ''),
                'trailer_plates': form_data.get('trailerLicensePlates', ''),
                'carrier_country': form_data.get('carrierCountry', ''),
                'carrier_name': form_data.get('carrierFullName', ''),
                'border_crossing': form_data.get('borderCrossing', ''),
                'crossing_date': form_data.get('borderCrossingDate', '')
            },
            'attachment': {
                'has_attachment': attachment_name is not None,
                'filename': attachment_name,
                'size_bytes': getattr(form_data, 'attachment_size', None)
            },
            'status': status,
            'error_message': error_message,
            'processing_time_ms': getattr(form_data, 'processing_time', None)
        }
        
        # Create log record with extra data
        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.ERROR if status == "ERROR" else logging.INFO,
            pathname="",
            lineno=0,
            msg=f"Form submission {status}: {request_id}",
            args=(),
            exc_info=None
        )
        record.extra_data = log_data
        
        self.logger.handle(record)
        
        # Also write to CSV for easy analysis
        self._write_csv_log(log_data)
    
    def _write_csv_log(self, log_data: Dict[str, Any]):
        """Write log entry to CSV file for easy analysis"""
        today = datetime.now().strftime("%Y%m%d")
        csv_file = self.log_dir / f"form_submissions_{today}.csv"
        
        # CSV headers
        headers = [
            'timestamp', 'event_type', 'request_id', 'user_ip', 'status',
            'delivery_note', 'truck_plates', 'trailer_plates', 
            'carrier_country', 'carrier_name', 'border_crossing', 'crossing_date',
            'has_attachment', 'attachment_filename', 'error_message'
        ]
        
        # Check if file exists to determine if we need headers
        file_exists = csv_file.exists()
        
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write headers if file is new
            if not file_exists:
                writer.writerow(headers)
            
            # Write data row
            writer.writerow([
                datetime.now().isoformat(),
                log_data['event_type'],
                log_data['request_id'],
                log_data['user_ip'],
                log_data['status'],
                log_data['form_data']['delivery_note'],
                log_data['form_data']['truck_plates'],
                log_data['form_data']['trailer_plates'],
                log_data['form_data']['carrier_country'],
                log_data['form_data']['carrier_name'],
                log_data['form_data']['border_crossing'],
                log_data['form_data']['crossing_date'],
                log_data['attachment']['has_attachment'],
                log_data['attachment']['filename'],
                log_data['error_message']
            ])
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error with full context"""
        error_data = {
            'event_type': 'ERROR',
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg=f"Error occurred: {str(error)}",
            args=(),
            exc_info=None
        )
        record.extra_data = error_data
        
        self.logger.handle(record)
    
    def log_info(self, message: str, extra_data: Dict[str, Any] = None):
        """Log general information"""
        log_data = {
            'event_type': 'INFO',
            'extra_data': extra_data or {}
        }
        
        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=message,
            args=(),
            exc_info=None
        )
        record.extra_data = log_data
        
        self.logger.handle(record)


# Global logger instance
app_logger = StructuredLogger()


def get_logger() -> StructuredLogger:
    """Get the application logger instance"""
    return app_logger