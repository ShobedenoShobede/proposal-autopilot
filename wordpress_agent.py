import os
import requests
import random
import datetime
import sys

# Read credentials from environment (set these as GitHub Secrets)
WP_URL = os.getenv("WP_URL")           # e.g., https://your-site.com
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
APP_URL = os.getenv("APP_URL", "https://proposal-autopilot-wjdcknhjrbchzcy8ydztas.streamlit.app/")

if not all([WP_URL, WP_USERNAME, WP_APP_PASSWORD]):
    print("❌ Missing required environment variables: WP_URL, WP_USERNAME, WP_APP_PASSWORD")
    sys.exit(1)

templates = [
    {
        "title": "Why Freelancers Lose 40% of Clients Before the First Meeting",
        "content": f"""<p>Cash flow kills more freelancers than lack of skill. The #1 reason? <strong>Slow, unprofessional proposals</strong>.</p>
<p>I built a free tool that generates a branded PDF proposal and collects a 50% deposit via PayPal in under 2 minutes. No more chasing invoices.</p>
<p>Try it here: <a href="{APP_URL}">{APP_URL}</a></p>
<p>Stop negotiating payment terms <em>after</em> the work. Get paid upfront, every time.</p>"""
    },
    {
        "title": "How to Automate Invoicing and Double Your Close Rate",
        "content": f"""<p>In 2026, clients expect speed. If your proposal takes longer than 5 minutes to send, you've already lost.</p>
<p>I automated my entire proposal-to-deposit flow using a simple web app: <a href="{APP_URL}">{APP_URL}</a></p>
<p>It handles scope, pricing, timeline, and the deposit button – all in one shareable link.</p>
<p>My results: 3x more deposits collected before starting work.</p>"""
    },
    {
        "title": "The 50% Deposit Rule That Saved My Business",
        "content": f"""<p>Every freelancer knows the pain of net-30 terms. I switched to <strong>50% upfront, 50% on delivery</strong> using this: <a href="{APP_URL}">{APP_URL}</a></p>
<p>It sends a professional PDF with a built-in PayPal deposit button. My clients actually <em>prefer</em> the clarity.</p>
<p>If you're tired of begging for payments, automate it today.</p>"""
    }
]


def publish_to_wp():
    post = random.choice(templates)
    api_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
    auth = (WP_USERNAME, WP_APP_PASSWORD)

    payload = {
        "title": post["title"],
        "content": post["content"],
        "status": "publish",
        "tags": "freelance, proposals, invoicing, automation",
        "categories": [1]
    }

    try:
        response = requests.post(api_url, auth=auth, json=payload, timeout=30)
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

    if response.status_code in (200, 201):
        link = response.json().get("link")
        print(f"✅ Article published successfully: {link}")
        return True
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
        return False


if __name__ == "__main__":
    success = publish_to_wp()
    if not success:
        sys.exit(1)
