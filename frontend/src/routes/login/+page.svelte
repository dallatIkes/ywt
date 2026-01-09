<script>
    import { goto } from '$app/navigation';

    let username = '';
    let password = '';
    let error = '';

    async function login() {
        error = '';

        // Calling the /token endpoint
        const res = await fetch('http://localhost:8000/token', {
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

        // Store the token for the upcomming fetches
        localStorage.setItem('access_token', token);

        // Redirectionn after login
        goto('/received');
    }
</script>

<h1>Login</h1>

<form on:submit|preventDefault={login}>
    <label>
        Username:
        <input bind:value={username} />
    </label>

    <label>
        Password:
        <input type="password" bind:value={password} />
    </label>

    <button type="submit">Login</button>
</form>

{#if error}
    <p style="color:red">{error}</p>
{/if}
