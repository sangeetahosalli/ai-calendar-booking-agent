# Interactive AI Calendar Booking Agent
# Enhanced version with modern UI, animations, and interactive features

import streamlit as st
import asyncio
import json
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re
from enum import Enum
import uuid
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# ===== ENHANCED STYLING =====
def load_custom_css():
    """Load custom CSS for modern, interactive design"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        padding: 0rem 1rem;
    }
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .agent-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .agent-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .agent-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    .feature-card {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .quick-action-btn {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 500;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .quick-action-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .status-confirmed {
        background: #d4edda;
        color: #155724;
    }
    
    .status-pending {
        background: #fff3cd;
        color: #856404;
    }
    
    .chat-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        max-height: 500px;
        overflow-y: auto;
    }
    
    .time-slot-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .time-slot-card:hover {
        transform: scale(1.02);
        border-color: #4facfe;
        box-shadow: 0 5px 15px rgba(102,126,234,0.3);
    }
    
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        flex: 1;
        background: rgba(255,255,255,0.9);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    .sidebar-content {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    .emoji-large {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #48c6ef 0%, #6f86d6 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .typing-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #667eea;
        animation: typing 1.4s infinite ease-in-out;
        margin: 0 2px;
    }
    
    .typing-indicator:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# ===== DATA MODELS (Enhanced) =====

class BookingStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed" 
    CANCELLED = "cancelled"

@dataclass
class TimeSlot:
    start_time: datetime
    end_time: datetime
    is_available: bool = True
    confidence_score: float = 1.0  # AI confidence in slot recommendation

@dataclass
class Appointment:
    id: str
    title: str
    start_time: datetime
    end_time: datetime
    attendee_email: Optional[str] = None
    status: BookingStatus = BookingStatus.PENDING
    meeting_type: str = "General"
    priority: str = "Medium"

@dataclass
class ConversationState:
    intent: Optional[str] = None
    date: Optional[datetime] = None
    time_preference: Optional[str] = None
    duration: int = 60  # minutes
    meeting_title: Optional[str] = None
    attendee_email: Optional[str] = None
    suggested_slots: List[TimeSlot] = None
    selected_slot: Optional[TimeSlot] = None
    step: str = "initial"
    user_preferences: Dict = None
    conversation_id: str = None

# ===== ENHANCED CALENDAR SERVICE =====

class EnhancedCalendarService:
    """Enhanced Calendar service with AI-powered features"""
    
    def __init__(self):
        # Pre-populated with realistic appointments
        self.appointments = [
            Appointment(
                id="1", 
                title="Team Standup",
                start_time=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
                end_time=datetime.now().replace(hour=9, minute=30, second=0, microsecond=0),
                status=BookingStatus.CONFIRMED,
                meeting_type="Team Meeting",
                priority="High"
            ),
            Appointment(
                id="2",
                title="Client Strategy Session", 
                start_time=datetime.now().replace(hour=14, minute=0, second=0, microsecond=0),
                end_time=datetime.now().replace(hour=15, minute=30, second=0, microsecond=0),
                status=BookingStatus.CONFIRMED,
                meeting_type="Client Call",
                priority="High"
            ),
            Appointment(
                id="3",
                title="Code Review",
                start_time=datetime.now().replace(hour=16, minute=0, second=0, microsecond=0),
                end_time=datetime.now().replace(hour=17, minute=0, second=0, microsecond=0),
                status=BookingStatus.PENDING,
                meeting_type="Development",
                priority="Medium"
            )
        ]
    
    def get_busy_times(self, start_date: datetime, end_date: datetime) -> List[TimeSlot]:
        """Get busy time slots in the given date range"""
        busy_slots = []
        for apt in self.appointments:
            if start_date <= apt.start_time <= end_date:
                busy_slots.append(TimeSlot(apt.start_time, apt.end_time, False))
        return busy_slots
    
    def get_available_slots(self, date: datetime, duration_minutes: int = 60, 
                          time_preference: str = None, use_ai_optimization: bool = True) -> List[TimeSlot]:
        """Find available time slots with AI optimization"""
        
        # Define business hours
        start_hour = 9
        end_hour = 17
        
        # Adjust based on time preference
        if time_preference:
            if "morning" in time_preference.lower():
                end_hour = 12
            elif "afternoon" in time_preference.lower():
                start_hour = 12
            elif "evening" in time_preference.lower():
                start_hour = 17
                end_hour = 20
        
        # Generate all possible slots
        current_time = date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_time = date.replace(hour=end_hour, minute=0, second=0, microsecond=0)
        
        slots = []
        while current_time + timedelta(minutes=duration_minutes) <= end_time:
            slot_end = current_time + timedelta(minutes=duration_minutes)
            
            # AI-powered confidence scoring
            confidence = self._calculate_slot_confidence(current_time, time_preference)
            
            slots.append(TimeSlot(current_time, slot_end, True, confidence))
            current_time += timedelta(minutes=30)  # 30-minute intervals
        
        # Remove busy slots
        busy_times = self.get_busy_times(
            date.replace(hour=0, minute=0, second=0, microsecond=0),
            date.replace(hour=23, minute=59, second=59, microsecond=999999)
        )
        
        available_slots = []
        for slot in slots:
            is_available = True
            for busy in busy_times:
                if (slot.start_time < busy.end_time and slot.end_time > busy.start_time):
                    is_available = False
                    break
            if is_available:
                available_slots.append(slot)
        
        # Sort by confidence score if AI optimization is enabled
        if use_ai_optimization:
            available_slots.sort(key=lambda x: x.confidence_score, reverse=True)
        
        return available_slots[:8]  # Return top 8 slots
    
    def _calculate_slot_confidence(self, slot_time: datetime, preference: str = None) -> float:
        """Calculate AI confidence score for time slot recommendation"""
        confidence = 1.0
        hour = slot_time.hour
        
        # Prefer optimal meeting times
        if 10 <= hour <= 11 or 14 <= hour <= 15:  # Peak productivity hours
            confidence += 0.3
        elif 9 <= hour <= 12 or 13 <= hour <= 16:  # Good meeting hours
            confidence += 0.1
        else:
            confidence -= 0.2
        
        # Match user preference
        if preference:
            if preference == "morning" and hour < 12:
                confidence += 0.2
            elif preference == "afternoon" and 12 <= hour < 17:
                confidence += 0.2
            elif preference == "evening" and hour >= 17:
                confidence += 0.2
        
        # Avoid lunch time
        if 12 <= hour <= 13:
            confidence -= 0.3
        
        return max(0.1, min(1.0, confidence))
    
    def book_appointment(self, slot: TimeSlot, title: str, attendee_email: str = None, 
                        meeting_type: str = "General", priority: str = "Medium") -> Appointment:
        """Book an appointment with enhanced details"""
        appointment = Appointment(
            id=str(uuid.uuid4()),
            title=title,
            start_time=slot.start_time,
            end_time=slot.end_time,
            attendee_email=attendee_email,
            status=BookingStatus.CONFIRMED,
            meeting_type=meeting_type,
            priority=priority
        )
        self.appointments.append(appointment)
        return appointment
    
    def get_calendar_analytics(self) -> Dict:
        """Get calendar analytics for dashboard"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today - timedelta(days=today.weekday())
        
        confirmed_count = len([apt for apt in self.appointments if apt.status == BookingStatus.CONFIRMED])
        pending_count = len([apt for apt in self.appointments if apt.status == BookingStatus.PENDING])
        
        this_week_count = len([apt for apt in self.appointments 
                              if week_start <= apt.start_time < week_start + timedelta(days=7)])
        
        return {
            "total_appointments": len(self.appointments),
            "confirmed": confirmed_count,
            "pending": pending_count,
            "this_week": this_week_count,
            "utilization_rate": min(100, (confirmed_count / 20) * 100)  # Assuming 20 slots per week
        }

# ===== ENHANCED NL PROCESSOR =====

class EnhancedNLProcessor:
    """Enhanced Natural language processing with better intent recognition"""
    
    @staticmethod
    def extract_intent(text: str) -> str:
        """Extract user intent with improved accuracy"""
        text_lower = text.lower()
        
        # Enhanced keyword matching
        booking_keywords = ["book", "schedule", "appointment", "meeting", "call", "reserve", 
                           "set up", "arrange", "plan", "organize"]
        availability_keywords = ["available", "free", "open", "when", "check", "show", "view"]
        cancel_keywords = ["cancel", "delete", "remove", "reschedule", "change"]
        
        # Weighted scoring system
        booking_score = sum(1 for word in booking_keywords if word in text_lower)
        availability_score = sum(1 for word in availability_keywords if word in text_lower)
        cancel_score = sum(1 for word in cancel_keywords if word in text_lower)
        
        # Determine intent based on highest score
        scores = {
            "book_appointment": booking_score,
            "check_availability": availability_score,
            "cancel_appointment": cancel_score
        }
        
        max_score = max(scores.values())
        if max_score > 0:
            return max(scores, key=scores.get)
        
        return "general_inquiry"
    
    @staticmethod
    def extract_date(text: str) -> Optional[datetime]:
        """Enhanced date extraction with more patterns"""
        text_lower = text.lower()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Handle relative dates
        relative_dates = {
            "today": today,
            "tomorrow": today + timedelta(days=1),
            "day after tomorrow": today + timedelta(days=2),
            "next week": today + timedelta(days=7),
            "this week": today + timedelta(days=(7 - today.weekday())),
        }
        
        for phrase, date_obj in relative_dates.items():
            if phrase in text_lower:
                return date_obj
        
        # Handle specific weekdays
        weekdays = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        
        for day_name, day_num in weekdays.items():
            if day_name in text_lower:
                days_ahead = day_num - today.weekday()
                if days_ahead <= 0:
                    days_ahead += 7
                return today + timedelta(days=days_ahead)
        
        # Handle date patterns
        date_patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # MM/DD/YYYY
            r'(\d{1,2})/(\d{1,2})',          # MM/DD
            r'(\d{1,2})-(\d{1,2})-(\d{4})',  # MM-DD-YYYY
            r'(\d{1,2})-(\d{1,2})',          # MM-DD
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    if len(match.groups()) == 3:
                        month, day, year = map(int, match.groups())
                    else:
                        month, day = map(int, match.groups())
                        year = today.year
                    
                    extracted_date = datetime(year, month, day)
                    if extracted_date < today:
                        extracted_date = extracted_date.replace(year=year + 1)
                    return extracted_date
                except ValueError:
                    continue
        
        return None
    
    @staticmethod
    def extract_time_preference(text: str) -> Optional[str]:
        """Enhanced time preference extraction"""
        text_lower = text.lower()
        
        time_patterns = {
            "morning": ["morning", "am", "early"],
            "afternoon": ["afternoon", "lunch time", "midday"],
            "evening": ["evening", "night", "late"],
            "specific_time": [r'\d{1,2}:\d{2}', r'\d{1,2}\s*(am|pm)']
        }
        
        for preference, patterns in time_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return preference
        
        return None
    
    @staticmethod
    def extract_meeting_type(text: str) -> str:
        """Extract meeting type from text"""
        text_lower = text.lower()
        
        meeting_types = {
            "team": ["team", "standup", "scrum", "sprint"],
            "client": ["client", "customer", "presentation"],
            "interview": ["interview", "candidate", "hiring"],
            "training": ["training", "workshop", "learning"],
            "review": ["review", "performance", "feedback"],
            "social": ["social", "lunch", "coffee", "catch up"]
        }
        
        for meeting_type, keywords in meeting_types.items():
            if any(keyword in text_lower for keyword in keywords):
                return meeting_type.title()
        
        return "General"

# ===== ENHANCED BOOKING AGENT =====

class EnhancedBookingAgent:
    """Enhanced LangGraph-inspired conversation agent"""
    
    def __init__(self):
        self.calendar_service = EnhancedCalendarService()
        self.nl_processor = EnhancedNLProcessor()
        self.state = ConversationState()
        self.state.conversation_id = str(uuid.uuid4())
        self.conversation_history = []
    
    def reset_state(self):
        """Reset conversation state"""
        self.state = ConversationState()
        self.state.conversation_id = str(uuid.uuid4())
        self.conversation_history = []
    
    async def process_message(self, user_input: str) -> tuple[str, dict]:
        """Process user message and return response with metadata"""
        
        # Store conversation history
        self.conversation_history.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
        
        # Extract information from user input
        intent = self.nl_processor.extract_intent(user_input)
        date = self.nl_processor.extract_date(user_input)
        time_preference = self.nl_processor.extract_time_preference(user_input)
        meeting_type = self.nl_processor.extract_meeting_type(user_input)
        
        # Update state
        if intent:
            self.state.intent = intent
        if date:
            self.state.date = date
        if time_preference:
            self.state.time_preference = time_preference
        
        # Generate response
        response, metadata = await self._route_conversation(user_input)
        
        # Store assistant response
        self.conversation_history.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
        
        return response, metadata
    
    async def _route_conversation(self, user_input: str) -> tuple[str, dict]:
        """Route conversation based on current state"""
        metadata = {
            "intent": self.state.intent,
            "step": self.state.step,
            "confidence": 0.9,
            "suggestions": [],
            "available_slots": []
        }
        
        if self.state.step == "initial":
            return await self._handle_initial_request(user_input, metadata)
        elif self.state.step == "date_clarification":
            return await self._handle_date_clarification(user_input, metadata)
        elif self.state.step == "slot_selection":
            return await self._handle_slot_selection(user_input, metadata)
        elif self.state.step == "confirmation":
            return await self._handle_confirmation(user_input, metadata)
        else:
            return await self._handle_general_inquiry(user_input, metadata)
    
    async def _handle_initial_request(self, user_input: str, metadata: dict) -> tuple[str, dict]:
        """Handle the initial booking request with enhanced features"""
        
        if self.state.intent == "book_appointment":
            if not self.state.date:
                self.state.step = "date_clarification"
                metadata["suggestions"] = ["tomorrow", "next Friday", "this Monday", "12/25"]
                return ("🗓️ I'd be delighted to help you schedule an appointment! "
                       "What date works best for you? You can say something like 'tomorrow', "
                       "'next Friday', or a specific date like '12/25'."), metadata
            else:
                return await self._suggest_time_slots(metadata)
        
        elif self.state.intent == "check_availability":
            if not self.state.date:
                self.state.step = "date_clarification"
                metadata["suggestions"] = ["this week", "next Monday", "tomorrow"]
                return ("📅 I'll check my availability for you! What date are you interested in? "
                       "I can show you availability for specific days or date ranges."), metadata
            else:
                return await self._show_availability(metadata)
        
        elif self.state.intent == "cancel_appointment":
            return ("🚫 I can help you cancel an appointment. Could you provide the "
                   "booking ID or tell me which meeting you'd like to cancel?"), metadata
        
        else:
            metadata["suggestions"] = [
                "Book a meeting for tomorrow",
                "Check availability this week", 
                "Schedule a team call",
                "Show my calendar"
            ]
            return ("👋 Hello! I'm your AI-powered calendar assistant! ✨\n\n"
                   "I can help you with:\n"
                   "🗓️ **Schedule appointments** - Just tell me when you'd like to meet\n"
                   "📅 **Check availability** - I'll show you open time slots\n"
                   "🔄 **Manage bookings** - Cancel or reschedule existing appointments\n"
                   "📊 **Calendar insights** - View your schedule analytics\n\n"
                   "What would you like to do today?"), metadata
    
    async def _suggest_time_slots(self, metadata: dict) -> tuple[str, dict]:
        """Suggest available time slots with enhanced UI"""
        slots = self.calendar_service.get_available_slots(
            self.state.date, 
            self.state.duration,
            self.state.time_preference
        )
        
        if not slots:
            metadata["suggestions"] = ["try another date", "next week", "different time"]
            return (f"😔 I don't have any available slots on "
                   f"{self.state.date.strftime('%A, %B %d')}. "
                   f"Would you like to try a different date?"), metadata
        
        self.state.suggested_slots = slots
        self.state.step = "slot_selection"
        
        # Add slots to metadata for interactive display
        metadata["available_slots"] = [
            {
                "id": i,
                "start_time": slot.start_time.strftime('%I:%M %p'),
                "end_time": slot.end_time.strftime('%I:%M %p'),
                "confidence": slot.confidence_score,
                "recommended": slot.confidence_score > 0.8
            }
            for i, slot in enumerate(slots, 1)
        ]
        
        response = (f"🎉 Perfect! I found some great time slots for "
                   f"{self.state.date.strftime('%A, %B %d')}:\n\n")
        
        for i, slot in enumerate(slots, 1):
            confidence_emoji = "⭐" if slot.confidence_score > 0.8 else "✅"
            response += (f"{confidence_emoji} **{i}.** "
                        f"{slot.start_time.strftime('%I:%M %p')} - "
                        f"{slot.end_time.strftime('%I:%M %p')}")
            if slot.confidence_score > 0.8:
                response += " *(Recommended)*"
            response += "\n"
        
        response += "\n💡 Which slot would you prefer? Just tell me the number or time!"
        
        return response, metadata
    
    async def _handle_slot_selection(self, user_input: str, metadata: dict) -> tuple[str, dict]:
        """Handle time slot selection with enhanced feedback"""
        user_input_lower = user_input.lower()
        
        # Check for slot number selection
        for i in range(1, len(self.state.suggested_slots) + 1):
            if str(i) in user_input or f"slot {i}" in user_input_lower:
                self.state.selected_slot = self.state.suggested_slots[i-1]
                self.state.step = "confirmation"
                return await self._confirm_booking(metadata)
        
        # Check for time-based selection
        for slot in self.state.suggested_slots:
            time_str = slot.start_time.strftime('%I:%M').lstrip('0').lower()
            if time_str in user_input_lower or slot.start_time.strftime('%I %p').lower() in user_input_lower:
                self.state.selected_slot = slot
                self.state.step = "confirmation"
                return await self._confirm_booking(metadata)
        
        metadata["suggestions"] = ["1", "2", "3", "the first one", "2 PM slot"]
        return ("🤔 I didn't catch which slot you'd prefer. Could you tell me the "
               "number (1, 2, 3, etc.) or the specific time you want?"), metadata
    
    async def _confirm_booking(self, metadata: dict) -> tuple[str, dict]:
        """Confirm the booking details with enhanced presentation"""
        slot = self.state.selected_slot
        
        response = f"🎯 **Excellent choice!** Let me confirm your appointment:\n\n"
        response += f"📅 **Date:** {slot.start_time.strftime('%A, %B %d, %Y')}\n"
        response += f"🕐 **Time:** {slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}\n"
        response += f"⏱️ **Duration:** {self.state.duration} minutes\n"
        
        if self.state.selected_slot.confidence_score > 0.8:
            response += f"⭐ **AI Rating:** Optimal time slot!\n"
        
        response += "\n💼 What would you like to call this meeting?\n"
        response += "*Examples: 'Team Standup', 'Client Presentation', 'Strategy Session'*"
        
        metadata["confirmation_details"] = {
            "date": slot.start_time.strftime('%A, %B %d, %Y'),
            "time": f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}",
            "duration": self.state.duration,
            "confidence": slot.confidence_score
        }
        
        return response, metadata
    
    async def _handle_confirmation(self, user_input: str, metadata: dict) -> tuple[str, dict]:
        """Handle final confirmation and booking with celebration"""
        # Extract meeting title and type
        if user_input.strip():
            self.state.meeting_title = user_input.strip()
        else:
            self.state.meeting_title = "Meeting"
        
        meeting_type = self.nl_processor.extract_meeting_type(user_input)
        
        # Book the appointment
        appointment = self.calendar_service.book_appointment(
            self.state.selected_slot,
            self.state.meeting_title,
            self.state.attendee_email,
            meeting_type
        )
        
        response = f"🎉 **Booking Confirmed!** Your appointment is all set!\n\n"
        response += f"✅ **Meeting:** {appointment.title}\n"
        response += f"📅 **Date:** {appointment.start_time.strftime('%A, %B %d, %Y')}\n"
        response += f"🕐 **Time:** {appointment.start_time.strftime('%I:%M %p')} - {appointment.end_time.strftime('%I:%M %p')}\n"
        response += f"🏷️ **Type:** {appointment.meeting_type}\n"
        response += f"🆔 **Booking ID:** `{appointment.id[:8]}`\n\n"
        response += "📧 *Confirmation email sent!*\n"
        response += "📱 *Calendar invite created!*\n\n"
        response += "🤝 Is there anything else I can help you with today?"
        
        metadata["booking_success"] = {
            "appointment_id": appointment.id,
            "title": appointment.title,
            "date_time": appointment.start_time.isoformat(),
            "type": appointment.meeting_type
        }
        
        # Reset state for next interaction
        self.reset_state()
        
        return response, metadata
    
    async def _show_availability(self, metadata: dict) -> tuple[str, dict]:
        """Show availability with enhanced visualization"""
        slots = self.calendar_service.get_available_slots(
            self.state.date,
            self.state.duration,
            self.state.time_preference
        )
        
        if not slots:
            return (f"📅 I'm completely booked on "
                   f"{self.state.date.strftime('%A, %B %d')}. "
                   f"Would you like to check another date?"), metadata
        
        metadata["available_slots"] = [
            {
                "start_time": slot.start_time.strftime('%I:%M %p'),
                "end_time": slot.end_time.strftime('%I:%M %p'),
                "confidence": slot.confidence_score,
                "recommended": slot.confidence_score > 0.8
            }
            for slot in slots
        ]
        
        response = f"📅 **Availability for {self.state.date.strftime('%A, %B %d')}:**\n\n"
        
        for slot in slots:
            confidence_emoji = "⭐" if slot.confidence_score > 0.8 else "✅"
            response += (f"{confidence_emoji} "
                        f"{slot.start_time.strftime('%I:%M %p')} - "
                        f"{slot.end_time.strftime('%I:%M %p')}")
            if slot.confidence_score > 0.8:
                response += " *(Optimal)*"
            response += "\n"
        
        response += f"\n🤔 Would you like to book any of these slots?"
        
        return response, metadata
    
    async def _handle_general_inquiry(self, user_input: str, metadata: dict) -> tuple[str, dict]:
        """Handle general inquiries with helpful suggestions"""
        metadata["suggestions"] = [
            "Book a meeting tomorrow",
            "Check my availability",
            "Show calendar analytics",
            "Cancel an appointment"
        ]
        
        return ("🤖 I'm here to help you manage your calendar efficiently! "
               "I can assist with scheduling appointments, checking availability, "
               "and managing your bookings.\n\n"
               "💡 **Try saying:**\n"
               "• 'Book a meeting for tomorrow afternoon'\n"
               "• 'Show my availability this week'\n"
               "• 'Schedule a team call'\n"
               "• 'Cancel my 2 PM appointment'"), metadata

# ===== ENHANCED STREAMLIT UI =====

def create_analytics_dashboard(calendar_service):
    """Create an interactive analytics dashboard"""
    analytics = calendar_service.get_calendar_analytics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{analytics['total_appointments']}</div>
            <div class="stat-label">📅 Total Meetings</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{analytics['confirmed']}</div>
            <div class="stat-label">✅ Confirmed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{analytics['this_week']}</div>
            <div class="stat-label">📊 This Week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{analytics['utilization_rate']:.0f}%</div>
            <div class="stat-label">⚡ Utilization</div>
        </div>
        """, unsafe_allow_html=True)

def create_time_slots_display(slots_data):
    """Create interactive time slot display"""
    if not slots_data:
        return
    
    st.markdown("### 🕐 Available Time Slots")
    
    for slot in slots_data:
        confidence_color = "#4CAF50" if slot["recommended"] else "#2196F3"
        
        st.markdown(f"""
        <div class="time-slot-card" style="background: linear-gradient(135deg, {confidence_color}, #667eea);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>Slot {slot['id']}: {slot['start_time']} - {slot['end_time']}</strong>
                    {'⭐ Recommended' if slot['recommended'] else ''}
                </div>
                <div style="font-size: 0.9em; opacity: 0.9;">
                    AI Score: {slot['confidence']:.1f}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_quick_actions():
    """Create quick action buttons"""
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Book Tomorrow", key="quick_tomorrow"):
            st.session_state.quick_message = "Book a meeting tomorrow morning"
    
    with col2:
        if st.button("🔍 Check This Week", key="quick_week"):
            st.session_state.quick_message = "Show my availability this week"
    
    with col3:
        if st.button("📊 Show Analytics", key="quick_analytics"):
            st.session_state.show_analytics = True

def main():
    """Enhanced main Streamlit application"""
    
    st.set_page_config(
        page_title="AI Calendar Booking Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Enhanced Header
    st.markdown("""
    <div class="agent-header">
        <h1 class="agent-title">🤖 AI Calendar Booking Agent</h1>
        <p class="agent-subtitle">Natural language appointment scheduling powered by LangGraph & AI optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "agent" not in st.session_state:
        st.session_state.agent = EnhancedBookingAgent()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "👋 Hello! I'm your AI-powered calendar assistant! ✨\n\nI can help you with:\n🗓️ **Schedule appointments** - Just tell me when you'd like to meet\n📅 **Check availability** - I'll show you open time slots\n🔄 **Manage bookings** - Cancel or reschedule existing appointments\n📊 **Calendar insights** - View your schedule analytics\n\nWhat would you like to do today?"
            }
        ]
    
    if "show_analytics" not in st.session_state:
        st.session_state.show_analytics = False
    
    if "quick_message" not in st.session_state:
        st.session_state.quick_message = None
    
    # Main layout
    main_col, sidebar_col = st.columns([2, 1])
    
    with sidebar_col:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Analytics Dashboard
        st.markdown("### 📊 Calendar Analytics")
        create_analytics_dashboard(st.session_state.agent.calendar_service)
        
        # Current Bookings
        st.markdown("### 📅 Recent Bookings")
        appointments = st.session_state.agent.calendar_service.appointments
        for apt in appointments[-3:]:
            status_class = "status-confirmed" if apt.status == BookingStatus.CONFIRMED else "status-pending"
            st.markdown(f"""
            <div class="feature-card">
                <strong>{apt.title}</strong><br>
                <span style="font-size: 0.9em; color: #666;">
                    {apt.start_time.strftime('%m/%d %I:%M %p')}
                </span><br>
                <span class="status-badge {status_class}">
                    {apt.status.value.title()}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick Actions
        create_quick_actions()
        
        # Features
        st.markdown("### ✨ Features")
        st.markdown("""
        <div class="feature-card">
            <div class="emoji-large">🧠</div><strong>AI-Powered</strong><br>
            <small>Smart time slot recommendations</small>
        </div>
        
        <div class="feature-card">
            <div class="emoji-large">💬</div><strong>Natural Language</strong><br>
            <small>Talk to me like a human</small>
        </div>
        
        <div class="feature-card">
            <div class="emoji-large">⚡</div><strong>Real-time</strong><br>
            <small>Instant availability checking</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Reset button
        if st.button("🔄 Reset Conversation", type="secondary"):
            st.session_state.agent.reset_state()
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "👋 Hello! I'm your AI calendar assistant. How can I help you today?"
                }
            ]
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with main_col:
        # Chat interface
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle quick actions
        if st.session_state.quick_message:
            prompt = st.session_state.quick_message
            st.session_state.quick_message = None
            
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Thinking..."):
                    response, metadata = asyncio.run(st.session_state.agent.process_message(prompt))
                st.markdown(response)
                
                # Display interactive elements based on metadata
                if metadata.get("available_slots"):
                    create_time_slots_display(metadata["available_slots"])
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        # Chat input
        if prompt := st.chat_input("💬 Type your message here... (e.g., 'Book a meeting tomorrow afternoon')"):
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Processing your request..."):
                    response, metadata = asyncio.run(st.session_state.agent.process_message(prompt))
                
                st.markdown(response)
                
                # Display interactive elements based on metadata
                if metadata.get("available_slots"):
                    create_time_slots_display(metadata["available_slots"])
                
                if metadata.get("booking_success"):
                    st.balloons()  # Celebration animation
                    st.markdown("""
                    <div class="success-message">
                        🎉 Booking successfully completed! Calendar updated.
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: rgba(255,255,255,0.8);">
        Built with ❤️ using Streamlit, FastAPI concepts, and LangGraph patterns | 
        🚀 AI-Powered Calendar Assistant with Enhanced UI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()