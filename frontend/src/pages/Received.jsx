import { useState, useEffect } from 'react'
import { getReceived, rateReco, answerReco } from '../api/recommendations'
import RecoCardFactory from '../components/cards/RecoCardFactory'
import './Page.css'

export default function Received() {
  const [recos, setRecos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getReceived()
      .then(setRecos)
      .catch(() => setError('Failed to load recommendations'))
      .finally(() => setLoading(false))
  }, [])

  async function handleRate(recoId, rating) {
    try {
      const updated = await rateReco(recoId, rating)
      setRecos((prev) =>
        prev.map((r) =>
          r.id === updated.id ? { ...r, rating: updated.rating } : r,
        ),
      )
    } catch {
      alert('Failed to rate recommendation')
    }
  }

  async function handleAnswer(recoId, answer) {
    try {
      const updated = await answerReco(recoId, answer)
      setRecos((prev) =>
        prev.map((r) =>
          r.id === updated.id ? { ...r, answer: updated.answer } : r,
        ),
      )
    } catch {
      alert('Failed to send answer')
    }
  }

  if (loading) return <div className="page-state">Loading...</div>
  if (error) return <div className="page-state error">{error}</div>

  return (
    <div className="page">
      <h2 className="page-title">Received</h2>
      {recos.length === 0 ? (
        <p className="page-empty">No recommendations received yet.</p>
      ) : (
        <div className="card-grid">
          {recos.map((reco) => (
            <RecoCardFactory
              key={reco.id}
              reco={reco}
              direction="received"
              onRate={handleRate}
              onAnswer={handleAnswer}
            />
          ))}
        </div>
      )}
    </div>
  )
}
