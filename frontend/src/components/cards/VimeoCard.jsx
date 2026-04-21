import BaseRecoCard from './BaseRecoCard'

export default function VimeoCard({ reco, direction, onRate, onAnswer }) {
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
          allow="autoplay; fullscreen; picture-in-picture"
          allowFullScreen
        />
      }
    />
  )
}
