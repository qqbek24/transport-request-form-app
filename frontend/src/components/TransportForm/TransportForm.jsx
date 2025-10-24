import React, { useState } from 'react'
import borderCrossingsData from '../../data/borderCrossings.json';
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import MuiFormField from '../FormField/MuiFormField'
import FileUpload from '../FileUpload/FileUpload'
import logger from '../../utils/logger'
import './TransportForm.css'


// Validation schema for new required fields
const schema = yup.object().shape({
  deliveryNoteNumber: yup.string().required('Delivery note number is required'),
  truckLicensePlates: yup.string().required('Truck license plate numbers are required'),
  trailerLicensePlates: yup.string().required('Trailer license plate numbers are required'),
  carrierCountry: yup.string().required("Carrier's country is required"),
  carrierTaxCode: yup.string().required("Carrier’s tax code is required"),
  carrierFullName: yup.string().required('Full name of the carrier is required'),
  borderCrossing: yup.string().required('Border crossing point in Romania is required'),
  borderCrossingDate: yup.date().required('Date of crossing border in Romania is required'),
})

const TransportForm = () => {

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [clearFileUpload, setClearFileUpload] = useState(false)
  
  const {
    handleSubmit,
    formState: { errors, isValid },
    reset,
  control
  } = useForm({
    resolver: yupResolver(schema),
    mode: 'onChange',
    defaultValues: {
      deliveryNoteNumber: '',
      truckLicensePlates: '',
      trailerLicensePlates: '',
      carrierCountry: '',
      carrierTaxCode: '',
      carrierFullName: '',
      borderCrossing: '',
      borderCrossingDate: null
    }
  })


  const onSubmit = async (data) => {
    setIsSubmitting(true)
    
    // Prepare logging data
    const formDataForLogging = {
      ...data,
      attachment: uploadedFiles && uploadedFiles.length > 0 ? uploadedFiles[0].file : null,
      borderCrossingDate: data.borderCrossingDate ? data.borderCrossingDate.toISOString().split('T')[0] : ''
    };
    
    // Log form submission attempt
    logger.logFormSubmit(formDataForLogging, 'ATTEMPT');
    
    try {
      // Prepare form data for FastAPI backend
      const formData = new FormData();
      
      // Convert form data to JSON string for the 'data' field
      const jsonData = {
        deliveryNoteNumber: data.deliveryNoteNumber,
        truckLicensePlates: data.truckLicensePlates,
        trailerLicensePlates: data.trailerLicensePlates,
        carrierCountry: data.carrierCountry,
        carrierTaxCode: data.carrierTaxCode,
        carrierFullName: data.carrierFullName,
        borderCrossing: data.borderCrossing,
        borderCrossingDate: data.borderCrossingDate ? data.borderCrossingDate.toISOString().split('T')[0] : ''
      };
      
      formData.append('data', JSON.stringify(jsonData));
      
      // Add single attachment if exists (first file only)
      if (uploadedFiles && uploadedFiles.length > 0) {
        formData.append('attachment', uploadedFiles[0].file);
      }
      
      // Send to FastAPI backend (development mode - direct connection)
      const response = await fetch('http://localhost:8000/api/submit', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        const errorMsg = errorData.detail || 'Failed to submit form';
        
        // Log API error
        logger.logFormSubmit(formDataForLogging, 'ERROR', errorMsg);
        logger.logApiError('/api/submit', new Error(errorMsg), jsonData);
        
        throw new Error(errorMsg);
      }
      
      const result = await response.json();
      console.log('Submit response:', result);
      
      // Log successful submission
      logger.logFormSubmit(formDataForLogging, 'SUCCESS', null, result.request_id);
      
      alert(`Form submitted successfully! Request ID: ${result.request_id}`);
      
      // Clear form and files
      reset()
      setUploadedFiles([])
      setClearFileUpload(true)
      
      // Reset clearFileUpload flag after a brief delay
      setTimeout(() => setClearFileUpload(false), 100)
    } catch (error) {
      console.error('Submit error:', error);
      
      // Determine error type
      let errorType = 'ERROR';
      if (error.name === 'TypeError' || error.message.includes('fetch')) {
        errorType = 'NETWORK_ERROR';
        logger.logApiError('/api/submit', error, formDataForLogging);
      }
      
      // Log error
      logger.logFormSubmit(formDataForLogging, errorType, error.message);
      alert(`Error submitting form: ${error.message}. Please try again.`);
    } finally {
      setIsSubmitting(false)
    }
  }


  // Use grouped border crossing points for select
  const borderCrossings = borderCrossingsData;


  return (
    <div className="transport-form">
      <form onSubmit={handleSubmit(onSubmit)} className="form">
        <div className="form-section">
          <h2>Transport Application</h2>
          <MuiFormField
            label="Delivery note number"
            name="deliveryNoteNumber"
            control={control}
            error={errors.deliveryNoteNumber}
            required
          />
          <hr className="form-divider" />
          <MuiFormField
            label="Truck license plate numbers"
            name="truckLicensePlates"
            control={control}
            error={errors.truckLicensePlates}
            required
          />
          <MuiFormField
            label="Trailer license plate numbers"
            name="trailerLicensePlates"
            control={control}
            error={errors.trailerLicensePlates}
            required
          />
          <MuiFormField
            label="Full name of the carrier"
            name="carrierFullName"
            control={control}
            error={errors.carrierFullName}
            required
          />
          <MuiFormField
            label="Carrier's country"
            name="carrierCountry"
            type="country"
            control={control}
            error={errors.carrierCountry}
            required
          />
          <MuiFormField
            label="Carrier’s tax code"
            name="carrierTaxCode"
            control={control}
            error={errors.carrierTaxCode}
            required
          />
          <hr className="form-divider" />
          <MuiFormField
            label="Border crossing point in Romania"
            name="borderCrossing"
            type="select"
            options={borderCrossings}
            control={control}
            error={errors.borderCrossing}
            required
          />
          {/* Ensure date field is not in a flex/grid row */}
          <div style={{ width: '100%', marginTop: '0.25rem' }}>
            <MuiFormField
              label="Date of crossing border in Romania"
              name="borderCrossingDate"
              type="date"
              control={control}
              error={errors.borderCrossingDate}
              required
            />
          </div>
          <hr className="form-divider" />
          <FileUpload 
            onFilesChange={setUploadedFiles} 
            clearFiles={clearFileUpload}
          />
        </div>
        <div className="form-actions">
          <button
            type="submit"
            className={`submit-button ${!isValid ? 'disabled' : ''}`}
            disabled={!isValid || isSubmitting}
          >
            {isSubmitting ? 'Submitting...' : 'Submit Application'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default TransportForm