#!/usr/bin/env python3
"""
Mission Control Examples

Demonstrates various mission scenarios using the Mission Control Test System.
"""

import json
import time
from mission_control import MissionControl, MissionStatus


def print_separator(title):
    """Print a formatted separator for different examples"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def example_mars_mission():
    """Example: Complete Mars mission lifecycle"""
    print_separator("MARS SAMPLE COLLECTION MISSION")
    
    mc = MissionControl()
    
    # Create Mars mission
    mission = mc.create_mission(
        "MARS_2024_001", 
        "Mars Sample Collection Mission",
        [
            "Launch from Earth",
            "Navigate to Mars",
            "Enter Mars orbit",
            "Land on Mars surface",
            "Collect geological samples",
            "Return to orbit",
            "Navigate back to Earth"
        ]
    )
    
    print(f"Created mission: {mission.name}")
    print(f"Objectives: {len(mission.objectives)}")
    
    # Start mission
    mc.start_mission("MARS_2024_001")
    print(f"Mission started: {mission.start_time}")
    
    # Launch sequence
    print("\n--- Launch Sequence ---")
    cmd1 = mc.send_command("MARS_2024_001", "ignition")
    mc.execute_command("MARS_2024_001", cmd1)
    print("✓ Engine ignition completed")
    
    # Add launch telemetry
    mc.add_telemetry("MARS_2024_001", 0.0, 0.0, 100.0, "pre_launch")
    mc.add_telemetry("MARS_2024_001", 1000.0, 100.0, 95.0, "ascending")
    mc.add_telemetry("MARS_2024_001", 50000.0, 1500.0, 85.0, "in_space")
    
    # Course corrections
    print("\n--- Navigation Phase ---")
    cmd2 = mc.send_command("MARS_2024_001", "adjust_course", {"heading": "Mars trajectory"})
    mc.execute_command("MARS_2024_001", cmd2)
    print("✓ Course adjusted for Mars")
    
    # Add cruise telemetry
    mc.add_telemetry("MARS_2024_001", 100000.0, 25000.0, 75.0, "cruise")
    mc.add_telemetry("MARS_2024_001", 200000.0, 30000.0, 65.0, "cruise")
    
    # Mars operations
    print("\n--- Mars Operations ---")
    cmd3 = mc.send_command("MARS_2024_001", "collect_sample", {"location": "Olympus Mons"})
    cmd4 = mc.send_command("MARS_2024_001", "collect_sample", {"location": "Valles Marineris"})
    mc.execute_command("MARS_2024_001", cmd3)
    mc.execute_command("MARS_2024_001", cmd4)
    print("✓ Samples collected from Olympus Mons")
    print("✓ Samples collected from Valles Marineris")
    
    # Mars surface telemetry
    mc.add_telemetry("MARS_2024_001", 0.0, 0.0, 60.0, "landed_mars")
    mc.add_telemetry("MARS_2024_001", 1000.0, 50.0, 55.0, "ascending_mars")
    
    # Return journey
    print("\n--- Return Journey ---")
    cmd5 = mc.send_command("MARS_2024_001", "adjust_course", {"heading": "Earth trajectory"})
    mc.execute_command("MARS_2024_001", cmd5)
    print("✓ Course set for Earth return")
    
    # Final telemetry
    mc.add_telemetry("MARS_2024_001", 150000.0, 28000.0, 40.0, "return_cruise")
    mc.add_telemetry("MARS_2024_001", 50000.0, 15000.0, 30.0, "approaching_earth")
    
    # Complete mission
    mc.complete_mission("MARS_2024_001")
    print(f"\n✓ Mission completed: {mission.end_time}")
    
    # Mission summary
    status = mc.get_mission_status("MARS_2024_001")
    print(f"\nMission Summary:")
    print(f"  Total commands executed: {status['completed_commands']}")
    print(f"  Failed commands: {status['failed_commands']}")
    print(f"  Telemetry readings: {len(status['mission']['telemetry'])}")
    print(f"  Final fuel level: {status['latest_telemetry']['fuel_level']}%")


def example_multiple_missions():
    """Example: Managing multiple concurrent missions"""
    print_separator("MULTIPLE MISSION MANAGEMENT")
    
    mc = MissionControl()
    
    # Create multiple missions
    missions = [
        ("LUNAR_001", "Lunar Base Setup", ["Land on Moon", "Deploy equipment", "Establish base"]),
        ("SAT_001", "Communications Satellite", ["Deploy satellite", "Test communications"]),
        ("ISS_001", "ISS Resupply", ["Dock with ISS", "Transfer supplies", "Return to Earth"])
    ]
    
    for mission_id, name, objectives in missions:
        mc.create_mission(mission_id, name, objectives)
        print(f"Created mission: {name}")
    
    # Start lunar mission
    mc.start_mission("LUNAR_001")
    print(f"\nStarted: Lunar Base Setup")
    
    # Execute lunar commands
    cmd1 = mc.send_command("LUNAR_001", "ignition")
    mc.execute_command("LUNAR_001", cmd1)
    mc.add_telemetry("LUNAR_001", 25000.0, 800.0, 90.0, "en_route_moon")
    
    # Start satellite mission
    mc.start_mission("SAT_001")
    print("Started: Communications Satellite")
    
    # Execute satellite commands
    cmd2 = mc.send_command("SAT_001", "ignition")
    mc.execute_command("SAT_001", cmd2)
    mc.add_telemetry("SAT_001", 35000.0, 1200.0, 85.0, "deploying")
    
    # Complete satellite mission quickly
    mc.complete_mission("SAT_001")
    print("✓ Satellite mission completed")
    
    # Continue lunar mission
    cmd3 = mc.send_command("LUNAR_001", "collect_sample", {"location": "Sea of Tranquility"})
    mc.execute_command("LUNAR_001", cmd3)
    mc.add_telemetry("LUNAR_001", 0.0, 0.0, 70.0, "lunar_surface")
    
    # Start ISS mission
    mc.start_mission("ISS_001")
    print("Started: ISS Resupply")
    
    # Get status of all missions
    all_missions = mc.get_all_missions()
    print(f"\nCurrent mission status:")
    for mission in all_missions:
        print(f"  {mission['name']}: {mission['status']}")
    
    # Complete remaining missions
    mc.complete_mission("LUNAR_001")
    mc.complete_mission("ISS_001")
    print("\n✓ All missions completed")


def example_mission_abort():
    """Example: Mission abort scenario"""
    print_separator("MISSION ABORT SCENARIO")
    
    mc = MissionControl()
    
    # Create a mission
    mc.create_mission("EMERGENCY_001", "Deep Space Probe", 
                     ["Launch", "Navigate to asteroid", "Study asteroid"])
    
    mc.start_mission("EMERGENCY_001")
    print("Mission started: Deep Space Probe")
    
    # Initial operations
    cmd1 = mc.send_command("EMERGENCY_001", "ignition")
    mc.execute_command("EMERGENCY_001", cmd1)
    print("✓ Launch successful")
    
    # Add normal telemetry
    mc.add_telemetry("EMERGENCY_001", 45000.0, 2000.0, 88.0, "nominal")
    mc.add_telemetry("EMERGENCY_001", 80000.0, 3500.0, 82.0, "nominal")
    
    # Simulate system problem
    mc.add_telemetry("EMERGENCY_001", 85000.0, 3200.0, 78.0, "warning")
    print("⚠ System warning detected")
    
    mc.add_telemetry("EMERGENCY_001", 82000.0, 2800.0, 75.0, "critical")
    print("🚨 Critical system failure detected")
    
    # Abort mission
    mc.abort_mission("EMERGENCY_001")
    print("🔴 Mission aborted due to critical failure")
    
    # Get final status
    status = mc.get_mission_status("EMERGENCY_001")
    print(f"\nAbort Summary:")
    print(f"  Mission status: {status['mission']['status']}")
    print(f"  Commands completed: {status['completed_commands']}")
    print(f"  Final system health: {status['latest_telemetry']['system_health']}")
    print(f"  Abort time: {status['mission']['end_time']}")


def example_command_failures():
    """Example: Handling command failures"""
    print_separator("COMMAND FAILURE HANDLING")
    
    mc = MissionControl()
    
    # Create mission
    mc.create_mission("TEST_001", "Command Testing Mission", ["Test various commands"])
    mc.start_mission("TEST_001")
    print("Mission started: Command Testing")
    
    # Mix of successful and failed commands
    commands = [
        ("ignition", {}),
        ("adjust_course", {"heading": "90 degrees"}),
        ("unknown_command", {}),  # This will fail
        ("collect_sample", {"location": "Test Site"}),
        ("invalid_command_type", {"param": "value"}),  # This will fail
    ]
    
    print("\nExecuting commands:")
    for cmd_type, params in commands:
        cmd_id = mc.send_command("TEST_001", cmd_type, params)
        success = mc.execute_command("TEST_001", cmd_id)
        
        # Get command result
        mission = mc.missions["TEST_001"]
        command = next(cmd for cmd in mission.commands if cmd.id == cmd_id)
        
        status_icon = "✓" if success else "✗"
        print(f"  {status_icon} {cmd_type}: {command.result}")
    
    # Add telemetry
    mc.add_telemetry("TEST_001", 15000.0, 500.0, 70.0, "testing_complete")
    
    # Complete mission
    mc.complete_mission("TEST_001")
    
    # Final status
    status = mc.get_mission_status("TEST_001")
    print(f"\nCommand Test Summary:")
    print(f"  Successful commands: {status['completed_commands']}")
    print(f"  Failed commands: {status['failed_commands']}")
    print(f"  Success rate: {status['completed_commands']/(status['completed_commands']+status['failed_commands'])*100:.1f}%")


def main():
    """Run all examples"""
    print("Mission Control Test System - Examples")
    print("=====================================")
    
    # Run all examples
    example_mars_mission()
    example_multiple_missions()
    example_mission_abort()
    example_command_failures()
    
    print_separator("ALL EXAMPLES COMPLETED")
    print("Mission Control Test System examples completed successfully!")


if __name__ == "__main__":
    main()