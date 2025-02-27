"""
Knowledge Base Builder Module (Fixed Version)

This module automatically builds a comprehensive knowledge base from document extractions.
It merges data from multiple document extractions and fills in gaps using LLMs.
"""
import os
import json
import glob
import re
from datetime import datetime
import uuid

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import STRUCTURED_DIR, TEXT_MODEL
from utils.llm_processor import LLMProcessor

class KnowledgeBaseBuilder:
    """Builds comprehensive knowledge bases from document extractions."""
    
    def __init__(self):
        """Initialize the knowledge base builder."""
        self.llm_processor = LLMProcessor()
    
    def build_comprehensive_kb(self, doc_id=None):
        """
        Build a comprehensive knowledge base from existing document extractions.
        
        Args:
            doc_id (str, optional): Specific document ID to process. If None, uses latest.
            
        Returns:
            str: ID of the created comprehensive knowledge base
        """
        # Find document extractions to process
        extraction_files = self._find_extraction_files(doc_id)
        
        if not extraction_files:
            print(f"No document extractions found for {doc_id if doc_id else 'any document'}")
            return None
        
        # Load all extractions
        extractions = []
        for file_path in extraction_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    extractions.append(data)
                    print(f"Loaded extraction: {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        # Merge extractions into comprehensive structure
        merged_data = self._merge_extractions(extractions)
        
        # Find and fill gaps in the knowledge base using LLM
        comprehensive_kb = self._fill_gaps(merged_data, extractions)
        
        # Save comprehensive knowledge base
        kb_id = f"kb_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d')}"
        file_path = os.path.join(STRUCTURED_DIR, f"{kb_id}.json")
        
        comprehensive_kb['_metadata'] = {
            'id': kb_id,
            'created_at': datetime.now().isoformat(),
            'version': '1.0',
            'type': 'comprehensive_kb',
            'source_extractions': [os.path.basename(f) for f in extraction_files]
        }
        
        with open(file_path, 'w') as f:
            json.dump(comprehensive_kb, f, indent=2)
        
        print(f"✅ Created comprehensive knowledge base: {kb_id}")
        print(f"📂 Saved to: {file_path}")
        
        return kb_id
    
    def _find_extraction_files(self, doc_id=None):
        """
        Find document extraction files to process.
        
        Args:
            doc_id (str, optional): Specific document ID. If None, finds all extractions.
            
        Returns:
            list: Paths to extraction files
        """
        if doc_id:
            # Find files for specific document ID
            pattern = os.path.join(STRUCTURED_DIR, f"{doc_id}.json")
            files = glob.glob(pattern)
        else:
            # Find all document extraction files (excluding KB files)
            pattern = os.path.join(STRUCTURED_DIR, "doc_*.json")
            files = glob.glob(pattern)
            # Sort by modification time (newest first)
            files.sort(key=os.path.getmtime, reverse=True)
        
        return files
    
    def _merge_extractions(self, extractions):
        """
        Merge multiple document extractions into a single structure.
        """
        # Start with base structure
        merged = {
            "title": None,
            "source_url": None,
            "machines": [],
            "images": []
        }
        
        # Track images to avoid duplicates
        image_ids = set()
        
        # Process each extraction
        for ext in extractions:
            # Get basics
            if not merged["title"] and "title" in ext:
                merged["title"] = ext["title"]
            
            if not merged["source_url"] and "source_url" in ext:
                merged["source_url"] = ext["source_url"]
            
            # Process machine types and configurations
            self._merge_machine_data(merged, ext)
            
            # Process images
            self._merge_image_data(merged, ext, image_ids)
        
        # After merging all extractions, ensure essential data is present
        merged = self._ensure_critical_data(merged)
        
        return merged
    


    def _ensure_critical_data(self, merged):
        """
        Ensure that critical data exists in the knowledge base.
        This acts as a safeguard against missing data.
        """
        # Ensure we have at least one machine type
        if not merged["machines"]:
            merged["machines"] = [{"type": "Fan", "configurations": [], "installation_methods": []}]
        
        # Process each machine
        for machine in merged["machines"]:
            # Ensure configurations
            if "configurations" not in machine or not machine["configurations"]:
                machine["configurations"] = [
                    {
                        "type": "Direct/Close Coupled",
                        "description": "Motor shaft and fan shaft connected without intermediary coupling, ensuring highly efficient power transfer.",
                        "sensor_placement": {
                            "locations": [
                                {
                                    "name": "Motor DE",
                                    "priority": 1,
                                    "justification": "Highest priority (typically experiences the most load and stress)"
                                },
                                {
                                    "name": "Motor NDE",
                                    "priority": 2,
                                    "justification": "Second priority (if motor is ≥ 150 hp)",
                                    "condition": "Only if motor is ≥ 150 hp"
                                }
                            ]
                        }
                    },
                    {
                        "type": "Belt Driven",
                        "description": "Motor and fan connected by belts and pulleys, allowing speed adjustments and easier maintenance access.",
                        "sensor_placement": {
                            "locations": [
                                {
                                    "name": "Motor DE",
                                    "priority": 1,
                                    "justification": "Highest priority (typically experiences the most load and stress)"
                                },
                                {
                                    "name": "Independent Bearing DE",
                                    "priority": 3,
                                    "justification": "Third priority (transfers the majority of power and experiences the highest dynamic forces)"
                                }
                            ]
                        }
                    }
                ]
            
            # Ensure installation methods
            if "installation_methods" not in machine or not machine["installation_methods"]:
                machine["installation_methods"] = [
                    {
                        "name": "Threaded Stud Mount (Drill & Tap)",
                        "recommendedFor": "Permanent installations",
                        "requirements": {
                            "surface_thickness": "Mounting surface must be at least ½\" thick"
                        },
                        "steps": [{"step": 1, "title": "Installation", "description": []}]
                    },
                    {
                        "name": "Adhesive",
                        "recommendedFor": "Permanent installations",
                        "options": {
                            "Direct Mount": "For clean, flat surfaces",
                            "Epoxy-Mounting Adapter": "For curved or uneven surfaces"
                        },
                        "steps": [{"step": 1, "title": "Installation", "description": []}]
                    },
                    {
                        "name": "High-Strength Magnet",
                        "notRecommended": True,
                        "reason": "Can shift or 'walk' over time, causing inaccurate readings.",
                        "steps": [{"step": 1, "title": "Installation", "description": []}]
                    }
                ]
                
        # Update merged data with critical data
        return merged

    def _merge_machine_data(self, merged, extraction):
        """
        Merge machine data from an extraction into the merged structure.
        
        Args:
            merged (dict): Merged data structure to update
            extraction (dict): Extraction data to merge in
        """
        # Create default "Fan" machine type if not exists
        fan_entry = next((m for m in merged["machines"] if m.get("type") == "Fan"), None)
        if not fan_entry:
            fan_entry = {"type": "Fan", "configurations": [], "installation_methods": []}
            merged["machines"].append(fan_entry)
        
        # Handle "machines" array (doc_34dbdbf7 format)
        if "machines" in extraction and isinstance(extraction["machines"], list):
            for machine in extraction["machines"]:
                machine_type = machine.get("name", "Unknown")
                machine_entry = next((m for m in merged["machines"] if m.get("type") == machine_type), None)
                
                if not machine_entry:
                    machine_entry = {"type": machine_type, "configurations": [], "installation_methods": []}
                    merged["machines"].append(machine_entry)
                
                # Process configurations
                if "configurations" in machine and isinstance(machine["configurations"], list):
                    for config in machine["configurations"]:
                        config_type = config.get("type")
                        if not config_type:
                            continue
                        
                        # Find or create configuration
                        config_entry = next((c for c in machine_entry["configurations"] if c.get("type") == config_type), None)
                        if not config_entry:
                            config_entry = {"type": config_type}
                            machine_entry["configurations"].append(config_entry)
                        
                        # Update with new data
                        for key, value in config.items():
                            if key != "type" and (key not in config_entry or not config_entry[key]):
                                config_entry[key] = value
                
                # Process installation methods
                if "installation_methods" in machine and isinstance(machine["installation_methods"], list):
                    for method in machine["installation_methods"]:
                        method_name = method.get("name")
                        if not method_name:
                            continue
                        
                        # Find or create method
                        method_entry = next((m for m in machine_entry["installation_methods"] if m.get("name") == method_name), None)
                        if not method_entry:
                            method_entry = {"name": method_name}
                            machine_entry["installation_methods"].append(method_entry)
                        
                        # Update with new data
                        for key, value in method.items():
                            if key != "name" and (key not in method_entry or not method_entry[key]):
                                method_entry[key] = value
        
        # Handle "machine_types" dict format (doc_32145bdb format)
        if "machine_types" in extraction and isinstance(extraction["machine_types"], dict):
            for machine_type, machine_data in extraction["machine_types"].items():
                # Add as configuration to Fan
                config_entry = next((c for c in fan_entry["configurations"] if c.get("type") == machine_type), None)
                if not config_entry:
                    config_entry = {"type": machine_type}
                    fan_entry["configurations"].append(config_entry)
                
                # Add description
                if isinstance(machine_data, str):
                    config_entry["description"] = machine_data
                elif isinstance(machine_data, dict):
                    for key, value in machine_data.items():
                        if key not in config_entry or not config_entry[key]:
                            config_entry[key] = value
        
        # Handle "machine_types" list format
        if "machine_types" in extraction and isinstance(extraction["machine_types"], list):
            for machine_type in extraction["machine_types"]:
                # Get matching configuration from "configurations" if available
                config_desc = None
                if "configurations" in extraction and isinstance(extraction["configurations"], dict):
                    config_desc = extraction["configurations"].get(machine_type)
                
                # Add as configuration to Fan
                config_entry = next((c for c in fan_entry["configurations"] if c.get("type") == machine_type), None)
                if not config_entry:
                    config_entry = {"type": machine_type}
                    if config_desc:
                        config_entry["description"] = config_desc
                    fan_entry["configurations"].append(config_entry)
        
        # Handle direct "configurations" dict format
        if "configurations" in extraction and isinstance(extraction["configurations"], dict):
            # Add configs directly to Fan
            for config_type, config_data in extraction["configurations"].items():
                config_entry = next((c for c in fan_entry["configurations"] if c.get("type") == config_type), None)
                if not config_entry:
                    config_entry = {"type": config_type}
                    fan_entry["configurations"].append(config_entry)
                
                # Add data to configuration
                if isinstance(config_data, str):
                    if "description" not in config_entry or not config_entry["description"]:
                        config_entry["description"] = config_data
                elif isinstance(config_data, dict):
                    for key, value in config_data.items():
                        if key not in config_entry or not config_entry[key]:
                            config_entry[key] = value
        
        # Handle "sensor_placement" data
        if "sensor_placement" in extraction:
            # Handle dict format (priority -> location mapping)
            if isinstance(extraction["sensor_placement"], dict):
                # Add to each configuration
                for config in fan_entry["configurations"]:
                    if "sensor_placement" not in config:
                        config["sensor_placement"] = {"locations": []}
                    elif "locations" not in config["sensor_placement"]:
                        # Add locations key if it doesn't exist
                        config["sensor_placement"]["locations"] = []
                    
                    for location, data in extraction["sensor_placement"].items():
                        # Create location entry
                        if isinstance(data, dict):
                            loc_entry = {
                                "name": location,
                                "priority": data.get("priority", 0),
                                "justification": data.get("reason", "")
                            }
                        else:
                            # Handle case where data is a string or other type
                            loc_entry = {
                                "name": location,
                                "priority": 0,
                                "justification": str(data) if data else ""
                            }
                        
                        # Condition for motor NDE
                        if "≥ 150 hp" in location:
                            loc_entry["condition"] = "Only if motor is ≥ 150 hp"
                        
                        # Add to locations
                        config["sensor_placement"]["locations"].append(loc_entry)
            
            # Handle list format (array of locations)
            elif isinstance(extraction["sensor_placement"], list):
                # Add to each configuration
                for config in fan_entry["configurations"]:
                    if "sensor_placement" not in config:
                        config["sensor_placement"] = {"locations": []}
                    elif "locations" not in config["sensor_placement"]:
                        # Add locations key if it doesn't exist
                        config["sensor_placement"]["locations"] = []
                    
                    for location in extraction["sensor_placement"]:
                        loc_entry = {
                            "name": location.get("location", "Unknown"),
                            "priority": location.get("priority", 0),
                            "justification": ""
                        }
                        
                        # Condition for motor NDE
                        if "≥ 150 hp" in loc_entry["name"]:
                            loc_entry["condition"] = "Only if motor is ≥ 150 hp"
                        
                        # Add to locations
                        config["sensor_placement"]["locations"].append(loc_entry)
            
            # Handle "installation_methods" data
            if "installation_methods" in extraction:
                # Handle dict format
                if isinstance(extraction["installation_methods"], dict):
                    for method_name, method_data in extraction["installation_methods"].items():
                        # Find or create method entry
                        method_entry = next((m for m in fan_entry["installation_methods"] if m.get("name") == method_name), None)
                        if not method_entry:
                            method_entry = {"name": method_name}
                            fan_entry["installation_methods"].append(method_entry)
                        
                        # Add data to method
                        if isinstance(method_data, dict):
                            # Special handling for steps - convert from array or string
                            if "steps" in method_data:
                                steps = method_data["steps"]
                                if isinstance(steps, list) and all(isinstance(step, str) for step in steps):
                                    # Convert simple string array to structured steps
                                    method_entry["steps"] = [
                                        {"step": i+1, "title": step, "description": ""}
                                        for i, step in enumerate(steps)
                                    ]
                                elif isinstance(steps, list) and all(isinstance(step, dict) for step in steps):
                                    method_entry["steps"] = steps
                            
                            # Add other fields
                            for key, value in method_data.items():
                                if key != "steps" and (key not in method_entry or not method_entry[key]):
                                    method_entry[key] = value
                            
                            # Convert "permanence" to "recommended_for"
                            if "permanence" in method_entry and "recommended_for" not in method_entry:
                                method_entry["recommended_for"] = f"{method_entry['permanence'].capitalize()} installations"
                            
                            # Convert "requirements" to structured format
                            if "requirements" in method_entry and isinstance(method_entry["requirements"], str):
                                method_entry["requirements"] = {
                                    "surface_thickness": method_entry["requirements"] if "thick" in method_entry["requirements"] else "",
                                    "general": method_entry["requirements"]
                                }
    
    def _merge_image_data(self, merged, extraction, image_ids):
        """
        Merge image data from an extraction into the merged structure.
        
        Args:
            merged (dict): Merged data structure to update
            extraction (dict): Extraction data to merge in
            image_ids (set): Set of image IDs already processed
        """
        # Process images array
        if "images" in extraction and isinstance(extraction["images"], list):
            for image in extraction["images"]:
                # Generate consistent image ID
                if "filename" in image:
                    image_id = image["filename"]
                elif "id" in image and not isinstance(image["id"], int):
                    image_id = image["id"]
                else:
                    # Handle numeric IDs by using filename
                    image_id = image.get("filename", str(uuid.uuid4()))
                
                # Skip if already processed
                if image_id in image_ids:
                    continue
                
                image_ids.add(image_id)
                
                # Get best caption available
                caption = image.get("generated_caption") or image.get("caption") or ""
                
                # Create image entry
                image_entry = {
                    "id": image_id,
                    "filename": image.get("filename", ""),
                    "caption": caption,
                    "section": image.get("section", "")
                }
                
                merged["images"].append(image_entry)
    
    def _fill_gaps(self, merged_data, extractions):
        """
        Fill gaps in the merged structure using LLM.
        
        Args:
            merged_data (dict): Merged data structure
            extractions (list): Original extractions for context
            
        Returns:
            dict: Complete knowledge base with gaps filled
        """
        print("🧠 Filling gaps in knowledge base using LLM...")
        
        # Create a gap analysis
        gaps = self._identify_gaps(merged_data)
        
        if not gaps:
            print("✓ No gaps identified in knowledge base")
            return merged_data
        
        # Fill gaps using LLM
        for gap_type, gap_locations in gaps.items():
            print(f"Filling {len(gap_locations)} gaps of type: {gap_type}")
            
            for location in gap_locations:
                self._fill_gap(merged_data, gap_type, location, extractions)
        
        # Post-process to clean up any JSON strings embedded as text
        self._post_process_json_strings(merged_data)
        
        return merged_data
    
    def _post_process_json_strings(self, data):
        """
        Clean up any JSON strings that were embedded as text.
        
        Args:
            data (dict): Data structure to clean up
        """
        if isinstance(data, dict):
            for key, value in list(data.items()):
                if isinstance(value, str) and value.strip().startswith('```json'):
                    # Try to parse the JSON string
                    try:
                        json_str = re.search(r'```json\s*([\s\S]*?)\s*```', value)
                        if json_str:
                            parsed = json.loads(json_str.group(1))
                            data[key] = parsed
                    except Exception:
                        pass
                elif isinstance(value, dict):
                    self._post_process_json_strings(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            self._post_process_json_strings(item)
    
    def _identify_gaps(self, data):
        """
        Identify gaps in the knowledge base structure.
        
        Args:
            data (dict): Merged knowledge base data
            
        Returns:
            dict: Dictionary of gaps by type
        """
        gaps = {
            "missing_description": [],
            "missing_steps": [],
            "missing_justification": [],
            "missing_sensor_placement": [],
            "missing_installation_methods": []
        }
        
        # Check for missing machine data
        if not data["machines"]:
            gaps["missing_machines"] = [{"path": "machines"}]
            return gaps  # If no machines, other checks won't apply
        
        # Check each machine
        for m_idx, machine in enumerate(data["machines"]):
            # Check configurations
            if "configurations" not in machine or not machine["configurations"]:
                gaps["missing_configurations"] = [{"path": f"machines[{m_idx}].configurations"}]
                continue  # If no configurations, other checks won't apply
            
            # Check installation methods
            if "installation_methods" not in machine or not machine["installation_methods"]:
                gaps["missing_installation_methods"].append({
                    "path": f"machines[{m_idx}].installation_methods",
                    "context": {"machine": machine["type"]}
                })
            else:
                # Check each installation method
                for i_idx, method in enumerate(machine["installation_methods"]):
                    # Check for missing steps
                    if "steps" not in method or not method["steps"]:
                        gaps["missing_steps"].append({
                            "path": f"machines[{m_idx}].installation_methods[{i_idx}].steps",
                            "context": {"machine": machine["type"], "method": method["name"]}
                        })
            
            # Check each configuration
            for c_idx, config in enumerate(machine["configurations"]):
                # Check for missing description
                if "description" not in config or not config["description"] or (isinstance(config["description"], dict) and not any(config["description"].values())):
                    gaps["missing_description"].append({
                        "path": f"machines[{m_idx}].configurations[{c_idx}].description",
                        "context": {"machine": machine["type"], "configuration": config["type"]}
                    })
                
                # Check for missing sensor placement
                if "sensor_placement" not in config:
                    gaps["missing_sensor_placement"].append({
                        "path": f"machines[{m_idx}].configurations[{c_idx}].sensor_placement",
                        "context": {"machine": machine["type"], "configuration": config["type"]}
                    })
                elif "locations" not in config["sensor_placement"] or not config["sensor_placement"]["locations"]:
                    gaps["missing_sensor_placement"].append({
                        "path": f"machines[{m_idx}].configurations[{c_idx}].sensor_placement.locations",
                        "context": {"machine": machine["type"], "configuration": config["type"]}
                    })
                else:
                    # Check each sensor location
                    for l_idx, location in enumerate(config["sensor_placement"]["locations"]):
                        # Check for missing justification
                        if "justification" not in location or not location["justification"]:
                            gaps["missing_justification"].append({
                                "path": f"machines[{m_idx}].configurations[{c_idx}].sensor_placement.locations[{l_idx}].justification",
                                "context": {
                                    "machine": machine["type"], 
                                    "configuration": config["type"],
                                    "location": location["name"]
                                }
                            })
        
        # Filter out empty gap types
        return {k: v for k, v in gaps.items() if v}
    
    def _fill_gap(self, data, gap_type, location, extractions):
        """
        Fill a specific gap in the knowledge base using LLM.
        
        Args:
            data (dict): Knowledge base data to update
            gap_type (str): Type of gap to fill
            location (dict): Location of the gap in the data structure
            extractions (list): Original extractions for context
        """
        path = location["path"]
        context = location.get("context", {})
        
        # Create a prompt based on gap type and context
        if gap_type == "missing_description":
            prompt = self._create_description_prompt(context, extractions)
            result = self._generate_completion(prompt)
            
            # Update the data structure
            self._update_path(data, path, result)
        
        elif gap_type == "missing_justification":
            prompt = self._create_justification_prompt(context, extractions)
            result = self._generate_completion(prompt)
            
            # Update the data structure
            self._update_path(data, path, result)
        
        elif gap_type == "missing_steps":
            prompt = self._create_steps_prompt(context, extractions)
            result = self._generate_completion(prompt)
            
            try:
                # Parse the steps from the result
                steps = json.loads(result)
                # Update the data structure
                self._update_path(data, path, steps)
            except json.JSONDecodeError:
                print(f"⚠️ Could not parse steps as JSON: {result[:100]}...")
                # Use a simple structure as fallback
                self._update_path(data, path, [{"step": 1, "title": "Installation", "description": result}])
        
        elif gap_type == "missing_sensor_placement":
            prompt = self._create_sensor_placement_prompt(context, extractions)
            result = self._generate_completion(prompt)
            
            try:
                # Parse the sensor placement from the result
                placements = json.loads(result)
                # Update the data structure
                self._update_path(data, path, placements)
            except json.JSONDecodeError:
                print(f"⚠️ Could not parse sensor placement as JSON: {result[:100]}...")
                # Use a simple structure as fallback
                if path.endswith(".locations"):
                    self._update_path(data, path, [{"priority": 1, "name": "Default", "description": result}])
                else:
                    self._update_path(data, path, {"locations": [{"priority": 1, "name": "Default", "description": result}]})
        
        elif gap_type == "missing_installation_methods":
            prompt = self._create_installation_methods_prompt(context, extractions)
            result = self._generate_completion(prompt)
            
            try:
                # Parse the installation methods from the result
                methods = json.loads(result)
                # Update the data structure
                self._update_path(data, path, methods)
            except json.JSONDecodeError:
                print(f"⚠️ Could not parse installation methods as JSON: {result[:100]}...")
                # Use a simple structure as fallback
                self._update_path(data, path, [
                    {"name": "Threaded Stud Mount (Drill & Tap)", "recommended_for": "Permanent installations"}, 
                    {"name": "Adhesive Mount", "recommended_for": "Most installations"}
                ])
    
    def _update_path(self, data, path, value):
        """
        Update a value at a specific path in a nested data structure.
        
        Args:
            data (dict): Data structure to update
            path (str): Path to update in dot notation (with array indices in brackets)
            value: Value to set at the path
        """
        # Parse the path
        parts = []
        current = ""
        in_brackets = False
        
        for char in path:
            if char == '[':
                if current:
                    parts.append(current)
                    current = ""
                in_brackets = True
            elif char == ']':
                if in_brackets:
                    parts.append(int(current))
                    current = ""
                in_brackets = False
            elif char == '.':
                if current:
                    parts.append(current)
                    current = ""
            else:
                current += char
        
        if current:
            parts.append(current)
        
        # Traverse the path
        current_obj = data
        for i, part in enumerate(parts[:-1]):
            if isinstance(part, int):
                # Array index
                if len(current_obj) <= part:
                    # Extend array if needed
                    current_obj.extend([{} for _ in range(part - len(current_obj) + 1)])
                if i + 1 < len(parts) - 1 and isinstance(parts[i + 1], int):
                    # Next part is also an array index, so we need a list
                    if not isinstance(current_obj[part], list):
                        current_obj[part] = []
                elif not isinstance(current_obj[part], dict):
                    current_obj[part] = {}
                current_obj = current_obj[part]
            else:
                # Object key
                if part not in current_obj:
                    if i + 1 < len(parts) - 1 and isinstance(parts[i + 1], int):
                        # Next part is an array index, so we need a list
                        current_obj[part] = []
                    else:
                        current_obj[part] = {}
                current_obj = current_obj[part]
        
        # Set the value
        last_part = parts[-1]
        if isinstance(last_part, int):
            if len(current_obj) <= last_part:
                # Extend array if needed
                current_obj.extend([None for _ in range(last_part - len(current_obj) + 1)])
            current_obj[last_part] = value
        else:
            current_obj[last_part] = value
    
    def _create_description_prompt(self, context, extractions):
        """Create a prompt for generating a missing description."""
        machine_type = context.get("machine", "Fan")
        config_type = context.get("configuration", "Unknown")
        
        prompt = f"""
        I need a detailed description for a {config_type} configuration of a {machine_type}.
        
        Based on the document extractions, describe what a {config_type} {machine_type} is, its key characteristics, 
        and any important details about how it works.
        
        Document extraction context:
        ```
        {json.dumps(extractions, indent=2)}
        ```
        
        Provide ONLY the description text, no additional explanations or formatting.
        """
        return prompt
    
    def _create_justification_prompt(self, context, extractions):
        """Create a prompt for generating a missing justification."""
        machine_type = context.get("machine", "Fan")
        config_type = context.get("configuration", "Unknown")
        location = context.get("location", "Unknown location")
        
        prompt = f"""
        I need a detailed justification for why the "{location}" is an important sensor placement location 
        for a {config_type} {machine_type}.
        
        Based on the document extractions, explain why this location is critical for monitoring, what types of issues
        it can detect, and any specific conditions or requirements for this placement.
        
        Document extraction context:
        ```
        {json.dumps(extractions, indent=2)}
        ```
        
        Provide ONLY the justification text, no additional explanations or formatting.
        """
        return prompt
    
    def _create_installation_methods_prompt(self, context, extractions):
        """Create a prompt for generating missing installation methods."""
        machine_type = context.get("machine", "Fan")
        
        prompt = f"""
        I need a list of installation methods for sensors on a {machine_type}.
        
        Based on the document extractions, create a structured list of installation methods including:
        - Method name
        - When it's recommended
        - Requirements or restrictions
        - Basic steps
        
        Document extraction context:
        ```
        {json.dumps(extractions, indent=2)}
        ```
        
        Format your response as a JSON array of methods, with each method having:
        - name: method name
        - recommended_for: when to use this method
        - requirements: any requirements
        - steps: array of step objects with "step", "title", "description" fields
        
        Example format:
        ```json
        [
          {{
            "name": "Threaded Stud Mount (Drill & Tap)",
            "recommended_for": "Permanent installations",
            "requirements": {{
              "surface_thickness": "At least ½ inch thick",
              "general": "Flat mounting surface"
            }},
            "steps": [
              {{
                "step": 1,
                "title": "Surface Preparation",
                "description": "Clean the surface thoroughly to remove any dirt, oil, or debris."
              }},
              {{
                "step": 2,
                "title": "Create Pilot Hole",
                "description": "Use a drill to create a pilot hole."
              }}
            ]
          }}
        ]
        ```
        
        Provide ONLY the JSON array, no additional explanations or formatting.
        """
        return prompt
    
    def _create_steps_prompt(self, context, extractions):
        """Create a prompt for generating missing installation steps."""
        machine_type = context.get("machine", "Fan")
        method_name = context.get("method", "Unknown method")
        
        prompt = f"""
        I need a detailed step-by-step procedure for the "{method_name}" installation method for a {machine_type}.
        
        Based on the document extractions, create a structured list of installation steps including:
        - Surface preparation
        - Tool requirements
        - Mounting process
        - Quality checks
        
        Document extraction context:
        ```
        {json.dumps(extractions, indent=2)}
        ```
        
        Format your response as a JSON array of steps, with each step having:
        - step: step number
        - title: short title for the step
        - description: detailed instructions
        
        Example format:
        ```json
        [
          {{
            "step": 1,
            "title": "Surface Preparation",
            "description": "Clean the surface thoroughly to remove any dirt, oil, or debris."
          }},
          {{
            "step": 2,
            "title": "Apply Adhesive",
            "description": "Apply a thin layer of adhesive to the mounting surface."
          }}
        ]
        ```
        
        Provide ONLY the JSON array, no additional explanations or formatting.
        """
        return prompt
    
    def _create_sensor_placement_prompt(self, context, extractions):
        """Create a prompt for generating missing sensor placement information."""
        machine_type = context.get("machine", "Fan")
        config_type = context.get("configuration", "Unknown")
        
        prompt = f"""
        I need detailed sensor placement recommendations for a {config_type} {machine_type}.
        
        Based on the document extractions, create a structured list of sensor placement locations including:
        - Priority order (which locations are most important)
        - Location descriptions
        - Justifications for each location
        - Any conditional requirements (e.g., only for motors above certain horsepower)
        
        Document extraction context:
        ```
        {json.dumps(extractions, indent=2)}
        ```
        
        Format your response as a JSON array of locations, with each location having:
        - priority: numeric priority (1 being highest)
        - name: name of the location (e.g., "Motor Drive-End (DE)")
        - description: brief description of where exactly to place the sensor
        - condition: any conditions that apply (optional)
        - justification: why this location is important
        
        Example format:
        ```json
        [
          {{
            "priority": 1,
            "name": "Motor Drive-End (DE)",
            "description": "Bearing closest to the driven component",
            "justification": "This bearing typically experiences the most load and stress."
          }},
          {{
            "priority": 2,
            "name": "Motor Non-Drive-End (NDE)",
            "description": "Opposite end of motor from drive end",
            "condition": "Only if motor is ≥ 150 hp",
            "justification": "Larger motors exert more stress across both ends."
          }}
        ]
        ```
        
        Provide ONLY the JSON array, no additional explanations or formatting.
        """
        return prompt
    
    def _generate_completion(self, prompt):
        """
        Generate a completion using the LLM.
        
        Args:
            prompt (str): Prompt to send to the LLM
            
        Returns:
            str: Generated text
        """
        try:
            response = self.llm_processor.text_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating completion: {e}")
            return "No information available"