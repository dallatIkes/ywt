import { useState, useEffect } from 'react'
import { getFriends, getPendingRequests, sendFriendRequest, respondToRequest } from '../api/friendships'
import { useAuth } from '../context/AuthContext'
import './Page.css'
import './Friends.css'

export default function Friends() {
    const { currentUser } = useAuth()
    const [friends, setFriends] = useState([])
    const [pending, setPending] = useState([])
    const [newId, setNewId] = useState('')
    const [error, setError] = useState(null)
    const [success, setSuccess] = useState(null)

    useEffect(() => {
        getFriends().then(setFriends).catch(() => { })
        getPendingRequests().then(setPending).catch(() => { })
    }, [])

    async function handleSendRequest(e) {
        e.preventDefault()
        setError(null)
        setSuccess(null)
        try {
            await sendFriendRequest(newId)
            setSuccess('Friend request sent!')
            setNewId('')
        } catch (err) {
            setError(err.response?.data?.detail ?? 'Failed to send request')
        }
    }

    async function handleRespond(friendshipId, status) {
        try {
            await respondToRequest(friendshipId, status)
            // Remove from pending and refresh friends if accepted
            setPending((prev) => prev.filter((r) => r.id !== friendshipId))
            if (status === 'accepted') {
                getFriends().then(setFriends)
            }
        } catch {
            alert('Failed to respond to request')
        }
    }

    return (
        <div className="page">
            <h2 className="page-title">Friends</h2>

            {/* Send friend request */}
            <section className="friends-section">
                <h3 className="section-title">Add a friend</h3>
                <form onSubmit={handleSendRequest} className="add-friend-form">
                    <input
                        type="text"
                        value={newId}
                        onChange={(e) => setNewId(e.target.value)}
                        placeholder="Paste a user ID"
                        required
                    />
                    <button type="submit" className="btn-primary">Send request</button>
                </form>
                {error && <p className="form-error">{error}</p>}
                {success && <p className="form-success">{success}</p>}
            </section>

            {/* Pending requests */}
            {pending.length > 0 && (
                <section className="friends-section">
                    <h3 className="section-title">Pending requests</h3>
                    <ul className="friends-list">
                        {pending.map((req) => (
                            <li key={req.id} className="friend-item">
                                <span className="friend-name">{req.requester_id}</span>
                                <div className="friend-actions">
                                    <button
                                        className="btn-accept"
                                        onClick={() => handleRespond(req.id, 'accepted')}
                                    >
                                        Accept
                                    </button>
                                    <button
                                        className="btn-decline"
                                        onClick={() => handleRespond(req.id, 'declined')}
                                    >
                                        Decline
                                    </button>
                                </div>
                            </li>
                        ))}
                    </ul>
                </section>
            )}

            {/* Friends list */}
            <section className="friends-section">
                <h3 className="section-title">My friends ({friends.length})</h3>
                {friends.length === 0 ? (
                    <p className="page-empty">No friends yet — send a request above.</p>
                ) : (
                    <ul className="friends-list">
                        {friends.map((f) => (
                            <li key={f.id} className="friend-item">
                                <div className="friend-avatar">
                                    {f.username[0].toUpperCase()}
                                </div>
                                <span className="friend-name">{f.username}</span>
                                <span className="friend-id">{f.id}</span>
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </div>
    )
}