from urllib.parse import urlparse, parse_qs, urlencode


def normalize_youtube_link(url: str) -> str:
    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        video_id = None

        # youtu.be/<id>
        if parsed.hostname == "youtu.be":
            video_id = parsed.path[1:]  # remove "/"

        # youtube.com/watch?v=<id>
        elif "youtube.com" in parsed.hostname and parsed.path == "/watch":
            video_id = query_params.get("v", [None])[0]

        if not video_id:
            return "https://youtube.com/embed/dQw4w9WgXcQ?list=RDdQw4w9WgXcQ"

        # Keep the parameters (playlist, t, etc.)
        # unless "v" that has already been used
        query_params.pop("v", None)
        new_query = f"?{urlencode(query_params, doseq=True)}" if query_params else ""

        return f"https://youtube.com/embed/{video_id}{new_query}"

    except Exception:
        return "https://youtube.com/embed/dQw4w9WgXcQ?list=RDdQw4w9WgXcQ"
