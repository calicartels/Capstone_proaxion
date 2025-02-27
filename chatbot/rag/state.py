# chatbot/state.py
"""
State management for chatbot conversations.
"""
from enum import Enum
import json

class ConversationStage(Enum):
    """Enumeration of conversation stages."""
    WELCOME = 0
    MACHINE_SELECTION = 1
    CONFIGURATION_SELECTION = 2
    ADDITIONAL_INFO = 3
    SENSOR_COUNT = 4
    RECOMMENDATION = 5
    INSTALLATION_START = 6
    INSTALLATION_STEPS = 7
    INSTALLATION_COMPLETE = 8

class ConversationState:
    """Manages the state of a conversation with a user."""
    
    def __init__(self):
        """Initialize the conversation state."""
        self.stage = ConversationStage.WELCOME
        self.machine_type = None
        self.configuration = None
        self.orientation = None  # e.g., center hung, overhung
        self.rpm = None
        self.sensor_count = None
        self.monitoring_target = None  # Specific part to monitor
        self.recommended_placement = []
        self.installation_method = None
        self.current_step = None
        self.installation_complete = False
        # Track any issues that occur during installation
        self.issues = []
    
    def to_dict(self):
        """Convert state to dictionary for storage."""
        return {
            "stage": self.stage.name,
            "machine_type": self.machine_type,
            "configuration": self.configuration,
            "orientation": self.orientation,
            "rpm": self.rpm,
            "sensor_count": self.sensor_count,
            "monitoring_target": self.monitoring_target,
            "recommended_placement": self.recommended_placement,
            "installation_method": self.installation_method,
            "current_step": self.current_step,
            "installation_complete": self.installation_complete,
            "issues": self.issues
        }
    
    def advance_stage(self):
        """Advance to the next conversation stage."""
        current_idx = self.stage.value
        next_idx = current_idx + 1
        
        # Ensure we don't go beyond the defined stages
        if next_idx < len(ConversationStage):
            self.stage = ConversationStage(next_idx)
    
    def add_issue(self, issue):
        """Add an installation issue or question."""
        self.issues.append(issue)
    
    def reset(self):
        """Reset the state to the beginning."""
        self.__init__()

class StateManager:
    """Manages conversation states for multiple users."""
    
    def __init__(self, storage_path=None):
        """Initialize the state manager."""
        self.states = {}
        self.storage_path = storage_path
        
        if storage_path:
            self._load_states()
    
    def get_state(self, user_id):
        """Get conversation state for a user."""
        # Create new state if none exists
        if user_id not in self.states:
            self.states[user_id] = ConversationState()
        
        return self.states[user_id]
    
    def save_state(self, user_id, state):
        """Save conversation state for a user."""
        self.states[user_id] = state
        
        if self.storage_path:
            self._save_states()
    
    def reset_state(self, user_id):
        """Reset conversation state for a user."""
        if user_id in self.states:
            self.states[user_id].reset()
            
            if self.storage_path:
                self._save_states()
    
    def _load_states(self):
        """Load states from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                state_dict = json.load(f)
                
                for user_id, state_data in state_dict.items():
                    self.states[user_id] = ConversationState.from_dict(state_data)
                    
            print(f"Loaded {len(self.states)} conversation states")
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"No valid state file found, starting fresh")
    
    def _save_states(self):
        """Save states to storage."""
        state_dict = {
            user_id: state.to_dict()
            for user_id, state in self.states.items()
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(state_dict, f, indent=2)