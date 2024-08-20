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
    if not NOTION_TOKEN:
        st.error("NOTION_TOKEN is not set. Please check your environment variables.")
        return None
    if not DATABASE_ID:
        st.error("NOTION_DATABASE_ID is not set. Please check your environment variables.")
        return None

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()['results']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from Notion: {str(e)}")
        if response:
            st.error(f"Response status code: {response.status_code}")
            st.error(f"Response content: {response.text}")
        return None

# Fetch and display data
if st.button("Fetch Notion Data"):
    st.write("Attempting to fetch data from Notion...")
    data = fetch_notion_data()
    if data:
        st.success("Successfully fetched data from Notion!")
        for item in data:
            st.write(item['properties'])  # Adjust this based on your database structure
    else:
        st.error("Failed to fetch data from Notion. Check the error messages above.")

# Display environment variable status
st.sidebar.title("Environment Variables")
st.sidebar.write(f"NOTION_TOKEN set: {'Yes' if NOTION_TOKEN else 'No'}")
st.sidebar.write(f"DATABASE_ID set: {'Yes' if DATABASE_ID else 'No'}")
