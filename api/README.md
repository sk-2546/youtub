# Minimal HTTP wrapper for `ytmusicapi`

This folder contains a small FastAPI app that exposes a couple of endpoints which call into the `ytmusicapi` library included in this repo.

Files:
- `index.py` — FastAPI application exposing `/search`, `/playlist/{playlist_id}` and `/health`.

Local run (development):

1. Create a Python environment and install dependencies (from the repository root):

```powershell
python -m pip install -r requirements.txt
```

2. Start the server:

```powershell
python -m uvicorn api.index:app --port 8000 --reload
```

Then open: `http://localhost:8000/search?q=adele` or `http://localhost:8000/playlist/<playlistId>`

Vercel deployment notes:

- Vercel's Python runtime will look for files under the `api/` directory and expose them as serverless endpoints.
- If you deploy this repository to Vercel, the FastAPI app in `api/index.py` will be available under the path `/api/index` on your deployment domain. The endpoints defined in the app are then:
  - `https://<your-deployment>.vercel.app/api/index/search?q=...`
  - `https://<your-deployment>.vercel.app/api/index/playlist/<playlistId>`

Notes & limitations:
- The library is used without authentication in this minimal wrapper. Many write operations (create/edit/delete playlists, library actions, some private playlist reads) require authentication. To support them you must initialize `YTMusic(auth=...)` with valid credentials and secure those credentials in your deployment (environment variables, secrets, or a safe auth flow).
- Rate limits and blocking from Google are possible; use responsibly.
- For production deployment you may want to:
  - Add request validation and better error handling.
  - Add authentication or per-client sessions.
  - Add caching and rate-limiting.
