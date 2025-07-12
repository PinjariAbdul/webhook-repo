# webhook-repo
# Webhook Receiver App

This is a Flask-based webhook receiver built for the Developer Internship Assessment. It listens for GitHub webhook events (`push`, `pull_request`, and `merge`) and stores them in a MongoDB database. The frontend UI displays the latest GitHub events in real-time, polling the backend every 15 seconds.

---

## 📌 Features

- ✅ Receives GitHub webhook events
- ✅ Handles Push, Pull Request, and Merge events
- ✅ Stores event data in MongoDB Atlas
- ✅ Minimal UI that polls every 15 seconds for updates
- ✅ Clean display of real-time GitHub activity

---

## 📦 Tech Stack

- **Flask** – Web framework for webhook endpoint and backend
- **MongoDB Atlas** – NoSQL database to store events
- **HTML + JS** – Frontend to display data
- **Ngrok** – Used for local testing of GitHub webhook delivery (optional)

---

## 📁 Folder Structure
webhook-repo/
├── app.py # Main Flask app
├── requirements.txt # Python dependencies
├── templates/
│ └── index.html # Frontend UI

