import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Tokens from './pages/Tokens'
import './App.css'

/**
 * Main App Component
 * Sets up React Router with routes:
 * - / → Home page
 * - /dashboard → Dashboard page
 * - /tokens → Tokens page
 */
function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/tokens" element={<Tokens />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

