import { useState, useEffect } from 'react'
import {
    getFriends,
    getPendingRequests,
    getSentPendingRequests,
    sendFriendRequest,
    respondToRequest
} from '../api/friendships'
import { useAuth } from '../context/AuthContext'
import './Page.css'
import './Friends.css'

export default function Friends() {
    const { currentUser } = useAuth()
    const [friends, setFriends] = useState([])
    const [pendingReceived, setPendingReceived] = useState([])
    const [pendingSent, setPendingSent] = useState([])
    const [newId, setNewId] = useState('')
    const [error, setError] = useState(null)
    const [success, setSuccess] = useState(null)
    const [copied, setCopied] = useState(false)

    useEffect(() => {
        getFriends().then(setFriends).catch(() => { })
        getPendingRequests().then(setPendingReceived).catch(() => { })
        getSentPendingRequests().then(setPendingSent).catch(() => { })
    }, [])

    async function copyId() {
        if (!currentUser?.id) return
        await navigator.clipboard.writeText(currentUser.id)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    async function handleSendRequest(e) {
        e.preventDefault()
        setError(null)
        setSuccess(null)
        try {
            const req = await sendFriendRequest(newId)
            setSuccess('Friend request sent!')
            setNewId('')
            setPendingSent((prev) => [...prev, req])
        } catch (err) {
            setError(err.response?.data?.detail ?? 'Failed to send request')
        }
    }

    async function handleRespond(friendshipId, status) {
        try {
            await respondToRequest(friendshipId, status)
            setPendingReceived((prev) => prev.filter((r) => r.id !== friendshipId))
            if (status === 'accepted') getFriends().then(setFriends)
        } catch {
            alert('Failed to respond to request')
        }
    }

    return (
        <div className="page">
            <h2 className="page-title">Friends</h2>

            {/* My ID */}
            <div className="my-id-card">
                <div className="my-id-info">
                    <span className="my-id-label">Your ID</span>
                    <span className="my-id-value">{currentUser?.id}</span>
                </div>
                <button className="btn-copy-id" onClick={copyId}>
                    {copied ? '✓ Copied' : '📋 Copy'}
                </button>
            </div>

            {/* Send request */}
            <section className="friends-section">
                <h3 className="section-title">Add a friend</h3>
                <form onSubmit={handleSendRequest} className="add-friend-form">
                    <input
                        type="text"
                        value={newId}
                        onChange={(e) => setNewId(e.target.value)}
                        placeholder="Paste a friend's user ID"
                        required
                    />
                    <button type="submit" className="btn-primary">Send request</button>
                </form>
                {error && <p className="form-error" style={{ marginTop: '0.5rem' }}>{error}</p>}
                {success && <p className="form-success" style={{ marginTop: '0.5rem' }}>{success}</p>}
            </section>

            {/* Pending received */}
            {pendingReceived.length > 0 && (
                <section className="friends-section">
                    <h3 className="section-title">
                        Requests received
                        <span className="badge">{pendingReceived.length}</span>
                    </h3>
                    <ul className="friends-list">
                        {pendingReceived.map((req) => (
                            <li key={req.id} className="friend-item">
                                <div className="friend-avatar">?</div>
                                <div className="friend-info">
                                    <span className="friend-name">{req.requester_username}</span>
                                    <span className="friend-sub">wants to be your friend</span>
                                </div>
                                <div className="friend-actions">
                                    <button className="btn-accept" onClick={() => handleRespond(req.id, 'accepted')}>Accept</button>
                                    <button className="btn-decline" onClick={() => handleRespond(req.id, 'declined')}>Decline</button>
                                </div>
                            </li>
                        ))}
                    </ul>
                </section>
            )}

            {/* Pending sent */}
            {pendingSent.length > 0 && (
                <section className="friends-section">
                    <h3 className="section-title">
                        Requests sent
                        <span className="badge pending">{pendingSent.length}</span>
                    </h3>
                    <ul className="friends-list">
                        {pendingSent.map((req) => (
                            <li key={req.id} className="friend-item">
                                <div className="friend-avatar pending-avatar">…</div>
                                <div className="friend-info">
                                    <span className="friend-name">{req.addressee_username}</span>
                                    <span className="friend-sub">pending response</span>
                                </div>
                                <span className="pending-chip">Pending</span>
                            </li>
                        ))}
                    </ul>
                </section>
            )}

            {/* Friends list */}
            <section className="friends-section">
                <h3 className="section-title">
                    My friends
                    <span className="badge">{friends.length}</span>
                </h3>
                {friends.length === 0 ? (
                    <p className="page-empty">No friends yet — send a request above.</p>
                ) : (
                    <ul className="friends-list">
                        {friends.map((f) => (
                            <li key={f.id} className="friend-item">
                                <div className="friend-avatar">{f.username[0].toUpperCase()}</div>
                                <div className="friend-info">
                                    <span className="friend-name">{f.username}</span>
                                    <span className="friend-sub friend-id-text">{f.id}</span>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </div>
    )
}