import webbrowser
import uvicorn
import time
import threading

from backend import web
from backend.core.constants import *


def open_browser() -> None:
    time.sleep(1)
    webbrowser.open(APP_URL)


def main() -> None:
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "backend.web:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=True
    )

if __name__ == "__main__":
    main()