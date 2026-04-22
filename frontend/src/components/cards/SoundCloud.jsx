import BaseRecoCard from './BaseRecoCard'

export default function SoundCloudCard({ reco, direction, onRate, onAnswer }) {
  return (
    <BaseRecoCard
      reco={reco}
      direction={direction}
      onRate={onRate}
      onAnswer={onAnswer}
      variant="soundcloud"
      player={
        <iframe
          src={reco.link}
          title={reco.description}
          allow="autoplay"
          scrolling="no"
        />
      }
    />
  )
}
