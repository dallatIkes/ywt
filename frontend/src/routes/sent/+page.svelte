<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let recommendations = [];
    let loading = true; // on ne rend rien tant que ce n’est pas vérifié

    onMount(async () => {
        const token = localStorage.getItem('access_token');

        if (!token) {
            goto('/login'); // redirection immédiate
            return;
        }

        try {
            const res = await fetch('http://localhost:8000/recommendations/sent', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!res.ok) {
                console.error("Failed to fetch:", res.status);
                goto('/login'); // si le token est invalide
                return;
            }

            recommendations = await res.json();
        } catch (err) {
            console.error(err);
            goto('/login'); // en cas d’erreur réseau
            return;
        } finally {
            loading = false; // fin du chargement
        }
    });
</script>

{#if loading}
    <p>Loading…</p> <!-- ou rien du tout -->
{:else}
    <h1>Recommended by me</h1>

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
