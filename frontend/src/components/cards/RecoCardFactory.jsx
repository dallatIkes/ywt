import { getMediaStrategy } from '../../lib/mediaStrategies'
import YouTubeCard from './YouTubeCard'
import VimeoCard from './VimeoCard'
import BaseRecoCard from './BaseRecoCard'
import DailymotionCard from './DailymotionCard'
import SpotifyCard from './SpotifyCard'

// Map platform name to card component
const CARD_COMPONENTS = {
  youtube: YouTubeCard,
  vimeo: VimeoCard,
  dailymotion: DailymotionCard,
  spotify: SpotifyCard,
}

export default function RecoCardFactory({ reco, direction, onRate, onAnswer }) {
  const strategy = getMediaStrategy(reco.link)
  const CardComponent = CARD_COMPONENTS[strategy.platform] ?? BaseRecoCard
  return (
    <CardComponent
      reco={reco}
      direction={direction}
      onRate={onRate}
      onAnswer={onAnswer}
    />
  )
}
