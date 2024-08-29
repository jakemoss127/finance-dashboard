import React, { useState } from 'react'
import './App.css'
import { Nav } from './components/NAv'

function App() {

  return (
    <div className='bg-zinc-200 min-w-full min-h-screen flex flex-col items-center justify-center'>
      <div className='absolute bg-white w-10/12 h-5/6 rounded-3xl'>
        <div className='p-6 bg-zinc-50 rounded-t-3xl h-2/5'>
          <Nav />
        </div>
      </div>
    </div>
  )
}

export default App
