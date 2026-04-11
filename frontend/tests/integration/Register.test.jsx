import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi } from 'vitest'
import Register from '../../src/pages/Register'
import { AuthContext } from '../../src/context/AuthContext'

const mockNavigate = vi.fn()
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal()
  return { ...actual, useNavigate: () => mockNavigate }
})

function renderRegister(registerFn) {
  return render(
    <MemoryRouter>
      <AuthContext.Provider value={{ register: registerFn }}>
        <Register />
      </AuthContext.Provider>
    </MemoryRouter>,
  )
}

describe('Register page', () => {
  it('renders all fields', () => {
    renderRegister(vi.fn())
    expect(screen.getByPlaceholderText('3–20 characters')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('min 8 characters')).toBeInTheDocument()
  })

  it('shows error when passwords do not match', async () => {
    renderRegister(vi.fn())

    await userEvent.type(
      screen.getByPlaceholderText('3–20 characters'),
      'newuser',
    )
    await userEvent.type(
      screen.getByPlaceholderText('min 8 characters'),
      'password123',
    )
    await userEvent.type(
      screen.getByPlaceholderText('••••••••'),
      'different123',
    )
    await userEvent.click(
      screen.getByRole('button', { name: /create account/i }),
    )

    expect(screen.getByText('Passwords do not match')).toBeInTheDocument()
  })

  it('calls register with correct credentials', async () => {
    const mockRegister = vi.fn().mockResolvedValue({})
    renderRegister(mockRegister)

    await userEvent.type(
      screen.getByPlaceholderText('3–20 characters'),
      'newuser',
    )
    await userEvent.type(
      screen.getByPlaceholderText('min 8 characters'),
      'password123',
    )
    await userEvent.type(screen.getByPlaceholderText('••••••••'), 'password123')
    await userEvent.click(
      screen.getByRole('button', { name: /create account/i }),
    )

    await waitFor(() =>
      expect(mockRegister).toHaveBeenCalledWith('newuser', 'password123'),
    )
  })

  it('navigates to /received after successful register', async () => {
    const mockRegister = vi.fn().mockResolvedValue({})
    renderRegister(mockRegister)

    await userEvent.type(
      screen.getByPlaceholderText('3–20 characters'),
      'newuser',
    )
    await userEvent.type(
      screen.getByPlaceholderText('min 8 characters'),
      'password123',
    )
    await userEvent.type(screen.getByPlaceholderText('••••••••'), 'password123')
    await userEvent.click(
      screen.getByRole('button', { name: /create account/i }),
    )

    await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/received'))
  })

  it('shows backend error on failed register', async () => {
    const mockRegister = vi.fn().mockRejectedValue({
      response: { data: { detail: 'Username already exists' } },
    })
    renderRegister(mockRegister)

    await userEvent.type(
      screen.getByPlaceholderText('3–20 characters'),
      'takenuser',
    )
    await userEvent.type(
      screen.getByPlaceholderText('min 8 characters'),
      'password123',
    )
    await userEvent.type(screen.getByPlaceholderText('••••••••'), 'password123')
    await userEvent.click(
      screen.getByRole('button', { name: /create account/i }),
    )

    await waitFor(() =>
      expect(screen.getByText('Username already exists')).toBeInTheDocument(),
    )
  })
})
