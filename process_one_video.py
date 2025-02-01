# process_one_video.py

# Import the 'json' module for handling JSON data serialization and deserialization
import json

# Import the 'boto3' library for interacting with AWS services like S3
import boto3

# Import the 'requests' library for making HTTP requests to external URLs
import requests

# Import 'BytesIO' from the 'io' module to handle in-memory binary streams
from io import BytesIO

# Import the 'dotenv' module to load environment variables from a .env file
from dotenv import load_dotenv

# Import the 'os' module to access environment variables
import os

# Import 'YouTube' from the 'pytube' module to download YouTube videos
import yt_dlp

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
INPUT_KEY = os.getenv('INPUT_KEY')
OUTPUT_KEY = os.getenv('OUTPUT_KEY')

def download_video(video_url, output_path):
    output_file = os.path.join(output_path, 'first_video.mp4')
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_file,
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Download completed successfully! File saved to: {output_file}")
        return output_file
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return None

def upload_to_s3(file_path, bucket_name, s3_key):
    s3 = boto3.client('s3', region_name=AWS_REGION)
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Video uploaded to S3: s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"An error occurred during upload: {e}")

def process_one_video():
    """
    Fetch a highlight URL from the JSON file in S3, download the video,
    and save it back to S3.
    
    This function performs the following steps:
    1. Connects to the specified S3 bucket.
    2. Retrieves the input JSON file containing video URLs.
    3. Extracts the first video URL from the JSON data.
    4. Downloads the video from the extracted URL.
    5. Uploads the downloaded video to the specified S3 location.
    """
    try:
        # Initialize the S3 client with the specified AWS region
        s3 = boto3.client("s3", region_name=AWS_REGION)

        print("Fetching JSON file from S3...")

        try:
            # Retrieve the JSON file from S3 using the specified bucket and key
            response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=INPUT_KEY)
            json_content = response['Body'].read().decode('utf-8')
            highlights = json.loads(json_content)

            if not highlights:
                print("No highlights data found")
                return

            # Extract video URL
            video_url = highlights[0]["url"]
            print(f"Processing video URL: {video_url}")

            # Download video using yt_dlp
            output_path = '/tmp'
            video_path = download_video(video_url, output_path)
            
            if video_path:
                upload_to_s3(video_path, S3_BUCKET_NAME, OUTPUT_KEY)
                os.remove(video_path)

        except Exception as e:
            print(f"Error processing video: {e}")
    
    except Exception as e:
        print(f"Error initializing S3 client: {e}")

# Example usage
if __name__ == "__main__":
    process_one_video()