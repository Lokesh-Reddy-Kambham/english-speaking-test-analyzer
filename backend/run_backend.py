import traceback
from pathlib import Path

log_path = Path("backend.run.log")

try:
    with log_path.open("a", encoding="utf-8") as log:
        log.write("Starting backend on http://127.0.0.1:8000\n")
        log.flush()
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level="info", log_config=None)
    with log_path.open("a", encoding="utf-8") as log:
        log.write("Backend stopped without exception.\n")
except Exception:
    with log_path.open("a", encoding="utf-8") as log:
        traceback.print_exc(file=log)
