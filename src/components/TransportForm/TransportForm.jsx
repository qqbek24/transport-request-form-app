import React, { useState } from 'react'
import borderCrossingsData from '../../data/borderCrossings.json';
import { useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import * as yup from 'yup'
import MuiFormField from '../FormField/MuiFormField'
import FileUpload from '../FileUpload/FileUpload'
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
  
  const {
    handleSubmit,
    formState: { errors, isValid },
    reset,
  control
// register removed, not needed with MuiFormField
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
    try {
      // Prepare form data for sending, including files if any
      const formData = new FormData();
      Object.entries(data).forEach(([key, value]) => {
        formData.append(key, value);
      });
      if (uploadedFiles && uploadedFiles.length > 0) {
        uploadedFiles.forEach((fileObj) => {
          formData.append('attachments', fileObj.file);
        });
      }
      // Example: send to backend (uncomment and adjust URL as needed)
      // await fetch('/api/submit', { method: 'POST', body: formData });
      console.log('FormData entries:', Array.from(formData.entries()));
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))
      alert('Form submitted successfully!')
      reset()
      setUploadedFiles([])
    } catch (error) {
      alert('Error submitting form. Please try again.')
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
          <FileUpload onFilesChange={setUploadedFiles} />
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