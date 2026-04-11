import client from './client'

export async function login(username, password) {
  // OAuth2 expects form data, not JSON
  const form = new URLSearchParams()
  form.append('username', username)
  form.append('password', password)

  const response = await client.post('/token', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    skipAuthRedirect: true, // flag custom
  })
  return response.data
}

export async function register(username, password) {
  const { data } = await client.post('/users', { username, password })
  return data // UserOut
}

export async function getMe() {
  const { data } = await client.get('/users/me')
  return data // UserOut
}
