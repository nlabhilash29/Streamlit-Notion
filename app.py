import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Notion API setup
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Streamlit app
st.title("Notion Database Viewer")

# Function to fetch data from Notion
def fetch_notion_data():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()['results']
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

# Fetch and display data
if st.button("Fetch Notion Data"):
    data = fetch_notion_data()
    if data:
        for item in data:
            st.write(item['properties'])  # Adjust this based on your database structure
