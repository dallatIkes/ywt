import { useState, useEffect } from 'react'
import { AuthContext } from './AuthContext'
import { login as apiLogin, register as apiRegister, getMe } from '../api/auth'

export function AuthProvider({ children }) {
    const [currentUser, setCurrentUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const token = localStorage.getItem('access_token')
        if (!token) { setLoading(false); return }
        getMe()
            .then(setCurrentUser)
            .catch(() => localStorage.removeItem('access_token'))
            .finally(() => setLoading(false))
    }, [])

    async function login(username, password) {
        const { access_token } = await apiLogin(username, password)
        localStorage.setItem('access_token', access_token)
        const user = await getMe()
        setCurrentUser(user)
        return user
    }

    async function register(username, password) {
        await apiRegister(username, password)
        return login(username, password)
    }

    function logout() {
        localStorage.removeItem('access_token')
        setCurrentUser(null)
    }

    return (
        <AuthContext.Provider value={{ currentUser, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    )
}