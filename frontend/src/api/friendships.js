import client from './client'

export async function getFriends() {
    const { data } = await client.get('/friendships/friends')
    return data
}

export async function getPendingRequests() {
    const { data } = await client.get('/friendships/pending')
    return data
}

export async function sendFriendRequest(addresseeId) {
    const { data } = await client.post('/friendships/request', {
        addressee_id: addresseeId,
    })
    return data
}

export async function respondToRequest(friendshipId, status) {
    const { data } = await client.patch(`/friendships/${friendshipId}/respond`, {
        status,
    })
    return data
}