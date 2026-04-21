from app.utils.url import (
    normalize_link,
    YouTubeNormalizer,
    VimeoNormalizer,
    DailymotionNormalizer,
    PassthroughNormalizer,
    NORMALIZERS,
)

# ── YouTubeNormalizer ─────────────────────────────────────────────────────────


def test_youtube_watch_url():
    n = YouTubeNormalizer()
    assert (
        n.normalize("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        == "https://youtube.com/embed/dQw4w9WgXcQ"
    )


def test_youtube_short_url():
    n = YouTubeNormalizer()
    assert (
        n.normalize("https://youtu.be/dQw4w9WgXcQ")
        == "https://youtube.com/embed/dQw4w9WgXcQ"
    )


def test_youtube_with_playlist():
    n = YouTubeNormalizer()
    result = n.normalize("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=ABC123")
    assert "embed/dQw4w9WgXcQ" in result
    assert "list=ABC123" in result


def test_youtube_invalid_returns_fallback():
    n = YouTubeNormalizer()
    assert "dQw4w9WgXcQ" in n.normalize("https://youtube.com/watch")


def test_youtube_matches():
    n = YouTubeNormalizer()
    assert n.matches("https://youtu.be/abc") is True
    assert n.matches("https://www.youtube.com/watch?v=abc") is True
    assert n.matches("https://vimeo.com/123") is False


# ── VimeoNormalizer ───────────────────────────────────────────────────────────


def test_vimeo_normalize():
    n = VimeoNormalizer()
    assert (
        n.normalize("https://vimeo.com/123456789")
        == "https://player.vimeo.com/video/123456789"
    )


def test_vimeo_matches():
    n = VimeoNormalizer()
    assert n.matches("https://vimeo.com/123456789") is True
    assert n.matches("https://youtube.com/watch?v=abc") is False


# ── DailymotionNormalizer ─────────────────────────────────────────────────────


def test_dailymotion_normalize():
    n = DailymotionNormalizer()
    assert (
        n.normalize("https://www.dailymotion.com/video/x9abc12")
        == "https://www.dailymotion.com/embed/video/x9abc12"
    )


def test_dailymotion_matches():
    n = DailymotionNormalizer()
    assert n.matches("https://www.dailymotion.com/video/x9abc12") is True
    assert n.matches("https://youtube.com/watch?v=abc") is False


# ── PassthroughNormalizer ─────────────────────────────────────────────────────


def test_passthrough_returns_url_unchanged():
    n = PassthroughNormalizer()
    url = "https://unknown-platform.com/video/123"
    assert n.normalize(url) == url


def test_passthrough_always_matches():
    n = PassthroughNormalizer()
    assert n.matches("https://anything.com") is True


# ── normalize_link factory ────────────────────────────────────────────────────


def test_factory_routes_youtube():
    assert "youtube.com/embed" in normalize_link("https://youtu.be/dQw4w9WgXcQ")


def test_factory_routes_vimeo():
    assert "player.vimeo.com" in normalize_link("https://vimeo.com/123456789")


def test_factory_routes_dailymotion():
    assert "dailymotion.com/embed" in normalize_link(
        "https://www.dailymotion.com/video/x9abc12"
    )


def test_factory_passthrough_unknown():
    url = "https://unknown.com/video/123"
    assert normalize_link(url) == url


def test_all_normalizers_registered():
    # Ensures new platforms don't get forgotten in NORMALIZERS
    assert "youtube" in NORMALIZERS
    assert "vimeo" in NORMALIZERS
    assert "dailymotion" in NORMALIZERS
    assert "passthrough" in NORMALIZERS
