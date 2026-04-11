import { render, screen, fireEvent } from '@testing-library/react'
import { vi } from 'vitest'
import BaseRecoCard from '../../src/components/cards/BaseRecoCard'

const baseReco = {
    id: 1,
    link: 'https://youtube.com/embed/dQw4w9WgXcQ',
    description: 'Watch this amazing video',
    from_user: 'johnDoe',
    to_user: 'janeDoe',
    rating: null,
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
        render(<BaseRecoCard reco={baseReco} direction="received" onRate={onRate} />)

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
            />
        )
        expect(screen.getByTestId('custom-player')).toBeInTheDocument()
    })
})