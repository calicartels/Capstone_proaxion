"""
Utilities for repairing malformed JSON from LLM outputs.
"""
import re
import json

def repair_json(text):
    """
    Attempt to repair common JSON formatting issues in LLM-generated responses.
    
    Args:
        text (str): The potentially malformed JSON text
    
    Returns:
        str: Repaired JSON text that should be valid
    """
    # Extract JSON if it's within triple backticks
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if json_match:
        text = json_match.group(1)
    
    # Remove any non-JSON text before or after the JSON object
    text = text.strip()
    if text.startswith('{') and '}' in text:
        text = text[:text.rindex('}')+1]
    elif text.startswith('[') and ']' in text:
        text = text[:text.rindex(']')+1]
    
    # Fix common JSON issues
    
    # 1. Fix trailing commas (not allowed in JSON)
    text = re.sub(r',\s*([}\]])', r'\1', text)
    
    # 2. Add missing quotes around property names
    text = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)(\s*:)', r'\1"\2"\3', text)
    
    # 3. Replace single quotes with double quotes
    # This is trickier as we need to avoid replacing quotes in already quoted strings
    # Basic implementation (may not handle all cases)
    text = re.sub(r":\s*'([^']*)'", r': "\1"', text)
    
    # 4. Fix missing commas between properties
    text = re.sub(r'(["}])\s*"', r'\1, "', text)
    
    # 5. Balance braces/brackets
    open_braces = text.count('{')
    close_braces = text.count('}')
    open_brackets = text.count('[')
    close_brackets = text.count(']')
    
    if open_braces > close_braces:
        text += '}' * (open_braces - close_braces)
    if open_brackets > close_brackets:
        text += ']' * (open_brackets - close_brackets)
    
    return text

def safe_parse_json(text):
    """
    Attempt to parse JSON safely, with multiple fallback options.
    
    Args:
        text (str): The JSON text to parse
    
    Returns:
        dict: The parsed JSON object, or an empty dict if parsing fails
    """
    try:
        # First try direct parsing
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            # Try repairing the JSON
            repaired = repair_json(text)
            return json.loads(repaired)
        except json.JSONDecodeError:
            try:
                # Try using a more lenient approach - extracting sections
                parts = re.findall(r'{[^{]*}', text)
                if parts:
                    # Use the first parseable section
                    for part in parts:
                        try:
                            return json.loads(part)
                        except:
                            continue
            except:
                pass
            
            # Return empty dict if all parsing attempts fail
            return {}