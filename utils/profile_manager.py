"""
Game Profile Management for Zio-Booster FPS Booster
"""
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class GameProfile:
    """Represents a game profile with custom optimization settings"""
    name: str
    executable_path: str = ""
    temp_threshold: float = 70.0
    optimize_network: bool = True
    high_priority: bool = True
    auto_optimize: bool = True
    created_at: str = ""
    last_used: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.last_used:
            self.last_used = self.created_at

class ProfileManager:
    """Manages game profiles and their optimization settings"""
    
    def __init__(self, profiles_file: str = "game_profiles.json"):
        self.profiles_file = profiles_file
        self.profiles: Dict[str, GameProfile] = {}
        self.load_profiles()
    
    def load_profiles(self):
        """Load game profiles from file"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    data = json.load(f)
                    for name, profile_data in data.items():
                        # Convert dict back to GameProfile
                        profile = GameProfile(
                            name=profile_data['name'],
                            executable_path=profile_data['executable_path'],
                            temp_threshold=profile_data['temp_threshold'],
                            optimize_network=profile_data['optimize_network'],
                            high_priority=profile_data['high_priority'],
                            auto_optimize=profile_data['auto_optimize'],
                            created_at=profile_data['created_at'],
                            last_used=profile_data['last_used']
                        )
                        self.profiles[name] = profile
            except Exception as e:
                print(f"Error loading profiles: {e}")
    
    def save_profiles(self):
        """Save game profiles to file"""
        try:
            data = {name: asdict(profile) for name, profile in self.profiles.items()}
            with open(self.profiles_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving profiles: {e}")
    
    def create_profile(self, name: str, executable_path: str = "", **kwargs) -> GameProfile:
        """Create a new game profile"""
        profile = GameProfile(
            name=name,
            executable_path=executable_path,
            **kwargs
        )
        self.profiles[name] = profile
        self.save_profiles()
        return profile
    
    def get_profile(self, name: str) -> Optional[GameProfile]:
        """Get a game profile by name"""
        return self.profiles.get(name)
    
    def update_profile(self, name: str, **kwargs) -> bool:
        """Update a game profile with new settings"""
        if name in self.profiles:
            profile = self.profiles[name]
            for key, value in kwargs.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            profile.last_used = datetime.now().isoformat()
            self.save_profiles()
            return True
        return False
    
    def delete_profile(self, name: str) -> bool:
        """Delete a game profile"""
        if name in self.profiles:
            del self.profiles[name]
            self.save_profiles()
            return True
        return False
    
    def list_profiles(self) -> List[GameProfile]:
        """List all game profiles"""
        return list(self.profiles.values())
    
    def apply_profile_settings(self, name: str, optimizer) -> bool:
        """Apply optimization settings from a profile to the system optimizer"""
        profile = self.get_profile(name)
        if profile:
            # Update optimizer settings based on profile
            # For now, we'll just return True to indicate the profile exists
            # In a real implementation, we'd modify the optimizer's behavior
            return True
        return False

# Example usage
if __name__ == "__main__":
    # Create a profile manager
    pm = ProfileManager()
    
    # Create a profile for a game
    profile = pm.create_profile(
        name="Cyberpunk 2077",
        executable_path="C:/Games/Cyberpunk 2077/bin/x64/Cyberpunk2077.exe",
        temp_threshold=65.0,
        optimize_network=True,
        high_priority=True,
        auto_optimize=True
    )
    
    print(f"Created profile: {profile.name}")
    print(f"All profiles: {[p.name for p in pm.list_profiles()]}")