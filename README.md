Overview

This repository contains a Streamlit web application (app.py) that visualizes and monitors system data in an interactive dashboard.
It’s built for clarity, professional aesthetics, and real-time performance tracking.

🚀 Run Locally

Create a virtual environment

python -m venv .venv
.venv\Scripts\activate    # on Windows
source .venv/bin/activate # on macOS/Linux


Install dependencies

pip install -r requirements.txt


Run Streamlit

streamlit run app.py


Open your browser and visit → http://localhost:8501

☁️ Deploy to Render (via GitHub)

Push your repo to GitHub with the following files:

app.py
requirements.txt
.streamlit/config.toml


(Optional but recommended: include a Dockerfile if you want reproducible builds.)

Go to Render.com
 → New → Web Service

Environment: Python

Build Command:

pip install -r requirements.txt


Start Command:

streamlit run app.py --server.port $PORT --server.address 0.0.0.0


Plan: Free (for testing)

Click Create Web Service → wait for build → open the live URL 🎉

⚙️ Example .streamlit/config.toml
[server]
headless = true
enableCORS = false
port = 8501
enableXsrfProtection = false
