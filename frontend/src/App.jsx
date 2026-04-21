import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthProvider'
import { useAuth } from './context/useAuth'
import ProtectedLayout from './components/layout/ProtectedLayout'
import Login from './pages/Login'
import Register from './pages/Register'
import Received from './pages/Received'
import Sent from './pages/Sent'
import Recommend from './pages/Recommend'
import Friends from './pages/Friends'
import ErrorBoundary from './components/ErrorBoundary'

function ProtectedRoute({ children }) {
  const { currentUser, loading } = useAuth()
  if (loading) return null
  if (!currentUser) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <ProtectedLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="/received" replace />} />
              <Route path="received" element={<Received />} />
              <Route path="sent" element={<Sent />} />
              <Route path="recommend" element={<Recommend />} />
              <Route path="friends" element={<Friends />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ErrorBoundary>
  )
}
