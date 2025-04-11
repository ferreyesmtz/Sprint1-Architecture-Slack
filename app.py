import streamlit as st
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from io import BytesIO

st.title('Slack Integration with Streamlit')

slack_token = 'YOUR-TOKEN'
client = WebClient(token=slack_token)

def send_message_to_slack(message):
    try:
        response = client.chat_postMessage(channel='#general-team43', text=message)
    except SlackApiError as e:
        st.error(f"Error sending message: {e.response['error']}")

def send_image_to_slack(image_url):
    try:
        # Subir la imagen a Slack
        response = client.chat_postMessage(
            channel='#general-team43',
            blocks=[
                {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "Imagen desde URL"
                }
            ]
        )
        if response['ok']:
            st.success("Image sent to Slack!")
        else:
            st.error(f"Error uploading image: {response['error']}")
    except Exception as e:
        st.error(f"Error uploading image: {str(e)}")

def send_file_to_slack(file):
    try:
        # Leer el archivo cargado por el usuario y convertirlo en un objeto BytesIO
        file_content = file.read()
        file_bytes = BytesIO(file_content)
        
        # Usar files_upload_v2 para cargar el archivo a Slack
        response = client.files_upload_v2(
            file_uploads=[{
                "file": file_bytes,
                "filename": file.name,
                "title": file.name,
                "channel": '#general-team43'
            }],
        )

        uploaded = response["files"][0]
        file_link = uploaded.get("permalink")
        published_channels = uploaded.get("channel", [])

        if not published_channels:
            # Si el archivo no se publicó automáticamente, lo hacemos manualmente
            client.chat_postMessage(
                channel='#general-team43',
                text=f"Archivo subido: <{file_link}>"
            )
            print("Archivo subido y publicado manualmente.")
        else:
            print("Archivo subido y publicado automáticamente.")

        return True

    except SlackApiError as e:
        print("Error al subir archivo:", e.response["error"])
        return False
    except Exception as ex:
        print("Error inesperado:", ex)
        return False

# Enviar mensaje a Slack
message = st.text_input('Enter your message:')
if st.button('Send Message'):
    # Llamada a Slack API para enviar mensaje
    send_message_to_slack(message)

# Subir imagen desde URL
image_url = st.text_input('Enter image URL:')
if st.button('Send Image'):
    send_image_to_slack(image_url)

# Subir archivo
file = st.file_uploader("Upload a file", type=["jpg", "png", "pdf", "txt"])
if file is not None:
    send_file_to_slack(file)
