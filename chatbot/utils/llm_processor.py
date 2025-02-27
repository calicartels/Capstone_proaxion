"""
Module for processing documents with Vertex AI LLMs.
"""
import os
import json
import re
import io
from PIL import Image

import vertexai
from vertexai.generative_models import GenerativeModel, Part

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LLM_MODEL, TEXT_MODEL, MULTIMODAL_MODEL, IMAGES_DIR, ENABLE_MULTIMODAL

class LLMProcessor:
    """Process documents with Vertex AI LLMs."""
    
    def __init__(self):
        """Initialize the LLM processor with appropriate models."""
        self.text_model = GenerativeModel(TEXT_MODEL)
        
        # Try to initialize the multimodal model, but don't fail if it's unavailable
        self.multimodal_model = None
        if ENABLE_MULTIMODAL:
            try:
                self.multimodal_model = GenerativeModel(MULTIMODAL_MODEL)
                print(f"✓ Successfully initialized multimodal model: {MULTIMODAL_MODEL}")
            except Exception as e:
                print(f"⚠️ Multimodal model initialization failed: {e}")
                print("⚠️ Image captioning will use section context instead of vision analysis")
    

    def analyze_document_structure(self, document_elements):
        """
        Analyze document elements to identify structure and relationships.
        """
        # Extract all text and headings to analyze the document structure
        document_text = ""
        
        # Track sections
        sections = []
        current_section = ""
        section_content = ""
        
        for element in document_elements:
            if element.get('type') == 'section_divider':
                # Found a section divider, process completed section
                if current_section and section_content:
                    sections.append({
                        "title": current_section,
                        "content": section_content
                    })
                    section_content = ""
            elif element.get('type') == 'heading':
                # Handle heading elements
                level = element.get('level', 1)
                heading_text = element.get('content', '').strip()
                
                if level <= 2:  # Major section heading
                    # Process previous section if exists
                    if current_section and section_content:
                        sections.append({
                            "title": current_section,
                            "content": section_content
                        })
                    
                    # Start new section
                    current_section = heading_text
                    section_content = f"# {heading_text}\n\n"
                else:
                    # Add sub-heading to current section
                    section_content += f"\n{'#' * level} {heading_text}\n\n"
                    document_text += f"\n{'#' * level} {heading_text}\n"
            elif element.get('type') == 'text':
                # Add text to current section
                text_content = element.get('content', '')
                section_content += text_content + "\n\n"
                document_text += text_content + "\n"
        
        # Add final section if not empty
        if current_section and section_content:
            sections.append({
                "title": current_section,
                "content": section_content
            })
        
        # Create enhanced prompt for better structure detection
        # Note: Double curly braces to escape them in f-string
        prompt = f"""
        Analyze the following document content that has {len(sections)} major sections:
        
        1. "Sensor Placement & Ranking"
        2. "Overview of how to install and set up sensors for the fan (or other machine)"
        3. "Hierarchy of Sensor Placement"
        
        For each section, identify:
        1. Machine configurations (Direct Coupled, Belt Driven, etc.)
        2. Sensor placement locations and their priorities
        3. Installation methods with their details
        
        Document content:
        ```
        {document_text[:30000]}
        ```
        
        Provide a structured JSON with:
        {{
        "machine_types": ["Motor", "Independent Bearing"],
        "configurations": {{"Direct/Close Coupled": {{}}, "Belt Driven": {{}}}},
        "sensor_placement": {{}},
        "installation_methods": {{}}
        }}
        """
        
        # Get response from LLM
        try:
            response = self.text_model.generate_content(prompt)
            
            # Extract JSON from response
            result = self._extract_json_from_text(response.text)
            return result
        except Exception as e:
            print(f"Error analyzing document structure: {e}")
            # Return a simplified structure as fallback
            return {
                "main_topics": [],
                "machine_configurations": [],
                "sensor_placements": [],
                "installation_methods": []
            }
        
    def generate_image_captions(self, image_elements, document_elements):
        """
        Generate captions for images based on surrounding context.
        
        Args:
            image_elements (list): List of image elements from the document
            document_elements (list): All document elements for context
            
        Returns:
            dict: Updated image elements with generated captions
        """
        updated_images = []
        
        for i, img in enumerate(image_elements):
            print(f"Processing image {i+1}/{len(image_elements)}: {img['filename']}")
            
            # Find position of this image in the elements list
            img_index = -1
            for i, el in enumerate(document_elements):
                if el['type'] == 'image' and el.get('object_id') == img.get('object_id'):
                    img_index = i
                    break
            
            if img_index == -1:
                # Image not found in elements
                print(f"Warning: Couldn't find position of image {img.get('object_id')} in document elements")
                img['generated_caption'] = f"Image in section: {img['section']}"
                updated_images.append(img)
                continue
            
            # Get context before and after the image
            context_before = self._get_context_elements(document_elements, img_index, -5, 5)
            context_after = self._get_context_elements(document_elements, img_index, 1, 3)
            
            # Combine contexts
            context_text = "Context before image:\n"
            for el in context_before:
                if el['type'] == 'heading':
                    context_text += f"\n{'#' * el.get('level', 1)} {el['content']}\n"
                else:
                    context_text += el['content'] + "\n"
                    
            context_text += "\nContext after image:\n"
            for el in context_after:
                if el['type'] == 'heading':
                    context_text += f"\n{'#' * el.get('level', 1)} {el['content']}\n"
                else:
                    context_text += el['content'] + "\n"
            
            # Load the image for multimodal processing
            image_path = os.path.join(IMAGES_DIR, img['filename'])
            if not os.path.exists(image_path):
                print(f"Warning: Image file not found: {image_path}")
                img['generated_caption'] = f"Image in section: {img['section']}"
                updated_images.append(img)
                continue
            
            # Generate caption
            caption = None
            
            # Try multimodal approach first if available
            if self.multimodal_model:
                try:
                    # Create prompt for caption generation
                    prompt = f"""
                    Generate a detailed caption for this image based on its context in the document.
                    
                    The image appears in the section: {img['section']}
                    
                    {context_text}
                    
                    Create a descriptive caption that explains:
                    1. What kind of machine or component is shown
                    2. What configuration or setup is visible
                    3. Any visible sensor locations or important features
                    
                    Provide only the caption text without any explanations or additional text.
                    """
                    
                    # Properly prepare the image for Vertex AI
                    with open(image_path, "rb") as f:
                        image_bytes = f.read()
                    
                    # Use multimodal model to generate caption
                    response = self.multimodal_model.generate_content([
                        prompt,
                        Part.from_data(image_bytes, mime_type="image/jpeg")
                    ])
                    
                    # Get caption from response
                    caption = response.text.strip()
                    print(f"Generated vision-based caption: {caption[:100]}...")
                    
                except Exception as e:
                    print(f"Error generating vision-based caption for image {img['filename']}: {e}")
                    # Will fall back to text-based caption
            
            # If multimodal failed or isn't available, use text-based approach
            if not caption:
                try:
                    # Create a text-only prompt using the context
                    prompt = f"""
                    Based on the following context, generate a caption for an image that appears in a document.
                    
                    The image appears in the section: {img['section']}
                    
                    Context surrounding the image:
                    {context_text}
                    
                    Generate a descriptive caption that likely describes this image based solely on this context.
                    Assume the image shows something related to the text immediately before or after it.
                    Provide only the caption, no additional text.
                    """
                    
                    # Use text model to generate caption
                    response = self.text_model.generate_content(prompt)
                    
                    # Get caption from response
                    caption = response.text.strip()
                    print(f"Generated context-based caption: {caption[:100]}...")
                    
                except Exception as e:
                    print(f"Error generating context-based caption: {e}")
                    # Use simple section-based caption as fallback
                    caption = f"Image in section: {img['section']}"
            
            # If all else fails, use a simple section-based caption
            if not caption:
                caption = f"Image in section: {img['section']}"
            
            # Update image with generated caption
            img['generated_caption'] = caption
            updated_images.append(img)
        
        print(f"✓ Generated captions for {len(updated_images)} images")
        return updated_images
    
    def structure_document_to_json(self, document_data, enhanced_images):
        """
        Convert document data into structured JSON knowledge base.
        
        Args:
            document_data (dict): Analyzed document structure
            enhanced_images (list): Image elements with generated captions
            
        Returns:
            dict: Structured JSON representation for the knowledge base
        """
        try:
            # Create a mapping of image filenames to their enhanced data
            image_map = {img['filename']: img for img in enhanced_images}
            
            # Use a more structured approach to prevent malformed JSON
            prompt = f"""
            I'll provide you with document structure data and image information. 
            Using this information, create a structured knowledge base in JSON format.
            
            Focus on organizing the information into these key categories:

            1. machine_types: Different types of machines described in the document
            2. configurations: Configuration types for each machine
            3. sensor_placement: Rules for where to place sensors
            4. installation_methods: Methods for installing sensors
            5. images: References to relevant images
            
            Document structure data:
            ```json
            {json.dumps(document_data, indent=2)}
            ```
            
            Enhanced image information:
            ```json
            {json.dumps([{
                "id": i,
                "filename": img["filename"],
                "section": img["section"],
                "caption": img["generated_caption"][:100] + "..."
            } for i, img in enumerate(enhanced_images)])}
            ```
            
            Return ONLY valid, parseable JSON. Triple check your JSON syntax for:
            - All property names must be in double quotes
            - No trailing commas
            - Properly nested braces and brackets
            - Properly escaped strings
            
            DO NOT include any explanatory text before or after the JSON.
            """
            
            # Get response from LLM
            response = self.text_model.generate_content(prompt)
            
            # Extract JSON from response
            result = self._extract_json_from_text(response.text)
            
            # Add the full image data back in
            if "images" not in result:
                result["images"] = enhanced_images
            
            return result
        except Exception as e:
            print(f"Error creating structured knowledge base: {e}")
            # Return a simplified structure as fallback that includes images
            return {
                "title": "Sensor Placement Guide",
                "machine_types": [],
                "configurations": [],
                "sensor_placement": [],
                "installation_methods": [],
                "images": enhanced_images
            }
    
    def _get_context_elements(self, elements, current_index, start_offset, count):
        """
        Get context elements around a specific element.
        
        Args:
            elements (list): All document elements
            current_index (int): Index of the current element
            start_offset (int): Offset from current index to start (negative for before)
            count (int): Number of elements to retrieve
            
        Returns:
            list: Relevant context elements
        """
        start_idx = max(0, current_index + start_offset)
        end_idx = min(len(elements), start_idx + count)
        
        context = []
        for i in range(start_idx, end_idx):
            if elements[i]['type'] in ['text', 'heading']:
                context.append(elements[i])
        
        return context
    
    def _extract_json_from_text(self, text):
        """
        Extract valid JSON from text that might contain additional content.
        
        Args:
            text (str): Text potentially containing JSON
            
        Returns:
            dict: Parsed JSON data
        """
        try:
            # Try to find JSON block in triple backticks
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
            
            if json_match:
                json_str = json_match.group(1)
            else:
                # If no JSON code block found, try to use the whole text
                json_str = text
            
            # Clean up the JSON string
            json_str = json_str.strip()
            
            try:
                # Parse the JSON directly first
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Initial JSON parsing failed: {e}")
                print("Attempting to repair malformed JSON...")
                
                # Import the JSON repair utility
                from utils.json_repair import repair_json, safe_parse_json
                
                # Try to repair and parse the JSON
                result = safe_parse_json(json_str)
                
                if result:
                    print("✓ Successfully repaired and parsed JSON")
                    return result
                else:
                    raise Exception("Failed to repair JSON")
                
        except Exception as e:
            print(f"Error parsing JSON from LLM response: {e}")
            print(f"Raw response: {text[:500]}...")
            
            # Return a minimal valid structure as fallback
            return {
                "machine_types": [],
                "images": [],
                "sensor_placements": [],
                "installation_methods": []
            }