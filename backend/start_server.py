"""
Start the FastAPI app with an explicit Windows selector event loop policy set
before Uvicorn creates any event loop. Use this script instead of calling
`uvicorn main:app` on Windows to avoid NotImplementedError from asyncio.create_subprocess_exec
when Playwright attempts to spawn browser subprocesses.
"""
import sys
import asyncio

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

import uvicorn

if __name__ == "__main__":
    # Start uvicorn WITHOUT the auto-reloader so the event loop policy set above
    # is applied in the actual server process that will run Playwright.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
