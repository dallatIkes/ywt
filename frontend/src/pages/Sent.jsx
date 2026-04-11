import { useState, useEffect } from 'react'
import { getSent } from '../api/recommendations'
import RecoCardFactory from '../components/cards/RecoCardFactory'
import './Page.css'

export default function Sent() {
  const [recos, setRecos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getSent()
      .then(setRecos)
      .catch(() => setError('Failed to load recommendations'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="page-state">Loading...</div>
  if (error) return <div className="page-state error">{error}</div>

  return (
    <div className="page">
      <h2 className="page-title">Sent</h2>
      {recos.length === 0 ? (
        <p className="page-empty">
          You haven&apos;t sent any recommendations yet.
        </p>
      ) : (
        <div className="card-grid">
          {recos.map((reco) => (
            <RecoCardFactory key={reco.id} reco={reco} direction="sent" />
          ))}
        </div>
      )}
    </div>
  )
}
