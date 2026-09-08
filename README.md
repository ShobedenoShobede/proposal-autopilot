# Proposal Autopilot

Minimal Streamlit app that generates a PDF proposal and a PayPal deposit button.

Quick start (locally)
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io and sign in with your GitHub account.
2. Click "New app".
3. For "Repository owner" choose `ShobedenoShobede` and for "Repository" choose `proposal-autopilot`.
4. Choose the branch (the default branch) and set the "Main file path" to `streamlit_app.py`.
5. Click "Deploy". Streamlit Cloud will install dependencies from `requirements.txt` and launch the app.

Notes
- The app includes a hardcoded PayPal email:
  `omni.growth.venture@gmail.com`. Replace PAYPAL_EMAIL in `streamlit_app.py` with your own email before deploying if you want payments to go to a different account.
- If you want a custom return/thank-you page after payment, update the `return` URL in the PayPal form inside `streamlit_app.py`.
- To update the app, push commits to the selected branch — Streamlit Cloud will rebuild and redeploy automatically.
