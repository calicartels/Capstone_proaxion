# chatbot/bot.py
"""
Main chatbot implementation for sensor installation guidance.
"""
import json
import re
import os

from rag.state import StateManager, ConversationStage
from rag.templates import *
from utils.video_processor import VideoProcessor

class InstallationBot:
    """Chatbot for sensor installation guidance."""
    
    def __init__(self, knowledge_base_path, state_storage_path=None, storage_client=None):
        """Initialize the installation bot."""
        self.knowledge_base_path = knowledge_base_path
        self.state_manager = StateManager(state_storage_path)
        self.video_processor = VideoProcessor(storage_client)
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Prepare video segments
        self.video_segments = {}
        # We'll load these on demand when a specific installation method is selected
    
    def _load_knowledge_base(self):
        """Load knowledge base from file."""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading knowledge base: {e}")
            return {}
    
    def process_message(self, user_id, message):
        """Process a user message and generate a response."""
        # Get conversation state for this user
        state = self.state_manager.get_state(user_id)
        
        # Handle special commands
        if message.lower() == "reset":
            state.reset()
            self.state_manager.save_state(user_id, state)
            return WELCOME_MESSAGE
        
        # Process message based on current conversation stage
        if state.stage == ConversationStage.WELCOME:
            response = self._handle_welcome(state)
        elif state.stage == ConversationStage.MACHINE_SELECTION:
            response = self._handle_machine_selection(state, message)
        elif state.stage == ConversationStage.CONFIGURATION_SELECTION:
            response = self._handle_configuration(state, message)
        elif state.stage == ConversationStage.ADDITIONAL_INFO:
            response = self._handle_additional_info(state, message)
        elif state.stage == ConversationStage.SENSOR_COUNT:
            response = self._handle_sensor_count(state, message)
        elif state.stage == ConversationStage.RECOMMENDATION:
            response = self._handle_recommendation(state, message)
        elif state.stage == ConversationStage.INSTALLATION_START:
            response = self._handle_installation_start(state, message)
        elif state.stage == ConversationStage.INSTALLATION_STEPS:
            response = self._handle_installation_steps(state, message)
        elif state.stage == ConversationStage.INSTALLATION_COMPLETE:
            response = self._handle_installation_complete(state, message)
        else:
            response = "I'm not sure how to respond to that. Let's start over."
            state.reset()
        
        # Save updated state
        self.state_manager.save_state(user_id, state)
        
        return response
        
    def _handle_welcome(self, state):
        """Handle welcome stage."""
        state.advance_stage()
        return WELCOME_MESSAGE
    
    def _handle_machine_selection(self, state, message):
        """Handle machine type selection."""
        machine_type = self._extract_machine_type(message)
        
        if not machine_type:
            return "I didn't understand your machine type. Please specify: Fans, Motors, or Pumps."
        
        state.machine_type = machine_type
        state.advance_stage()
        
        # Return appropriate prompt for the machine type
        if machine_type == "Fan":
            return FAN_CONFIGURATION_PROMPT
        else:
            return f"Please specify the configuration for your {machine_type}."
    
    def _handle_configuration(self, state, message):
        """Handle configuration selection."""
        configuration = self._extract_configuration(message)
        
        if not configuration:
            return "Please specify if your fan is Belt Driven, Direct/Close Coupled, or has Independent Bearings."
        
        state.configuration = configuration
        state.advance_stage()
        
        return "Is your fan center hung or overhung?"
    
    def _handle_additional_info(self, state, message):
        """Handle orientation and RPM collection."""
        if not state.orientation:
            orientation = self._extract_orientation(message)
            
            if not orientation:
                return "Please specify if your fan is center hung or overhung."
            
            state.orientation = orientation
            return "What is the operational speed of your fan in RPM?"
        
        # Handle RPM input if orientation is already set
        rpm = self._extract_rpm(message)
        
        if not rpm:
            return "Please provide the operational speed in RPM (e.g., 1750)."
        
        state.rpm = rpm
        state.advance_stage()
        
        return "How many sensors do you currently have available for installation?"
    
    def _handle_sensor_count(self, state, message):
        """Handle sensor count collection."""
        sensor_count = self._extract_number(message)
        
        if not sensor_count:
            return "Please provide the number of sensors you have available."
        
        state.sensor_count = sensor_count
        state.advance_stage()
        
        return "Is there a specific part of the machine you'd like to monitor (motor, bearing housing, fan housing)?"
    
    def _handle_recommendation(self, state, message):
        """Handle recommendation phase."""
        if not state.monitoring_target:
            monitoring_target = self._extract_monitoring_target(message)
            state.monitoring_target = monitoring_target or "General"
            
            # Generate placement recommendations based on machine type and configuration
            if state.configuration == "Direct/Close Coupled":
                ideal_count = 3
                
                # Basic recommendations always include Motor DE
                recommendations = ["Motor Drive-End (DE) - HIGHEST PRIORITY"]
                
                # Add more recommendations based on available sensors
                if state.sensor_count >= 2:
                    recommendations.append("Motor Non-Drive-End (NDE) - For motors ≥ 150 hp")
                
                if state.sensor_count >= 3:
                    recommendations.append("Fan shaft bearings (if accessible)")
                
                state.recommended_placement = recommendations
                
                recommendation_text = f"""
Based on your Direct/Close Coupled fan configuration, the ideal setup would be {ideal_count} sensors for comprehensive monitoring.

With your {state.sensor_count} available sensor(s), here's my recommendation for optimal placement:

1. {recommendations[0]}
   This bearing experiences the most load and stress, making it critical for monitoring.
"""
                if len(recommendations) > 1:
                    recommendation_text += f"\n2. {recommendations[1]}\n   Larger motors benefit from monitoring both ends for a complete vibration profile.\n"
                
                if len(recommendations) > 2:
                    recommendation_text += f"\n3. {recommendations[2]}\n   These provide additional insights into fan health.\n"
                
                recommendation_text += "\nWould you like to proceed with the installation instructions?"
                return recommendation_text
                
            elif state.configuration == "Belt Driven":
                # Similar logic for Belt Driven configuration
                ideal_count = 4
                
                # Basic recommendations always include Motor DE
                recommendations = ["Motor Drive-End (DE) - HIGHEST PRIORITY"]
                
                # Add more recommendations based on available sensors
                if state.sensor_count >= 2:
                    recommendations.append("Motor Non-Drive-End (NDE) - For motors ≥ 150 hp")
                
                if state.sensor_count >= 3:
                    recommendations.append("Belt-Side bearing")
                
                if state.sensor_count >= 4:
                    recommendations.append("Fan-Side bearing")
                
                state.recommended_placement = recommendations
                
                recommendation_text = f"""
Based on your Belt Driven fan configuration, the ideal setup would be {ideal_count} sensors for comprehensive monitoring.

With your {state.sensor_count} available sensor(s), here's my recommendation for optimal placement:

1. {recommendations[0]}
   This bearing experiences the most load and stress, making it critical for monitoring.
"""
                if len(recommendations) > 1:
                    recommendation_text += f"\n2. {recommendations[1]}\n   Larger motors benefit from monitoring both ends for a complete vibration profile.\n"
                
                if len(recommendations) > 2:
                    recommendation_text += f"\n3. {recommendations[2]}\n   This bearing transfers power from motor to fan, critical for early fault detection.\n"
                
                if len(recommendations) > 3:
                    recommendation_text += f"\n4. {recommendations[3]}\n   Supports fan shaft, important for complete system coverage.\n"
                
                recommendation_text += "\nWould you like to proceed with the installation instructions?"
                return recommendation_text
            else:
                # Generic recommendation for other configurations
                return f"""
Based on your {state.configuration} configuration, I recommend placing your {state.sensor_count} sensor(s) on the most critical components for monitoring.

Would you like to proceed with the installation instructions?
"""
        elif "yes" in message.lower() or "proceed" in message.lower():
            # User wants to proceed with installation
            state.advance_stage()
            return "For your fan configuration, I recommend the Drill and Tap installation method for the most secure and accurate readings. Would you like to proceed with this method?"
        else:
            # Ask again about specific part
            state.monitoring_target = None
            return "Is there a specific part of the machine you'd like to monitor (motor, bearing housing, fan housing)?"
    
    def _handle_installation_start(self, state, message):
        """Handle installation method selection and start."""
        if not state.installation_method:
            if "yes" in message.lower() or "drill" in message.lower() or "tap" in message.lower():
                state.installation_method = "Drill and Tap"
            elif "epoxy" in message.lower() or "adhesive" in message.lower():
                state.installation_method = "Epoxy Mount"
            elif "magnet" in message.lower():
                state.installation_method = "Magnets"
            elif "adapter" in message.lower():
                state.installation_method = "Other Adapter Options"
            else:
                return "Please select an installation method: Drill and Tap (recommended), Epoxy Mount, Other Adapter Options, or Magnets."
            
            # Prepare video segments for the selected method
            self.video_segments = self.video_processor.prepare_segments_from_kb(
                self.knowledge_base, 
                state.installation_method
            )
            
            # Materials needed for the selected method
            materials = {
                "Drill and Tap": [
                    "Drill with appropriate bit",
                    "¼\"-28 thread tap",
                    "Spot-face tool",
                    "Thread locker",
                    "Silicone sealant",
                    "Sensor with threaded stud"
                ],
                "Epoxy Mount": [
                    "High-strength adhesive",
                    "Epoxy-mounting adapter (for curved surfaces)",
                    "Cleaning solvent",
                    "Sensor"
                ]
            }.get(state.installation_method, ["Sensor and necessary installation tools"])
            
            materials_text = "\n".join([f"- {m}" for m in materials])
            
            return f"""
Great! Let's install your sensor using the {state.installation_method} method. I'll guide you through each step.

Here's what you'll need:
{materials_text}

Would you like to see the full installation video, or shall we proceed step by step?
- Show me the full video
- Guide me step by step
"""
        
        # Process response to installation intro
        if "full video" in message.lower():
            # Show full installation video
            if "full" in self.video_segments:
                full_video = self.video_segments["full"]
                state.advance_stage()
                state.current_step = 1  # Start with first step
                
                return f"""
Here's the complete installation video (1:41):

[VIDEO: {full_video["video_path"]}]

The video covers all steps from start to finish. Would you like me to also guide you through the specific steps?
- Yes, guide me through the steps
- No, I'll follow the video
"""
            else:
                # No full video available, fall back to step-by-step
                state.advance_stage()
                state.current_step = 1
                return self._get_step_guidance(state.installation_method, 1)
        elif "step by step" in message.lower() or "guide" in message.lower():
            # Start step by step guidance
            state.advance_stage()
            state.current_step = 1
            return self._get_step_guidance(state.installation_method, 1)
        else:
            # Unclear response
            return "Would you like to see the full installation video, or shall we proceed step by step?"
    
    def _handle_installation_steps(self, state, message):
        """Handle installation steps guidance."""
        # Check for help request with specific step
        if "video" in message.lower() or "show me" in message.lower():
            step_reference = state.current_step
            
            # Check if we have a video segment for this step
            if step_reference in self.video_segments:
                segment = self.video_segments[step_reference]
                
                return f"""
Here's a video segment showing {segment["title"]} ({segment["start_time"]}-{segment["end_time"]}):

[VIDEO: {segment["video_path"]}]

Does this help with your current step?
"""
            else:
                # If no specific segment, offer the full video
                if "full" in self.video_segments:
                    full_video = self.video_segments["full"]
                    
                    return f"""
I don't have a specific video for just this step, but you can watch the full installation video and skip to around {self._get_timestamp_for_step(state.current_step)}:

[VIDEO: {full_video["video_path"]}]

Does this help?
"""
                else:
                    return "I'm sorry, I don't have a video available for this step. Would you like more detailed instructions?"
        
        # Handle help request
        elif "help" in message.lower() or "issue" in message.lower() or "problem" in message.lower():
            # User needs help with current step
            state.add_issue(f"Needed help with step {state.current_step}")
            
            return """
I understand installation can be challenging. Would you like me to:
1. Give more detailed instructions for this step
2. Show you a video for this part specifically
3. Connect you with ProAxion support
"""
        
        # Handle escalation request
        elif "proaxion" in message.lower() or "support" in message.lower() or "expert" in message.lower():
            return """
I'll be happy to connect you with our experts. Please fill out this form and a ProAxion representative will contact you:
[FORM LINK]

In the meantime, you can review our installation guides or call our technical support line at [phone number].
"""
        
        # Check if ready for next step
        elif self._is_affirmative(message) or "next" in message.lower() or "ready" in message.lower():
            # Move to next step
            total_steps = self._get_total_steps(state.installation_method)
            state.current_step += 1
            
            # Check if all steps completed
            if state.current_step > total_steps:
                state.installation_complete = True
                state.advance_stage()
                
                return f"""
Congratulations! You've successfully installed your sensor using the {state.installation_method} method.

After installation, please check that:
1. The sensor is properly secured
2. The sensor cable is not under tension
3. The sensor is not in contact with moving parts
4. The sensor readings appear in your monitoring system

Is everything working correctly?
"""
            else:
                # Get next step guidance
                return self._get_step_guidance(state.installation_method, state.current_step)
        else:
            # Unclear response, repeat current step
            return self._get_step_guidance(state.installation_method, state.current_step)
    
    def _handle_installation_complete(self, state, message):
        """Handle installation completion."""
        if "yes" in message.lower() or "working" in message.lower():
            # Installation successful
            return "Great! Your sensor installation is complete. If you have any questions in the future or need to install more sensors, just let me know."
        
        elif "issue" in message.lower() or "problem" in message.lower() or "not working" in message.lower():
            # User has an issue
            state.add_issue("Issue after installation")
            
            return """
I understand you're experiencing an issue. Let me connect you with ProAxion support for assistance.

Please contact [support contact information] and mention the following issues:
1. Problem with sensor installation
2. [Any specific issues noted]

In the meantime, please verify:
- The sensor is firmly attached
- Connections are secure
- No obstructions are present
"""
        else:
            # Unclear response
            return "Is your sensor working correctly? If you're experiencing any issues, I can connect you with ProAxion support for assistance."
    
    def _get_step_guidance(self, method, step_number):
        """Get guidance for a specific installation step."""
        # Get steps for the selected method from knowledge base
        steps = []
        for machine in self.knowledge_base.get("machines", []):
            for installation_method in machine.get("installation_methods", []):
                if installation_method.get("name") == method:
                    if "steps" in installation_method and installation_method["steps"]:
                        # Extract the actual step descriptions
                        step_descriptions = installation_method["steps"][0].get("description", [])
                        steps = step_descriptions
                        break
        
        # If no steps found or step number out of range, provide generic guidance
        if not steps or step_number > len(steps):
            return f"""
Step {step_number}: Continue with Installation

Please continue following the installation procedure according to the manufacturer's guidelines.

Are you ready for the next step, or do you need help?
"""
        
        # Get the requested step
        step = steps[step_number - 1]
        
        return f"""
Step {step_number} of {len(steps)}: {step.get('title', f'Step {step_number}')}

{step.get('description', '')}

Are you ready for the next step, or would you like to see a video of this step?
- I'm ready for the next step
- Show me a video of this step
- I need help with this step
"""
    
    def _get_total_steps(self, method):
        """Get the total number of steps for an installation method."""
        for machine in self.knowledge_base.get("machines", []):
            for installation_method in machine.get("installation_methods", []):
                if installation_method.get("name") == method:
                    if "steps" in installation_method and installation_method["steps"]:
                        return len(installation_method["steps"][0].get("description", []))
        
        return 6  # Default fallback
    
    def _get_timestamp_for_step(self, step_number):
        """Estimate timestamp in the video for a given step."""
        # This is a simple estimation based on the step number
        # In a real implementation, you would use actual timestamps from the knowledge base
        if step_number == 1:
            return "0:09"
        elif step_number == 2:
            return "0:20"
        elif step_number == 3:
            return "0:38"
        elif step_number in [4, 5]:
            return "0:50"
        else:
            return "1:24"
    
    def _extract_machine_type(self, message):
        """Extract machine type from message."""
        message = message.lower()
        
        if "fan" in message:
            return "Fan"
        elif "motor" in message:
            return "Motor"
        elif "pump" in message:
            return "Pump"
        
        return None
    
    def _extract_configuration(self, message):
        """Extract configuration from message."""
        message = message.lower()
        
        if "belt" in message:
            return "Belt Driven"
        elif "direct" in message or "close" in message or "coupled" in message:
            return "Direct/Close Coupled"
        elif "independent" in message or "bearing" in message:
            return "Independent Bearing"
        
        return None
    
    def _extract_orientation(self, message):
        """Extract orientation from message."""
        message = message.lower()
        
        if "center" in message:
            return "Center Hung"
        elif "over" in message:
            return "Overhung"
        
        return None
    
    def _extract_rpm(self, message):
        """Extract RPM from message."""
        match = re.search(r'(\d+)', message)
        if match:
            return int(match.group(1))
        return None
    
    def _extract_number(self, message):
        """Extract a number from message."""
        match = re.search(r'(\d+)', message)
        if match:
            return int(match.group(1))
        return None
    
    def _extract_monitoring_target(self, message):
        """Extract monitoring target from message."""
        message = message.lower()
        
        if "motor" in message:
            return "Motor"
        elif "bearing" in message:
            return "Bearing"
        elif "fan" in message:
            return "Fan"
        
        return None
    
    def _is_affirmative(self, message):
        """Check if message is affirmative."""
        affirmatives = ["yes", "yeah", "sure", "ok", "okay", "ready", "proceed", "continue"]
        message = message.lower()
        
        return any(word in message for word in affirmatives)