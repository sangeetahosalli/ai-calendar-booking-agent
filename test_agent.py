# tests/test_agent.py
# Tests for the BookingAgent class

import pytest
import asyncio
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calendar_booking_agent import BookingAgent, ConversationState, TimeSlot


class TestBookingAgent:
    """Test suite for BookingAgent functionality"""
    
    @pytest.fixture
    def agent(self):
        """Create a fresh agent for each test"""
        return BookingAgent()
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes properly"""
        assert agent.calendar_service is not None
        assert agent.nl_processor is not None
        assert agent.state is not None
        assert agent.state.step == "initial"
        assert agent.state.intent is None
    
    def test_state_reset(self, agent):
        """Test state reset functionality"""
        # Modify state
        agent.state.intent = "book_appointment"
        agent.state.date = datetime.now()
        agent.state.step = "confirmation"
        agent.state.meeting_title = "Test Meeting"
        
        # Reset and verify
        agent.reset_state()
        assert agent.state.intent is None
        assert agent.state.date is None
        assert agent.state.step == "initial"
        assert agent.state.meeting_title is None
    
    @pytest.mark.asyncio
    async def test_greeting_response(self, agent):
        """Test initial greeting and general inquiries"""
        response = await agent.process_message("Hello")
        assert len(response) > 0
        assert any(word in response.lower() for word in ["hello", "help", "calendar", "assistant"])
    
    @pytest.mark.asyncio
    async def test_booking_intent_with_date(self, agent):
        """Test booking request that includes a date"""
        response = await agent.process_message("Book a meeting for tomorrow")
        
        assert agent.state.intent == "book_appointment"
        assert agent.state.date is not None
        assert "slots" in response.lower() or "available" in response.lower()
        assert agent.state.step == "slot_selection"
    
    @pytest.mark.asyncio
    async def test_booking_intent_without_date(self, agent):
        """Test booking request that needs date clarification"""
        response = await agent.process_message("I want to schedule a meeting")
        
        assert agent.state.intent == "book_appointment"
        assert "date" in response.lower()
        assert agent.state.step == "date_clarification"
    
    @pytest.mark.asyncio
    async def test_availability_check(self, agent):
        """Test checking availability"""
        response = await agent.process_message("Are you available tomorrow?")
        
        assert agent.state.intent == "check_availability"
        assert agent.state.date is not None
        assert "availability" in response.lower() or "available" in response.lower()
    
    @pytest.mark.asyncio
    async def test_date_clarification_flow(self, agent):
        """Test the date clarification conversation flow"""
        # Start with booking request without date
        await agent.process_message("Book a meeting")
        assert agent.state.step == "date_clarification"
        
        # Provide date
        response = await agent.process_message("tomorrow")
        assert agent.state.date is not None
        assert agent.state.step == "slot_selection"
        assert "slots" in response.lower()
    
    @pytest.mark.asyncio
    async def test_invalid_date_handling(self, agent):
        """Test handling of invalid date input"""
        # Start date clarification
        await agent.process_message("Book a meeting")
        
        # Provide invalid date
        response = await agent.process_message("some random text")
        assert agent.state.step == "date_clarification"
        assert "date" in response.lower()
    
    @pytest.mark.asyncio
    async def test_slot_selection_by_number(self, agent):
        """Test selecting a time slot by number"""
        # Set up state for slot selection
        agent.state.step = "slot_selection"
        agent.state.intent = "book_appointment"
        agent.state.date = datetime.now() + timedelta(days=1)
        agent.state.suggested_slots = [
            TimeSlot(datetime.now() + timedelta(days=1, hours=9), 
                    datetime.now() + timedelta(days=1, hours=10)),
            TimeSlot(datetime.now() + timedelta(days=1, hours=11), 
                    datetime.now() + timedelta(days=1, hours=12))
        ]
        
        response = await agent.process_message("I'll take slot 1")
        assert agent.state.selected_slot is not None
        assert agent.state.step == "confirmation"
        assert "confirm" in response.lower()
    
    @pytest.mark.asyncio
    async def test_slot_selection_by_time(self, agent):
        """Test selecting a time slot by mentioning the time"""
        # Set up state for slot selection
        agent.state.step = "slot_selection"
        agent.state.intent = "book_appointment"
        agent.state.date = datetime.now() + timedelta(days=1)
        
        # Create slots with specific times
        morning_slot = TimeSlot(
            datetime.now().replace(hour=9, minute=0) + timedelta(days=1),
            datetime.now().replace(hour=10, minute=0) + timedelta(days=1)
        )
        agent.state.suggested_slots = [morning_slot]
        
        response = await agent.process_message("9 AM works for me")
        assert agent.state.selected_slot is not None
        assert agent.state.step == "confirmation"
    
    @pytest.mark.asyncio
    async def test_invalid_slot_selection(self, agent):
        """Test handling invalid slot selection"""
        # Set up state for slot selection
        agent.state.step = "slot_selection"
        agent.state.suggested_slots = [
            TimeSlot(datetime.now(), datetime.now() + timedelta(hours=1))
        ]
        
        response = await agent.process_message("slot 999")
        assert agent.state.step == "slot_selection"  # Should stay in same step
        assert "didn't catch" in response.lower() or "number" in response.lower()
    
    @pytest.mark.asyncio
    async def test_confirmation_and_booking(self, agent):
        """Test final confirmation and booking process"""
        # Set up state for confirmation
        agent.state.step = "confirmation"
        agent.state.selected_slot = TimeSlot(
            datetime.now() + timedelta(days=1, hours=10),
            datetime.now() + timedelta(days=1, hours=11)
        )
        
        initial_appointment_count = len(agent.calendar_service.appointments)
        
        response = await agent.process_message("Team Standup")
        
        # Should complete booking and reset state
        assert "booked successfully" in response.lower()
        assert "Team Standup" in response
        assert agent.state.step == "initial"  # Should reset
        assert len(agent.calendar_service.appointments) == initial_appointment_count + 1
    
    @pytest.mark.asyncio
    async def test_complete_booking_flow(self, agent):
        """Test a complete end-to-end booking flow"""
        # Step 1: Initial booking request
        response1 = await agent.process_message("Book a meeting for tomorrow morning")
        assert agent.state.step == "slot_selection"
        
        # Step 2: Select a slot
        response2 = await agent.process_message("I'll take the first one")
        assert agent.state.step == "confirmation"
        
        # Step 3: Provide meeting title and complete booking
        response3 = await agent.process_message("Project Review")
        assert "booked successfully" in response3.lower()
        assert agent.state.step == "initial"  # Should reset after booking
    
    @pytest.mark.asyncio
    async def test_time_preference_handling(self, agent):
        """Test handling of time preferences"""
        response = await agent.process_message("Book a meeting tomorrow afternoon")
        
        assert agent.state.time_preference == "afternoon"
        assert agent.state.date is not None
        assert "slots" in response.lower()
    
    @pytest.mark.asyncio
    async def test_multiple_conversations(self, agent):
        """Test that agent can handle multiple separate conversations"""
        # Complete first booking
        await agent.process_message("Book tomorrow at 10 AM")
        await agent.process_message("1")
        await agent.process_message("Meeting 1")
        
        # Start second booking - state should be reset
        assert agent.state.step == "initial"
        
        response = await agent.process_message("Check availability for Friday")
        assert agent.state.intent == "check_availability"
    
    @pytest.mark.asyncio
    async def test_error_recovery(self, agent):
        """Test agent's ability to recover from errors and unclear input"""
        # Send unclear message
        response1 = await agent.process_message("asdfasdf random text")
        assert len(response1) > 0  # Should provide helpful response
        
        # Should still be able to process valid request after error
        response2 = await agent.process_message("Book a meeting tomorrow")
        assert agent.state.intent == "book_appointment"


class TestConversationScenarios:
    """Test realistic conversation scenarios"""
    
    @pytest.mark.asyncio
    async def test_polite_conversation(self):
        """Test polite, natural conversation flow"""
        agent = BookingAgent()
        
        responses = []
        responses.append(await agent.process_message("Hi there! Hope you're having a good day."))
        responses.append(await agent.process_message("I was wondering if I could schedule a meeting with you for tomorrow afternoon?"))
        responses.append(await agent.process_message("The 2 PM slot would be perfect, thank you!"))
        responses.append(await agent.process_message("Let's call it 'Quarterly Business Review'"))
        
        # Verify polite responses and successful booking
        assert all(len(r) > 0 for r in responses)
        assert "booked successfully" in responses[-1].lower()
    
    @pytest.mark.asyncio
    async def test_uncertain_user_flow(self):
        """Test conversation with an uncertain user"""
        agent = BookingAgent()
        
        responses = []
        responses.append(await agent.process_message("I need to book something"))
        responses.append(await agent.process_message("maybe tomorrow? or the day after?"))
        responses.append(await agent.process_message("tomorrow is fine"))
        responses.append(await agent.process_message("any afternoon slot"))
        responses.append(await agent.process_message("the first afternoon one"))
        responses.append(await agent.process_message("Strategy Discussion"))
        
        assert "booked successfully" in responses[-1].lower()
    
    @pytest.mark.asyncio
    async def test_busy_schedule_scenario(self):
        """Test scenario where user checks availability first"""
        agent = BookingAgent()
        
        # Check availability first
        response1 = await agent.process_message("What does your schedule look like this week?")
        
        # Then decide to book
        response2 = await agent.process_message("I'd like to book one of those Friday slots")
        
        # Complete booking
        response3 = await agent.process_message("slot 1")
        response4 = await agent.process_message("Weekly Check-in")
        
        assert "availability" in response1.lower() or "available" in response1.lower()
        assert "booked successfully" in response4.lower()


if __name__ == "__main__":
    # Run basic tests without pytest
    print("Running BookingAgent tests...")
    
    async def run_basic_tests():
        agent = BookingAgent()
        
        # Test initialization
        assert agent.state.step == "initial"
        print("✅ Agent initialization works")
        
        # Test basic interaction
        response = await agent.process_message("Hello")
        assert len(response) > 0
        print("✅ Agent responds to greetings")
        
        # Test booking intent
        response = await agent.process_message("Book a meeting tomorrow")
        assert agent.state.intent == "book_appointment"
        print("✅ Agent recognizes booking intent")
        
        # Test state reset
        agent.reset_state()
        assert agent.state.intent is None
        print("✅ State reset works")
    
    asyncio.run(run_basic_tests())
    print("\n🎉 Basic BookingAgent tests passed!")