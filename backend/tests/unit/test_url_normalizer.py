from app.services.recommendation_service import YouTubeNormalizer, PassthroughNormalizer


def test_watch_url():
    n = YouTubeNormalizer()
    assert (
        n.normalize("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        == "https://youtube.com/embed/dQw4w9WgXcQ"
    )


def test_short_url():
    n = YouTubeNormalizer()
    assert (
        n.normalize("https://youtu.be/dQw4w9WgXcQ")
        == "https://youtube.com/embed/dQw4w9WgXcQ"
    )


def test_watch_url_with_playlist():
    n = YouTubeNormalizer()
    result = n.normalize("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=ABC123")
    assert "embed/dQw4w9WgXcQ" in result
    assert "list=ABC123" in result


def test_invalid_url_returns_fallback():
    n = YouTubeNormalizer()
    result = n.normalize("https://vimeo.com/123456")
    assert "dQw4w9WgXcQ" in result


def test_malformed_url_returns_fallback():
    n = YouTubeNormalizer()
    result = n.normalize("not_a_url")
    assert "dQw4w9WgXcQ" in result


def test_passthrough_returns_url_unchanged():
    n = PassthroughNormalizer()
    url = "https://vimeo.com/123456"
    assert n.normalize(url) == url
