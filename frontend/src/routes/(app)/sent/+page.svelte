<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let recommendations = [];
    let loading = true;

    onMount(async () => {
        const token = localStorage.getItem('access_token');

        if (!token) {
            goto('/login');
            return;
        }

        const res = await fetch('http://localhost:8000/recommendations/sent', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!res.ok) {
            goto('/login');
            return;
        }

        recommendations = await res.json();
        loading = false;
    });
</script>


<div class="page-container">
    <h1>Recommended by me</h1>
    {#if loading}
        <p>Loading…</p>
    {:else}
        {#if recommendations.length === 0}
            <p>No recommendations yet</p>
        {:else}
            <ul class="reco-list">
                {#each recommendations as r}
                    <li class="reco-item">
                        <p>You recommended to {r.to_user}</p>
                        <iframe title="Video" src={r.link}></iframe>
                    </li>
                {/each}
            </ul>
        {/if}
    {/if}
</div>


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

    .navbar button.logout-btn {
        background-color: #dc3545;
        border-color: white;
    }

    .navbar button.logout-btn:hover {
        background-color: white;
        color: #dc3545;
        border-color: #dc3545;
    }

    /* ============== */
    /* Page container */
    /* ============== */
    .page-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 6rem 1rem 2rem; 
        max-width: 1200px;
        margin: 0 auto;
    }

    h1 {
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
    }

    p {
        text-align: center;
        color: #555;
        font-size: 1rem;
    }

    ul.reco-list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2rem;
    }

    li.reco-item {
        background: #fff;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 420px;
        transition: transform 0.2s ease;
    }

    li.reco-item:hover {
        transform: translateY(-5px);
    }

    li.reco-item p {
        margin-bottom: 0.5rem;
        font-weight: 600;
        color: #444;
    }

    iframe {
        width: 100%;
        aspect-ratio: 16/9;
        border: none;
        border-radius: 8px;
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

        ul.reco-list {
            gap: 1rem;
        }

        li.reco-item {
            padding: 0.5rem;
        }

        li.reco-item p {
            font-size: 0.9rem;
        }
    }
</style>