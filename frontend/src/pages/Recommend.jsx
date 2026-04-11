import { useState, useEffect } from 'react'
import { sendReco } from '../api/recommendations'
import { getFriends } from '../api/friendships'
import './Page.css'
import './Recommend.css'

export default function Recommend() {
  const [friends, setFriends] = useState([])
  const [selectedId, setSelectedId] = useState('')
  const [link, setLink] = useState('')
  const [description, setDescription] = useState('')
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [previewUrl, setPreviewUrl] = useState(null)

  useEffect(() => {
    getFriends()
      .then(setFriends)
      .catch(() => {})
  }, [])

  // Build embed URL from raw YouTube link for preview
  function buildPreview(url) {
    try {
      const parsed = new URL(url)
      let videoId = null
      if (parsed.hostname === 'youtu.be') {
        videoId = parsed.pathname.slice(1)
      } else if (parsed.hostname.includes('youtube.com')) {
        videoId = parsed.searchParams.get('v')
      }
      return videoId ? `https://www.youtube.com/embed/${videoId}` : null
    } catch {
      return null
    }
  }

  function handleLinkChange(e) {
    const val = e.target.value
    setLink(val)
    setPreviewUrl(buildPreview(val))
  }

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
      setPreviewUrl(null)
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
              <label>YouTube link</label>
              <input
                type="url"
                value={link}
                onChange={handleLinkChange}
                placeholder="https://youtube.com/watch?v=..."
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

        {/* Right: preview */}
        <div className="recommend-preview">
          {previewUrl ? (
            <iframe
              src={previewUrl}
              title="Video preview"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : (
            <div className="preview-placeholder">
              <span className="preview-icon">▶</span>
              <p>Paste a YouTube link to preview the video</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
