import YouTubeCard from './YouTubeCard'
import VimeoCard from './VimeoCard'
import BaseRecoCard from './BaseRecoCard'

function detectPlatform(link) {
  if (!link) return 'unknown'
  if (link.includes('youtube.com/embed') || link.includes('youtu.be'))
    return 'youtube'
  if (link.includes('vimeo.com')) return 'vimeo'
  return 'unknown'
}

export default function RecoCardFactory({ reco, direction, onRate }) {
  const platform = detectPlatform(reco.link)

  switch (platform) {
    case 'youtube':
      return <YouTubeCard reco={reco} direction={direction} onRate={onRate} />
    case 'vimeo':
      return <VimeoCard reco={reco} direction={direction} onRate={onRate} />
    default:
      return <BaseRecoCard reco={reco} direction={direction} onRate={onRate} />
  }
}
