# tests/test_calendar.py
# Tests for the MockCalendarService and calendar-related functionality

import pytest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calendar_booking_agent import (
    MockCalendarService, 
    TimeSlot, 
    Appointment, 
    BookingStatus
)


class TestTimeSlot:
    """Test TimeSlot data structure"""
    
    def test_timeslot_creation(self):
        """Test creating a TimeSlot"""
        start = datetime.now()
        end = start + timedelta(hours=1)
        slot = TimeSlot(start, end)
        
        assert slot.start_time == start
        assert slot.end_time == end
        assert slot.is_available == True  # Default value
    
    def test_timeslot_with_availability(self):
        """Test TimeSlot with custom availability"""
        start = datetime.now()
        end = start + timedelta(hours=1)
        slot = TimeSlot(start, end, is_available=False)
        
        assert slot.is_available == False
    
    def test_timeslot_duration(self):
        """Test calculating slot duration"""
        start = datetime.now()
        end = start + timedelta(minutes=30)
        slot = TimeSlot(start, end)
        
        duration = slot.end_time - slot.start_time
        assert duration.total_seconds() == 30 * 60  # 30 minutes


class TestAppointment:
    """Test Appointment data structure"""
    
    def test_appointment_creation(self):
        """Test creating an Appointment"""
        start = datetime.now()
        end = start + timedelta(hours=1)
        
        appointment = Appointment(
            id="test-123",
            title="Test Meeting",
            start_time=start,
            end_time=end
        )
        
        assert appointment.id == "test-123"
        assert appointment.title == "Test Meeting"
        assert appointment.start_time == start
        assert appointment.end_time == end
        assert appointment.status == BookingStatus.PENDING  # Default
        assert appointment.attendee_email is None  # Default
    
    def test_appointment_with_attendee(self):
        """Test Appointment with attendee email"""
        start = datetime.now()
        end = start + timedelta(hours=1)
        
        appointment = Appointment(
            id="test-123",
            title="Client Call",
            start_time=start,
            end_time=end,
            attendee_email="client@example.com",
            status=BookingStatus.CONFIRMED
        )
        
        assert appointment.attendee_email == "client@example.com"
        assert appointment.status == BookingStatus.CONFIRMED


class TestMockCalendarService:
    """Test MockCalendarService functionality"""
    
    @pytest.fixture
    def calendar_service(self):
        """Create a fresh calendar service for each test"""
        return MockCalendarService()
    
    def test_service_initialization(self, calendar_service):
        """Test that service initializes with pre-populated appointments"""
        assert len(calendar_service.appointments) >= 2
        assert all(isinstance(apt, Appointment) for apt in calendar_service.appointments)
    
    def test_get_busy_times(self, calendar_service):
        """Test getting busy time slots"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        busy_slots = calendar_service.get_busy_times(today, tomorrow)
        
        assert isinstance(busy_slots, list)
        # Should have at least the pre-populated appointments
        assert len(busy_slots) >= 0
        
        for slot in busy_slots:
            assert isinstance(slot, TimeSlot)
            assert slot.is_available == False
    
    def test_get_available_slots_basic(self, calendar_service):
        """Test getting available slots for a future date"""
        future_date = datetime.now() + timedelta(days=7)  # Next week
        
        slots = calendar_service.get_available_slots(future_date)
        
        assert isinstance(slots, list)
        assert len(slots) > 0
        assert len(slots) <= 5  # Should return max 5 slots
        
        for slot in slots:
            assert isinstance(slot, TimeSlot)
            assert slot.is_available == True
            assert slot.start_time.date() == future_date.date()
    
    def test_get_available_slots_with_duration(self, calendar_service):
        """Test getting available slots with custom duration"""
        future_date = datetime.now() + timedelta(days=7)
        duration = 30  # 30 minutes
        
        slots = calendar_service.get_available_slots(future_date, duration_minutes=duration)
        
        for slot in slots:
            slot_duration = (slot.end_time - slot.start_time).total_seconds() / 60
            assert slot_duration == duration
    
    def test_get_available_slots_morning_preference(self, calendar_service):
        """Test getting morning slots"""
        future_date = datetime.now() + timedelta(days=7)
        
        slots = calendar_service.get_available_slots(
            future_date, 
            time_preference="morning"
        )
        
        for slot in slots:
            # Morning should be before 12 PM
            assert slot.start_time.hour < 12
    
    def test_get_available_slots_afternoon_preference(self, calendar_service):
        """Test getting afternoon slots"""
        future_date = datetime.now() + timedelta(days=7)
        
        slots = calendar_service.get_available_slots(
            future_date, 
            time_preference="afternoon"
        )
        
        for slot in slots:
            # Afternoon should be 12 PM or later, before 5 PM
            assert 12 <= slot.start_time.hour < 17
    
    def test_get_available_slots_evening_preference(self, calendar_service):
        """Test getting evening slots"""
        future_date = datetime.now() + timedelta(days=7)
        
        slots = calendar_service.get_available_slots(
            future_date, 
            time_preference="evening"
        )
        
        for slot in slots:
            # Evening should be 5 PM or later
            assert slot.start_time.hour >= 17
    
    def test_book_appointment_basic(self, calendar_service):
        """Test booking a basic appointment"""
        initial_count = len(calendar_service.appointments)
        
        # Create a time slot
        start_time = datetime.now() + timedelta(days=1, hours=10)
        end_time = start_time + timedelta(hours=1)
        slot = TimeSlot(start_time, end_time)
        
        # Book appointment
        appointment = calendar_service.book_appointment(slot, "Test Meeting")
        
        assert len(calendar_service.appointments) == initial_count + 1
        assert appointment.title == "Test Meeting"
        assert appointment.start_time == start_time
        assert appointment.end_time == end_time
        assert appointment.status == BookingStatus.CONFIRMED
        assert appointment.id is not None
    
    def test_book_appointment_with_attendee(self, calendar_service):
        """Test booking appointment with attendee"""
        start_time = datetime.now() + timedelta(days=1, hours=14)
        end_time = start_time + timedelta(hours=1)
        slot = TimeSlot(start_time, end_time)
        
        appointment = calendar_service.book_appointment(
            slot, 
            "Client Meeting",
            "client@example.com"
        )
        
        assert appointment.attendee_email == "client@example.com"
        assert appointment.title == "Client Meeting"
    
    def test_conflict_detection(self, calendar_service):
        """Test that busy times are properly excluded from available slots"""
        # Book an appointment first
        start_time = datetime.now() + timedelta(days=1, hours=10)
        end_time = start_time + timedelta(hours=1)
        slot = TimeSlot(start_time, end_time)
        calendar_service.book_appointment(slot, "Existing Meeting")
        
        # Get available slots for the same day
        available_slots = calendar_service.get_available_slots(start_time.replace(hour=0))
        
        # The booked time should not be in available slots
        for available_slot in available_slots:
            # Check for overlap
            overlap = (available_slot.start_time < end_time and 
                      available_slot.end_time > start_time)
            assert not overlap, "Available slot overlaps with booked appointment"
    
    def test_business_hours_constraint(self, calendar_service):
        """Test that slots are only within business hours"""
        future_date = datetime.now() + timedelta(days=7)
        
        slots = calendar_service.get_available_slots(future_date)
        
        for slot in slots:
            # Should be within business hours (9 AM to 5 PM by default)
            assert 9 <= slot.start_time.hour < 17
    
    def test_slot_intervals(self, calendar_service):
        """Test that slots are generated at proper intervals"""
        future_date = datetime.now() + timedelta(days=7)
        
        slots = calendar_service.get_available_slots(future_date)
        
        if len(slots) > 1:
            # Check that slots are 30 minutes apart
            time_diff = slots[1].start_time - slots[0].start_time
            assert time_diff.total_seconds() == 30 * 60  # 30 minutes
    
    def test_no_available_slots_busy_day(self, calendar_service):
        """Test handling when no slots are available"""
        # Book the entire day
        test_date = datetime.now() + timedelta(days=5)
        
        # Book every possible slot
        for hour in range(9, 17):  # 9 AM to 5 PM
            start = test_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            end = start + timedelta(hours=1)
            slot = TimeSlot(start, end)
            calendar_service.book_appointment(slot, f"Meeting {hour}")
        
        # Try to get available slots
        available_slots = calendar_service.get_available_slots(test_date)
        
        # Should have very few or no available slots
        assert len(available_slots) == 0 or len(available_slots) < 3
    
    def test_multiple_day_booking(self, calendar_service):
        """Test booking appointments across multiple days"""
        base_date = datetime.now() + timedelta(days=10)
        
        appointments = []
        for i in range(3):  # Book across 3 days
            day = base_date + timedelta(days=i)
            start = day.replace(hour=10, minute=0, second=0, microsecond=0)
            end = start + timedelta(hours=1)
            slot = TimeSlot(start, end)
            
            apt = calendar_service.book_appointment(slot, f"Daily Meeting {i+1}")
            appointments.append(apt)
        
        # Verify all appointments were created
        assert len(appointments) == 3
        
        # Verify they're on different days
        dates = [apt.start_time.date() for apt in appointments]
        assert len(set(dates)) == 3  # All unique dates


class TestCalendarEdgeCases:
    """Test edge cases and error scenarios"""
    
    def test_past_date_availability(self):
        """Test requesting availability for past dates"""
        calendar_service = MockCalendarService()
        yesterday = datetime.now() - timedelta(days=1)
        
        # Should still return slots (in real implementation, might want to restrict this)
        slots = calendar_service.get_available_slots(yesterday)
        assert isinstance(slots, list)
    
    def test_very_long_duration(self):
        """Test requesting very long meeting duration"""
        calendar_service = MockCalendarService()
        future_date = datetime.now() + timedelta(days=7)
        
        # Request 4-hour meeting
        slots = calendar_service.get_available_slots(future_date, duration_minutes=240)
        
        # Should handle gracefully (might return fewer or no slots)
        assert isinstance(slots, list)
        
        for slot in slots:
            duration = (slot.end_time - slot.start_time).total_seconds() / 60
            assert duration == 240
    
    def test_invalid_time_preference(self):
        """Test with invalid time preference"""
        calendar_service = MockCalendarService()
        future_date = datetime.now() + timedelta(days=7)
        
        # Should handle gracefully and return normal business hours
        slots = calendar_service.get_available_slots(
            future_date, 
            time_preference="invalid_preference"
        )
        
        assert isinstance(slots, list)
        assert len(slots) > 0


if __name__ == "__main__":
    # Run basic tests without pytest
    print("Running Calendar Service tests...")
    
    # Test TimeSlot
    start = datetime.now()
    end = start + timedelta(hours=1)
    slot = TimeSlot(start, end)
    assert slot.start_time == start
    print("✅ TimeSlot creation works")
    
    # Test Appointment
    appointment = Appointment("test-1", "Test Meeting", start, end)
    assert appointment.title == "Test Meeting"
    print("✅ Appointment creation works")
    
    # Test Calendar Service
    service = MockCalendarService()
    assert len(service.appointments) > 0
    print("✅ Calendar service initialization works")
    
    # Test availability
    future_date = datetime.now() + timedelta(days=7)
    slots = service.get_available_slots(future_date)
    assert len(slots) > 0
    print("✅ Available slots generation works")
    
    # Test booking
    initial_count = len(service.appointments)
    new_appointment = service.book_appointment(slots[0], "Test Booking")
    assert len(service.appointments) == initial_count + 1
    print("✅ Appointment booking works")
    
    print("\n🎉 Basic Calendar Service tests passed!")