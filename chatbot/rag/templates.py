"""
Response templates and standardized messages for the installation chatbot.
"""

# Welcome and introduction messages
WELCOME_MESSAGE = """
👋 Welcome to the ProAxion Sensor Installation Assistant!

I'll help you determine the optimal sensor placement for your machine and guide you through the installation process step-by-step.

To get started, please tell me what type of machine you're working with: Fan, Motor, or Pump?
"""

# Machine type selection prompts
FAN_CONFIGURATION_PROMPT = """
Great! Let's set up your fan sensors.

What type of fan configuration do you have?
- Belt Driven: Uses belts and pulleys to connect motor and fan
- Direct/Close Coupled: Motor shaft directly connected to fan
- Independent Bearing: Separate bearing system for the fan shaft

Please select one of these options or describe your setup.
"""

MOTOR_CONFIGURATION_PROMPT = """
Great! Let's set up your motor sensors.

What type of motor configuration do you have?
- AC Induction Motor
- DC Motor
- Synchronous Motor
- Variable Frequency Drive (VFD)

Please select one of these options or describe your setup.
"""

PUMP_CONFIGURATION_PROMPT = """
Great! Let's set up your pump sensors.

What type of pump configuration do you have?
- Centrifugal Pump
- Positive Displacement Pump
- Submersible Pump
- Vertical Turbine Pump

Please select one of these options or describe your setup.
"""

# Additional information prompts
ORIENTATION_PROMPT = """
Is your {machine_type} center hung or overhung?

- Center Hung: Support on both sides of the {machine_type}
- Overhung: Support on only one side
"""

RPM_PROMPT = """
What is the operational speed of your {machine_type} in RPM?

This helps determine the optimal sensor configuration for your specific equipment.
"""

SENSOR_COUNT_PROMPT = """
How many sensors do you currently have available for installation?

This will help me recommend the most effective placement based on your available resources.
"""

MONITORING_TARGET_PROMPT = """
Is there a specific part of the machine you'd like to monitor?

For example:
- Motor bearings
- Fan housing
- Drive shaft
- Coupling

Or type "general" if you want a recommendation for overall monitoring.
"""

# Recommendation templates
RECOMMENDATION_TEMPLATE = """
Based on your {configuration} {machine_type} configuration, the ideal setup would be {ideal_count} sensors for comprehensive monitoring.

With your {sensor_count} available sensor(s), here's my recommendation for optimal placement:

{recommendations}

Would you like to proceed with the installation instructions?
"""

# Installation method templates
INSTALLATION_METHOD_PROMPT = """
For your {machine_type} configuration, I recommend the {recommended_method} installation method for the most secure and accurate readings.

Would you like to proceed with this method, or would you prefer to use a different method?
- Drill and Tap (recommended for permanent installations)
- Epoxy Mount (alternative permanent installation)
- Magnetic Mount (not recommended for vibration monitoring)
- Other Adapter Options
"""

INSTALLATION_START_TEMPLATE = """
Great! Let's install your sensor using the {method} method. I'll guide you through each step.

Here's what you'll need:
{materials}

Would you like to see the full installation video, or shall we proceed step by step?
- Show me the full video
- Guide me step by step
"""

INSTALLATION_MATERIALS = {
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
    ],
    "Magnets": [
        "Magnetic mount sensor",
        "Cleaning solvent",
        "Safety gloves"
    ],
    "Other Adapter Options": [
        "Appropriate adapter for your setup",
        "Mounting hardware",
        "Sensor"
    ]
}

# Step guidance templates
STEP_GUIDANCE_TEMPLATE = """
Step {step_number} of {total_steps}: {step_title}

{step_description}

Are you ready for the next step, or would you like to see a video of this step?
- I'm ready for the next step
- Show me a video of this step
- I need help with this step
"""

VIDEO_SEGMENT_TEMPLATE = """
Here's a video segment showing {title} ({start_time}-{end_time}):

[VIDEO: {video_path}]

Does this help with your current step?
"""

FULL_VIDEO_TEMPLATE = """
Here's the complete installation video ({duration}):

[VIDEO: {video_path}]

The video covers all steps from start to finish. Would you like me to also guide you through the specific steps?
- Yes, guide me through the steps
- No, I'll follow the video
"""

# Completion templates
INSTALLATION_COMPLETE_MESSAGE = """
Congratulations! You've successfully installed your sensor using the {method} method.

After installation, please check that:
1. The sensor is properly secured
2. The sensor cable is not under tension
3. The sensor is not in contact with moving parts
4. The sensor readings appear in your monitoring system

Is everything working correctly?
"""

SUCCESSFUL_INSTALLATION_MESSAGE = """
Great! Your sensor installation is complete. 

If you have any questions in the future or need to install more sensors, just let me know.

Would you like assistance with anything else?
"""

# Help and support templates
HELP_OPTIONS_MESSAGE = """
I understand installation can be challenging. Would you like me to:
1. Give more detailed instructions for this step
2. Show you a video for this part specifically
3. Connect you with ProAxion support
"""

SUPPORT_ESCALATION_MESSAGE = """
I'll be happy to connect you with our experts. Please fill out this form and a ProAxion representative will contact you:
[FORM LINK: https://www.proaxion.io/support]

In the meantime, you can review our installation guides or call our technical support line at 1-800-555-0123.
"""

INSTALLATION_ISSUE_MESSAGE = """
I understand you're experiencing an issue. Let me connect you with ProAxion support for assistance.

Please contact support@proaxion.io and mention the following issues:
1. Problem with sensor installation
2. {specific_issues}

In the meantime, please verify:
- The sensor is firmly attached
- Connections are secure
- No obstructions are present
"""

# Error and fallback messages
MACHINE_TYPE_ERROR = "I didn't understand your machine type. Please specify: Fans, Motors, or Pumps."

CONFIGURATION_ERROR = "Please specify your {machine_type} configuration from the options provided."

ORIENTATION_ERROR = "Please specify if your {machine_type} is center hung or overhung."

RPM_ERROR = "Please provide the operational speed in RPM (e.g., 1750)."

SENSOR_COUNT_ERROR = "Please provide the number of sensors you have available."

UNCLEAR_RESPONSE_ERROR = "I'm not sure I understood your response. {prompt}"

RESET_MESSAGE = """
Let's start over. 

I'll help you determine the optimal sensor placement for your machine and guide you through the installation process.

What type of machine are you working with: Fan, Motor, or Pump?
"""