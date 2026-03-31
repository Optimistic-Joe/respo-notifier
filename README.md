# 🔔 Respondent.io Task Notifier

A Python script that monitors [Respondent.io](https://app.respondent.io) and sends you an **instant Telegram notification** the moment a new paid research task goes live.

Never miss a high-paying study again! 🚀

---

## 💡 How It Works

1. Logs into your Respondent.io account automatically
2. Checks for new available projects every 60 seconds
3. The moment a new task appears — you get a Telegram message instantly
4. Includes the task title, pay, duration, and a direct apply link

---

## 📬 Example Notification

```
🚨 New Respondent.io Task!

📋 Title: UX Research Study
💰 Pay: $75
⏱ Duration: 60 minutes
🔗 Apply Now → https://app.respondent.io/...
```

---

## 🛠 Setup Instructions

### 1. Clone this repo
```bash
git clone https://github.com/YOUR_USERNAME/respondent-notifier.git
cd respondent-notifier
```

### 2. Install dependencies
```bash
pip install requests python-dotenv
```

### 3. Create your `.env` file
Copy the example file and fill in your credentials:
```bash
cp .env.example .env
```

Then open `.env` and fill in:
```
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
RESPONDENT_EMAIL=your_email_here
RESPONDENT_PASSWORD=your_password_here
```

> 🔒 **Your `.env` file is listed in `.gitignore` — it will NEVER be uploaded to GitHub.**

### 4. Get Your Telegram Credentials
- **Bot Token** → Open Telegram, search `@BotFather`, type `/newbot` and follow the steps
- **Chat ID** → Search `@userinfobot` on Telegram and click Start

### 5. Run the script
```bash
python respondent_notifier.py
```

You'll receive a Telegram message confirming it's running. ✅

---

## ☁️ Running 24/7 (Without Your PC)

To keep this running even when your computer is off, you can deploy it to:
- **GitHub Codespaces** (free 60hrs/month)
- **Replit** + UptimeRobot (free, always on)

---

## 📦 Requirements

- Python 3.7+
- A free Telegram account
- A Respondent.io participant account

---

## ⚠️ Disclaimer

This tool is for personal use only. Use responsibly and in accordance with Respondent.io's terms of service.
