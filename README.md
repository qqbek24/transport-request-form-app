# Transport Form Application

A React-based web application for collecting transport company and driver information for UIT-RO (Uniunea Internationala a Transportatorilor Rutieri din Romania) registration.

## Features

- **Comprehensive Form Validation**: Real-time validation for all required fields
- **File Upload**: Support for PDF, JPG, and PNG documents with drag-and-drop functionality
- **Responsive Design**: Works on desktop and mobile devices
- **User-Friendly Interface**: Clear sections and intuitive form layout
- **Border Crossing Points**: Pre-populated dropdown with Romanian border crossings
- **Transport Types**: Dropdown with various transport categories

## Form Sections

### 1. Company Information
- Company name, address, phone, and email
- All fields required

### 2. Driver Information
- Driver's first name, last name, phone
- Driver's license number and expiry date
- All fields required

### 3. Vehicle Information
- Vehicle registration number, make, model, year
- Optional VIN number field

### 4. Transport Information
- Departure date, route (from/to)
- Border crossing point selection
- Transport type selection

### 5. Documents Upload (Optional)
- Support for multiple file uploads
- File type validation (PDF, JPG, PNG)
- File size limits (10MB per file, 5 files total)
- Drag and drop functionality

## Tech Stack

- **React 18** - Frontend framework
- **React Hook Form** - Form state management and validation
- **Yup** - Schema validation
- **React Dropzone** - File upload functionality
- **Vite** - Build tool and development server

## Getting Started

### Prerequisites
- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Form Validation Rules

### Required Fields
- All company information fields
- All driver information fields
- All vehicle information fields (except VIN)
- All transport information fields

### Validation Rules
- **Email**: Must be valid email format
- **License Expiry**: Must be a future date
- **Departure Date**: Must be a future date
- **Vehicle Year**: Must be between 1900 and current year
- **File Upload**: PDF, JPG, PNG only, max 10MB per file

## Border Crossing Points

The application includes pre-configured Romanian border crossing points:
- Albita, Borș, Calafat, Constanța Sud Agigea, Constanța Port
- Giurgiu, Nădlac, Otopeni, Stamora Moravița
- Turnu Severin, Vama Veche

## Transport Types

Supported transport categories:
- Freight Transport
- Passenger Transport
- Combined Transport
- Dangerous Goods Transport
- Oversized Transport

## Development

### Project Structure
```
src/
├── components/
│   ├── TransportForm/     # Main form component
│   ├── FormField/         # Reusable form field component
│   └── FileUpload/        # File upload component
├── App.jsx                # Main application component
├── main.jsx              # Application entry point
└── index.css             # Global styles
```

### Future Enhancements
- Backend API integration
- Form data persistence
- Email notifications
- PDF generation
- Multi-language support
- Form progress saving

## License

This project is licensed under the MIT License.