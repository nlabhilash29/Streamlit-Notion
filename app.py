import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Notion API setup
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PAGE_ID = os.getenv("NOTION_PAGE_ID")  # Now using PAGE_ID from environment variables
NOTION_API_VERSION = "2022-02-22"

# Streamlit app
st.title("Notion Page Viewer")

def fetch_notion_page():
    if not NOTION_TOKEN:
        st.error("NOTION_TOKEN is not set. Please check your environment variables.")
        return None
    if not PAGE_ID:
        st.error("NOTION_PAGE_ID is not set. Please check your environment variables.")
        return None

    url = f"https://api.notion.com/v1/pages/{PAGE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_API_VERSION
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from Notion: {str(e)}")
        if response:
            st.error(f"Response status code: {response.status_code}")
            st.error(f"Response content: {response.text}")
        return None

def display_page_content(page_data):
    if 'properties' in page_data:
        title = page_data['properties'].get('title', {}).get('title', [{}])[0].get('plain_text', 'Untitled')
        st.header(title)

    if 'content' in page_data:
        for block in page_data['content']:
            if block['type'] == 'paragraph':
                text = block['paragraph']['rich_text'][0]['plain_text'] if block['paragraph']['rich_text'] else ''
                st.write(text)
            # Add more block types as needed (e.g., headings, lists, etc.)

if st.button("Fetch Notion Page"):
    st.write("Attempting to fetch the Notion page...")
    page_data = fetch_notion_page()
    if page_data:
        st.success("Successfully fetched the Notion page!")
        display_page_content(page_data)
    else:
        st.error("Failed to fetch the Notion page. Check the error messages above.")

# Display environment variable status
st.sidebar.title("Environment Variables")
st.sidebar.write(f"NOTION_TOKEN set: {'Yes' if NOTION_TOKEN else 'No'}")
st.sidebar.write(f"NOTION_PAGE_ID set: {'Yes' if PAGE_ID else 'No'}")
if PAGE_ID:
    st.sidebar.write(f"Page ID: {PAGE_ID}")
else:
    st.sidebar.write("Page ID not set")
