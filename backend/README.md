# 📋 Transport Request System - Backend Configuration

## 🔧 Configuration Overview

Backend używa pliku `config.yaml` do konfiguracji ścieżek i ustawień:

### 📁 **Lokalne ścieżki (Development):**
- **Załączniki:** `./backend/attachments/`
- **Dane Excel:** `./backend/data/transport_requests.json` (tymczasowo jako JSON)

### ☁️ **SharePoint ścieżki (Production):**
- **Załączniki:** `/Shared Documents/Attachments`
- **Excel:** `/Shared Documents/transport_requests.xlsx`

## 🗂️ **Struktura danych w Excel/JSON:**

```json
{
  "Request_ID": "REQ-20251021-201256-890",
  "Timestamp": "2025-10-21T20:12:56.890",
  "Delivery_Note_Number": "54455424",
  "Truck_License_Plates": "EL2222gggg", 
  "Trailer_License_Plates": "14554e1gdggf2333",
  "Carrier_Country": "Albania",
  "Carrier_Tax_Code": "sdfds4353535",
  "Carrier_Full_Name": "Transport_testy54454",
  "Border_Crossing": "Ostrov",
  "Border_Crossing_Date": "2025-10-22",
  "Has_Attachment": "Yes"
}
```

## 🔄 **Workflow:**

1. **Formularz wysyła dane** → FastAPI endpoint `/api/submit`
2. **Backend generuje Request ID** (format: `REQ-YYYYMMDD-HHMMSS-XXX`)
3. **Załącznik zapisywany lokalnie** → `backend/attachments/attachment_{REQUEST_ID}.ext`
4. **Dane zapisywane lokalnie** → `backend/data/transport_requests.json`
5. **TODO: Upload do SharePoint** (Excel + załączniki)

## ⚙️ **Konfiguracja w config.yaml:**

```yaml
default:
  transport:
    # Local development paths (relative to backend folder)
    local_attachments_folder: "./attachments"
    local_excel_file: "./data/transport_requests.xlsx"
    
    # SharePoint production settings
    sharepoint_site: "https://your-sharepoint-site.sharepoint.com/sites/transport"
    sharepoint_excel_path: "/Shared Documents/transport_requests.xlsx"
    sharepoint_attachments_folder: "/Shared Documents/Attachments"
```

## 🚀 **Następne kroki:**

1. **Implementacja zapisu do Excel** (openpyxl/pandas)
2. **Integracja z SharePoint API**
3. **Uwierzytelnianie SharePoint**
4. **Upload plików do SharePoint**