<script>
    import { goto } from '$app/navigation';

    const API_URL = import.meta.env.VITE_API_URL;
    
    let username = '';
    let password = '';
    let error = '';
    
    async function login() {
        error = '';
        
        // Calling the /token endpoint
        const res = await fetch(`${API_URL}/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username, password })
        });
        
        if (!res.ok) {
            error = 'Invalid username or password';
            return;
        }
        
        const data = await res.json();
        const token = data.access_token;
        
        // Store the token for the upcoming fetches
        localStorage.setItem('access_token', token);
        
        // Fetch and store current user info
        try {
            const userRes = await fetch(`${API_URL}/users/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (userRes.ok) {
                const userData = await userRes.json();
                localStorage.setItem('current_user', JSON.stringify(userData));
            }
        } catch (err) {
            console.error('Failed to fetch user data:', err);
        }
        
        // Redirection after login
        goto('/received');
    }
</script>

<form on:submit|preventDefault={login}>
    <h1>Login</h1>
    <label>
        Username:
        <input bind:value={username} placeholder="johnDoe"/>
    </label>
    <label>
        Password:
        <input type="password" bind:value={password} />
    </label>
    <button type="submit">Login</button>
    {#if error}
        <p style="color:red">{error}</p>
    {/if}
</form>

<style>
    /* Container */
    :global(body) {
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f0f2f5;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }

    h1 {
        text-align: center;
        margin-bottom: 1rem;
        color: #333;
    }

    form {
        background: #fff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        width: 100%;
        max-width: 400px;
        box-sizing: border-box;
    }

    label {
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
        font-weight: 500;
        color: #555;
    }

    input {
        padding: 0.6rem 0.8rem;
        margin-top: 0.4rem;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 1rem;
        transition: border-color 0.2s;
    }

    input:focus {
        outline: none;
        border-color: #007bff;
    }

    button {
        padding: 0.8rem;
        background-color: #007bff;
        color: #fff;
        font-size: 1rem;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    button:hover {
        background-color: #0056b3;
    }

    p {
        margin-top: 1rem;
        text-align: center;
        color: red;
        font-weight: bold;
    }

    /* Responsive */
    @media (max-width: 480px) {
        form {
            padding: 1.5rem;
            width: 90%;
        }
    }
</style>