import { useState } from 'react'
import './RecoCard.css'

export default function BaseRecoCard({
  reco,
  direction,
  onRate,
  onAnswer,
  player,
}) {
  const isReceived = direction === 'received'
  const [answerInput, setAnswerInput] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleAnswerSubmit() {
    if (!answerInput.trim()) return
    setSubmitting(true)
    try {
      await onAnswer(reco.id, answerInput.trim())
      setAnswerInput('')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="reco-card">
      <div className="reco-player">
        {player ?? (
          <a
            href={reco.link}
            target="_blank"
            rel="noreferrer"
            className="reco-link"
          >
            {reco.link}
          </a>
        )}
      </div>

      <div className="reco-meta">
        <p className="reco-description">{reco.description}</p>

        {/* Star rating — received only */}
        {isReceived && (
          <div className="reco-rating">
            <div className="reco-rating-inner">
              {[5, 4, 3, 2, 1].map((star) => (
                <button
                  key={star}
                  className={`star ${reco.rating >= star ? 'filled' : ''}`}
                  onClick={() => onRate?.(reco.id, star)}
                  title={`Rate ${star}`}
                >
                  ★
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Rating read-only — sent only */}
        {!isReceived && reco.rating && (
          <p className="reco-rated">
            {'★'.repeat(reco.rating)}
            {'☆'.repeat(5 - reco.rating)}
          </p>
        )}

        {/* Answer section */}
        <div className="reco-answer-section">
          {reco.answer ? (
            // Answer exists — show it in both directions
            <div className="reco-answer-display">
              <span className="reco-answer-label">
                {isReceived ? 'Your reply' : 'Their reply'}
              </span>
              <p className="reco-answer-text">{reco.answer}</p>
            </div>
          ) : isReceived ? (
            // No answer yet — show input on received side
            <div className="reco-answer-form">
              <input
                type="text"
                value={answerInput}
                onChange={(e) => setAnswerInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAnswerSubmit()}
                placeholder="Reply to this recommendation..."
                maxLength={280}
                className="reco-answer-input"
              />
              <button
                className="reco-answer-btn"
                onClick={handleAnswerSubmit}
                disabled={submitting || !answerInput.trim()}
              >
                {submitting ? '...' : '↩'}
              </button>
            </div>
          ) : (
            // No answer yet — show placeholder on sent side
            <p className="reco-answer-pending">No reply yet</p>
          )}
        </div>

        <div className="reco-footer">
          <span className="reco-user">
            {isReceived ? `From ${reco.from_user}` : `To ${reco.to_user}`}
          </span>
          <span className="reco-date">
            {new Date(reco.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>
    </div>
  )
}
