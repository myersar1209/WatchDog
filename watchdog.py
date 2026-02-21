#!/usr/bin/env python3
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from collections import deque

# ---------------- TUNING ----------------
ERROR_PATTERNS = [
    re.compile(r"HTTP Error 403: Forbidden"),
    re.compile(r"fragment not found"),
]
WINDOW_LINES = 120          # recent lines to keep in memory
THRESHOLD = 10              # restart if >= this many matches in window
COOLDOWN_SECONDS = 15       # minimum time between restarts
# --download-archive creates a text file of finished IDs to skip them INSTANTLY
EXTRA_ARGS = [
    "--continue",
    "--retries", "10",
    "--download-archive", "archive_log.txt",
    "--no-post-overwrites"
]
# ----------------------------------------

def which_ytdlp() -> str | None:
    return shutil.which("yt-dlp")

def ensure_ytdlp() -> None:
    if which_ytdlp():
        return

    print("yt-dlp is NOT installed. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-U", "yt-dlp"])
    except subprocess.CalledProcessError as e:
        print("\nAutomatic install failed. Please install manually.")
        sys.exit(e.returncode)

def prompt_url() -> str:
    while True:
        url = input("Enter YouTube video or playlist URL: ").strip()
        if url.startswith("http"):
            return url
        print("Invalid URL.\n")

def prompt_dir() -> str:
    while True:
        path = input("Enter download folder path: ").strip()
        if not path: continue
        path = os.path.expanduser(path)
        try:
            os.makedirs(path, exist_ok=True)
            return os.path.abspath(path)
        except Exception as e:
            print(f"Path error: {e}\n")

def prompt_mode() -> list[str]:
    print("\nDownload options:\n1) Normal\n2) Audio only (mp3)")
    choice = input("Choose (1 or 2): ").strip()
    if choice == "2":
        return ["-x", "--audio-format", "mp3", "--audio-quality", "0"]
    return []

def build_cmd(url: str, out_dir: str, mode_args: list[str]) -> list[str]:
    output_template = os.path.join(out_dir, "%(title)s.%(ext)s")
    return ["yt-dlp", *mode_args, "-o", output_template, *EXTRA_ARGS, url]

def spawn(cmd: list[str], cwd: str) -> subprocess.Popen:
    print(f"\n[{time.ctime()}] Spawning yt-dlp...")
    return subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
        preexec_fn=None if sys.platform == "win32" else os.setsid,
    )

def should_restart(recent_lines: deque[str]) -> int:
    text = "".join(recent_lines)
    return sum(len(pat.findall(text)) for pat in ERROR_PATTERNS)

def kill_proc(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    try:
        if sys.platform != "win32":
            os.killpg(proc.pid, signal.SIGTERM)
        else:
            proc.terminate()
        time.sleep(1)
    except ProcessLookupError:
        pass

def main() -> None:
    ensure_ytdlp()
    url = prompt_url()
    out_dir = prompt_dir()
    mode_args = prompt_mode()
    cmd = build_cmd(url, out_dir, mode_args)

    recent = deque(maxlen=WINDOW_LINES)
    last_restart = 0.0
    proc = spawn(cmd, cwd=out_dir)

    try:
        while True:
            # Check if process ended
            retcode = proc.poll()
            if retcode is not None:
                if retcode == 0:
                    print(f"\n[{time.ctime()}] Download process completed successfully.")
                    break
                else:
                    print(f"\n[{time.ctime()}] yt-dlp exited with code {retcode}. Restarting...")
                    time.sleep(3)
                    proc = spawn(cmd, cwd=out_dir)
                    recent.clear()
                    continue

            # Read output
            line = proc.stdout.readline() if proc.stdout else ""
            if line:
                print(line, end="")
                recent.append(line)

                hits = should_restart(recent)
                now = time.time()

                if hits >= THRESHOLD and (now - last_restart) >= COOLDOWN_SECONDS:
                    print(f"\n[{time.ctime()}] Error threshold hit ({hits}). Resetting connection...")
                    last_restart = now
                    kill_proc(proc)
                    proc = spawn(cmd, cwd=out_dir)
                    recent.clear()
            else:
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nUser stopped the script.")
        kill_proc(proc)

if __name__ == "__main__":
    main()
