import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/useAuth'
import './Navbar.css'

export default function Navbar() {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  function isActive(path) {
    return location.pathname === path ? 'nav-btn active' : 'nav-btn'
  }

  return (
    <nav className="navbar">
      {/* Desktop layout */}
      <div className="navbar-inner">
        <span className="brand">Yo Watch This!</span>

        <div className="nav-links">
          <button
            className={isActive('/received')}
            onClick={() => navigate('/received')}
          >
            Received
          </button>
          <button
            className={isActive('/sent')}
            onClick={() => navigate('/sent')}
          >
            Sent
          </button>
          <button
            className={isActive('/recommend')}
            onClick={() => navigate('/recommend')}
          >
            Recommend
          </button>
          <button
            className={isActive('/friends')}
            onClick={() => navigate('/friends')}
          >
            Friends
          </button>
        </div>

        <div className="nav-right">
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      {/* Mobile tab bar — shown via CSS on small screens */}
      <div className="tab-bar">
        <button
          className={isActive('/received')}
          onClick={() => navigate('/received')}
        >
          <span className="tab-icon">📥</span>
          <span className="tab-label">Received</span>
        </button>
        <button className={isActive('/sent')} onClick={() => navigate('/sent')}>
          <span className="tab-icon">📤</span>
          <span className="tab-label">Sent</span>
        </button>
        <button
          className={isActive('/recommend')}
          onClick={() => navigate('/recommend')}
        >
          <span className="tab-icon">➕</span>
          <span className="tab-label">Recommend</span>
        </button>
        <button
          className={isActive('/friends')}
          onClick={() => navigate('/friends')}
        >
          <span className="tab-icon">👥</span>
          <span className="tab-label">Friends</span>
        </button>
      </div>
    </nav>
  )
}
