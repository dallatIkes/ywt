// Mirror of the backend logic — keeps frontend and backend in sync
const VALID_TRANSITIONS = {
  pending: ['accepted', 'declined'],
  accepted: [],
  declined: [],
}

function canTransition(current, target) {
  return VALID_TRANSITIONS[current]?.includes(target) ?? false
}

describe('friendship state transitions', () => {
  it('allows pending → accepted', () => {
    expect(canTransition('pending', 'accepted')).toBe(true)
  })

  it('allows pending → declined', () => {
    expect(canTransition('pending', 'declined')).toBe(true)
  })

  it('blocks accepted → declined', () => {
    expect(canTransition('accepted', 'declined')).toBe(false)
  })

  it('blocks declined → accepted', () => {
    expect(canTransition('declined', 'accepted')).toBe(false)
  })

  it('blocks accepted → pending', () => {
    expect(canTransition('accepted', 'pending')).toBe(false)
  })

  it('returns false for unknown status', () => {
    expect(canTransition('unknown', 'accepted')).toBe(false)
  })
})
