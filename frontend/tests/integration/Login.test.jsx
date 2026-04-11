import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { vi } from 'vitest'
import Login from '../../src/pages/Login'
import { AuthContext } from '../../src/context/AuthContext'

// Mock useNavigate
const mockNavigate = vi.fn()
vi.mock('react-router-dom', async (importOriginal) => {
    const actual = await importOriginal()
    return { ...actual, useNavigate: () => mockNavigate }
})

function renderLogin(loginFn) {
    return render(
        <MemoryRouter>
            <AuthContext.Provider value={{ login: loginFn }}>
                <Login />
            </AuthContext.Provider>
        </MemoryRouter>
    )
}

describe('Login page', () => {
    it('renders username and password fields', () => {
        renderLogin(vi.fn())
        expect(screen.getByPlaceholderText('your username')).toBeInTheDocument()
        expect(screen.getByPlaceholderText('••••••••')).toBeInTheDocument()
    })

    it('navigates to /received on successful login', async () => {
        const mockLogin = vi.fn().mockResolvedValue({})
        renderLogin(mockLogin)

        await userEvent.type(screen.getByPlaceholderText('your username'), 'johnDoe')
        await userEvent.type(screen.getByPlaceholderText('••••••••'), 'admin1234')
        await userEvent.click(screen.getByRole('button', { name: /sign in/i }))

        await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/received'))
    })

    it('shows error message on failed login', async () => {
        const mockLogin = vi.fn().mockRejectedValue({
            response: { data: { detail: 'Incorrect username or password' } }
        })
        renderLogin(mockLogin)

        await userEvent.type(screen.getByPlaceholderText('your username'), 'johnDoe')
        await userEvent.type(screen.getByPlaceholderText('••••••••'), 'wrongpass')
        await userEvent.click(screen.getByRole('button', { name: /sign in/i }))

        await waitFor(() =>
            expect(screen.getByText('Incorrect username or password')).toBeInTheDocument()
        )
    })

    it('clears password field on failed login', async () => {
        const mockLogin = vi.fn().mockRejectedValue({
            response: { data: { detail: 'Incorrect username or password' } }
        })
        renderLogin(mockLogin)

        await userEvent.type(screen.getByPlaceholderText('your username'), 'johnDoe')
        await userEvent.type(screen.getByPlaceholderText('••••••••'), 'wrongpass')
        await userEvent.click(screen.getByRole('button', { name: /sign in/i }))

        await waitFor(() =>
            expect(screen.getByPlaceholderText('••••••••')).toHaveValue('')
        )
    })

    it('keeps username field on failed login', async () => {
        const mockLogin = vi.fn().mockRejectedValue({
            response: { data: { detail: 'Incorrect username or password' } }
        })
        renderLogin(mockLogin)

        await userEvent.type(screen.getByPlaceholderText('your username'), 'johnDoe')
        await userEvent.type(screen.getByPlaceholderText('••••••••'), 'wrongpass')
        await userEvent.click(screen.getByRole('button', { name: /sign in/i }))

        await waitFor(() =>
            expect(screen.getByPlaceholderText('your username')).toHaveValue('johnDoe')
        )
    })

    it('disables button while loading', async () => {
        // Login never resolves — simulates slow network
        const mockLogin = vi.fn().mockReturnValue(new Promise(() => { }))
        renderLogin(mockLogin)

        await userEvent.type(screen.getByPlaceholderText('your username'), 'johnDoe')
        await userEvent.type(screen.getByPlaceholderText('••••••••'), 'admin1234')
        await userEvent.click(screen.getByRole('button', { name: /sign in/i }))

        expect(screen.getByRole('button', { name: /signing in/i })).toBeDisabled()
    })

    it('has a link to register page', () => {
        renderLogin(vi.fn())
        expect(screen.getByRole('link', { name: /create one/i })).toBeInTheDocument()
    })
})