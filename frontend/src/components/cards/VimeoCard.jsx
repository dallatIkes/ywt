import BaseRecoCard from './BaseRecoCard'

export default function VimeoCard({ reco, direction, onRate }) {
    return (
        <BaseRecoCard
            reco={reco}
            direction={direction}
            onRate={onRate}
            player={
                <iframe
                    src={reco.link}
                    title={reco.description}
                    frameBorder="0"
                    allow="autoplay; fullscreen; picture-in-picture"
                    allowFullScreen
                />
            }
        />
    )
}