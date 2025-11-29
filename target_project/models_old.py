"""
OLD VERSION: models.py before changes
This file represents the state before refactoring
"""

class User:
    """User model representing a system user"""
    
    def __init__(self):
        self.id = None
        self.first_name = None  # Will be renamed to 'name'
        self.last_name = None   # Will be deleted
        self.email = None
        self.created_at = None


class Product:
    """Product model for e-commerce"""
    
    def __init__(self):
        self.id = None
        self.title = None
        self.price = None
        self.description = None
        self.stock = None
