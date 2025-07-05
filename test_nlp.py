# tests/test_nlp.py
# Tests for the NLProcessor (Natural Language Processing) functionality

import pytest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calendar_booking_agent import NLProcessor


class TestIntentExtraction:
    """Test intent recognition from natural language"""
    
    @pytest.fixture
    def processor(self):
        """Create NLProcessor instance for each test"""
        return NLProcessor()
    
    def test_booking_intents(self, processor):
        """Test recognition of booking/scheduling intents"""
        booking_phrases = [
            "Book a meeting",
            "Schedule an appointment", 
            "I want to schedule a call",
            "Can we book a slot?",
            "Reserve a time for meeting",
            "Set up an appointment",
            "Book me a slot tomorrow",
            "Schedule something for next week"
        ]
        
        for phrase in booking_phrases:
            intent = processor.extract_intent(phrase)
            assert intent == "book_appointment", f"Failed for: '{phrase}'"
    
    def test_availability_intents(self, processor):
        """Test recognition of availability checking intents"""
        availability_phrases = [
            "Are you available tomorrow?",
            "What's your availability?",
            "Do you have any free time?",
            "When are you open?",
            "Check your availability for Friday",
            "Are you free this afternoon?",
            "What times are available?",
            "Show me your open slots"
        ]
        
        for phrase in availability_phrases:
            intent = processor.extract_intent(phrase)
            assert intent == "check_availability", f"Failed for: '{phrase}'"
    
    def test_cancellation_intents(self, processor):
        """Test recognition of cancellation intents"""
        cancel_phrases = [
            "Cancel my appointment",
            "Delete the meeting",
            "Remove my booking",
            "Cancel the scheduled call",
            "I need to cancel",
            "Delete my reservation"
        ]
        
        for phrase in cancel_phrases:
            intent = processor.extract_intent(phrase)
            assert intent == "cancel_appointment", f"Failed for: '{phrase}'"
    
    def test_general_inquiry_intents(self, processor):
        """Test recognition of general inquiries"""
        general_phrases = [
            "Hello",
            "How are you?",
            "What can you do?",
            "Help me understand",
            "Good morning",
            "Thanks for your help",
            "What's the weather like?"
        ]
        
        for phrase in general_phrases:
            intent = processor.extract_intent(phrase)
            assert intent == "general_inquiry", f"Failed for: '{phrase}'"
    
    def test_case_insensitive_intent_recognition(self, processor):
        """Test that intent recognition works regardless of case"""
        test_cases = [
            ("BOOK A MEETING", "book_appointment"),
            ("book a meeting", "book_appointment"),
            ("Book A Meeting", "book_appointment"),
            ("ARE YOU AVAILABLE?", "check_availability"),
            ("are you available?", "check_availability"),
            ("CANCEL MY APPOINTMENT", "cancel_appointment"),
            ("cancel my appointment", "cancel_appointment")
        ]
        
        for phrase, expected_intent in test_cases:
            intent = processor.extract_intent(phrase)
            assert intent == expected_intent, f"Failed for: '{phrase}'"
    
    def test_complex_sentences_intent(self, processor):
        """Test intent recognition in complex sentences"""
        complex_phrases = [
            ("Hi there! I was wondering if I could book a meeting for tomorrow?", "book_appointment"),
            ("Good morning! Could you please check your availability for next week?", "check_availability"),
            ("Sorry, but I need to cancel my appointment due to a conflict", "cancel_appointment"),
            ("Hello! I'm new here and not sure how this works", "general_inquiry")
        ]
        
        for phrase, expected_intent in complex_phrases:
            intent = processor.extract_intent(phrase)
            assert intent == expected_intent, f"Failed for: '{phrase}'"


class TestDateExtraction:
    """Test date extraction from natural language"""
    
    @pytest.fixture
    def processor(self):
        return NLProcessor()
    
    def test_relative_dates(self, processor):
        """Test extraction of relative dates"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        test_cases = [
            ("today", today),
            ("Tomorrow", today + timedelta(days=1)),
            ("TOMORROW", today + timedelta(days=1)),
            ("next week", today + timedelta(days=7))
        ]
        
        for phrase, expected_date in test_cases:
            extracted_date = processor.extract_date(phrase)
            assert extracted_date == expected_date, f"Failed for: '{phrase}'"
    
    def test_specific_weekdays(self, processor):
        """Test extraction of specific weekdays"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Test Friday
        friday_date = processor.extract_date("this Friday")
        assert friday_date is not None
        assert friday_date.weekday() == 4  # Friday is weekday 4
        assert friday_date >= today  # Should be future Friday
        
        # Test Monday
        monday_date = processor.extract_date("this Monday")
        assert monday_date is not None
        assert monday_date.weekday() == 0  # Monday is weekday 0
        assert monday_date >= today  # Should be future Monday
        
        # Test case insensitive
        friday_date2 = processor.extract_date("FRIDAY")
        assert friday_date2 is not None
        assert friday_date2.weekday() == 4
    
    def test_date_formats(self, processor):
        """Test extraction of various date formats"""
        current_year = datetime.now().year
        
        test_cases = [
            ("12/25", 12, 25),  # MM/DD format
            ("1/1", 1, 1),      # M/D format
            ("06/15", 6, 15),   # MM/DD format
            ("12-25", 12, 25),  # MM-DD format
            ("3-5", 3, 5)       # M-D format
        ]
        
        for phrase, expected_month, expected_day in test_cases:
            extracted_date = processor.extract_date(phrase)
            assert extracted_date is not None, f"Failed to extract: '{phrase}'"
            assert extracted_date.month == expected_month
            assert extracted_date.day == expected_day
            # Should be current year or next year if date has passed
            assert extracted_date.year >= current_year
    
    def test_complex_date_sentences(self, processor):
        """Test date extraction from complex sentences"""
        tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        complex_phrases = [
            "I want to book a meeting for tomorrow afternoon",
            "Can we schedule something tomorrow?",
            "Let's meet tomorrow morning",
            "Tomorrow would be great for me"
        ]
        
        for phrase in complex_phrases:
            extracted_date = processor.extract_date(phrase)
            assert extracted_date == tomorrow, f"Failed for: '{phrase}'"
    
    def test_no_date_in_text(self, processor):
        """Test that None is returned when no date is found"""
        no_date_phrases = [
            "Hello there",
            "How are you?", 
            "I want to book a meeting",  # No specific date
            "What can you do?",
            "Random text without dates"
        ]
        
        for phrase in no_date_phrases:
            extracted_date = processor.extract_date(phrase)
            assert extracted_date is None, f"Incorrectly extracted date from: '{phrase}'"
    
    def test_invalid_date_formats(self, processor):
        """Test handling of invalid date formats"""
        invalid_phrases = [
            "13/45",  # Invalid month/day
            "2/30",   # Invalid day for February
            "25/13",  # Invalid format
            "abc/def" # Non-numeric
        ]
        
        for phrase in invalid_phrases:
            extracted_date = processor.extract_date(phrase)
            # Should either return None or handle gracefully
            if extracted_date is not None:
                # If it returns a date, it should be valid
                assert isinstance(extracted_date, datetime)
    
    def test_past_date_handling(self, processor):
        """Test that past dates are moved to next year"""
        # This test might need adjustment based on current date
        current_date = datetime.now()
        
        # If we're testing in December, January dates should be next year
        if current_date.month == 12:
            jan_date = processor.extract_date("1/15")
            if jan_date:
                assert jan_date.year == current_date.year + 1


class TestTimePreferenceExtraction:
    """Test time preference extraction from natural language"""
    
    @pytest.fixture
    def processor(self):
        return NLProcessor()
    
    def test_time_of_day_preferences(self, processor):
        """Test extraction of general time preferences"""
        test_cases = [
            ("tomorrow morning", "morning"),
            ("Morning meeting", "morning"),
            ("MORNING appointment", "morning"),
            ("afternoon call", "afternoon"),
            ("Afternoon session", "afternoon"),
            ("AFTERNOON time", "afternoon"),
            ("evening meeting", "evening"),
            ("Evening call", "evening"),
            ("EVENING appointment", "evening")
        ]
        
        for phrase, expected_preference in test_cases:
            preference = processor.extract_time_preference(phrase)
            assert preference == expected_preference, f"Failed for: '{phrase}'"
    
    def test_specific_time_recognition(self, processor):
        """Test recognition of specific times"""
        specific_time_phrases = [
            "at 3:30 PM",
            "2:15 PM works",
            "around 10:00 AM",
            "3 PM would be good",
            "at 9 am",
            "11 PM tonight",
            "2:30",
            "14:30"  # 24-hour format
        ]
        
        for phrase in specific_time_phrases:
            preference = processor.extract_time_preference(phrase)
            assert preference == "specific_time", f"Failed for: '{phrase}'"
    
    def test_no_time_preference(self, processor):
        """Test that None is returned when no time preference is found"""
        no_time_phrases = [
            "book a meeting",
            "schedule an appointment",
            "are you available?",
            "hello there",
            "random text",
            "some day next week"
        ]
        
        for phrase in no_time_phrases:
            preference = processor.extract_time_preference(phrase)
            assert preference is None, f"Incorrectly extracted preference from: '{phrase}'"
    
    def test_mixed_time_preferences(self, processor):
        """Test complex sentences with time preferences"""
        test_cases = [
            ("I'd like a morning meeting tomorrow", "morning"),
            ("Can we do afternoon sometime next week?", "afternoon"),
            ("Evening would work better for me", "evening"),
            ("Maybe around 3:30 PM if possible", "specific_time"),
            ("2 PM or 3 PM would work", "specific_time")
        ]
        
        for phrase, expected_preference in test_cases:
            preference = processor.extract_time_preference(phrase)
            assert preference == expected_preference, f"Failed for: '{phrase}'"


class TestNLProcessorIntegration:
    """Test integration of all NL processing features"""
    
    @pytest.fixture
    def processor(self):
        return NLProcessor()
    
    def test_complete_sentence_processing(self, processor):
        """Test processing complete, realistic sentences"""
        test_sentences = [
            {
                "text": "Hi! I'd like to book a meeting for tomorrow afternoon",
                "expected_intent": "book_appointment",
                "expected_time_preference": "afternoon",
                "should_have_date": True
            },
            {
                "text": "Are you available this Friday morning?",
                "expected_intent": "check_availability", 
                "expected_time_preference": "morning",
                "should_have_date": True
            },
            {
                "text": "I need to cancel my appointment scheduled for tomorrow",
                "expected_intent": "cancel_appointment",
                "expected_time_preference": None,
                "should_have_date": True
            },
            {
                "text": "Can we schedule something at 3:30 PM next Monday?",
                "expected_intent": "book_appointment",
                "expected_time_preference": "specific_time", 
                "should_have_date": True
            }
        ]
        
        for test_case in test_sentences:
            text = test_case["text"]
            
            # Test intent extraction
            intent = processor.extract_intent(text)
            assert intent == test_case["expected_intent"], f"Intent failed for: '{text}'"
            
            # Test time preference extraction
            time_pref = processor.extract_time_preference(text)
            assert time_pref == test_case["expected_time_preference"], f"Time preference failed for: '{text}'"
            
            # Test date extraction
            date = processor.extract_date(text)
            if test_case["should_have_date"]:
                assert date is not None, f"Date extraction failed for: '{text}'"
            else:
                assert date is None, f"Unexpected date extracted for: '{text}'"
    
    def test_ambiguous_sentences(self, processor):
        """Test handling of ambiguous sentences"""
        ambiguous_phrases = [
            "book tomorrow",  # Clear intent and date, no time preference
            "are you free?",  # Clear intent, no date or time
            "3 PM",           # Time but no clear intent or date
            "next week",      # Date but no clear intent
            "meeting"         # Vague, could be many things
        ]
        
        for phrase in ambiguous_phrases:
            # Should not crash and should return reasonable results
            intent = processor.extract_intent(phrase)
            date = processor.extract_date(phrase)
            time_pref = processor.extract_time_preference(phrase)
            
            # All should be valid return types
            assert intent in ["book_appointment", "check_availability", "cancel_appointment", "general_inquiry"]
            assert date is None or isinstance(date, datetime)
            assert time_pref is None or isinstance(time_pref, str)
    
    def test_multilingual_robustness(self, processor):
        """Test basic robustness with non-English words mixed in"""
        # Note: This is basic testing since we don't have full multilingual support
        mixed_phrases = [
            "book a meeting por favor",  # Spanish mixed in
            "schedule rendez-vous tomorrow",  # French mixed in
            "available heute?",  # German mixed in
        ]
        
        for phrase in mixed_phrases:
            # Should not crash
            intent = processor.extract_intent(phrase)
            assert isinstance(intent, str)


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture 
    def processor(self):
        return NLProcessor()
    
    def test_empty_and_whitespace_input(self, processor):
        """Test handling of empty or whitespace-only input"""
        edge_inputs = ["", "   ", "\n", "\t", "   \n  \t  "]
        
        for input_text in edge_inputs:
            intent = processor.extract_intent(input_text)
            date = processor.extract_date(input_text)
            time_pref = processor.extract_time_preference(input_text)
            
            # Should handle gracefully
            assert intent == "general_inquiry"  # Default for unclear input
            assert date is None
            assert time_pref is None
    
    def test_very_long_input(self, processor):
        """Test handling of very long input text"""
        long_text = "book a meeting " * 100 + "tomorrow afternoon"
        
        # Should still extract key information despite length
        intent = processor.extract_intent(long_text)
        date = processor.extract_date(long_text)
        time_pref = processor.extract_time_preference(long_text)
        
        assert intent == "book_appointment"
        assert date is not None
        assert time_pref == "afternoon"
    
    def test_special_characters(self, processor):
        """Test handling of special characters and symbols"""
        special_inputs = [
            "book a meeting @#$%",
            "schedule !@# tomorrow &*()",
            "available??? $$$ morning",
            "meeting... 3:30 PM!!!"
        ]
        
        for input_text in special_inputs:
            # Should not crash
            intent = processor.extract_intent(input_text)
            date = processor.extract_date(input_text)
            time_pref = processor.extract_time_preference(input_text)
            
            assert isinstance(intent, str)
            assert date is None or isinstance(date, datetime)
            assert time_pref is None or isinstance(time_pref, str)


if __name__ == "__main__":
    # Run basic tests without pytest
    print("Running NL Processor tests...")
    
    processor = NLProcessor()
    
    # Test intent extraction
    assert processor.extract_intent("book a meeting") == "book_appointment"
    print("✅ Intent extraction works")
    
    # Test date extraction
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    extracted_today = processor.extract_date("today")
    assert extracted_today == today
    print("✅ Date extraction works")
    
    # Test time preference extraction
    assert processor.extract_time_preference("tomorrow morning") == "morning"
    print("✅ Time preference extraction works")
    
    # Test complex sentence
    intent = processor.extract_intent("I'd like to book a meeting for tomorrow afternoon")
    date = processor.extract_date("I'd like to book a meeting for tomorrow afternoon") 
    time_pref = processor.extract_time_preference("I'd like to book a meeting for tomorrow afternoon")
    
    assert intent == "book_appointment"
    assert date is not None
    assert time_pref == "afternoon"
    print("✅ Complex sentence processing works")
    
    # Test edge case
    assert processor.extract_intent("") == "general_inquiry"
    print("✅ Edge case handling works")
    
    print("\n🎉 Basic NL Processor tests passed!")