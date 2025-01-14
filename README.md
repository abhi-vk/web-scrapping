Twitter Trends Scraper

This project implements a Twitter trends scraper using Selenium, Flask, and MongoDB. The Flask app allows users to run a script that fetches trending topics from Twitter, stores them in MongoDB, and displays them on a web page.

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Chrome browser (and ChromeDriver)
- MongoDB (local or MongoDB Atlas)

### Steps to Get Started

1. **Install Python dependencies**:
   ```bash
   pip install selenium flask pymongo
   ```

2. **Download ChromeDriver**:
   - Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads) and download the correct version based on your Chrome version.
   - Place ChromeDriver in the project folder or add it to your system's PATH.

3. **Set up MongoDB**:
   - Use a local MongoDB instance or create a free cluster on [MongoDB Atlas](https://www.mongodb.com/atlas).

4. **Configure Proxy** (optional):
   - Sign up for a proxy service at [ProxyMesh](https://proxymesh.com/) and obtain your proxy URL and credentials.

---

## Folder Structure

```
tech_internship_task/
│
├── app.py              # Flask application
├── selenium_script.py  # Selenium script for scraping Twitter trends
├── requirements.txt    # List of dependencies
├── templates/
│   └── index.html      # HTML template for displaying results
├── config/
│   ├── db_config.py    # MongoDB configuration
│   └── proxy_config.py # Proxy configuration (if using ProxyMesh)
```

---

## How to Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask app**:
   ```bash
   python app.py
   ```

3. Open the web app in your browser: [http://127.0.0.1:5000](http://127.0.0.1:5000).

4. Click the "Run Script" button to execute the Selenium script and display the results.

---

## Troubleshooting

- Ensure your `ChromeDriver` is compatible with your Chrome version.
- Verify that MongoDB is running and accessible.
- Double-check the ProxyMesh configuration if you are using a proxy.
- If the page doesn't load, try clearing your browser's cache or restarting the Flask app.


```
