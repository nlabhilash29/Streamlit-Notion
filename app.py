import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Notion API setup
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PAGE_ID = os.getenv("NOTION_PAGE_ID")
NOTION_API_VERSION = "2022-06-28"

# Streamlit app
st.title("Notion Page Viewer")

def fetch_notion_page():
    if not NOTION_TOKEN:
        st.error("NOTION_TOKEN is not set. Please check your environment variables.")
        return None
    if not PAGE_ID:
        st.error("NOTION_PAGE_ID is not set. Please check your environment variables.")
        return None

    # First, fetch the page metadata
    url = f"https://api.notion.com/v1/pages/{PAGE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_API_VERSION
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        page_metadata = response.json()

        # Then, fetch the page content
        content_url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
        content_response = requests.get(content_url, headers=headers)
        content_response.raise_for_status()
        page_content = content_response.json()

        return {"metadata": page_metadata, "content": page_content}
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        st.error(f"Response content: {response.text}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

def display_page_content(page_data):
    st.subheader("Page Content")
    
    # Display page title from metadata
    if 'title' in page_data['metadata']['properties']:
        title = page_data['metadata']['properties']['title']['title'][0]['plain_text']
        st.header(title)

    # Display page content
    for block in page_data['content'].get('results', []):
        if block['type'] == 'paragraph':
            text = block['paragraph']['rich_text'][0]['plain_text'] if block['paragraph']['rich_text'] else ''
            st.write(text)
        # Add more block types as needed

if st.button("Fetch Notion Page"):
    st.write("Attempting to fetch the Notion page...")
    page_data = fetch_notion_page()
    if page_data:
        st.success("Successfully fetched the Notion page!")
        display_page_content(page_data)
    else:
        st.error("Failed to fetch the Notion page. Check the error messages above.")

# Display token and page ID (first few characters only for security)
st.sidebar.title("Environment Variables")
st.sidebar.write(f"NOTION_TOKEN set: {'Yes' if NOTION_TOKEN else 'No'}")
if NOTION_TOKEN:
    st.sidebar.write(f"Token (first 5 chars): {NOTION_TOKEN[:5]}...")
st.sidebar.write(f"NOTION_PAGE_ID set: {'Yes' if PAGE_ID else 'No'}")
if PAGE_ID:
    st.sidebar.write(f"Page ID: {PAGE_ID}")
