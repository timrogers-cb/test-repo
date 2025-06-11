# Shiba Inu Test Repository

This repository contains a Python module for working with Shiba Inu dogs and comprehensive tests to validate the functionality.

## Files

- `shiba_inu.py` - Main module containing the ShibaInu class and utility functions
- `test_shiba_inu.py` - Comprehensive test suite for the Shiba Inu functionality

## Features

### ShibaInu Class

The `ShibaInu` class represents a Shiba Inu dog with the following features:

- **Initialization**: Create a Shiba Inu with name, age, and color
- **Bark**: Get the characteristic bark sound
- **Info**: Get formatted information about the dog
- **Adult Check**: Determine if the dog is an adult (2+ years)
- **Breed Characteristics**: Get general breed information
- **Puppy Creation**: Class method to create puppy instances

### Utility Functions

- `count_shiba_inus(shiba_list)` - Count ShibaInu instances in a list
- `get_oldest_shiba(shiba_list)` - Find the oldest Shiba Inu in a list

## Usage

```python
from shiba_inu import ShibaInu, count_shiba_inus, get_oldest_shiba

# Create a Shiba Inu
hachi = ShibaInu("Hachi", age=5, color="red")

# Get basic info
print(hachi.get_info())  # Name: Hachi, Breed: Shiba Inu, Color: red, Age: 5 years

# Check if adult
print(hachi.is_adult())  # True

# Create a puppy
puppy = ShibaInu.create_puppy("Yuki", color="cream")

# Get breed characteristics
characteristics = ShibaInu.get_breed_characteristics()
print(characteristics["origin"])  # Japan

# Use utility functions
shibas = [hachi, puppy]
print(count_shiba_inus(shibas))  # 2
oldest = get_oldest_shiba(shibas)
print(oldest.name)  # Hachi
```

## Running Tests

Run the test suite using Python's unittest module:

```bash
python -m unittest test_shiba_inu.py -v
```

All tests should pass, covering various scenarios including:
- Object initialization and properties
- Method functionality
- Edge cases and error conditions
- Utility function behavior

## Test Coverage

The test suite includes 20 comprehensive tests covering:
- ShibaInu class initialization
- Instance methods (bark, get_info, is_adult)
- Static and class methods
- Utility functions with various input scenarios
- Edge cases and boundary conditions