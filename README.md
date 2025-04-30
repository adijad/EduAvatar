# 🧑‍🏫 EduAvatar

**EduAvatar** is a generative AI tool that transforms educational topics into short, avatar-narrated videos.  
It blends Google’s **Gemini 1.5 Flash** for summarization and **D-ID** avatars for expressive lip-synced narration — delivered in a polished **Streamlit** interface with real-time video generation.

This project demonstrates how language models and avatar synthesis APIs can come together to create engaging microlearning content — ideal for educators, researchers, or anyone curious about AI-powered presentations.

---

## 🚀 Live Demo

Try it out: [Launch EduAvatar](https://edu-avatar.streamlit.app/)

---

## 🖼 Sample Workflow

1. **Input Topic:** `Introduction to Quantum Physics`
2. **Generated Script (Gemini):**

   > "Quantum physics explores the strange behavior of particles at the atomic scale.  
   > Concepts like superposition and entanglement redefine how we understand the universe.  
   > Let’s take a quick peek into the quantum world."

3. **Output:** A D-ID avatar of your choice narrates this script in a short lip-synced video, generated in ~20s.

---

## ✨ Key Features

- **Gemini-Powered Summarization:**  
  Generates short, spoken-style 3–4 line scripts using Gemini 1.5 Flash, fine-tuned for delivery by avatars.

- **D-ID Avatar Integration:**  
  Supports expressive, lip-synced avatar narration using D-ID’s `/talks` API and prebuilt character IDs.

- **Polished Frontend with Streamlit:**  
  Features loading spinners, avatar dropdowns, and real-time generation timers to improve UX.

- **Fully Local Execution:**  
  Runs entirely from your local machine with only your API keys required.

---

## 🔧 Tech Stack

| Component        | Role                                     |
|------------------|------------------------------------------|
| [Gemini 1.5 Flash](https://ai.google.dev/) | Summarization of topics into short scripts |
| [D-ID API](https://www.d-id.com/)          | Generation of lip-synced avatar videos     |
| [Streamlit](https://streamlit.io/)         | UI for user input, video playback, and control |
| Python + `requests`                        | Backend logic and API communication        |
| `dotenv`                                   | Secure API key management                  |

---
