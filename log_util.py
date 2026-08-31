# log_util.py
# Homemade logger for the nightly fleet run.
# Written 2013. Modernized 2024.

import time

LOG_LINES: list[str] = []   # in-memory buffer, flushed to disk by flush_log()
DEBUG = False


def log(message: str) -> None:
    """Append a timestamped line to the in-memory buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a DEBUG-level message (only when DEBUG is True)."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Write all buffered log lines to the given file and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
