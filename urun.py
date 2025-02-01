import os
import yt_dlp

def download_video():
    # Specific YouTube video URL
    video_url = "https://www.youtube.com/watch?v=HGf0IoWI4N0"
    
    # Set output path
    output_path = '/tmp'
    output_file = os.path.join(output_path, 'first_video.mp4')
    
    try:
        # Create yt-dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_file,
            'quiet': True
        }
        
        # Download video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        print(f"Download completed successfully! File saved to: {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_video()
