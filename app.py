import streamlit as st
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from io import BytesIO

st.title('Slack Integration with Streamlit')

slack_token = 'SLACK_TOKEN'
client = WebClient(token=slack_token)

def send_message_to_slack(message):
    try:
        response = client.chat_postMessage(channel='#general-team43', text=message)
    except SlackApiError as e:
        st.error(f"Error sending message: {e.response['error']}")

def send_image_to_slack(image_url):
    try:
        response = client.chat_postMessage(
            channel='#general-43',
            blocks=[
                {
                    "type": "image",
                    "image_url": image_url
                }
            ]
        )
        st.success("Image sent to Slack!")
    except Exception as e:
        st.error(f"Error uploading image: {str(e)}")

def send_file_to_slack(file):
    try:
        response = client.files_upload(
            channels='#general-team43',
            file=file
        )
    except SlackApiError as e:
        st.error(f"Error uploading file: {e.response['error']}")


# Enviar mensaje a Slack
message = st.text_input('Enter your message:')
if st.button('Send Message'):
    # Llamada a Slack API para enviar mensaje
    send_message_to_slack(message)

# Subir imagen
image_url = st.text_input('Enter image URL:')
if st.button('Send Image'):
    send_image_to_slack(image_url)

# Subir archivo
file = st.file_uploader("Upload a file", type=["jpg", "png", "pdf", "txt"])
if file is not None:
    send_file_to_slack(file)

