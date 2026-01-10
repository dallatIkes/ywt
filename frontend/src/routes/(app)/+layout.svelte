<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let currentUser = null;
    let copySuccess = false;

    onMount(async () => {
        const token = localStorage.getItem('access_token');

        if (!token) {
            goto('/login');
            return;
        }

        // Check if user data is cached
        const cachedUser = localStorage.getItem('current_user');
        if (cachedUser) {
            currentUser = JSON.parse(cachedUser);
        }

        try {
            // Fetch current user only if not cached
            if (!cachedUser) {
                const userRes = await fetch('http://localhost:8000/users/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (userRes.ok) {
                    currentUser = await userRes.json();
                    localStorage.setItem('current_user', JSON.stringify(currentUser));
                }
            }
        } catch (err) {
            console.error(err);
            goto('/login');
            return;
        }
    });

    function handleLogout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('current_user');
        goto('/login');
    }

    async function copyUserId() {
        if (currentUser && currentUser.id) {
            try {
                await navigator.clipboard.writeText(currentUser.id);
                copySuccess = true;
                setTimeout(() => {
                    copySuccess = false;
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        }
    }
</script>

<nav class="navbar">
    <ul>
        <li class="brand-item"><span class="brand">Yo Watch This!</span></li>
        <li><button on:click={() => goto('/received')}>Received</button></li>
        <li><button on:click={() => goto('/sent')}>Sent</button></li>
        <li class="right-section">
            <div class="right-content">
                {#if currentUser}
                    <span class="user-id">ID: {currentUser.id}</span>
                    {/if}
                    <button class="copy-btn" on:click={copyUserId} title="Copy ID">
                        {copySuccess ? '✓' : '📋'}
                    </button>
                <button class="logout-btn" on:click={handleLogout}>Logout</button>
            </div>
        </li>
    </ul>
</nav>
<main class="layout-content">
    <slot />
</main>


<style>
    :global(body) {
        margin: 0;
        font-family: 'Arial', sans-serif;
        background: #f0f2f5;
    }

    /* ======= */
    /* Navbar  */
    /* ======= */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #0077cc;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        z-index: 1000;
        box-sizing: border-box;
    }

    .navbar ul {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 0.5rem;
        list-style: none;
        margin: 0;
        padding: 0;
        width: 100%;
        max-width: 100%;
    }

    .navbar li {
        flex: none;
    }

    .navbar li.brand-item {
        margin-right: 0.5rem;
    }

    .navbar li.right-section {
        margin-left: auto;
    }

    .navbar .right-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .navbar .brand {
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }

    .navbar button {
        display: block;
        width: 100%;
        background-color: #0077cc;
        color: white;
        border: 2px solid white;
        border-radius: 6px;
        padding: 0.5rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        text-align: center;
        transition: all 0.2s ease;
    }

    .navbar button:hover {
        background-color: white;
        color: #0077cc;
        border-color: #0077cc;
    }

    .navbar .user-id {
        color: white;
        font-size: 1rem;
        font-weight: 600;
        font-family: 'Arial', sans-serif;
        white-space: nowrap;
        min-width: 280px;
    }

    .navbar button.copy-btn {
        padding: 0.5rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        min-width: 60px;
        width: 60px;
    }

    .navbar button.copy-btn:hover {
        transform: scale(1.05);
    }

    .navbar button.logout-btn {
        background-color: #dc3545;
        border-color: white;
    }

    .navbar button.logout-btn:hover {
        background-color: white;
        color: #dc3545;
        border-color: #dc3545;
    }

    /* ========== */
    /* Responsive */
    /* ========== */
    @media (max-width: 600px) {
        .navbar ul {
            flex-direction: column;
            gap: 0.5rem;
            align-items: stretch;
        }

        .navbar li.brand-item {
            text-align: center;
        }

        .navbar button {
            width: 100%;
        }
    }
</style>