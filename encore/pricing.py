"""
Pricing strategies for ticket sales (Strategy Pattern).
Implements StandardPricing, EarlyBirdPricing, and GroupPricing.
"""

from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    """Abstract base class for pricing strategies."""
    
    @abstractmethod
    def price(self, subtotal: float, quantity: int) -> float:
        """
        Calculate the final price based on the strategy.
        
        Args:
            subtotal: The base price before discounts
            quantity: Number of tickets
            
        Returns:
            Final price (clamped at 0.0 minimum)
        """
        pass


class StandardPricing(PricingStrategy):
    """Standard pricing with no discounts."""
    
    def price(self, subtotal: float, quantity: int) -> float:
        """Return subtotal unchanged."""
        return max(0.0, subtotal)


class EarlyBirdPricing(PricingStrategy):
    """Early bird pricing with percentage discount."""
    
    def __init__(self, percent: float):
        """
        Initialize early bird pricing.
        
        Args:
            percent: Discount percentage (0-100 inclusive)
            
        Raises:
            ValueError: If percent is not between 0 and 100
        """
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100")
        self.percent = percent
    
    def price(self, subtotal: float, quantity: int) -> float:
        """Apply percentage discount to subtotal."""
        discount = subtotal * (self.percent / 100.0)
        final_price = subtotal - discount
        return max(0.0, final_price)


class GroupPricing(PricingStrategy):
    """Group pricing with per-ticket discount above threshold."""
    
    def __init__(self, threshold: int, per_ticket_off: float):
        """
        Initialize group pricing.
        
        Args:
            threshold: Minimum quantity to trigger discount
            per_ticket_off: Discount amount per ticket
        """
        self.threshold = threshold
        self.per_ticket_off = per_ticket_off
    
    def price(self, subtotal: float, quantity: int) -> float:
        """Apply per-ticket discount if quantity meets threshold."""
        if quantity >= self.threshold:
            discount = self.per_ticket_off * quantity
            final_price = subtotal - discount
        else:
            final_price = subtotal
        
        return max(0.0, final_price)
