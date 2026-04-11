import { render, screen } from '@testing-library/react'
import RecoCardFactory from '../../src/components/cards/RecoCardFactory'

const baseReco = {
  id: 1,
  description: 'Great video',
  from_user: 'johnDoe',
  to_user: 'janeDoe',
  rating: null,
  created_at: '2024-01-01T00:00:00',
}

describe('RecoCardFactory', () => {
  it('renders YouTubeCard for youtube embed links', () => {
    const reco = { ...baseReco, link: 'https://youtube.com/embed/dQw4w9WgXcQ' }
    render(<RecoCardFactory reco={reco} direction="received" />)
    expect(screen.getByTitle('Great video')).toBeInTheDocument()
    // iframe is rendered for YouTube
    expect(document.querySelector('iframe')).toBeInTheDocument()
  })

  it('renders BaseRecoCard with plain link for unknown platforms', () => {
    const reco = { ...baseReco, link: 'https://unknown-platform.com/video/123' }
    render(<RecoCardFactory reco={reco} direction="received" />)
    expect(
      screen.getByText('https://unknown-platform.com/video/123'),
    ).toBeInTheDocument()
    expect(document.querySelector('iframe')).not.toBeInTheDocument()
  })

  it('shows from_user on received recos', () => {
    const reco = { ...baseReco, link: 'https://youtube.com/embed/abc' }
    render(<RecoCardFactory reco={reco} direction="received" />)
    expect(screen.getByText(/johnDoe/)).toBeInTheDocument()
  })

  it('shows to_user on sent recos', () => {
    const reco = { ...baseReco, link: 'https://youtube.com/embed/abc' }
    render(<RecoCardFactory reco={reco} direction="sent" />)
    expect(screen.getByText(/janeDoe/)).toBeInTheDocument()
  })

  it('shows star rating on received recos', () => {
    const reco = { ...baseReco, link: 'https://youtube.com/embed/abc' }
    render(<RecoCardFactory reco={reco} direction="received" />)
    const stars = document.querySelectorAll('.star')
    expect(stars.length).toBe(5)
  })

  it('does not show star rating on sent recos', () => {
    const reco = { ...baseReco, link: 'https://youtube.com/embed/abc' }
    render(<RecoCardFactory reco={reco} direction="sent" />)
    expect(document.querySelectorAll('.star').length).toBe(0)
  })

  it('shows filled stars up to rating value', () => {
    const reco = {
      ...baseReco,
      link: 'https://youtube.com/embed/abc',
      rating: 3,
    }
    render(<RecoCardFactory reco={reco} direction="received" />)
    const filled = document.querySelectorAll('.star.filled')
    expect(filled.length).toBe(3)
  })
})
