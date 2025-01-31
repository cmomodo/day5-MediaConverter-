# mediaconvert_process.py

# Import the 'json' module for handling JSON data serialization and deserialization
import json

# Import the 'boto3' library for interacting with AWS services like MediaConvert and S3
import boto3

# Import the 'datetime' module for handling date and time objects
from datetime import datetime

# Import the 'dotenv' library to load environment variables from a .env file
from dotenv import load_dotenv

# Import the 'os' module to access environment variables
import os

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
AWS_REGION = os.getenv('AWS_REGION')
MEDIACONVERT_ENDPOINT = os.getenv('MEDIACONVERT_ENDPOINT')
MEDIACONVERT_ROLE_ARN = os.getenv('MEDIACONVERT_ROLE_ARN')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Add custom JSON encoder
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def create_job():
    """
    Create a MediaConvert job to process a video.
    
    This function initializes the MediaConvert client, defines the job settings,
    and submits a job to AWS MediaConvert for processing a video file stored in S3.
    """
    try:
        if not MEDIACONVERT_ROLE_ARN:
            print("Error: MEDIACONVERT_ROLE_ARN not set in environment variables")
            return
            
        # Initialize the MediaConvert client with specified region and endpoint
        mediaconvert = boto3.client(
            "mediaconvert",                    # AWS MediaConvert service
            region_name=AWS_REGION,            # AWS region from configuration
            endpoint_url=MEDIACONVERT_ENDPOINT  # MediaConvert endpoint URL from configuration
        )

        # Define the S3 URL for the input video file to be processed
        input_s3_url = f"s3://{S3_BUCKET_NAME}/videos/first_video.mp4"

        # Define the S3 URL where the processed videos will be saved
        output_s3_url = f"s3://{S3_BUCKET_NAME}/processed_videos/"

        # Define the job settings for MediaConvert
        job_settings = {
            "Inputs": [  # List of input sources for the MediaConvert job
                {
                    "AudioSelectors": {  # Define audio selection settings
                        "Audio Selector 1": {"DefaultSelection": "DEFAULT"}  # Select default audio track
                    },
                    "FileInput": input_s3_url,  # Specify the input video file S3 URL
                    "VideoSelector": {}         # Video selection settings (empty means default)
                }
            ],
            "OutputGroups": [  # Define output group settings
                {
                    "Name": "File Group",  # Name identifier for the output group
                    "OutputGroupSettings": {  # Settings specific to the output group
                        "Type": "FILE_GROUP_SETTINGS",  # Type of output group
                        "FileGroupSettings": {  # Settings related to file group outputs
                            "Destination": output_s3_url  # S3 destination URL for processed videos
                        }
                    },
                    "Outputs": [  # List of output configurations within the output group
                        {
                            "ContainerSettings": {  # Container format settings
                                "Container": "MP4",       # Output container format (MP4)
                                "Mp4Settings": {}         # Additional MP4-specific settings (empty for defaults)
                            },
                            "VideoDescription": {
                                "CodecSettings": {
                                    "Codec": "H_264",
                                    "H264Settings": {
                                        "Bitrate": 5000000,
                                        "RateControlMode": "CBR",
                                        "QualityTuningLevel": "SINGLE_PASS",
                                        "CodecProfile": "MAIN"
                                    }
                                },
                                "Width": 1920,
                                "Height": 1080
                            },
                            "AudioDescriptions": [{
                                "CodecSettings": {
                                    "Codec": "AAC",
                                    "AacSettings": {
                                        "Bitrate": 96000,
                                        "CodingMode": "CODING_MODE_2_0",
                                        "SampleRate": 48000
                                    }
                                }
                            }]
                        }
                    ]
                }
            ]
        }

        # Use custom encoder when creating job
        response = mediaconvert.create_job(
            Role=MEDIACONVERT_ROLE_ARN,                 # IAM role ARN that MediaConvert assumes
            Settings=job_settings,                      # Job settings defined above
            StatusUpdateInterval="SECONDS_60",           # Interval for status updates (every 60 seconds)
            Queue="Default"                              # Queue for the job
        )

        # Print a success message indicating the job was created
        print(f"MediaConvert job created successfully: {response['Job']['Id']}")

    except Exception as e:
        # Catch any exceptions that occur during job creation and print an error message
        print(f"Error creating MediaConvert job: {e}")

# Check if this script is being run as the main program
if __name__ == "__main__":
    # Call the 'create_job' function to initiate the MediaConvert job
    create_job()