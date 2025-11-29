"""
Example models.py file for testing Avelio MVP
This represents a typical backend data model
"""

class User:
    """User model representing a system user"""
    
    def __init__(self):
        self.id = None
        self.name = None  # Previously: first_name
        self.email = None
        self.created_at = None
        # Note: 'last_name' field was deleted


class Product:
    """Product model for e-commerce"""
    
    def __init__(self):
        self.id = None
        self.title = None
        self.price = None
        self.description = None
        self.stock = None
