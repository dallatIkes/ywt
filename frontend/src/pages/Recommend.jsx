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

    useEffect(() => {
        getFriends().then(setFriends).catch(() => { })
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

            <div className="recommend-card">
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
                                    <option key={f.id} value={f.id}>{f.username}</option>
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
                            onChange={(e) => setLink(e.target.value)}
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
                            rows={3}
                            required
                        />
                        <span className="char-count">{description.length}/280</span>
                    </div>

                    {error && <p className="form-error">{error}</p>}
                    {success && <p className="form-success">Recommendation sent!</p>}

                    <button type="submit" className="btn-primary" disabled={loading}>
                        {loading ? 'Sending...' : 'Send recommendation'}
                    </button>
                </form>
            </div>
        </div>
    )
}