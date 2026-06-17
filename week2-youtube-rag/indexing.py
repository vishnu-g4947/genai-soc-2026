import config
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_video_id(video_url):
    """Extract the video id from a youtube url"""
    if "v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    raise ValueError("Invalid YouTube URL")

def get_transcript(video_url):
    video_id = extract_video_id(video_url)
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(
            video_id,
            languages=['hi', 'en']
        )
        transcript_text = " ".join(
            chunk.text for chunk in transcript_list
        )
        return transcript_text
    except Exception as e:
        print(f"Transcript Error: {e}")
        return None

def create_chunks (transcript):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000, 
        chunk_overlap = 200
    )
    chunks = splitter.create_documents([transcript])
    return chunks
