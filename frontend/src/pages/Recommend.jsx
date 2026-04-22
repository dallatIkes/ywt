// src/pages/Recommend.jsx
import { useState, useEffect } from 'react'
import { sendReco } from '../api/recommendations'
import { getFriends } from '../api/friendships'
import { getMediaStrategy } from '../lib/mediaStrategies'
import './Page.css'
import './Recommend.css'

function Preview({ url }) {
  if (!url) {
    return (
      <div className="preview-placeholder">
        <span className="preview-icon">▶</span>
        <p>Paste a media link to preview the video</p>
      </div>
    )
  }

  const strategy = getMediaStrategy(url)
  const embedUrl = strategy.buildEmbedUrl(url)

  if (embedUrl) {
    return (
      <div className={`preview-embed preview-embed--${strategy.platform}`}>
        <iframe
          src={embedUrl}
          title="Video preview"
          frameBorder="0"
          allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen"
          allowFullScreen
        />
      </div>
    )
  }

  // Valid URL but no embed available — show link preview
  return (
    <div className="preview-external">
      <span className="preview-icon">🔗</span>
      <p className="preview-url">{url}</p>
      <a href={url} target="_blank" rel="noreferrer" className="preview-open">
        Open link
      </a>
    </div>
  )
}

export default function Recommend() {
  const [friends, setFriends] = useState([])
  const [selectedId, setSelectedId] = useState('')
  const [link, setLink] = useState('')
  const [description, setDescription] = useState('')
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    getFriends()
      .then(setFriends)
      .catch(() => {})
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setSuccess(false)
    setLoading(true)
    try {
      await sendReco(link, description, selectedId)
      setSuccess(true)
      setLink('')
      setDescription('')
      setSelectedId('')
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Failed to send recommendation')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <h2 className="page-title">Recommend a video</h2>

      <div className="recommend-layout">
        {/* Left: form */}
        <div className="recommend-form-card">
          <form onSubmit={handleSubmit} className="recommend-form">
            <div className="field">
              <label>Send to</label>
              {friends.length > 0 ? (
                <select
                  value={selectedId}
                  onChange={(e) => setSelectedId(e.target.value)}
                  required
                >
                  <option value="">Select a friend...</option>
                  {friends.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.username}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type="text"
                  value={selectedId}
                  onChange={(e) => setSelectedId(e.target.value)}
                  placeholder="Paste a user ID"
                  required
                />
              )}
            </div>

            <div className="field">
              <label>Media link</label>
              <input
                type="url"
                value={link}
                onChange={(e) => setLink(e.target.value)}
                placeholder="YouTube, Vimeo, or any video link..."
                required
              />
            </div>

            <div className="field">
              <label>Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Why should they watch this?"
                maxLength={280}
                rows={4}
                required
              />
              <span className="char-count">{description.length} / 280</span>
            </div>

            {error && <p className="form-error">{error}</p>}
            {success && <p className="form-success">Recommendation sent!</p>}

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Sending...' : 'Send recommendation'}
            </button>
          </form>
        </div>

        {/* Right: preview — updates live as user types */}
        <div className="recommend-preview">
          <Preview url={link} />
        </div>
      </div>
    </div>
  )
}
