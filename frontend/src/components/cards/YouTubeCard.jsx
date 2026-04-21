import BaseRecoCard from './BaseRecoCard'

export default function YouTubeCard({ reco, direction, onRate, onAnswer }) {
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
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      }
    />
  )
}
