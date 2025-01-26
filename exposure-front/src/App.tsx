import { Routes, Route } from 'react-router-dom'
import './App.css'

// Other components for routes
import Home from './Home.tsx'
import Upload from './Upload.tsx'
import Report from './Report.tsx'

function App() {
  return (
    <>
      <Routes>
       <Route path="/" element={<Home />} />
       <Route path="/upload" element={<Upload />} />
       <Route path="/report/:rpt" element={<Report />} />
      </Routes>
    </>
  )
}

export default App
