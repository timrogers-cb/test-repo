# Mission Control Test System

A simple but comprehensive mission control simulation system designed for testing and demonstration purposes.

## Overview

This mission control system provides core functionality for managing space missions including:

- **Mission Lifecycle Management**: Create, start, abort, and complete missions
- **Command Execution**: Send and execute various mission commands
- **Telemetry Monitoring**: Track mission telemetry data (altitude, velocity, fuel, system health)
- **Status Reporting**: Comprehensive mission and system status reporting

## Features

### Mission Management
- Create missions with objectives
- Track mission status (planned, active, completed, aborted, failed)
- Support for multiple concurrent missions
- Complete mission lifecycle tracking

### Command System
- Send commands to active missions
- Built-in support for common mission commands:
  - `ignition`: Engine ignition sequence
  - `adjust_course`: Course correction with heading parameter
  - `collect_sample`: Sample collection at specified location
- Extensible command framework for custom command types
- Command status tracking (pending, executing, completed, failed)

### Telemetry System
- Real-time telemetry data collection
- Tracks key mission parameters:
  - Altitude (km)
  - Velocity (km/h)
  - Fuel level (%)
  - System health status
- Historical telemetry data storage

## Quick Start

### Basic Usage

```python
from mission_control import MissionControl

# Create mission control instance
mc = MissionControl()

# Create a new mission
mission = mc.create_mission("MARS_001", "Mars Sample Collection", 
                           ["Land on Mars", "Collect samples", "Return to orbit"])

# Start the mission
mc.start_mission("MARS_001")

# Send commands
cmd1 = mc.send_command("MARS_001", "ignition")
cmd2 = mc.send_command("MARS_001", "adjust_course", {"heading": "270 degrees"})
cmd3 = mc.send_command("MARS_001", "collect_sample", {"location": "Olympus Mons"})

# Execute commands
mc.execute_command("MARS_001", cmd1)
mc.execute_command("MARS_001", cmd2)
mc.execute_command("MARS_001", cmd3)

# Add telemetry data
mc.add_telemetry("MARS_001", altitude=15000.0, velocity=250.0, fuel_level=75.5)

# Get mission status
status = mc.get_mission_status("MARS_001")
print(f"Mission status: {status['mission']['status']}")
print(f"Completed commands: {status['completed_commands']}")

# Complete the mission
mc.complete_mission("MARS_001")
```

### Running the Demo

```bash
python mission_control.py
```

This will run a demonstration showing the complete mission lifecycle.

## Testing

The system includes a comprehensive test suite covering all functionality:

### Running Tests

```bash
python test_mission_control.py
```

### Test Coverage

The test suite includes:

- **Mission Lifecycle Tests**: Creation, starting, aborting, completing missions
- **Command System Tests**: Command sending, execution, and status tracking
- **Telemetry Tests**: Data collection and retrieval
- **Error Handling Tests**: Invalid operations and edge cases
- **Integration Tests**: Complete mission scenarios
- **Data Structure Tests**: Validation of all data models

### Test Categories

1. **Unit Tests**: Individual component functionality
2. **Integration Tests**: End-to-end mission scenarios
3. **Error Case Tests**: Invalid input and state handling
4. **Data Structure Tests**: Model validation

## API Reference

### MissionControl Class

#### Mission Management Methods

- `create_mission(mission_id, name, objectives=None)`: Create a new mission
- `start_mission(mission_id)`: Start a planned mission
- `abort_mission(mission_id)`: Abort an active mission
- `complete_mission(mission_id)`: Complete an active mission successfully

#### Command Methods

- `send_command(mission_id, command_type, parameters=None)`: Send a command to a mission
- `execute_command(mission_id, command_id)`: Execute a pending command

#### Telemetry Methods

- `add_telemetry(mission_id, altitude, velocity, fuel_level, system_health="nominal")`: Add telemetry data

#### Status Methods

- `get_mission_status(mission_id)`: Get comprehensive mission status
- `get_all_missions()`: Get status summary of all missions

### Data Structures

#### Mission
- `id`: Unique mission identifier
- `name`: Human-readable mission name
- `status`: Current mission status (MissionStatus enum)
- `start_time`: Mission start timestamp
- `end_time`: Mission end timestamp
- `objectives`: List of mission objectives
- `telemetry`: List of telemetry readings
- `commands`: List of mission commands

#### Command
- `id`: Unique command identifier
- `type`: Command type string
- `parameters`: Command parameters dictionary
- `status`: Command execution status (CommandStatus enum)
- `timestamp`: Command creation timestamp
- `result`: Command execution result

#### Telemetry
- `timestamp`: Data collection timestamp
- `altitude`: Current altitude (km)
- `velocity`: Current velocity (km/h)
- `fuel_level`: Current fuel level (%)
- `system_health`: System health status string

## Architecture

The system is built with a modular architecture:

```
MissionControl (Main Controller)
├── Mission Management
├── Command System
├── Telemetry System
└── Status Reporting

Data Models:
├── Mission
├── Command
└── Telemetry

Enums:
├── MissionStatus
└── CommandStatus
```

## Design Principles

1. **Simplicity**: Easy to understand and use
2. **Extensibility**: Support for custom commands and telemetry
3. **Reliability**: Comprehensive error handling and validation
4. **Testability**: Full test coverage with clear test scenarios
5. **Modularity**: Clean separation of concerns

## Error Handling

The system includes robust error handling for:

- Invalid mission states
- Nonexistent missions or commands
- Invalid command parameters
- State transition violations

## Future Enhancements

Potential areas for expansion:

1. **Persistence**: Save/load mission data
2. **Real-time Communication**: WebSocket support for live updates
3. **Advanced Telemetry**: More complex sensor data
4. **Mission Planning**: Automated mission planning and scheduling
5. **Multi-vehicle Support**: Support for multiple spacecraft
6. **Alert System**: Automated alert generation based on telemetry thresholds

## License

Licensed under the Apache License, Version 2.0. See LICENSE file for details.