SPOOKY_PREFIX = "spooky_"

class HauntedMansion:
    def __init__(self, **kwargs):
        for attribute_name, value in kwargs.items():
            setattr(self, attribute_name, value)
    
    def __getattr__(self, attribute_name):
        return "Booooo, only ghosts here!"
    
    def __setattr__(self, attribute_name, value):
        attribute_name = SPOOKY_PREFIX + attribute_name
        super().__setattr__(attribute_name, value)
