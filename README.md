# Watchdog 🐶
### Auto-Restart Wrapper for yt-dlp (Debian-Based Systems Only)

Watchdog is a Python wrapper around **yt-dlp** that automatically monitors downloads and restarts them when repeated transient errors occur.

It is designed for **Debian-based Linux systems only** (Debian, Ubuntu, Linux Mint, Pop!_OS, etc.).

---

# What Problem Does This Solve?

When downloading large YouTube playlists or videos, you may encounter:

- `HTTP Error 403: Forbidden`
- `fragment not found`
- Connection resets
- Partial downloads
- Random yt-dlp crashes

Instead of manually restarting downloads, **Watchdog detects repeated errors and automatically restarts yt-dlp safely**.

It keeps your downloads running with minimal supervision.

---

# Features

- Prompts for:
  - YouTube video or playlist URL
  - Download directory
  - Download mode (Video or MP3)
- Automatically installs yt-dlp if missing
- Resumes partial downloads
- Retries failed fragments
- Uses a download archive to prevent re-downloading completed items
- Monitors output in real-time
- Automatically restarts yt-dlp when error thresholds are exceeded
- Clean Ctrl+C shutdown

---

# Debian System Requirements

Watchdog is currently supported **only on Debian-based systems**.

## Install Required Packages

```bash
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg
Package Explanation

python3 – required to run the script

python3-pip – required for installing yt-dlp

ffmpeg – required for audio extraction (mp3 mode)

Installation
Download or Clone
git clone https://github.com/myersar1209/WatchDog.git
cd WatchDog

OR manually download the script and save it as:

watchdog.py
Make it Executable
chmod +x watchdog.py
Running Watchdog

Run:

./watchdog.py

You will be prompted for:

1) YouTube URL

Paste a full YouTube video or playlist URL.

Example:

https://www.youtube.com/playlist?list=XXXXXXXX
2) Download Folder

Enter a folder path where files should be saved.

Examples:

~/Downloads
/home/username/Videos

The folder will be created automatically if it does not exist.

3) Download Mode

You will see:

1) Normal
2) Audio only (mp3)

Enter 1 for full video downloads

Enter 2 to extract MP3 audio only

How It Works Internally

Watchdog:

Launches yt-dlp

Monitors the last 120 lines of output

Counts occurrences of known error patterns

If 10+ matches occur within that window:

Terminates yt-dlp

Waits briefly

Restarts it automatically

Continues until the download completes successfully

Files Created

Inside your download directory:

archive_log.txt

This file stores downloaded video IDs.

It prevents re-downloading completed videos instantly when restarting playlists.

Do not delete this file unless you want to re-download everything.

Customization

At the top of watchdog.py, you can adjust:

WINDOW_LINES = 120
THRESHOLD = 10
COOLDOWN_SECONDS = 15
Meaning

WINDOW_LINES → How many recent output lines to analyze

THRESHOLD → How many error matches trigger a restart

COOLDOWN_SECONDS → Minimum seconds between restarts

You can also modify:

ERROR_PATTERNS

To add or remove error detection patterns.

Stopping Watchdog

Press:

Ctrl + C

Watchdog will safely terminate yt-dlp.

Troubleshooting
yt-dlp command not found

Add pip’s local bin to PATH:

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
MP3 mode fails

Ensure ffmpeg is installed:

sudo apt install -y ffmpeg
Infinite Restarting

If Watchdog keeps restarting:

The error may be persistent (network block or IP rate limiting)

Increase THRESHOLD

Remove or modify error patterns

Consider using cookies or a proxy (advanced usage)

Important Notes

Debian-based systems only

Not tested on Windows or macOS

Does not bypass YouTube bans or permanent 403 blocks

Intended for handling unstable connections and transient failures

Example Full Setup (Quick Start)
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg

git clone https://github.com/myersar1209/WatchDog.git
cd WatchDog
chmod +x watchdog.py

./watchdog.py
License

Add your preferred license here (MIT recommended).

Disclaimer

This project is intended for personal use and educational purposes.
Follow YouTube’s terms of service and local laws.

🐶 Watchdog keeps an eye on your downloads so you don't have to.
