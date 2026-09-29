"""
Show waitlist with observer pattern for seat availability notifications.
Implements Show (Subject), EmailWaitlistNotifier, and SMSWaitlistNotifier (Observers).
"""

from abc import ABC, abstractmethod
from typing import List


class WaitlistObserver(ABC):
    """Abstract observer for waitlist notifications."""
    
    @abstractmethod
    def notify(self, show_name: str):
        """
        Notify observer that seats are available.
        
        Args:
            show_name: Name of the show with available seats
        """
        pass


class Show:
    """Subject that maintains a waitlist and notifies observers when seats become available."""
    
    def __init__(self, name: str, available_seats: int = 0):
        """
        Initialize a show.
        
        Args:
            name: Name of the show
            available_seats: Initial number of available seats
        """
        self.name = name
        self.available_seats = available_seats
        self._observers: List[WaitlistObserver] = []
    
    def join_waitlist(self, observer: WaitlistObserver):
        """Add an observer to the waitlist."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def leave_waitlist(self, observer: WaitlistObserver):
        """Remove an observer from the waitlist."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def release_seats(self, count: int):
        """
        Release seats back to inventory and notify waitlist if show was sold out.
        
        Args:
            count: Number of seats to release
            
        Raises:
            ValueError: If count is not positive
        """
        if count <= 0:
            raise ValueError("Count must be positive")
        
        was_sold_out = self.available_seats == 0
        self.available_seats += count
        
        # Only notify if show was previously sold out
        if was_sold_out:
            self._notify_observers()
    
    def sell_seats(self, count: int):
        """
        Sell seats (reduce availability) without notifying waitlist.
        
        Args:
            count: Number of seats to sell
            
        Raises:
            ValueError: If trying to sell more seats than available
        """
        if count > self.available_seats:
            raise ValueError("Cannot sell more seats than available")
        
        self.available_seats -= count
    
    def _notify_observers(self):
        """Notify all observers that seats are available."""
        for observer in self._observers:
            observer.notify(self.name)


class EmailWaitlistNotifier(WaitlistObserver):
    """Observer that sends email notifications when seats become available."""
    
    def __init__(self, email: str):
        """
        Initialize email notifier.
        
        Args:
            email: Email address to send notifications to
        """
        self.email = email
        self.sent: List[str] = []  # Track sent messages for testing
    
    def notify(self, show_name: str):
        """Send email notification."""
        message = f"Seats available for {show_name}! Book now at encore.example.com"
        self.sent.append(message)
        # In real implementation, would send actual email


class SMSWaitlistNotifier(WaitlistObserver):
    """Observer that sends SMS notifications when seats become available."""
    
    def __init__(self, phone: str):
        """
        Initialize SMS notifier.
        
        Args:
            phone: Phone number to send notifications to
        """
        self.phone = phone
        self.sent: List[str] = []  # Track sent messages for testing
    
    def notify(self, show_name: str):
        """Send SMS notification."""
        message = f"Seats available for {show_name}! Book now at encore.example.com"
        self.sent.append(message)
        # In real implementation, would send actual SMS
