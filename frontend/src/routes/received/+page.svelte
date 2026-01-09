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

        try {
            const res = await fetch('http://localhost:8000/recommendations/received', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!res.ok) {
                console.error("Failed to fetch:", res.status);
                goto('/login');
                return;
            }

            recommendations = await res.json();
        } catch (err) {
            console.error(err);
            goto('/login');
            return;
        } finally {
            loading = false; 
        }
    });
</script>

{#if loading}
    <p>Loading…</p>
{:else}
    <h1>Recommended to me</h1>

    {#if recommendations.length === 0}
        <p>No recommendations yet</p>
    {:else}
        <ul>
            {#each recommendations as r}
                <li><iframe title="" width="420" height="315" src={r.link}></iframe></li> 
            {/each}
        </ul>
    {/if}
{/if}
