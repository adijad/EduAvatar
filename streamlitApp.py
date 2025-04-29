#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import os
import base64
import google.generativeai as genai
from dotenv import load_dotenv
import time

# ---------------------------
# Load Environment Variables
# ---------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DID_USERNAME_PASSWORD = os.getenv("DID_USERNAME_PASSWORD")  # username:password

# ---------------------------
# Configure Gemini Client
# ---------------------------
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ---------------------------
# Talking Head Video Generator
# ---------------------------
def generate_video(input_text, source_id):
    url = "https://api.d-id.com/talks"
    encoded_credentials = base64.b64encode(DID_USERNAME_PASSWORD.encode()).decode()

    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-JennyNeural"
            },
            "ssml": "false",
            "input": input_text
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0",
            "driver_expressions": {
                "expressions": [
                    {
                        "start_frame": 0,
                        "expression": "happy",
                        "intensity": 0.75
                    }
                ]
            }
        },
        "source_id": source_id
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Basic {encoded_credentials}"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    talk_id = json.loads(response.text)['id']
    talk_url = f"{url}/{talk_id}"

    # Start spinner and timer
    with st.spinner("🎥 Generating video, please wait..."):
        timer_placeholder = st.empty()
        start_time = time.time()

        while True:
            response = requests.get(talk_url, headers=headers)
            video_response = json.loads(response.text)

            # Update timer display
            elapsed = int(time.time() - start_time)
            timer_placeholder.info(f"⏳ Waiting... {elapsed} seconds elapsed.")

            if video_response["status"] == "done":
                return video_response["result_url"]
            elif video_response["status"] == "error":
                st.error("❌ Error generating video.")
                return None

            time.sleep(2)  # Check every 2 seconds

# ---------------------------
# Generate Short Script using Gemini
# ---------------------------
def generate_script(user_prompt):
    try:
        instruction = (
            f"Generate a short 3–4 line introductory script for the topic: '{user_prompt}'. "
            "Keep it friendly, concise, conversational, and easy to speak aloud. "
            "Do not exceed 4 sentences."
        )
        response = model.generate_content(instruction)
        return response.text
    except Exception as e:
        st.error(f"Error generating script: {e}")
        return ""

# ---------------------------
# Streamlit App
# ---------------------------
def main():
    st.set_page_config(page_title="Talking Head Video Generator", layout="wide")
    st.title("🎥 Create a Talking Head Video")

    with st.sidebar:
        selected = option_menu(
            "Menu",
            ["Generate Video"],
            icons=["camera-video"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Generate Video":
        st.header("Step 1: Provide your script")
        opt2 = st.radio("How would you like to provide your script?", ["Manually enter it", "Use Gemini 1.5 Flash-8B to generate it"])

        if opt2 == "Manually enter it":
            script = st.text_area("✍️ Enter or paste your script here:", "", height=200)
        else:
            user_prompt = st.text_input("🎯 Enter a topic or idea to generate your short intro script:", "")
            script = ""
            if user_prompt:
                script = generate_script(user_prompt)
                if script:
                    st.success("✅ Short script generated successfully!")
                    st.text_area("Generated Short Script:", script, height=150)

        st.header("Step 2: Choose your Talking Avatar")

        # Avatar dropdown
        avatars = {
            "Anna (Standard)": "anna_standard",
            "Ella (Standard)": "ella_standard",
            "Michael (Standard)": "michael_standard",
            "Sophia (Standard)": "sophia_standard",
            "William (Standard)": "william_standard"
        }

        selected_avatar_name = st.selectbox("🖼️ Choose your Avatar:", list(avatars.keys()))
        source_id = avatars[selected_avatar_name]

        if st.button("🎬 Generate Talking Head Video"):
            if script.strip() and source_id.strip():
                video_url = generate_video(script, source_id)
                if video_url:
                    st.video(video_url)
                    st.success("✅ Video created successfully!")
            else:
                st.error("❗ Please provide both script and avatar selection.")

# ---------------------------
# Main Entry
# ---------------------------
if __name__ == "__main__":
    main()
