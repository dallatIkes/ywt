from abc import ABC, abstractmethod
from urllib.parse import urlparse, parse_qs, urlencode

# ── Strategy interface ────────────────────────────────────────────────────────


class VideoLinkNormalizer(ABC):
    """Strategy interface — all normalizers must implement these two methods."""

    @abstractmethod
    def matches(self, url: str) -> bool:
        """Returns True if this strategy handles the given URL."""
        ...

    @abstractmethod
    def normalize(self, url: str) -> str:
        """Returns a normalized embeddable URL."""
        ...


# ── Concrete strategies ───────────────────────────────────────────────────────


class YouTubeNormalizer(VideoLinkNormalizer):
    """Handles youtube.com and youtu.be URLs."""

    def matches(self, url: str) -> bool:
        try:
            hostname = urlparse(url).hostname or ""
            return hostname == "youtu.be" or "youtube.com" in hostname
        except Exception:
            return False

    def normalize(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            video_id = None

            if parsed.hostname == "youtu.be":
                video_id = parsed.path[1:]
            elif parsed.hostname and "youtube.com" in parsed.hostname:
                video_id = params.get("v", [None])[0]

            if not video_id:
                return self._fallback()

            # Keep extra params (playlist, timestamp) but drop v=
            params.pop("v", None)
            query = f"?{urlencode(params, doseq=True)}" if params else ""
            return f"https://youtube.com/embed/{video_id}{query}"

        except Exception:
            return self._fallback()

    def _fallback(self) -> str:
        return "https://youtube.com/embed/dQw4w9WgXcQ"


class VimeoNormalizer(VideoLinkNormalizer):
    """Handles vimeo.com URLs."""

    def matches(self, url: str) -> bool:
        try:
            return "vimeo.com" in (urlparse(url).hostname or "")
        except Exception:
            return False

    def normalize(self, url: str) -> str:
        try:
            path = urlparse(url).path
            # vimeo.com/123456789 → player.vimeo.com/video/123456789
            video_id = path.strip("/").split("/")[0]
            if not video_id.isdigit():
                return url
            return f"https://player.vimeo.com/video/{video_id}"
        except Exception:
            return url


class DailymotionNormalizer(VideoLinkNormalizer):
    """Handles dailymotion.com and dai.ly (short) URLs."""

    def matches(self, url: str) -> bool:
        try:
            hostname = urlparse(url).hostname or ""
            return "dailymotion.com" in hostname or "dai.ly" in hostname
        except Exception:
            return False

    def normalize(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            video_id = None

            if "dailymotion.com" in hostname:
                # ex: dailymotion.com/video/xa5zx1e
                video_id = parsed.path.split("/")[-1]
            elif "dai.ly" in hostname:
                # ex: dai.ly/xa5zx1e
                video_id = parsed.path.replace("/", "")

            if not video_id:
                return url

            return f"https://www.dailymotion.com/embed/video/{video_id}?autostart=0&mute=0&controls=1"
        except Exception:
            return url


class SpotifyNormalizer(VideoLinkNormalizer):
    """Handles open.spotify.com URLs."""

    def matches(self, url: str) -> bool:
        try:
            return "open.spotify.com" in (urlparse(url).hostname or "")
        except Exception:
            return False

    def normalize(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) < 2:
                return url
            media_type, media_id = path_parts[0], path_parts[1]
            return f"https://open.spotify.com/embed/{media_type}/{media_id}?utm_source=generator"
        except Exception:
            return url


class SoundCloudNormalizer(VideoLinkNormalizer):
    """Handles soundcloud.com URLs."""

    def matches(self, url: str) -> bool:
        try:
            return "soundcloud.com" in (urlparse(url).hostname or "")
        except Exception:
            return False

    def normalize(self, url: str) -> str:
        try:
            from urllib.parse import quote

            encoded = quote(url, safe="")
            return (
                f"https://w.soundcloud.com/player/?url={encoded}"
                f"&color=%23ff5500&auto_play=false&hide_related=false"
                f"&show_comments=true&show_user=true&show_reposts=false"
                f"&show_teaser=true&visual=true"
            )
        except Exception:
            return url


class PassthroughNormalizer(VideoLinkNormalizer):
    """Fallback — returns the URL as-is for unsupported platforms."""

    def matches(self, url: str) -> bool:
        # Always matches — used as fallback
        return True

    def normalize(self, url: str) -> str:
        return url


# ── Factory ───────────────────────────────────────────────────────────────────
# To add a new platform: instantiate its strategy and add it to the dict.
# normalize_link() picks it up automatically — nothing else changes.

NORMALIZERS: dict[str, VideoLinkNormalizer] = {
    "youtube": YouTubeNormalizer(),
    "vimeo": VimeoNormalizer(),
    "dailymotion": DailymotionNormalizer(),
    "spotify": SpotifyNormalizer(),
    "soundcloud": SoundCloudNormalizer(),
    "passthrough": PassthroughNormalizer(),
}


def normalize_link(url: str) -> str:
    """Factory function — finds the first matching strategy and normalizes."""
    for name, normalizer in NORMALIZERS.items():
        if name == "passthrough":
            continue  # checked last
        if normalizer.matches(url):
            return normalizer.normalize(url)
    return NORMALIZERS["passthrough"].normalize(url)
