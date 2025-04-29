import streamlit as st
import speech_recognition as sr
import os
import platform
from datetime import datetime

# Load chatbot responses
def load_chatbot_data():
    return {
        "tell me a story": "Once upon a time, there was a chatbot who helped many people.",
        "how are you": "I’m just a chatbot, but I’m doing great! How about you?",
        "what is your name": "I’m your friendly chatbot, here to assist you.",
        "hello": "Hello! How can I assist you today?",
        "hi": "Hi there! How can I help you?",
        "riddle": "I have a riddle for you: What has keys but can't open locks? (Answer: A piano)",
        "fun fact": "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
        "joke": "Why don’t skeletons fight each other? They don’t have the guts!",
        "default": "Sorry, I didn’t understand that. Could you rephrase or ask something else?"
    }

chatbot_data = load_chatbot_data()
transcript = []

# Get bot response
def get_bot_response(user_input):
    user_input = user_input.lower()
    for key in chatbot_data:
        if key in user_input:
            return chatbot_data[key]
    return chatbot_data["default"]

# Speak response (macOS-friendly)
def speak_text(text):
    if platform.system() == "Darwin":  # macOS
        os.system(f'say "{text}"')
    else:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

# Save transcript to Downloads and return the file path
def save_transcript(transcript):
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chatbot_transcript_{timestamp}.txt"
    file_path = os.path.join(downloads_path, filename)

    with open(file_path, "w") as file:
        for line in transcript:
            file.write(line + "\n")

    return file_path  # Return the file path so we can use it for the download button

# Main Streamlit App
def main():
    st.title("🗣️ Chat Mate")
    st.write("### 🤖 You can say:")
    st.markdown("""
        - **Hello** or **Hi**
        - **How are you**
        - **What is your name**
        - **Tell me a story**
        - **Riddle**
        - **Fun fact**
        - **Joke**
        - **I don’t understand**    """)

    input_mode = st.radio("Choose input mode:", ("Text", "Speech"))

    # Text input section
    if input_mode == "Text":
        user_input = st.text_input("Type your message:")
        if user_input:
            response = get_bot_response(user_input)
            transcript.append(f"You: {user_input}")
            transcript.append(f"Bot: {response}")
            st.text(f"🤖 ConvoBot Response: {response}")
            speak_text(response)

            # Show the download button and save the transcript
            if transcript:
                st.text("📝 Transcript is ready! Click below to download.")
                file_path = save_transcript(transcript)
                with open(file_path, "rb") as f:
                    st.download_button(label="⬇️ Download Transcript", data=f, file_name=f"chatbot_transcript.txt", mime="text/plain")

    # Speech input section
    elif input_mode == "Speech":
        if st.button("🎙️ Start Listening"):
            st.text("Listening... Please speak!")

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    user_input = recognizer.recognize_google(audio)
                    st.text(f"You said: {user_input}")
                    response = get_bot_response(user_input)
                    transcript.append(f"You: {user_input}")
                    transcript.append(f"Bot: {response}")
                    st.text(f"🤖 ConvoBot Response: {response}")
                    speak_text(response)

                except sr.UnknownValueError:
                    st.warning("Sorry, I couldn't understand the speech.")
                except sr.RequestError:
                    st.error("Speech Recognition service is unavailable.")
                except Exception as e:
                    st.error(f"Error: {e}")
                
                # Show the download button after the speech input is processed
                if transcript:
                    st.text("📝 Transcript is ready! Click below to download.")
                    file_path = save_transcript(transcript)
                    with open(file_path, "rb") as f:
                        st.download_button(label="⬇️ Download Transcript", data=f, file_name=f"chatbot_transcript.txt", mime="text/plain")

    # Save Transcript Button (for both Text and Speech)
    if transcript:
        if st.button("💾 Replay Audio"):
            file_path = save_transcript(transcript)
            

if __name__ == "__main__":
    main()
