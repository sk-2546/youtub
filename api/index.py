from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional

from ytmusicapi.ytmusic import YTMusic
from ytmusicapi.exceptions import YTMusicUserError, YTMusicServerError

app = FastAPI(title="ytmusicapi-wrapper", version="0.1")

# Create a singleton YTMusic instance. This will use default unauthenticated headers.
# For authenticated endpoints (create/edit playlists, etc.) you'll need to provide
# authentication per the library docs and modify this app to instantiate YTMusic with
# the proper `auth` argument or expose an authenticated session management.
yt = YTMusic()


@app.get("/search")
def search(q: str = Query(..., alias="q"), limit: int = 20, filter: Optional[str] = None):
    """Search YouTube Music.

    Query parameters:
    - q: search query (required)
    - limit: number of results (default 20)
    - filter: optional filter (songs, albums, artists...)
    """
    try:
        results = yt.search(query=q, filter=filter, limit=limit)
        return JSONResponse(content=results)
    except YTMusicUserError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except YTMusicServerError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/playlist/{playlist_id}")
def get_playlist(playlist_id: str, limit: Optional[int] = Query(100), related: bool = False, suggestions_limit: int = 0):
    """Get a playlist by id. Public playlists and many playlists should work unauthenticated.

    - playlist_id: playlist id (without VL prefix)
    - limit: how many tracks to return (None for all; default 100)
    - related: whether to include related playlists
    - suggestions_limit: how many suggestion items to include
    """
    try:
        result = yt.get_playlist(playlistId=playlist_id, limit=limit, related=related, suggestions_limit=suggestions_limit)
        return JSONResponse(content=result)
    except YTMusicUserError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except YTMusicServerError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
