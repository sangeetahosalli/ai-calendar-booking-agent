# test_booking_agent.py
# Comprehensive tests for the Calendar Booking Agent

import pytest
import asyncio
from datetime import datetime, timedelta
from calendar_booking_agent import (
    BookingAgent, 
    NLProcessor, 
    MockCalendarService,
    ConversationState,
    TimeSlot
)

class TestNLProcessor:
    """Test natural language processing functionality"""
    
    def test_intent_extraction(self):
        processor = NLProcessor()
        
        # Test booking intents
        assert processor.extract_intent("I want to book a meeting") == "book_appointment"
        assert processor.extract_intent("Schedule a call for tomorrow") == "book_appointment"
        assert processor.extract_intent("Can we reserve a slot?") == "book_appointment"
        
        # Test availability intents
        assert processor.extract_intent("Are you free tomorrow?") == "check_availability"
        assert processor.extract_intent("What's your availability?") == "check_availability"
        assert processor.extract_intent("When are you open?") == "check_availability"
        
        # Test general intents
        assert processor.extract_intent("Hello there") == "general_inquiry"
        assert processor.extract_intent("How are you?") == "general_inquiry"
    
    def test_date_extraction(self):
        processor = NLProcessor()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Test relative dates
        assert processor.extract_date("today") == today
        assert processor.extract_date("tomorrow") == today + timedelta(days=1)
        
        # Test specific days
        friday_date = processor.extract_date("this Friday")
        assert friday_date is not None
        assert friday_date.weekday() == 4  # Friday is weekday 4
        
        # Test date formats
        date_result = processor.extract_date("12/25")
        assert date_result is not None
        assert date_result.month == 12
        assert date_result.day == 25
    
    def test_time_preference_extraction(self):
        processor = NLProcessor()
        
        assert processor.extract_time_preference("tomorrow morning") == "morning"
        assert processor.extract_time_preference("afternoon meeting") == "afternoon"
        assert processor.extract_time_preference("evening call") == "evening"
        assert processor.extract_time_preference("at 3:30 PM") == "specific_time"
        assert processor.extract_time_preference("just sometime") is None

class TestMockCalendarService:
    """Test calendar service functionality"""
    
    def test_initialization(self):
        service = MockCalendarService()
        assert len(service.appointments) >= 2  # Pre-populated appointments
    
    def test_get_available_slots(self):
        service = MockCalendarService()
        tomorrow = datetime.now() + timedelta(days=1)
        
        slots = service.get_available_slots(tomorrow, duration_minutes=60)
        assert len(slots) > 0
        assert all(slot.is_available for slot in slots)
        assert all(isinstance(slot, TimeSlot) for slot in slots)
    
    def test_book_appointment(self):
        service = MockCalendarService()
        initial_count = len(service.appointments)
        
        # Create a test slot
        start_time = datetime.now() + timedelta(days=1, hours=10)
        end_time = start_time + timedelta(hours=1)
        slot = TimeSlot(start_time, end_time)
        
        # Book appointment
        appointment = service.book_appointment(slot, "Test Meeting", "test@example.com")
        
        assert len(service.appointments) == initial_count + 1
        assert appointment.title == "Test Meeting"
        assert appointment.attendee_email == "test@example.com"
        assert appointment.start_time == start_time

class TestBookingAgent:
    """Test the main booking agent functionality"""
    
    @pytest.fixture
    def agent(self):
        return BookingAgent()
    
    @pytest.mark.asyncio
    async def test_initial_greeting(self, agent):
        response = await agent.process_message("Hello")
        assert "calendar" in response.lower() or "help" in response.lower()
    
    @pytest.mark.asyncio
    async def test_booking_flow_with_date(self, agent):
        # Test booking request with date
        response = await agent.process_message("Book a meeting for tomorrow")
        assert "available slots" in response.lower() or "slots" in response
        assert agent.state.intent == "book_appointment"
        assert agent.state.date is not None
    
    @pytest.mark.asyncio
    async def test_booking_flow_without_date(self, agent):
        # Test booking request without date
        response = await agent.process_message("I want to schedule a meeting")
        assert "date" in response.lower()
        assert agent.state.step == "date_clarification"
    
    @pytest.mark.asyncio
    async def test_availability_check(self, agent):
        response = await agent.process_message("Are you free tomorrow?")
        assert "availability" in response.lower() or "available" in response.lower()
        assert agent.state.intent == "check_availability"
    
    @pytest.mark.asyncio
    async def test_complete_booking_flow(self, agent):
        # Step 1: Initial booking request
        response1 = await agent.process_message("Book a meeting for tomorrow afternoon")
        assert "slots" in response1.lower()
        assert agent.state.step == "slot_selection"
        
        # Step 2: Select a slot
        response2 = await agent.process_message("I'll take slot 1")
        assert "confirm" in response2.lower()
        assert agent.state.step == "confirmation"
        assert agent.state.selected_slot is not None
        
        # Step 3: Provide meeting title
        response3 = await agent.process_message("Team Standup")
        assert "booked successfully" in response3.lower()
        assert "Team Standup" in response3
    
    @pytest.mark.asyncio
    async def test_edge_case_invalid_slot_selection(self, agent):
        # Set up state for slot selection
        agent.state.step = "slot_selection"
        agent.state.suggested_slots = [
            TimeSlot(datetime.now(), datetime.now() + timedelta(hours=1))
        ]
        
        response = await agent.process_message("I want slot 999")
        assert "didn't catch" in response.lower() or "number" in response.lower()
    
    def test_state_reset(self, agent):
        # Modify state
        agent.state.intent = "book_appointment"
        agent.state.date = datetime.now()
        agent.state.step = "confirmation"
        
        # Reset and verify
        agent.reset_state()
        assert agent.state.intent is None
        assert agent.state.date is None
        assert agent.state.step == "initial"

class TestConversationFlow:
    """Test realistic conversation scenarios"""
    
    @pytest.mark.asyncio
    async def test_scenario_morning_meeting(self):
        agent = BookingAgent()
        
        # User wants a morning meeting
        responses = []
        responses.append(await agent.process_message("I need to book a meeting tomorrow morning"))
        responses.append(await agent.process_message("The first slot looks good"))
        responses.append(await agent.process_message("Client Strategy Session"))
        
        # Verify final response indicates successful booking
        assert "booked successfully" in responses[-1].lower()
        assert "Client Strategy Session" in responses[-1]
    
    @pytest.mark.asyncio
    async def test_scenario_availability_then_booking(self):
        agent = BookingAgent()
        
        # Check availability first, then book
        responses = []
        responses.append(await agent.process_message("What's your availability this Friday?"))
        responses.append(await agent.process_message("Yes, I'd like to book the 2 PM slot"))
        responses.append(await agent.process_message("Weekly Review"))
        
        # Verify booking was successful
        assert "booked successfully" in responses[-1].lower()
    
    @pytest.mark.asyncio
    async def test_scenario_unclear_date_clarification(self):
        agent = BookingAgent()
        
        responses = []
        responses.append(await agent.process_message("Book me a meeting"))
        responses.append(await agent.process_message("sometime next week"))
        
        # Should ask for more specific date
        assert "date" in responses[0].lower()
        # Should handle "next week" request
        assert len(responses[1]) > 0

# Performance and Integration Tests
class TestPerformance:
    """Test performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_response_time(self):
        agent = BookingAgent()
        
        import time
        start_time = time.time()
        await agent.process_message("Book a meeting for tomorrow")
        end_time = time.time()
        
        # Should respond within reasonable time (adjust threshold as needed)
        assert end_time - start_time < 1.0  # 1 second max
    
    def test_memory_usage_state_management(self):
        agent = BookingAgent()
        
        # Simulate multiple conversations
        for i in range(100):
            agent.reset_state()
            agent.state.intent = "book_appointment"
            agent.state.date = datetime.now() + timedelta(days=i)
        
        # Memory should be stable (no significant leaks)
        assert len(agent.calendar_service.appointments) < 1000  # Reasonable limit

# Run tests
if __name__ == "__main__":
    # Run basic tests without pytest
    print("Running basic functionality tests...")
    
    # Test NLP
    processor = NLProcessor()
    assert processor.extract_intent("book a meeting") == "book_appointment"
    print("✅ NLP Intent extraction works")
    
    assert processor.extract_date("tomorrow") is not None
    print("✅ NLP Date extraction works")
    
    # Test Calendar Service
    service = MockCalendarService()
    slots = service.get_available_slots(datetime.now() + timedelta(days=1))
    assert len(slots) > 0
    print("✅ Calendar service generates slots")
    
    # Test Agent
    async def test_agent():
        agent = BookingAgent()
        response = await agent.process_message("Hello")
        assert len(response) > 0
        print("✅ Agent responds to messages")
    
    asyncio.run(test_agent())
    
    print("\n🎉 All basic tests passed! Run 'pytest test_booking_agent.py -v' for comprehensive testing.")