# Reddit Keyword Sentiment Tracker 

A **Flask web application** that analyzes the sentiment of a keyword on Reddit’s r/nba subreddit.  
It fetches the top 30 hot posts and all their comments, counts how often your keyword appears and shows how many mentions are positive or negative. Results are displayed as a clear chart for visualization.

All required Python packages are specified in the included `requirements.txt` file. Simply install them with `pip install -r requirements.txt`.

---
## ✅ User Stories

The following **required** functionality is implemented:

- ✅ User can **enter a keyword and subreddit** into the input fields on the homepage  
- ✅ User can **submit the form** to trigger a sentiment analysis using Reddit's top 30 hot posts  
- ✅ The app fetches **comments from all posts**, filters them for keyword mentions, and classifies sentiment as positive or negative  
- ✅ Results display a **count of total, positive, and negative mentions** along with example words  
- ✅ User sees a **bar chart visualization** that distinguishes sentiment categories  
- ✅ The app provides a clean **dark-themed UI** featuring NBA imagery and branding  
- ✅ Includes a **"Analyze another keyword"** button to restart the flow  


## Optional Features

- ✅ Keyword sentiment is based on **custom positive and negative slang dictionaries**  
- ✅ Sentiment scoring uses **simple NLP logic** with manually curated vocabulary  
- ✅ Default subreddit is **pre-filled as "nba"** but can be changed manually  
- ✅ Supports **real-time chart rendering** using `matplotlib` and `base64` encoding  
- ✅ Displays **loading notice** when processing large amounts of comments  


## Additional Features

- ✅ Custom UI built with **Flask templates** and static assets  
- ✅ **Matplotlib charts** rendered on the server and embedded into HTML  
- ✅ NBA-themed styling with image backgrounds and branding consistency  
- ✅ Clear modular separation between logic, templates, and configuration  
- ✅ Environment variables (`.env`) used to protect Reddit API credentials  

---

## Screenshots of my project 

### Home Page Screenshot 
![Home Page](screenshots/home_page.JPG)

### Results Page Screenshot
![Results Page](screenshots/results_page.JPG)

---

## How to Run

**Clone this repo**

```bash
git clone https://github.com/YOUR_USERNAME/reddit-sentiment-tracker.git
cd reddit-sentiment-tracker
