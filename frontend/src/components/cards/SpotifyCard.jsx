import BaseRecoCard from "./BaseRecoCard";

export default function SpotifyCard({ reco, direction, onRate, onAnswer }) {
    return (
        <BaseRecoCard
            reco={reco}
            direction={direction}
            onRate={onRate}
            onAnswer={onAnswer}
            player={
                <iframe
                    src={reco.link}
                    title={reco.description}
                    allow="encrypted-media"
                    allowFullScreen
                />
            }
        />
    )
}