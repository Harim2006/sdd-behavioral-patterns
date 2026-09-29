"""
Ticket cart with command pattern for undo/redo functionality.
Implements AddTicketCommand, RemoveTicketCommand, and SetPricingStrategyCommand.
"""

from abc import ABC, abstractmethod
from typing import Dict, List
from .pricing import PricingStrategy, StandardPricing


class Command(ABC):
    """Abstract base class for commands."""
    
    @abstractmethod
    def execute(self):
        """Execute the command."""
        pass
    
    @abstractmethod
    def undo(self):
        """Undo the command."""
        pass


class Cart:
    """Shopping cart for tickets."""
    
    def __init__(self):
        # Dict mapping category -> (quantity, unit_price)
        self._items: Dict[str, tuple] = {}
        self.pricing_strategy: PricingStrategy = StandardPricing()
    
    def add_item(self, category: str, qty: int, unit_price: float):
        """Add tickets to the cart."""
        if category in self._items:
            existing_qty, existing_price = self._items[category]
            # Accumulate quantity, keep the same unit price
            self._items[category] = (existing_qty + qty, existing_price)
        else:
            self._items[category] = (qty, unit_price)
    
    def remove_item(self, category: str, qty: int) -> int:
        """
        Remove up to qty tickets of category.
        
        Returns:
            Actual quantity removed (for undo purposes)
        """
        if category not in self._items:
            return 0
        
        current_qty, unit_price = self._items[category]
        qty_to_remove = min(qty, current_qty)
        new_qty = current_qty - qty_to_remove
        
        if new_qty > 0:
            self._items[category] = (new_qty, unit_price)
        else:
            del self._items[category]
        
        return qty_to_remove
    
    def items(self) -> Dict[str, tuple]:
        """Return cart items."""
        return self._items.copy()
    
    def subtotal(self) -> float:
        """Calculate subtotal before pricing strategy."""
        total = 0.0
        for qty, unit_price in self._items.values():
            total += unit_price * qty
        return total
    
    def quantity(self) -> int:
        """Total number of tickets in cart."""
        return sum(qty for qty, _ in self._items.values())
    
    def total(self) -> float:
        """Calculate final total with pricing strategy applied."""
        return self.pricing_strategy.price(self.subtotal(), self.quantity())


class AddTicketCommand(Command):
    """Command to add tickets to cart."""
    
    def __init__(self, cart: Cart, category: str, qty: int, unit_price: float):
        self.cart = cart
        self.category = category
        self.qty = qty
        self.unit_price = unit_price
    
    def execute(self):
        """Add tickets to cart."""
        self.cart.add_item(self.category, self.qty, self.unit_price)
    
    def undo(self):
        """Remove the exact tickets that were added."""
        self.cart.remove_item(self.category, self.qty)


class RemoveTicketCommand(Command):
    """Command to remove tickets from cart."""
    
    def __init__(self, cart: Cart, category: str, qty: int):
        self.cart = cart
        self.category = category
        self.qty = qty
        self.removed_qty = 0
        self.removed_price = 0.0
    
    def execute(self):
        """Remove tickets and remember what was removed."""
        # Get price before removing
        if self.category in self.cart._items:
            _, self.removed_price = self.cart._items[self.category]
        
        self.removed_qty = self.cart.remove_item(self.category, self.qty)
    
    def undo(self):
        """Restore the exact tickets that were removed."""
        if self.removed_qty > 0:
            self.cart.add_item(self.category, self.removed_qty, self.removed_price)


class SetPricingStrategyCommand(Command):
    """Command to change the pricing strategy."""
    
    def __init__(self, cart: Cart, strategy: PricingStrategy):
        self.cart = cart
        self.new_strategy = strategy
        self.old_strategy = None
    
    def execute(self):
        """Set new pricing strategy and remember the old one."""
        self.old_strategy = self.cart.pricing_strategy
        self.cart.pricing_strategy = self.new_strategy
    
    def undo(self):
        """Restore the previous pricing strategy."""
        if self.old_strategy is not None:
            self.cart.pricing_strategy = self.old_strategy


class CartInvoker:
    """Invoker that manages command history for undo/redo."""
    
    def __init__(self):
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []
    
    def run(self, command: Command):
        """Execute a command and add it to history."""
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()  # Clear redo stack on new command
    
    def undo(self, n: int = 1) -> int:
        """
        Undo up to n commands.
        
        Returns:
            Number of commands actually undone
        """
        undone = 0
        while undone < n and self.history:
            command = self.history.pop()
            command.undo()
            self.redo_stack.append(command)
            undone += 1
        return undone
    
    def redo(self, n: int = 1) -> int:
        """
        Redo up to n commands.
        
        Returns:
            Number of commands actually redone
        """
        redone = 0
        while redone < n and self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.history.append(command)
            redone += 1
        return redone
