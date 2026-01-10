<script>
    import { goto } from '$app/navigation';
    
    let link = '';
    let user_id = '';
    let error = '';
    
    async function new_reco() {
        const token = localStorage.getItem('access_token');

        if (!token) {
            goto('/login');
            return;
        }

        const res = await fetch('http://localhost:8000/recommendations/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                link: link,
                to_user_id: user_id
            })
        });
    };
</script>

<form on:submit|preventDefault={new_reco}>
    <h1>Recommend a video to your friends</h1>
    <label>
        Video link:
        <input bind:value={link} placeholder="https://youtu.be/dQw4w9WgXcQ"/>
    </label>
    <label>
        Your friend's ID:
        <input bind:value={user_id} placeholder="1"/>
    </label>
    <button type="submit">Recommend</button>
    {#if error}
        <p style="color:red">{error}</p>
    {/if}
</form>

<style>
    /* Container */
    :global(body) {
        margin: 0;
        font-family: 'Arial', sans-serif;
        background: #f0f2f5;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
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
        border-color: #0077cc;
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
    
    p {
        margin-top: 1rem;
        text-align: center;
        color: red;
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