import React from 'react'
import TransportForm from './components/TransportForm/TransportForm'
import './App.css'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>UIT-RO Transport Form</h1>
        <p>Please fill out the form below for transport registration</p>
      </header>
      <main>
        <TransportForm />
      </main>
    </div>
  )
}

export default App