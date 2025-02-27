# rag/process_videos.py
"""
Video segment processing tool for the installation chatbot.
This tool processes installation videos and creates segments that can be
referenced during the installation guidance process.
"""
import os
import sys
import json
import argparse
import subprocess
from datetime import datetime

# Add parent directory to path for module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import STRUCTURED_DIR
from utils.video_processor import VideoProcessor
from utils.storage import StorageManager

def process_video_file(video_path, segments_file=None, method_name="Drill and Tap", kb_id=None):
    """
    Process a video file and create segments based on a JSON configuration.
    
    Args:
        video_path (str): Path to the video file
        segments_file (str): Path to a JSON file with segment definitions
        method_name (str): Installation method name
        kb_id (str): Knowledge base ID to update
    
    Returns:
        dict: Information about the processed video and segments
    """
    # Initialize video processor
    video_processor = VideoProcessor()
    
    # Check if video exists
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return None
    
    # Get video info using ffprobe
    try:
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        video_info = json.loads(result.stdout)
        
        # Extract basic info
        video_duration = float(video_info['format'].get('duration', 0))
        video_size = int(video_info['format'].get('size', 0))
        
        print(f"Video duration: {video_duration:.2f} seconds")
        print(f"Video size: {video_size/1024/1024:.2f} MB")
    except Exception as e:
        print(f"Error getting video info: {e}")
        video_duration = 0
        video_size = 0
    
    # Load segments from file if provided
    segments = []
    if segments_file and os.path.exists(segments_file):
        try:
            with open(segments_file, 'r') as f:
                segments = json.load(f)
                print(f"Loaded {len(segments)} segments from {segments_file}")
        except Exception as e:
            print(f"Error loading segments file: {e}")
            segments = []
    
    # If no segments file provided, create default segments
    if not segments:
        # Create default segments for Drill and Tap method
        if method_name == "Drill and Tap":
            segments = [
                {
                    "start": "0:00",
                    "end": "0:10",
                    "title": "Materials and Tools",
                    "description": "Overview of tools and materials needed for installation",
                    "step_reference": 1
                },
                {
                    "start": "0:10",
                    "end": "0:30",
                    "title": "Surface Preparation",
                    "description": "Creating a pilot hole and preparing the mounting surface",
                    "step_reference": 1
                },
                {
                    "start": "0:30",
                    "end": "0:50",
                    "title": "Tapping the Hole",
                    "description": "Using a thread tap to create screw threads",
                    "step_reference": 2
                },
                {
                    "start": "0:50",
                    "end": "1:10",
                    "title": "Applying Thread Locker",
                    "description": "Preparing the sensor with thread locker",
                    "step_reference": 4
                },
                {
                    "start": "1:10",
                    "end": "1:30",
                    "title": "Mounting the Sensor",
                    "description": "Final installation of the sensor",
                    "step_reference": 5
                }
            ]
        else:
            # Generate generic segments based on video duration
            segment_duration = min(30, video_duration / 5)  # 5 segments or 30 seconds each, whichever is smaller
            segments = []
            
            for i in range(min(5, int(video_duration / segment_duration))):
                start_time = i * segment_duration
                end_time = (i + 1) * segment_duration
                
                segments.append({
                    "start": f"{int(start_time/60)}:{int(start_time % 60):02d}",
                    "end": f"{int(end_time/60)}:{int(end_time % 60):02d}",
                    "title": f"Step {i+1}",
                    "description": f"Installation step {i+1}",
                    "step_reference": i+1
                })
        
        print(f"Created {len(segments)} default segments")
    
    # Process each segment
    processed_segments = []
    for i, segment in enumerate(segments):
        start_time = segment.get("start")
        end_time = segment.get("end")
        title = segment.get("title", f"Segment {i+1}")
        
        if not start_time or not end_time:
            print(f"Skipping segment {i+1}: Missing start or end time")
            continue
        
        try:
            # Extract the segment
            segment_path = video_processor.extract_segment(video_path, start_time, end_time)
            
            # Add to processed segments
            processed_segments.append({
                "index": i+1,
                "start": start_time,
                "end": end_time,
                "title": title,
                "description": segment.get("description", f"Segment {i+1}"),
                "step_reference": segment.get("step_reference", i+1),
                "file_path": segment_path
            })
            
            print(f"Processed segment {i+1}: {title} ({start_time}-{end_time})")
        except Exception as e:
            print(f"Error processing segment {i+1}: {e}")
    
    # Create video data structure
    video_data = {
        "id": os.path.splitext(os.path.basename(video_path))[0],
        "title": f"{method_name} Installation",
        "uri": video_path,
        "duration": f"{int(video_duration/60)}:{int(video_duration % 60):02d}",
        "segments": segments
    }
    
    # Update knowledge base if requested
    if kb_id:
        update_knowledge_base(kb_id, method_name, video_data)
    
    return {
        "video": video_data,
        "processed_segments": processed_segments
    }

def update_knowledge_base(kb_id, method_name, video_data):
    """
    Update a knowledge base with video information.
    
    Args:
        kb_id (str): Knowledge base ID to update
        method_name (str): Installation method name
        video_data (dict): Video data to add
    """
    # Initialize storage manager
    storage_manager = StorageManager()
    
    # Load knowledge base
    kb_data = storage_manager.load_structured_data(kb_id)
    if not kb_data:
        print(f"Error: Knowledge base not found: {kb_id}")
        return False
    
    # Find the installation method
    updated = False
    for machine in kb_data.get("machines", []):
        for method in machine.get("installation_methods", []):
            if method.get("name") == method_name:
                # Add or update video information
                if "videos" not in method:
                    method["videos"] = []
                
                # Check if video already exists
                video_id = video_data.get("id")
                existing_video = next((v for v in method["videos"] if v.get("id") == video_id), None)
                
                if existing_video:
                    # Update existing video
                    existing_video.update(video_data)
                else:
                    # Add new video
                    method["videos"].append(video_data)
                
                updated = True
                break
        
        if updated:
            break
    
    if not updated:
        print(f"Warning: Installation method '{method_name}' not found in knowledge base")
        return False
    
    # Save updated knowledge base
    storage_manager.save_structured_data(kb_data, kb_id)
    print(f"Updated knowledge base {kb_id} with video information")
    return True

def list_kb_methods(kb_id):
    """
    List installation methods in a knowledge base.
    
    Args:
        kb_id (str): Knowledge base ID
        
    Returns:
        list: Installation methods
    """
    # Initialize storage manager
    storage_manager = StorageManager()
    
    # Load knowledge base
    kb_data = storage_manager.load_structured_data(kb_id)
    if not kb_data:
        print(f"Error: Knowledge base not found: {kb_id}")
        return []
    
    # Find installation methods
    methods = []
    for machine in kb_data.get("machines", []):
        for method in machine.get("installation_methods", []):
            method_name = method.get("name")
            if method_name:
                methods.append({
                    "name": method_name,
                    "has_videos": "videos" in method and len(method["videos"]) > 0
                })
    
    return methods

def main():
    """Main function to process video files."""
    parser = argparse.ArgumentParser(description="Process installation videos for the chatbot")
    
    # Add arguments
    parser.add_argument("--video", help="Path to video file")
    parser.add_argument("--segments", help="Path to segments JSON file")
    parser.add_argument("--method", default="Drill and Tap", help="Installation method name")
    parser.add_argument("--kb", help="Knowledge base ID to update")
    parser.add_argument("--list-methods", action="store_true", help="List installation methods in a knowledge base")
    
    # Parse arguments
    args = parser.parse_args()
    
    # List methods in a knowledge base
    if args.list_methods and args.kb:
        methods = list_kb_methods(args.kb)
        if methods:
            print(f"\nInstallation methods in knowledge base {args.kb}:")
            for i, method in enumerate(methods, 1):
                status = "✓" if method["has_videos"] else " "
                print(f"{i}. [{status}] {method['name']}")
        else:
            print(f"No installation methods found in knowledge base {args.kb}")
        return
    
    # Process video
    if args.video:
        result = process_video_file(args.video, args.segments, args.method, args.kb)
        if result:
            print(f"\nProcessed video: {args.video}")
            print(f"Created {len(result['processed_segments'])} segments")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()