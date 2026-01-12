<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    const API_URL = import.meta.env.VITE_API_URL;

    let link = '';
    let user_id = '';
    let description = '';
    let error = '';
    let success = false;

    onMount(async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            goto('/login');
            return;
        }

        // Verify token is valid by making a request
        try {
            const res = await fetch(`${API_URL}/recommendations/sent`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!res.ok) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('current_user');
                goto('/login');
                return;
            }
        } catch (err) {
            console.error(err);
            goto('/login');
        }
    });

    async function new_reco() {
        error = '';
        success = false;

        const token = localStorage.getItem('access_token');
        if (!token) {
            goto('/login');
            return;
        }

        try {
            const res = await fetch(`${API_URL}/users/me`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    link: link,
                    description: description,
                    to_user_id: user_id
                })
            });

            // Token expired / invalid
            if (res.status === 401 || res.status === 403) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('current_user');
                goto('/login');
                return;
            }

            if (!res.ok) {
                let err = {};
                try { err = await res.json(); } catch {}
                error = err.detail || 'Failed to create recommendation';
                return;
            }

            // Success
            success = true;
            link = '';
            description = '';
            user_id = '';
        } catch (err) {
            console.error(err);
            error = 'Network error';
        }
    }
</script>

<div class="page-container">
    <form on:submit|preventDefault={new_reco}>
        <h1>Recommend a video to your friends</h1>

        <label>
            Your friend's ID:
            <input bind:value={user_id} placeholder="d1fb30d4-1259-4ffc-926a-e311e24907e2" required/>
        </label>

        <label>
            Video link:
            <input bind:value={link} placeholder="https://youtu.be/dQw4w9WgXcQ" required/>
        </label>

        <label>
            Quick description:
            <textarea 
                bind:value={description} 
                placeholder="A cool nintendo playlist!" 
                maxlength="280"
                required
            ></textarea>
            <span class="char-count">{description.length}/280</span>
        </label>

        <button type="submit">Recommend</button>

        {#if error}
            <p class="error">{error}</p>
        {:else if success}
            <p class="success">Recommendation sent!</p>
        {/if}
    </form>
</div>

<style>
    /* ============== */
    /* Page container */
    /* ============== */
    .page-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 6rem 1rem 2rem; 
        min-height: calc(100vh - 6rem);
    }

    h1 {
        text-align: center;
        margin-bottom: 2rem;
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
        max-width: 650px;
        box-sizing: border-box;
    }

    label {
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
        font-weight: 700;
        color: #555;
        position: relative;
    }

    input {
        padding: 0.6rem 0.8rem;
        margin-top: 0.4rem;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 1rem;
        transition: border-color 0.2s;
    }

    textarea {
        padding: 0.6rem 0.8rem;
        margin-top: 0.4rem;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 1rem;
        font-family: 'Arial', sans-serif;
        resize: none;
        min-height: 100px;
        transition: border-color 0.2s;
    }

    input:focus,
    textarea:focus {
        outline: none;
        border-color: #0077cc;
    }

    .char-count {
        align-self: flex-end;
        font-size: 0.85rem;
        color: #888;
        margin-top: 0.3rem;
    }

    button {
        padding: 0.8rem;
        background-color: #0077cc;
        color: #fff;
        font-size: 1rem;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    button:hover {
        background-color: #0056b3;
    }

    p.error {
        margin-top: 1rem;
        text-align: center;
        color: #dc3545;
        font-weight: bold;
    }

    p.success {
        margin-top: 1rem;
        text-align: center;
        color: #28a745;
        font-weight: bold;
    }

    /* Responsive */
    @media (max-width: 600px) {
        form {
            padding: 1.5rem;
            width: 90%;
            max-width: none;
        }
    }
</style>