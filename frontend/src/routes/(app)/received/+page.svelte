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

        const res = await fetch('http://localhost:8000/recommendations/received', {
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
    <h1>Recommended to me</h1>

    {#if loading}
        <p>Loading…</p>
    {:else if recommendations.length === 0}
        <p>No recommendations yet</p>
    {:else}
        <ul class="reco-list">
            {#each recommendations as r}
                <li class="reco-item">
                    <p>Recommended to you by {r.from_user}</p>
                    <iframe title="Video" src={r.link}></iframe>
                </li>
            {/each}
        </ul>
    {/if}
</div>


<style>
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