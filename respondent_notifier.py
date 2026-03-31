import requests
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load your secret credentials from the .env file
load_dotenv()

# ============================================================
#  These are read from your .env file — no secrets in here!
# ============================================================
TELEGRAM_BOT_TOKEN  = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID    = os.getenv("TELEGRAM_CHAT_ID")
RESPONDENT_EMAIL    = os.getenv("RESPONDENT_EMAIL")
RESPONDENT_PASSWORD = os.getenv("RESPONDENT_PASSWORD")

CHECK_INTERVAL = 60  # Check every 60 seconds
# ============================================================

SEEN_PROJECTS_FILE = "seen_projects.json"
LOGIN_URL          = "https://app.respondent.io/api/v2/auth/login"
PROJECTS_URL       = "https://app.respondent.io/api/v2/respondents/projects/browse"
PROJECT_BASE_URL   = "https://app.respondent.io/respondents/v2/projects"

session = requests.Session()


def load_seen_projects():
    """Load the list of projects we've already seen."""
    if os.path.exists(SEEN_PROJECTS_FILE):
        with open(SEEN_PROJECTS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen_projects(seen):
    """Save the list of projects we've already seen."""
    with open(SEEN_PROJECTS_FILE, "w") as f:
        json.dump(list(seen), f)


def send_telegram(message):
    """Send a message to your Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"[{now()}] ✅ Telegram alert sent.")
    except Exception as e:
        print(f"[{now()}] ❌ Telegram error: {e}")


def now():
    """Return the current time as a readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def login():
    """Log in to Respondent.io."""
    payload = {"email": RESPONDENT_EMAIL, "password": RESPONDENT_PASSWORD}
    try:
        resp = session.post(LOGIN_URL, json=payload, timeout=15)
        resp.raise_for_status()
        print(f"[{now()}] ✅ Logged in to Respondent.io")
        return True
    except Exception as e:
        print(f"[{now()}] ❌ Login failed: {e}")
        return False


def fetch_projects():
    """Fetch the current list of available projects."""
    try:
        resp = session.get(PROJECTS_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        projects = data.get("projects") or data.get("data") or data.get("results") or []
        return projects
    except Exception as e:
        print(f"[{now()}] ❌ Failed to fetch projects: {e}")
        return []


def check_new_projects(seen):
    """Compare fetched projects against ones we've already seen."""
    projects = fetch_projects()
    new_projects = []

    for project in projects:
        pid = str(project.get("id") or project.get("_id") or "")
        if not pid:
            continue
        if pid not in seen:
            seen.add(pid)
            new_projects.append(project)

    return new_projects, seen


def format_alert(project):
    """Format a nice Telegram message for a new project."""
    title     = project.get("title") or project.get("name") or "New Project"
    incentive = project.get("incentive") or project.get("compensation") or "N/A"
    duration  = project.get("duration") or project.get("length") or "N/A"
    pid       = project.get("id") or project.get("_id") or ""
    link      = f"{PROJECT_BASE_URL}/{pid}" if pid else PROJECT_BASE_URL

    return (
        f"🚨 *New Respondent.io Task!*\n\n"
        f"📋 *Title:* {title}\n"
        f"💰 *Pay:* {incentive}\n"
        f"⏱ *Duration:* {duration}\n"
        f"🔗 [Apply Now]({link})"
    )


def check_credentials():
    """Make sure all credentials are present before starting."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")
    if not RESPONDENT_EMAIL:
        missing.append("RESPONDENT_EMAIL")
    if not RESPONDENT_PASSWORD:
        missing.append("RESPONDENT_PASSWORD")

    if missing:
        print(f"❌ Missing credentials in your .env file: {', '.join(missing)}")
        print("👉 Please fill in your .env file and try again.")
        return False
    return True


def main():
    print("=" * 50)
    print("  Respondent.io Notifier")
    print("=" * 50)

    # Check credentials first
    if not check_credentials():
        return

    print(f"[{now()}] 🚀 Notifier started! Checking every {CHECK_INTERVAL} seconds...")
    send_telegram("🤖 *Respondent Notifier is now running!*\nYou'll be alerted the moment a new task goes live. ✅")

    # Log in to Respondent.io
    if not login():
        send_telegram("❌ Login to Respondent.io failed.\nDouble-check your email and password in the .env file.")
        return

    seen = load_seen_projects()

    # First run: save existing projects so we don't alert on old ones
    if not seen:
        print(f"[{now()}] 🌱 First run — saving existing projects (you won't be alerted for these)...")
        projects = fetch_projects()
        for p in projects:
            pid = str(p.get("id") or p.get("_id") or "")
            if pid:
                seen.add(pid)
        save_seen_projects(seen)
        print(f"[{now()}] ✅ Found {len(seen)} existing projects. Now watching for NEW ones only...")

    # Main loop — runs forever
    while True:
        try:
            new_projects, seen = check_new_projects(seen)

            if new_projects:
                save_seen_projects(seen)
                for project in new_projects:
                    alert = format_alert(project)
                    send_telegram(alert)
                    print(f"[{now()}] 🔔 New project: {project.get('title', 'Unknown')}")
            else:
                print(f"[{now()}] 🔍 No new projects. Checking again in {CHECK_INTERVAL}s...")

        except Exception as e:
            print(f"[{now()}] ⚠️ Something went wrong: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
