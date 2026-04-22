// ── Strategy interface (duck typing) ─────────────────────────────────────────
// Each strategy must implement:
//   matches(url: string) -> boolean
//   buildEmbedUrl(url: string) -> string | null
//   platform: string

class YouTubeStrategy {
    platform = 'youtube'

    matches(url) {
        try {
            const { hostname } = new URL(url)
            return hostname === 'youtu.be' || hostname.includes('youtube.com')
        } catch { return false }
    }

    buildEmbedUrl(url) {
        try {
            const parsed = new URL(url)
            const videoId = parsed.hostname === 'youtu.be'
                ? parsed.pathname.slice(1)
                : parsed.searchParams.get('v')
            return videoId ? `https://www.youtube.com/embed/${videoId}` : null
        } catch { return null }
    }
}

class VimeoStrategy {
    platform = 'vimeo'

    matches(url) {
        try {
            return new URL(url).hostname.includes('vimeo.com')
        } catch { return false }
    }

    buildEmbedUrl(url) {
        try {
            const videoId = new URL(url).pathname.slice(1)
            return videoId ? `https://player.vimeo.com/video/${videoId}` : null
        } catch { return null }
    }
}

class DailymotionStrategy {
    platform = 'dailymotion'

    matches(url) {
        try {
            const hostname = new URL(url).hostname
            return hostname.includes('dailymotion.com') || hostname.includes('dai.ly')
        } catch {
            return false
        }
    }

    buildEmbedUrl(url) {
        try {
            const parsed = new URL(url)
            let videoId = null

            if (parsed.hostname.includes('dailymotion.com')) {
                // ex: /video/xa5zx1e
                videoId = parsed.pathname.split('/').pop()
            } else if (parsed.hostname.includes('dai.ly')) {
                // ex: /xa5zx1e
                videoId = parsed.pathname.replace('/', '')
            }

            return videoId
                ? `https://www.dailymotion.com/embed/video/${videoId}?autostart=0&mute=0&controls=1`
                : null

        } catch {
            return null
        }
    }
}

class SpotifyStrategy {
    platform = 'spotify'

    matches(url) {
        try {
            return new URL(url).hostname.includes('spotify.com')
        } catch {
            return false
        }
    }

    buildEmbedUrl(url) {
        try {
            const parsed = new URL(url)
            const pathParts = parsed.pathname.split('/').filter(Boolean)

            // ex: /track/{id}
            if (pathParts.length < 2) return null

            const type = pathParts[0]   // track, album, playlist, etc.
            const id = pathParts[1]

            return `https://open.spotify.com/embed/${type}/${id}?utm_source=generator`
        } catch {
            return null
        }
    }
}

class FallbackStrategy {
    platform = 'other'

    matches(url) {
        try { new URL(url); return true } catch { return false }
    }

    buildEmbedUrl() {
        // No embed possible — caller handles this case
        return null
    }
}

// ── Factory ───────────────────────────────────────────────────────────────────
// To add a new platform: instantiate its strategy and add it to the dict.
// Nothing else changes.

const STRATEGIES = {
    youtube: new YouTubeStrategy(),
    vimeo: new VimeoStrategy(),
    dailymotion: new DailymotionStrategy(),
    spotify: new SpotifyStrategy(),
    other: new FallbackStrategy(),
}

export function getMediaStrategy(url) {
    for (const strategy of Object.values(STRATEGIES)) {
        if (strategy.platform === 'other') continue  // fallback checked last
        if (strategy.matches(url)) return strategy
    }
    return STRATEGIES.other
}

export { STRATEGIES }