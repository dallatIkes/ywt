import './RecoCard.css'

export default function BaseRecoCard({ reco, direction, onRate, player }) {
    const isReceived = direction === 'received'

    return (
        <div className="reco-card">
            <div className="reco-player">
                {player ?? (
                    <a href={reco.link} target="_blank" rel="noreferrer" className="reco-link">
                        {reco.link}
                    </a>
                )}
            </div>

            <div className="reco-meta">
                <p className="reco-description">{reco.description}</p>
                <div className="reco-footer">
                    <span className="reco-user">
                        {isReceived ? `From: ${reco.from_user}` : `To: ${reco.to_user}`}
                    </span>
                    <span className="reco-date">
                        {new Date(reco.created_at).toLocaleDateString()}
                    </span>
                </div>
                {isReceived && (
                    <div className="reco-rating">
                        {[1, 2, 3, 4, 5].map((star) => (
                            <button
                                key={star}
                                className={`star ${reco.rating >= star ? 'filled' : ''}`}
                                onClick={() => onRate?.(reco.id, star)}
                            >
                                ★
                            </button>
                        ))}
                    </div>
                )}
                {!isReceived && reco.rating && (
                    <p className="reco-rated">Rated: {'★'.repeat(reco.rating)}</p>
                )}
            </div>
        </div>
    )
}