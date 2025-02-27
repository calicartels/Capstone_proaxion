"""
Utilities for parsing Google Docs content with improved image extraction.
"""
import os
import re
import base64
from datetime import datetime
import io
import uuid
from PIL import Image
import requests

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DOCS_DIR, IMAGES_DIR

class DocParser:
    """Parse Google Docs content and extract text, structure, and images."""
    
    def __init__(self, docs_service, drive_service):
        """
        Initialize the DocParser.
        
        Args:
            docs_service: Google Docs API service
            drive_service: Google Drive API service
        """
        self.docs_service = docs_service
        self.drive_service = drive_service
    
    def extract_doc_content(self, doc_id):
        """
        Extract content from a Google Doc, including text and images.
        
        Args:
            doc_id (str): Google Docs document ID
        
        Returns:
            dict: Document content with text and image information
        """
        try:
            # Get document content
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            
            print(f"Retrieved document: {document.get('title', 'Untitled')}")
            
            # Prepare result structure
            result = {
                'doc_id': doc_id,
                'title': document.get('title', 'Untitled Document'),
                'elements': [],
                'sections': [],
                'extracted_on': datetime.now().isoformat()
            }
            
            # Process document content
            current_text = ""
            current_section = ""
            elements = []
            
            # Track hierarchical structure
            section_stack = []
            
            # Process positionedObjects (floating images)
            positioned_objects = document.get('positionedObjects', {})
            if positioned_objects:
                print(f"Found {len(positioned_objects)} positioned objects")
                
                for obj_id, obj in positioned_objects.items():
                    if 'positionedObjectProperties' in obj and 'embeddedObject' in obj['positionedObjectProperties']:
                        embedded_obj = obj['positionedObjectProperties']['embeddedObject']
                        if 'imageProperties' in embedded_obj:
                            # This is an image
                            image_filename = f"{doc_id}_positioned_{obj_id}.jpg"
                            image_path = os.path.join(IMAGES_DIR, image_filename)
                            
                            # Extract image source
                            image_source = None
                            if 'contentUri' in embedded_obj['imageProperties']:
                                image_source = embedded_obj['imageProperties']['contentUri']
                            
                            if image_source:
                                elements.append({
                                    'type': 'image',
                                    'object_id': obj_id,
                                    'object_type': 'positioned',
                                    'filename': image_filename,
                                    'section': current_section,
                                    'caption': self._generate_caption_from_context(current_section)
                                })
                                
                                # Extract and save the image
                                try:
                                    self._download_image_from_uri(image_source, image_path)
                                    print(f"Saved positioned image to {image_path}")
                                except Exception as e:
                                    print(f"Error downloading positioned image {obj_id}: {e}")
            
            # Process drawings
            drawings = []
            
            # Extract content from document elements
            if 'body' in document and 'content' in document['body']:
                for element in document['body']['content']:
                    # Process paragraph elements
                    if 'paragraph' in element:
                        paragraph = element['paragraph']
                        
                        # Extract text from paragraph
                        para_text = ""
                        if 'elements' in paragraph:
                            for text_element in paragraph['elements']:
                                if 'textRun' in text_element:
                                    para_text += text_element['textRun'].get('content', '')
                        
                        # Handle section divisions with asterisks
                        if re.match(r'\*{10,}', para_text.strip()):
                            # This is a section separator
                            if current_text:
                                elements.append({
                                    'type': 'text',
                                    'content': current_text.strip(),
                                    'section': current_section,
                                    'section_marker': 'end'  # Mark as section end
                                })
                                current_text = ""
                            
                            # Add a special section divider element
                            elements.append({
                                'type': 'section_divider',
                                'section': current_section
                            })
                            
                            # Reset section tracking for the next major section
                            continue
                        
                        # Determine if the paragraph is a heading
                        is_heading = 'paragraphStyle' in paragraph and 'namedStyleType' in paragraph['paragraphStyle'] and paragraph['paragraphStyle']['namedStyleType'].startswith('HEADING_')
                        heading_level = int(paragraph['paragraphStyle']['namedStyleType'].split('_')[-1]) if is_heading else None

                        # Process headings to track document structure
                        if is_heading:
                            # If we have accumulated text, add it to elements
                            if current_text:
                                elements.append({
                                    'type': 'text',
                                    'content': current_text.strip(),
                                    'section': current_section
                                })
                                current_text = ""
                            
                            # Update section stack based on heading level
                            while section_stack and len(section_stack) >= heading_level:
                                section_stack.pop()
                            
                            section_stack.append(para_text.strip())
                            current_section = " > ".join(section_stack)
                            
                            # Add heading to elements
                            elements.append({
                                'type': 'heading',
                                'level': heading_level,
                                'content': para_text.strip(),
                                'section': current_section
                            })
                        else:
                            # Regular paragraph text
                            current_text += para_text
                    
                    # Look for tables and images in tables
                    elif 'table' in element:
                        table = element['table']
                        # Process table cells for images
                        for row_idx, row in enumerate(table.get('tableRows', [])):
                            for cell_idx, cell in enumerate(row.get('tableCells', [])):
                                for cell_content in cell.get('content', []):
                                    if 'paragraph' in cell_content:
                                        cell_para = cell_content['paragraph']
                                        if 'elements' in cell_para:
                                            for cell_element in cell_para['elements']:
                                                if 'inlineObjectElement' in cell_element:
                                                    obj_id = cell_element['inlineObjectElement']['inlineObjectId']
                                                    # Process this later with other inline objects
            
            # Process inlineObjects (these contain the actual image data)
            inline_objects = document.get('inlineObjects', {})
            if inline_objects:
                print(f"Found {len(inline_objects)} inline objects")
                
                for obj_id, obj in inline_objects.items():
                    if 'inlineObjectProperties' in obj and 'embeddedObject' in obj['inlineObjectProperties']:
                        embedded_obj = obj['inlineObjectProperties']['embeddedObject']
                        
                        # Check for image properties
                        if 'imageProperties' in embedded_obj:
                            image_source = None
                            
                            # Try to find image source in different locations
                            if 'contentUri' in embedded_obj['imageProperties']:
                                image_source = embedded_obj['imageProperties']['contentUri']
                            
                            if image_source:
                                # We have an image
                                image_filename = f"{doc_id}_inline_{obj_id}.jpg"
                                image_path = os.path.join(IMAGES_DIR, image_filename)
                                
                                # Add image to elements
                                elements.append({
                                    'type': 'image',
                                    'object_id': obj_id,
                                    'object_type': 'inline',
                                    'filename': image_filename,
                                    'section': current_section,
                                    'caption': self._generate_caption_from_context(current_section)
                                })
                                
                                # Extract and save the image
                                try:
                                    self._download_image_from_uri(image_source, image_path)
                                    print(f"Saved inline image to {image_path}")
                                except Exception as e:
                                    print(f"Error downloading inline image {obj_id}: {e}")
            
            # Add any remaining text
            if current_text:
                elements.append({
                    'type': 'text',
                    'content': current_text.strip(),
                    'section': current_section
                })
            
            result['elements'] = elements
            
            # Extract top-level sections for easier navigation
            sections = {}
            for el in elements:
                if el['type'] == 'heading' and el['level'] == 1:
                    sections[el['content']] = []
            
            result['sections'] = list(sections.keys())
            
            # Count and report images
            image_elements = [el for el in elements if el['type'] == 'image']
            print(f"Successfully extracted {len(image_elements)} images from the document")
            
            return result
            
        except Exception as e:
            print(f"Error extracting document content: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _download_image_from_uri(self, image_uri, save_path):
        """
        Download image from contentUri and save it.
        Tries multiple methods to download the image.
        
        Args:
            image_uri (str): Image content URI
            save_path (str): Path to save the image
        """
        try:
            # Method 1: For Google Docs images with Drive file ID
            match = re.search(r'id=([^&]+)', image_uri)
            if match:
                file_id = match.group(1)
                
                # Download the image using Drive API
                request = self.drive_service.files().get_media(fileId=file_id)
                image_content = request.execute()
                
                # Save the image
                with open(save_path, 'wb') as f:
                    f.write(image_content)
                return
            
            # Method 2: Direct HTTP request for publicly accessible images
            response = requests.get(image_uri)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return
            
            # Method 3: If it's a full Drive URL
            drive_match = re.search(r'drive\.google\.com/file/d/([^/]+)', image_uri)
            if drive_match:
                file_id = drive_match.group(1)
                request = self.drive_service.files().get_media(fileId=file_id)
                image_content = request.execute()
                
                with open(save_path, 'wb') as f:
                    f.write(image_content)
                return
                
            print(f"Could not extract image from URI: {image_uri}")
            
        except Exception as e:
            print(f"Error downloading image: {e}")
            raise
    
    def _generate_caption_from_context(self, section_path):
        """
        Generate a basic caption based on the section context.
        
        Args:
            section_path (str): Hierarchical section path where the image appears
        
        Returns:
            str: Generated caption
        """
        # For now, just use the section path as the caption
        # This will be enhanced with LLM processing later
        return section_path.split(" > ")[-1] if section_path else "Untitled image"

    def extract_doc_from_url(self, doc_url):
        """
        Extract document ID from Google Docs URL and process it.
        
        Args:
            doc_url (str): Google Docs URL
            
        Returns:
            dict: Processed document content
        """
        # Extract document ID from URL
        match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', doc_url)
        if match:
            doc_id = match.group(1)
            return self.extract_doc_content(doc_id)
        else:
            print(f"Invalid Google Docs URL: {doc_url}")
            return None