import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import BaseRecoCard from '../../src/components/cards/BaseRecoCard'

const baseReco = {
  id: 1,
  link: 'https://youtube.com/embed/dQw4w9WgXcQ',
  description: 'Watch this amazing video',
  from_user: 'johnDoe',
  to_user: 'janeDoe',
  rating: null,
  anwer: null,
  created_at: '2024-06-15T10:30:00',
}

describe('BaseRecoCard', () => {
  it('renders description', () => {
    render(<BaseRecoCard reco={baseReco} direction="received" />)
    expect(screen.getByText('Watch this amazing video')).toBeInTheDocument()
  })

  it('renders formatted date', () => {
    render(<BaseRecoCard reco={baseReco} direction="received" />)
    // Date formatted via toLocaleDateString — just check it's there
    expect(screen.getByText(/2024/)).toBeInTheDocument()
  })

  it('calls onRate with correct id and rating when star clicked', () => {
    const onRate = vi.fn()
    render(
      <BaseRecoCard reco={baseReco} direction="received" onRate={onRate} />,
    )

    const stars = document.querySelectorAll('.star')
    fireEvent.click(stars[0]) // first star in row-reverse = star 1

    expect(onRate).toHaveBeenCalledWith(1, expect.any(Number))
  })

  it('does not call onRate if not provided', () => {
    render(<BaseRecoCard reco={baseReco} direction="received" />)
    const stars = document.querySelectorAll('.star')
    expect(() => fireEvent.click(stars[0])).not.toThrow()
  })

  it('renders custom player when provided', () => {
    render(
      <BaseRecoCard
        reco={baseReco}
        direction="received"
        player={<div data-testid="custom-player">Custom</div>}
      />,
    )
    expect(screen.getByTestId('custom-player')).toBeInTheDocument()
  })

  it('shows answer input on received reco with no answer', () => {
    render(<BaseRecoCard reco={baseReco} direction="received" />)
    expect(
      screen.getByPlaceholderText('Reply to this recommendation...'),
    ).toBeInTheDocument()
  })

  it('does not show answer input on sent reco', () => {
    render(<BaseRecoCard reco={baseReco} direction="sent" />)
    expect(
      screen.queryByPlaceholderText('Reply to this recommendation...'),
    ).not.toBeInTheDocument()
  })

  it('shows no reply yet on sent reco with no answer', () => {
    render(<BaseRecoCard reco={baseReco} direction="sent" />)
    expect(screen.getByText('No reply yet')).toBeInTheDocument()
  })

  it('calls onAnswer with correct args on button click', async () => {
    const onAnswer = vi.fn().mockResolvedValue({})
    render(
      <BaseRecoCard reco={baseReco} direction="received" onAnswer={onAnswer} />,
    )

    fireEvent.change(
      screen.getByPlaceholderText('Reply to this recommendation...'),
      { target: { value: 'Loved it!' } },
    )
    fireEvent.click(screen.getByRole('button', { name: '↩' }))

    await waitFor(() => expect(onAnswer).toHaveBeenCalledWith(1, 'Loved it!'))
  })

  it('calls onAnswer on Enter key press', async () => {
    const onAnswer = vi.fn().mockResolvedValue({})
    render(
      <BaseRecoCard reco={baseReco} direction="received" onAnswer={onAnswer} />,
    )

    const input = screen.getByPlaceholderText('Reply to this recommendation...')
    fireEvent.change(input, { target: { value: 'Great pick!' } })
    fireEvent.keyDown(input, { key: 'Enter' })

    await waitFor(() => expect(onAnswer).toHaveBeenCalledWith(1, 'Great pick!'))
  })

  it('disables submit button when input is empty', () => {
    render(
      <BaseRecoCard reco={baseReco} direction="received" onAnswer={vi.fn()} />,
    )
    expect(screen.getByRole('button', { name: '↩' })).toBeDisabled()
  })

  it('shows answer text on received reco with existing answer', () => {
    const reco = { ...baseReco, answer: 'Loved it!' }
    render(<BaseRecoCard reco={reco} direction="received" />)
    expect(screen.getByText('Loved it!')).toBeInTheDocument()
    expect(screen.getByText('Your reply')).toBeInTheDocument()
  })

  it('shows answer text on sent reco with existing answer', () => {
    const reco = { ...baseReco, answer: 'Loved it!' }
    render(<BaseRecoCard reco={reco} direction="sent" />)
    expect(screen.getByText('Loved it!')).toBeInTheDocument()
    expect(screen.getByText('Their reply')).toBeInTheDocument()
  })

  it('clears input after successful answer', async () => {
    const onAnswer = vi.fn().mockResolvedValue({})
    render(
      <BaseRecoCard reco={baseReco} direction="received" onAnswer={onAnswer} />,
    )

    const input = screen.getByPlaceholderText('Reply to this recommendation...')
    fireEvent.change(input, { target: { value: 'Nice!' } })
    fireEvent.click(screen.getByRole('button', { name: '↩' }))

    await waitFor(() => expect(input).toHaveValue(''))
  })
})
