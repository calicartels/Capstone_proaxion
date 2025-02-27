# utils/video_processor.py
"""
Video processing utilities for working with installation videos.
"""
import os
import subprocess
import tempfile
from urllib.parse import urlparse

class VideoProcessor:
    """Process and serve video files for the chatbot."""
    
    def __init__(self, storage_client=None):
        """Initialize the video processor."""
        self.storage_client = storage_client
        self.use_cloud = storage_client is not None
        self.local_video_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                           'data', 'videos')
        
        # Create videos directory if it doesn't exist
        os.makedirs(self.local_video_dir, exist_ok=True)
    
    def download_from_cloud(self, gcs_uri, local_filename=None):
        """Download a video file from Google Cloud Storage."""
        if not self.use_cloud:
            raise ValueError("Storage client not initialized for cloud operations")
        
        # Parse the GCS URI
        parsed_url = urlparse(gcs_uri)
        if parsed_url.scheme != 'gs':
            raise ValueError(f"Invalid GCS URI scheme: {parsed_url.scheme}")
        
        bucket_name = parsed_url.netloc
        blob_path = parsed_url.path.lstrip('/')
        
        # Generate local filename if not provided
        if not local_filename:
            local_filename = os.path.basename(blob_path)
        
        # Path to save the file
        local_path = os.path.join(self.local_video_dir, local_filename)
        
        # Download the file
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        blob.download_to_filename(local_path)
        
        print(f"Downloaded {gcs_uri} to {local_path}")
        return local_path
    
    def extract_segment(self, video_path, start_time, end_time, output_path=None):
        """Extract a segment from a video file."""
        # Convert time format to seconds for ffmpeg
        start_seconds = self._time_to_seconds(start_time)
        end_seconds = self._time_to_seconds(end_time)
        duration = end_seconds - start_seconds
        
        # Generate output path if not provided
        if not output_path:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            segment_name = f"{base_name}_{start_time.replace(':', '')}_{end_time.replace(':', '')}.mp4"
            output_path = os.path.join(self.local_video_dir, segment_name)
        
        # Extract the segment using ffmpeg
        command = [
            'ffmpeg',
            '-i', video_path,
            '-ss', str(start_seconds),
            '-t', str(duration),
            '-c:v', 'copy',
            '-c:a', 'copy',
            output_path
        ]
        
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Extracted segment {start_time}-{end_time} to {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Error extracting segment: {e}")
            raise
            
    def _time_to_seconds(self, time_str):
        """Convert time string to seconds."""
        parts = time_str.split(':')
        if len(parts) == 2:
            minutes, seconds = map(float, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = map(float, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError(f"Invalid time format: {time_str}")
    
    def prepare_segments_from_kb(self, knowledge_base, installation_method="Drill and Tap"):
        """Extract video segments defined in the knowledge base."""
        # Find the installation method in the knowledge base
        method = None
        for machine in knowledge_base.get("machines", []):
            for method_data in machine.get("installation_methods", []):
                if method_data.get("name") == installation_method:
                    method = method_data
                    break
            if method:
                break
        
        if not method:
            print(f"Installation method '{installation_method}' not found in knowledge base")
            return {}
        
        # Get videos from the installation method
        videos = method.get("videos", [])
        if not videos:
            print(f"No videos found for installation method '{installation_method}'")
            return {}
        
        # For now, just use the first video
        video = videos[0]
        video_uri = video.get("uri")
        segments = video.get("segments", [])
        
        if not video_uri or not segments:
            print(f"Invalid video data for installation method '{installation_method}'")
            return {}
        
        # Download the video if using cloud storage
        if self.use_cloud and video_uri.startswith("gs://"):
            try:
                local_path = self.download_from_cloud(video_uri)
            except Exception as e:
                print(f"Error downloading video: {e}")
                return {}
        else:
            # For local development, the video should already be in the videos directory
            local_path = os.path.join(self.local_video_dir, os.path.basename(video_uri))
            if not os.path.exists(local_path):
                print(f"Video file not found locally: {local_path}")
                return {}
        
        # Prepare segments
        segment_map = {}
        for segment in segments:
            start_time = segment.get("start")
            end_time = segment.get("end")
            title = segment.get("title")
            description = segment.get("description")
            step_reference = segment.get("step_reference")
            
            if not all([start_time, end_time, title, description]):
                print(f"Incomplete segment data: {segment}")
                continue
            
            # Extract segment
            try:
                segment_path = self.extract_segment(local_path, start_time, end_time)
                
                segment_info = {
                    "title": title,
                    "description": description,
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": self._time_to_seconds(end_time) - self._time_to_seconds(start_time),
                    "video_path": segment_path
                }
                
                if step_reference:
                    segment_map[step_reference] = segment_info
                
            except Exception as e:
                print(f"Error processing segment {title}: {e}")
        
        # Also add the full video
        segment_map["full"] = {
            "title": video.get("title", "Full Installation Video"),
            "description": "Complete installation process from start to finish",
            "video_path": local_path,
            "is_full_video": True
        }
        
        return segment_map