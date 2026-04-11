import './RecoCard.css'

export default function BaseRecoCard({ reco, direction, onRate, player }) {
  const isReceived = direction === 'received'

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

        {/* Rating */}
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

        {!isReceived && reco.rating && (
          <p className="reco-rated">
            {'★'.repeat(reco.rating)}
            {'☆'.repeat(5 - reco.rating)}
          </p>
        )}

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
