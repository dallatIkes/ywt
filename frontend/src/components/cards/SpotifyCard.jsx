import BaseRecoCard from './BaseRecoCard'

export default function SpotifyCard({ reco, direction, onRate, onAnswer }) {
    return (
        <BaseRecoCard
            reco={reco}
            direction={direction}
            onRate={onRate}
            onAnswer={onAnswer}
            variant="spotify"
            player={
                <iframe
                    src={reco.link}
                    title={reco.description}
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy"
                />
            }
        />
    )
}