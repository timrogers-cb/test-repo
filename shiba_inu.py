"""
Shiba Inu module for handling information about Shiba Inu dogs.
"""


class ShibaInu:
    """
    A class representing a Shiba Inu dog with basic characteristics and behaviors.
    """
    
    def __init__(self, name, age=None, color="red"):
        """
        Initialize a Shiba Inu instance.
        
        Args:
            name (str): The name of the Shiba Inu
            age (int, optional): Age in years. Defaults to None.
            color (str): Coat color. Defaults to "red".
        """
        self.name = name
        self.age = age
        self.color = color
        self.breed = "Shiba Inu"
        
    def bark(self):
        """Return the Shiba Inu's characteristic bark sound."""
        return "Woof!"
    
    def get_info(self):
        """Return basic information about the Shiba Inu."""
        info = f"Name: {self.name}, Breed: {self.breed}, Color: {self.color}"
        if self.age is not None:
            info += f", Age: {self.age} years"
        return info
    
    def is_adult(self):
        """Check if the Shiba Inu is an adult (2+ years old)."""
        if self.age is None:
            return None
        return self.age >= 2
    
    @staticmethod
    def get_breed_characteristics():
        """Return general characteristics of the Shiba Inu breed."""
        return {
            "origin": "Japan",
            "size": "Small to medium",
            "temperament": ["Alert", "Agile", "Independent", "Good-natured"],
            "life_span": "13-16 years",
            "common_colors": ["Red", "Black and tan", "Sesame", "Cream"]
        }
    
    @classmethod
    def create_puppy(cls, name, color="red"):
        """Create a Shiba Inu puppy (under 1 year old)."""
        return cls(name, age=0, color=color)


def count_shiba_inus(shiba_list):
    """
    Count the number of Shiba Inu instances in a list.
    
    Args:
        shiba_list (list): List of objects to check
        
    Returns:
        int: Number of ShibaInu instances found
    """
    return sum(1 for item in shiba_list if isinstance(item, ShibaInu))


def get_oldest_shiba(shiba_list):
    """
    Find the oldest Shiba Inu in a list.
    
    Args:
        shiba_list (list): List of ShibaInu instances
        
    Returns:
        ShibaInu or None: The oldest Shiba Inu, or None if list is empty or no ages are set
    """
    shiba_with_ages = [s for s in shiba_list if isinstance(s, ShibaInu) and s.age is not None]
    if not shiba_with_ages:
        return None
    return max(shiba_with_ages, key=lambda s: s.age)