import client from './client'

export async function getSent() {
  const { data } = await client.get('/recommendations/sent')
  return data
}

export async function getReceived() {
  const { data } = await client.get('/recommendations/received')
  return data
}

export async function sendReco(link, description, toUserId) {
  const { data } = await client.post('/recommendations/send', {
    link,
    description,
    to_user_id: toUserId,
  })
  return data
}

export async function rateReco(recoId, rating) {
  const { data } = await client.patch(`/recommendations/${recoId}/rating`, {
    rating,
  })
  return data
}

export async function answerReco(recoId, answer) {
  const { data } = await client.patch(`/recommendations/${recoId}/answer`, {
    answer,
  })
  return data
}
