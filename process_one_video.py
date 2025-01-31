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

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
INPUT_KEY = os.getenv('INPUT_KEY')
OUTPUT_KEY = os.getenv('OUTPUT_KEY')

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

            # Read the content of the retrieved object and decode it from bytes to a UTF-8 string
            json_content = response['Body'].read().decode('utf-8')

            # Parse the JSON string into a Python dictionary
            highlights = json.loads(json_content)

            if not highlights:
                print("No highlights data found")
                return

            # Extract the first video URL from the JSON data
            video_url = highlights[0]["url"]

            # Inform the user about the video URL being processed
            print(f"Processing video URL: {video_url}")

            # Download the video from the extracted URL
            video_response = requests.get(video_url)
            video_data = video_response.content

            # Upload the downloaded video to the specified S3 location
            s3.put_object(Bucket=S3_BUCKET_NAME, Key=OUTPUT_KEY, Body=video_data)
            print(f"Video uploaded to S3: s3://{S3_BUCKET_NAME}/{OUTPUT_KEY}")
        
        except Exception as e:
            print(f"Error fetching JSON file from S3: {e}")
    
    except Exception as e:
        print(f"Error initializing S3 client: {e}")

# Example usage
if __name__ == "__main__":
    process_one_video()