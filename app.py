import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import whisper

prompt = ''' You are a Text Summarizer. You'll take the text and summarize the entire content, providing us with the important points in bullets. The first line should be the title and what is going to come in that text beneath it as a description, followed by the summary. The transcript text is appended here, please provide its summary: '''

def load_env_and_configure():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

def generate_result(content_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + content_text)
    return response.text

def extract_content_from_youtube(youtube_url):
    try:
        youtube_video_id = youtube_url.split("v=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(youtube_video_id)
        transcript = ""
        for text in transcript_text:
            transcript += " " + text["text"]
        return transcript
    except Exception as e:
        st.error(f"Error retrieving transcript: {e}")
        return None

def transcribe_audio(file):
    # model = whisper.load_model("gemini-pro")
    # audio = whisper.load_audio(file)
    # result = model.transcribe(audio)
    # return result['text']
    pass

def main():
    load_env_and_configure()

    st.title("Content Summarizer")

    option = st.selectbox("Choose input type", ["Text", "YouTube URL", "Audio"])

    if option == "Text":
        text_input = st.text_area("Enter text here")
        if st.button("Get Summary") and text_input:
            summary = generate_result(text_input)
            if summary:
                st.write(summary)
            else:
                st.write("Summary could not be generated")

    elif option == "YouTube URL":
        youtube_url = st.text_input("YouTube URL")
        if youtube_url:
            try:
                youtube_video_id = youtube_url.split("v=")[1].split("&")[0]
                st.image(f"http://img.youtube.com/vi/{youtube_video_id}/0.jpg", use_column_width=True)
            except IndexError:
                st.error("Invalid YouTube URL. Please enter a valid URL.")

        if st.button("Get Summary"):
            transcript_text = extract_content_from_youtube(youtube_url)
            if transcript_text:
                summary = generate_result(transcript_text)
                if summary:
                    st.write(summary)
                else:
                    st.write("Summary could not be generated")

    # elif option == "Audio":
    #     audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])
    #     if audio_file:
    #         if st.button("Get Summary"):
    #             transcript_text = transcribe_audio(audio_file)
    #             if transcript_text:
    #                 summary = generate_result(transcript_text)
    #                 if summary:
    #                     st.write(summary)
    #                 else:
    #                     st.write("Summary could not be generated")

if __name__ == "__main__":
    main()