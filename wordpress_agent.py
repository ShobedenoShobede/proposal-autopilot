import os
import requests
import random

# --- READ FROM GITHUB SECRETS ---
WP_SITE = os.environ.get("WP_URL")
WP_USERNAME = os.environ.get("WP_USERNAME")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD")
APP_URL = os.environ.get("APP_URL", "https://your-app.streamlit.app")

# Clean the site name (strip https:// and trailing slashes)
if WP_SITE:
    WP_SITE = WP_SITE.replace("https://", "").replace("http://", "").strip("/")

# --- CORRECT WORDPRESS.COM ENDPOINT ---
API_URL = f"https://public-api.wordpress.com/wp/v2/sites/{WP_SITE}/posts"

templates = [
    {
        "title": "Why Freelancers Lose 40% of Clients Before the First Meeting",
        "content": f"<p>Cash flow kills more freelancers than lack of skill. The #1 reason? <strong>Slow, unprofessional proposals</strong>.</p><p>I built a free tool that generates a branded PDF proposal and collects a 50% deposit via PayPal in under 2 minutes.</p><p>Try it here: <a href='{APP_URL}'>{APP_URL}</a></p>"
    },
    {
        "title": "How to Automate Invoicing and Double Your Close Rate",
        "content": f"<p>In 2026, clients expect speed. If your proposal takes longer than 5 minutes to send, you've already lost.</p><p>I automated my entire proposal-to-deposit flow: <a href='{APP_URL}'>{APP_URL}</a></p><p>My results: 3x more deposits collected before starting work.</p>"
    },
    {
        "title": "The 50% Deposit Rule That Saved My Business",
        "content": f"<p>Every freelancer knows the pain of net-30 terms. I switched to <strong>50% upfront, 50% on delivery</strong> using this: <a href='{APP_URL}'>{APP_URL}</a></p><p>If you're tired of begging for payments, automate it today.</p>"
    }
]

def publish():
    post = random.choice(templates)
    auth = (WP_USERNAME, WP_APP_PASSWORD)
    payload = {
        "title": post["title"],
        "content": post["content"],
        "status": "publish"
    }
    print(f"POSTing to: {API_URL}")
    print(f"Auth user: {WP_USERNAME}")
    r = requests.post(API_URL, auth=auth, json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:500]}")

if __name__ == "__main__":
    publish()