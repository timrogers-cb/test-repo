#!/usr/bin/env python3
"""
Test suite for Mission Control System

Comprehensive tests for all mission control functionality including
mission lifecycle, command execution, telemetry handling, and error cases.
"""

import unittest
import time
from datetime import datetime
from mission_control import (
    MissionControl, MissionStatus, CommandStatus,
    Mission, Command, Telemetry
)


class TestMissionControl(unittest.TestCase):
    """Test cases for Mission Control System"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.mc = MissionControl()
    
    def test_create_mission(self):
        """Test mission creation"""
        mission = self.mc.create_mission("TEST_001", "Test Mission", ["Objective 1", "Objective 2"])
        
        self.assertEqual(mission.id, "TEST_001")
        self.assertEqual(mission.name, "Test Mission")
        self.assertEqual(mission.status, MissionStatus.PLANNED)
        self.assertEqual(len(mission.objectives), 2)
        self.assertIsNone(mission.start_time)
        self.assertIsNone(mission.end_time)
        self.assertEqual(len(mission.commands), 0)
        self.assertEqual(len(mission.telemetry), 0)
    
    def test_create_duplicate_mission(self):
        """Test that creating duplicate mission raises error"""
        self.mc.create_mission("DUP_001", "First Mission")
        
        with self.assertRaises(ValueError) as context:
            self.mc.create_mission("DUP_001", "Duplicate Mission")
        
        self.assertIn("already exists", str(context.exception))
    
    def test_start_mission(self):
        """Test starting a mission"""
        self.mc.create_mission("START_001", "Start Test Mission")
        result = self.mc.start_mission("START_001")
        
        self.assertTrue(result)
        mission = self.mc.missions["START_001"]
        self.assertEqual(mission.status, MissionStatus.ACTIVE)
        self.assertIsNotNone(mission.start_time)
        self.assertEqual(self.mc.active_mission, "START_001")
    
    def test_start_nonexistent_mission(self):
        """Test starting a mission that doesn't exist"""
        with self.assertRaises(ValueError) as context:
            self.mc.start_mission("NONEXISTENT")
        
        self.assertIn("not found", str(context.exception))
    
    def test_start_already_active_mission(self):
        """Test starting a mission that's already active"""
        self.mc.create_mission("ACTIVE_001", "Already Active Mission")
        self.mc.start_mission("ACTIVE_001")
        
        # Try to start again
        result = self.mc.start_mission("ACTIVE_001")
        self.assertFalse(result)
    
    def test_abort_mission(self):
        """Test aborting an active mission"""
        self.mc.create_mission("ABORT_001", "Abort Test Mission")
        self.mc.start_mission("ABORT_001")
        
        result = self.mc.abort_mission("ABORT_001")
        
        self.assertTrue(result)
        mission = self.mc.missions["ABORT_001"]
        self.assertEqual(mission.status, MissionStatus.ABORTED)
        self.assertIsNotNone(mission.end_time)
        self.assertIsNone(self.mc.active_mission)
    
    def test_abort_inactive_mission(self):
        """Test aborting an inactive mission"""
        self.mc.create_mission("INACTIVE_001", "Inactive Mission")
        
        result = self.mc.abort_mission("INACTIVE_001")
        self.assertFalse(result)
    
    def test_complete_mission(self):
        """Test completing an active mission"""
        self.mc.create_mission("COMPLETE_001", "Complete Test Mission")
        self.mc.start_mission("COMPLETE_001")
        
        result = self.mc.complete_mission("COMPLETE_001")
        
        self.assertTrue(result)
        mission = self.mc.missions["COMPLETE_001"]
        self.assertEqual(mission.status, MissionStatus.COMPLETED)
        self.assertIsNotNone(mission.end_time)
        self.assertIsNone(self.mc.active_mission)
    
    def test_send_command(self):
        """Test sending a command to an active mission"""
        self.mc.create_mission("CMD_001", "Command Test Mission")
        self.mc.start_mission("CMD_001")
        
        command_id = self.mc.send_command("CMD_001", "test_command", {"param1": "value1"})
        
        self.assertIsNotNone(command_id)
        mission = self.mc.missions["CMD_001"]
        self.assertEqual(len(mission.commands), 1)
        
        command = mission.commands[0]
        self.assertEqual(command.id, command_id)
        self.assertEqual(command.type, "test_command")
        self.assertEqual(command.parameters["param1"], "value1")
        self.assertEqual(command.status, CommandStatus.PENDING)
    
    def test_send_command_to_inactive_mission(self):
        """Test sending command to inactive mission raises error"""
        self.mc.create_mission("INACTIVE_CMD", "Inactive Command Mission")
        
        with self.assertRaises(ValueError) as context:
            self.mc.send_command("INACTIVE_CMD", "test_command")
        
        self.assertIn("inactive mission", str(context.exception))
    
    def test_execute_ignition_command(self):
        """Test executing an ignition command"""
        self.mc.create_mission("IGNITION_001", "Ignition Test Mission")
        self.mc.start_mission("IGNITION_001")
        
        command_id = self.mc.send_command("IGNITION_001", "ignition")
        result = self.mc.execute_command("IGNITION_001", command_id)
        
        self.assertTrue(result)
        mission = self.mc.missions["IGNITION_001"]
        command = mission.commands[0]
        self.assertEqual(command.status, CommandStatus.COMPLETED)
        self.assertIn("ignited successfully", command.result)
    
    def test_execute_course_adjustment_command(self):
        """Test executing a course adjustment command"""
        self.mc.create_mission("COURSE_001", "Course Test Mission")
        self.mc.start_mission("COURSE_001")
        
        command_id = self.mc.send_command("COURSE_001", "adjust_course", {"heading": "180 degrees"})
        result = self.mc.execute_command("COURSE_001", command_id)
        
        self.assertTrue(result)
        mission = self.mc.missions["COURSE_001"]
        command = mission.commands[0]
        self.assertEqual(command.status, CommandStatus.COMPLETED)
        self.assertIn("180 degrees", command.result)
    
    def test_execute_sample_collection_command(self):
        """Test executing a sample collection command"""
        self.mc.create_mission("SAMPLE_001", "Sample Test Mission")
        self.mc.start_mission("SAMPLE_001")
        
        command_id = self.mc.send_command("SAMPLE_001", "collect_sample", {"location": "Mars North Pole"})
        result = self.mc.execute_command("SAMPLE_001", command_id)
        
        self.assertTrue(result)
        mission = self.mc.missions["SAMPLE_001"]
        command = mission.commands[0]
        self.assertEqual(command.status, CommandStatus.COMPLETED)
        self.assertIn("Mars North Pole", command.result)
    
    def test_execute_unknown_command(self):
        """Test executing an unknown command type"""
        self.mc.create_mission("UNKNOWN_001", "Unknown Command Test Mission")
        self.mc.start_mission("UNKNOWN_001")
        
        command_id = self.mc.send_command("UNKNOWN_001", "unknown_command")
        result = self.mc.execute_command("UNKNOWN_001", command_id)
        
        self.assertFalse(result)
        mission = self.mc.missions["UNKNOWN_001"]
        command = mission.commands[0]
        self.assertEqual(command.status, CommandStatus.FAILED)
        self.assertIn("Unknown command type", command.result)
    
    def test_execute_nonexistent_command(self):
        """Test executing a command that doesn't exist"""
        self.mc.create_mission("NONCMD_001", "Non-command Test Mission")
        self.mc.start_mission("NONCMD_001")
        
        with self.assertRaises(ValueError) as context:
            self.mc.execute_command("NONCMD_001", "nonexistent_cmd")
        
        self.assertIn("not found", str(context.exception))
    
    def test_add_telemetry(self):
        """Test adding telemetry data"""
        self.mc.create_mission("TELEM_001", "Telemetry Test Mission")
        
        self.mc.add_telemetry("TELEM_001", 10000.0, 300.0, 85.5, "nominal")
        
        mission = self.mc.missions["TELEM_001"]
        self.assertEqual(len(mission.telemetry), 1)
        
        telemetry = mission.telemetry[0]
        self.assertEqual(telemetry.altitude, 10000.0)
        self.assertEqual(telemetry.velocity, 300.0)
        self.assertEqual(telemetry.fuel_level, 85.5)
        self.assertEqual(telemetry.system_health, "nominal")
        self.assertIsNotNone(telemetry.timestamp)
    
    def test_add_multiple_telemetry(self):
        """Test adding multiple telemetry readings"""
        self.mc.create_mission("MULTI_TELEM", "Multi Telemetry Test Mission")
        
        self.mc.add_telemetry("MULTI_TELEM", 10000.0, 300.0, 85.5)
        self.mc.add_telemetry("MULTI_TELEM", 9500.0, 280.0, 83.2)
        self.mc.add_telemetry("MULTI_TELEM", 9000.0, 260.0, 80.8)
        
        mission = self.mc.missions["MULTI_TELEM"]
        self.assertEqual(len(mission.telemetry), 3)
        
        # Check that values are decreasing (as expected for a landing)
        self.assertGreater(mission.telemetry[0].altitude, mission.telemetry[1].altitude)
        self.assertGreater(mission.telemetry[1].altitude, mission.telemetry[2].altitude)
    
    def test_get_mission_status(self):
        """Test getting comprehensive mission status"""
        self.mc.create_mission("STATUS_001", "Status Test Mission", ["Test objective"])
        self.mc.start_mission("STATUS_001")
        
        # Add some commands
        cmd1 = self.mc.send_command("STATUS_001", "ignition")
        cmd2 = self.mc.send_command("STATUS_001", "unknown_command")
        self.mc.execute_command("STATUS_001", cmd1)  # This should succeed
        self.mc.execute_command("STATUS_001", cmd2)  # This should fail
        
        # Add telemetry
        self.mc.add_telemetry("STATUS_001", 5000.0, 150.0, 60.0, "nominal")
        
        status = self.mc.get_mission_status("STATUS_001")
        
        self.assertEqual(status["mission"]["id"], "STATUS_001")
        self.assertEqual(status["mission"]["status"], MissionStatus.ACTIVE)
        self.assertEqual(status["completed_commands"], 1)
        self.assertEqual(status["failed_commands"], 1)
        self.assertEqual(status["active_commands"], 0)
        self.assertEqual(status["latest_telemetry"]["altitude"], 5000.0)
    
    def test_get_mission_status_nonexistent(self):
        """Test getting status of nonexistent mission"""
        with self.assertRaises(ValueError) as context:
            self.mc.get_mission_status("NONEXISTENT")
        
        self.assertIn("not found", str(context.exception))
    
    def test_get_all_missions(self):
        """Test getting status of all missions"""
        # Create multiple missions
        self.mc.create_mission("ALL_001", "First Mission")
        self.mc.create_mission("ALL_002", "Second Mission")
        self.mc.start_mission("ALL_001")
        
        # Add some data to first mission before completing it
        self.mc.send_command("ALL_001", "test_command")
        self.mc.complete_mission("ALL_001")
        
        # Add telemetry to second mission
        self.mc.add_telemetry("ALL_002", 1000.0, 50.0, 90.0)
        
        all_missions = self.mc.get_all_missions()
        
        self.assertEqual(len(all_missions), 2)
        
        # Find missions by ID
        mission1 = next(m for m in all_missions if m["id"] == "ALL_001")
        mission2 = next(m for m in all_missions if m["id"] == "ALL_002")
        
        self.assertEqual(mission1["status"], "completed")
        self.assertEqual(mission1["commands_count"], 1)
        
        self.assertEqual(mission2["status"], "planned")
        self.assertEqual(mission2["telemetry_count"], 1)
    
    def test_mission_lifecycle_complete(self):
        """Test complete mission lifecycle"""
        # Create mission
        mission = self.mc.create_mission("LIFECYCLE_001", "Complete Lifecycle Test", 
                                        ["Launch", "Navigate", "Land"])
        self.assertEqual(mission.status, MissionStatus.PLANNED)
        
        # Start mission
        self.mc.start_mission("LIFECYCLE_001")
        self.assertEqual(mission.status, MissionStatus.ACTIVE)
        self.assertEqual(self.mc.active_mission, "LIFECYCLE_001")
        
        # Execute mission commands
        cmd1 = self.mc.send_command("LIFECYCLE_001", "ignition")
        cmd2 = self.mc.send_command("LIFECYCLE_001", "adjust_course", {"heading": "45 degrees"})
        cmd3 = self.mc.send_command("LIFECYCLE_001", "collect_sample", {"location": "Landing Zone Alpha"})
        
        self.mc.execute_command("LIFECYCLE_001", cmd1)
        self.mc.execute_command("LIFECYCLE_001", cmd2)
        self.mc.execute_command("LIFECYCLE_001", cmd3)
        
        # Add telemetry throughout mission
        self.mc.add_telemetry("LIFECYCLE_001", 20000.0, 500.0, 95.0, "nominal")
        self.mc.add_telemetry("LIFECYCLE_001", 15000.0, 400.0, 90.0, "nominal")
        self.mc.add_telemetry("LIFECYCLE_001", 1000.0, 50.0, 85.0, "landing_sequence")
        self.mc.add_telemetry("LIFECYCLE_001", 0.0, 0.0, 82.0, "landed")
        
        # Complete mission
        self.mc.complete_mission("LIFECYCLE_001")
        self.assertEqual(mission.status, MissionStatus.COMPLETED)
        self.assertIsNone(self.mc.active_mission)
        
        # Verify final status
        status = self.mc.get_mission_status("LIFECYCLE_001")
        self.assertEqual(status["completed_commands"], 3)
        self.assertEqual(status["failed_commands"], 0)
        self.assertEqual(len(status["mission"]["telemetry"]), 4)
        self.assertEqual(status["latest_telemetry"]["system_health"], "landed")


class TestDataStructures(unittest.TestCase):
    """Test the data structures used in mission control"""
    
    def test_mission_enum_values(self):
        """Test mission status enum values"""
        self.assertEqual(MissionStatus.PLANNED.value, "planned")
        self.assertEqual(MissionStatus.ACTIVE.value, "active")
        self.assertEqual(MissionStatus.COMPLETED.value, "completed")
        self.assertEqual(MissionStatus.ABORTED.value, "aborted")
        self.assertEqual(MissionStatus.FAILED.value, "failed")
    
    def test_command_enum_values(self):
        """Test command status enum values"""
        self.assertEqual(CommandStatus.PENDING.value, "pending")
        self.assertEqual(CommandStatus.EXECUTING.value, "executing")
        self.assertEqual(CommandStatus.COMPLETED.value, "completed")
        self.assertEqual(CommandStatus.FAILED.value, "failed")
    
    def test_telemetry_creation(self):
        """Test telemetry data structure creation"""
        timestamp = datetime.now().isoformat()
        telemetry = Telemetry(
            timestamp=timestamp,
            altitude=12000.0,
            velocity=350.0,
            fuel_level=75.5,
            system_health="nominal"
        )
        
        self.assertEqual(telemetry.timestamp, timestamp)
        self.assertEqual(telemetry.altitude, 12000.0)
        self.assertEqual(telemetry.velocity, 350.0)
        self.assertEqual(telemetry.fuel_level, 75.5)
        self.assertEqual(telemetry.system_health, "nominal")
    
    def test_command_creation(self):
        """Test command data structure creation"""
        timestamp = datetime.now().isoformat()
        command = Command(
            id="cmd_001",
            type="test_command",
            parameters={"param1": "value1"},
            status=CommandStatus.PENDING,
            timestamp=timestamp
        )
        
        self.assertEqual(command.id, "cmd_001")
        self.assertEqual(command.type, "test_command")
        self.assertEqual(command.parameters["param1"], "value1")
        self.assertEqual(command.status, CommandStatus.PENDING)
        self.assertEqual(command.timestamp, timestamp)
        self.assertIsNone(command.result)


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMissionControl))
    suite.addTests(loader.loadTestsFromTestCase(TestDataStructures))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)