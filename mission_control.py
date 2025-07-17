#!/usr/bin/env python3
"""
Mission Control Test System

A simple simulation of a mission control system for testing purposes.
Provides basic functionality for mission management, command execution,
and telemetry monitoring.
"""

import time
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


class MissionStatus(Enum):
    """Mission status enumeration"""
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    ABORTED = "aborted"
    FAILED = "failed"


class CommandStatus(Enum):
    """Command execution status"""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Telemetry:
    """Telemetry data structure"""
    timestamp: str
    altitude: float
    velocity: float
    fuel_level: float
    system_health: str


@dataclass
class Command:
    """Command data structure"""
    id: str
    type: str
    parameters: Dict[str, Any]
    status: CommandStatus
    timestamp: str
    result: Optional[str] = None


@dataclass
class Mission:
    """Mission data structure"""
    id: str
    name: str
    status: MissionStatus
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    objectives: List[str] = None
    telemetry: List[Telemetry] = None
    commands: List[Command] = None

    def __post_init__(self):
        if self.objectives is None:
            self.objectives = []
        if self.telemetry is None:
            self.telemetry = []
        if self.commands is None:
            self.commands = []


class MissionControl:
    """Main Mission Control System"""
    
    def __init__(self):
        self.missions: Dict[str, Mission] = {}
        self.active_mission: Optional[str] = None
    
    def create_mission(self, mission_id: str, name: str, objectives: List[str] = None) -> Mission:
        """Create a new mission"""
        if mission_id in self.missions:
            raise ValueError(f"Mission {mission_id} already exists")
        
        mission = Mission(
            id=mission_id,
            name=name,
            status=MissionStatus.PLANNED,
            objectives=objectives or []
        )
        
        self.missions[mission_id] = mission
        return mission
    
    def start_mission(self, mission_id: str) -> bool:
        """Start a mission"""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        
        mission = self.missions[mission_id]
        if mission.status != MissionStatus.PLANNED:
            return False
        
        mission.status = MissionStatus.ACTIVE
        mission.start_time = datetime.now().isoformat()
        self.active_mission = mission_id
        
        return True
    
    def abort_mission(self, mission_id: str) -> bool:
        """Abort a mission"""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        
        mission = self.missions[mission_id]
        if mission.status != MissionStatus.ACTIVE:
            return False
        
        mission.status = MissionStatus.ABORTED
        mission.end_time = datetime.now().isoformat()
        
        if self.active_mission == mission_id:
            self.active_mission = None
        
        return True
    
    def complete_mission(self, mission_id: str) -> bool:
        """Complete a mission successfully"""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        
        mission = self.missions[mission_id]
        if mission.status != MissionStatus.ACTIVE:
            return False
        
        mission.status = MissionStatus.COMPLETED
        mission.end_time = datetime.now().isoformat()
        
        if self.active_mission == mission_id:
            self.active_mission = None
        
        return True
    
    def send_command(self, mission_id: str, command_type: str, parameters: Dict[str, Any] = None) -> str:
        """Send a command to a mission"""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        
        mission = self.missions[mission_id]
        if mission.status != MissionStatus.ACTIVE:
            raise ValueError(f"Cannot send commands to inactive mission {mission_id}")
        
        command_id = f"cmd_{len(mission.commands) + 1:04d}"
        command = Command(
            id=command_id,
            type=command_type,
            parameters=parameters or {},
            status=CommandStatus.PENDING,
            timestamp=datetime.now().isoformat()
        )
        
        mission.commands.append(command)
        return command_id
    
    def execute_command(self, mission_id: str, command_id: str) -> bool:
        """Execute a pending command"""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        
        mission = self.missions[mission_id]
        command = None
        
        for cmd in mission.commands:
            if cmd.id == command_id:
                command = cmd
                break
        
        if not command:
            raise ValueError(f"Command {command_id} not found")
        
        if command.status != CommandStatus.PENDING:
            return False
        
        # Simulate command execution
        command.status = CommandStatus.EXECUTING
        time.sleep(0.1)  # Simulate processing time
        
        # Simple command simulation
        if command.type == "ignition":
            command.result = "Engine ignited successfully"
            command.status = CommandStatus.COMPLETED
        elif command.type == "adjust_course":
            course = command.parameters.get("heading", "unknown")
            command.result = f"Course adjusted to {course}"
            command.status = CommandStatus.COMPLETED
        elif command.type == "collect_sample":
            location = command.parameters.get("location", "unknown")
            command.result = f"Sample collected at {location}"
            command.status = CommandStatus.COMPLETED
        else:
            command.result = f"Unknown command type: {command.type}"
            command.status = CommandStatus.FAILED
        
        return command.status == CommandStatus.COMPLETED
    
    def add_telemetry(self, mission_id: str, altitude: float, velocity: float, fuel_level: float, system_health: str = "nominal") -> None:
        """Add telemetry data to a mission"""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        
        mission = self.missions[mission_id]
        telemetry = Telemetry(
            timestamp=datetime.now().isoformat(),
            altitude=altitude,
            velocity=velocity,
            fuel_level=fuel_level,
            system_health=system_health
        )
        
        mission.telemetry.append(telemetry)
    
    def get_mission_status(self, mission_id: str) -> Dict[str, Any]:
        """Get comprehensive mission status"""
        if mission_id not in self.missions:
            raise ValueError(f"Mission {mission_id} not found")
        
        mission = self.missions[mission_id]
        return {
            "mission": asdict(mission),
            "active_commands": len([cmd for cmd in mission.commands if cmd.status in [CommandStatus.PENDING, CommandStatus.EXECUTING]]),
            "completed_commands": len([cmd for cmd in mission.commands if cmd.status == CommandStatus.COMPLETED]),
            "failed_commands": len([cmd for cmd in mission.commands if cmd.status == CommandStatus.FAILED]),
            "latest_telemetry": asdict(mission.telemetry[-1]) if mission.telemetry else None
        }
    
    def get_all_missions(self) -> List[Dict[str, Any]]:
        """Get status of all missions"""
        return [
            {
                "id": mission.id,
                "name": mission.name,
                "status": mission.status.value,
                "start_time": mission.start_time,
                "end_time": mission.end_time,
                "commands_count": len(mission.commands),
                "telemetry_count": len(mission.telemetry)
            }
            for mission in self.missions.values()
        ]


def main():
    """Demo of the mission control system"""
    mc = MissionControl()
    
    # Create a test mission
    mission = mc.create_mission("MARS_001", "Mars Sample Collection", 
                               ["Land on Mars", "Collect samples", "Return to orbit"])
    
    print(f"Created mission: {mission.name}")
    print(f"Mission status: {mission.status.value}")
    
    # Start the mission
    mc.start_mission("MARS_001")
    print(f"Mission started at: {mission.start_time}")
    
    # Send some commands
    cmd1 = mc.send_command("MARS_001", "ignition")
    cmd2 = mc.send_command("MARS_001", "adjust_course", {"heading": "270 degrees"})
    cmd3 = mc.send_command("MARS_001", "collect_sample", {"location": "Olympus Mons"})
    
    print(f"Sent commands: {cmd1}, {cmd2}, {cmd3}")
    
    # Execute commands
    mc.execute_command("MARS_001", cmd1)
    mc.execute_command("MARS_001", cmd2)
    mc.execute_command("MARS_001", cmd3)
    
    # Add some telemetry
    mc.add_telemetry("MARS_001", 15000.0, 250.0, 75.5, "nominal")
    mc.add_telemetry("MARS_001", 12000.0, 200.0, 70.2, "nominal")
    
    # Get mission status
    status = mc.get_mission_status("MARS_001")
    print(f"\nMission Status:")
    print(f"  Status: {status['mission']['status']}")
    print(f"  Completed commands: {status['completed_commands']}")
    print(f"  Latest altitude: {status['latest_telemetry']['altitude']} km")
    
    # Complete the mission
    mc.complete_mission("MARS_001")
    print(f"\nMission completed at: {mission.end_time}")


if __name__ == "__main__":
    main()