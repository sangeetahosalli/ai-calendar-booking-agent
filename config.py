# config.py
# Configuration module to load environment variables

import os
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Configuration class to manage environment variables"""
    
    # =============================================================================
    # APPLICATION SETTINGS
    # =============================================================================
    APP_NAME: str = os.getenv("APP_NAME", "AI Calendar Booking Agent")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # =============================================================================
    # STREAMLIT CONFIGURATION
    # =============================================================================
    STREAMLIT_SERVER_PORT: int = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    STREAMLIT_SERVER_ADDRESS: str = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
    STREAMLIT_SERVER_HEADLESS: bool = os.getenv("STREAMLIT_SERVER_HEADLESS", "false").lower() == "true"
    STREAMLIT_THEME_PRIMARY_COLOR: str = os.getenv("STREAMLIT_THEME_PRIMARY_COLOR", "#667eea")
    STREAMLIT_THEME_BACKGROUND_COLOR: str = os.getenv("STREAMLIT_THEME_BACKGROUND_COLOR", "#FFFFFF")
    
    # =============================================================================
    # GOOGLE CALENDAR API
    # =============================================================================
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_PROJECT_ID: Optional[str] = os.getenv("GOOGLE_PROJECT_ID")
    GOOGLE_CALENDAR_CREDENTIALS_FILE: str = os.getenv("GOOGLE_CALENDAR_CREDENTIALS_FILE", "credentials.json")
    GOOGLE_CALENDAR_TOKEN_FILE: str = os.getenv("GOOGLE_CALENDAR_TOKEN_FILE", "token.json")
    GOOGLE_CALENDAR_SCOPES: str = os.getenv("GOOGLE_CALENDAR_SCOPES", "https://www.googleapis.com/auth/calendar")
    
    # =============================================================================
    # DATABASE CONFIGURATION
    # =============================================================================
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./calendar_agent.db")
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"
    
    # =============================================================================
    # EMAIL CONFIGURATION
    # =============================================================================
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAIL_FROM: Optional[str] = os.getenv("EMAIL_FROM")
    EMAIL_FROM_NAME: str = os.getenv("EMAIL_FROM_NAME", "AI Calendar Assistant")
    
    # =============================================================================
    # AI/ML CONFIGURATION
    # =============================================================================
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "150"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    
    # =============================================================================
    # SECURITY SETTINGS
    # =============================================================================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ENCRYPT_KEY: Optional[str] = os.getenv("ENCRYPT_KEY")
    
    # Session settings
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    ACCOUNT_LOCKOUT_DURATION_MINUTES: int = int(os.getenv("ACCOUNT_LOCKOUT_DURATION_MINUTES", "15"))
    
    # =============================================================================
    # RATE LIMITING
    # =============================================================================
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    RATE_LIMIT_PER_HOUR: int = int(os.getenv("RATE_LIMIT_PER_HOUR", "1000"))
    RATE_LIMIT_PER_DAY: int = int(os.getenv("RATE_LIMIT_PER_DAY", "10000"))
    
    # =============================================================================
    # THIRD-PARTY INTEGRATIONS
    # =============================================================================
    # Zoom
    ZOOM_CLIENT_ID: Optional[str] = os.getenv("ZOOM_CLIENT_ID")
    ZOOM_CLIENT_SECRET: Optional[str] = os.getenv("ZOOM_CLIENT_SECRET")
    ZOOM_ACCOUNT_ID: Optional[str] = os.getenv("ZOOM_ACCOUNT_ID")
    
    # Microsoft Teams
    TEAMS_CLIENT_ID: Optional[str] = os.getenv("TEAMS_CLIENT_ID")
    TEAMS_CLIENT_SECRET: Optional[str] = os.getenv("TEAMS_CLIENT_SECRET")
    TEAMS_TENANT_ID: Optional[str] = os.getenv("TEAMS_TENANT_ID")
    
    # Slack
    SLACK_BOT_TOKEN: Optional[str] = os.getenv("SLACK_BOT_TOKEN")
    SLACK_APP_TOKEN: Optional[str] = os.getenv("SLACK_APP_TOKEN")
    SLACK_SIGNING_SECRET: Optional[str] = os.getenv("SLACK_SIGNING_SECRET")
    
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: Optional[str] = os.getenv("TWILIO_PHONE_NUMBER")
    
    # =============================================================================
    # CALENDAR BUSINESS RULES
    # =============================================================================
    DEFAULT_MEETING_DURATION: int = int(os.getenv("DEFAULT_MEETING_DURATION", "60"))
    MIN_MEETING_DURATION: int = int(os.getenv("MIN_MEETING_DURATION", "15"))
    MAX_MEETING_DURATION: int = int(os.getenv("MAX_MEETING_DURATION", "480"))
    BUSINESS_HOURS_START: int = int(os.getenv("BUSINESS_HOURS_START", "9"))
    BUSINESS_HOURS_END: int = int(os.getenv("BUSINESS_HOURS_END", "17"))
    BUSINESS_DAYS: List[int] = [int(x) for x in os.getenv("BUSINESS_DAYS", "1,2,3,4,5").split(",")]
    DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", "UTC")
    BOOKING_BUFFER_MINUTES: int = int(os.getenv("BOOKING_BUFFER_MINUTES", "15"))
    MAX_ADVANCE_BOOKING_DAYS: int = int(os.getenv("MAX_ADVANCE_BOOKING_DAYS", "90"))
    MIN_ADVANCE_BOOKING_HOURS: int = int(os.getenv("MIN_ADVANCE_BOOKING_HOURS", "2"))
    
    # =============================================================================
    # NOTIFICATION SETTINGS
    # =============================================================================
    ENABLE_EMAIL_NOTIFICATIONS: bool = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "true").lower() == "true"
    ENABLE_SMS_NOTIFICATIONS: bool = os.getenv("ENABLE_SMS_NOTIFICATIONS", "false").lower() == "true"
    ENABLE_PUSH_NOTIFICATIONS: bool = os.getenv("ENABLE_PUSH_NOTIFICATIONS", "true").lower() == "true"
    REMINDER_INTERVALS: List[str] = os.getenv("REMINDER_INTERVALS", "24h,1h,15m").split(",")
    DEFAULT_REMINDER_TIME: str = os.getenv("DEFAULT_REMINDER_TIME", "15m")
    
    # =============================================================================
    # ANALYTICS & MONITORING
    # =============================================================================
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "true").lower() == "true"
    ANALYTICS_RETENTION_DAYS: int = int(os.getenv("ANALYTICS_RETENTION_DAYS", "90"))
    ENABLE_PERFORMANCE_MONITORING: bool = os.getenv("ENABLE_PERFORMANCE_MONITORING", "true").lower() == "true"
    
    GA_MEASUREMENT_ID: Optional[str] = os.getenv("GA_MEASUREMENT_ID")
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    
    # =============================================================================
    # CACHING CONFIGURATION
    # =============================================================================
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    
    # =============================================================================
    # FILE STORAGE
    # =============================================================================
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_EXTENSIONS: List[str] = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,pdf,doc,docx").split(",")
    
    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: Optional[str] = os.getenv("AWS_S3_BUCKET")
    AWS_S3_REGION: str = os.getenv("AWS_S3_REGION", "us-east-1")
    
    # =============================================================================
    # DEVELOPMENT SETTINGS
    # =============================================================================
    DEV_MOCK_GOOGLE_CALENDAR: bool = os.getenv("DEV_MOCK_GOOGLE_CALENDAR", "true").lower() == "true"
    DEV_MOCK_EMAIL_SENDING: bool = os.getenv("DEV_MOCK_EMAIL_SENDING", "true").lower() == "true"
    DEV_ENABLE_TEST_DATA: bool = os.getenv("DEV_ENABLE_TEST_DATA", "true").lower() == "true"
    DEV_SHOW_DEBUG_INFO: bool = os.getenv("DEV_SHOW_DEBUG_INFO", "true").lower() == "true"
    
    # =============================================================================
    # FEATURE FLAGS
    # =============================================================================
    FEATURE_AI_RECOMMENDATIONS: bool = os.getenv("FEATURE_AI_RECOMMENDATIONS", "true").lower() == "true"
    FEATURE_MULTI_LANGUAGE: bool = os.getenv("FEATURE_MULTI_LANGUAGE", "false").lower() == "true"
    FEATURE_VOICE_INPUT: bool = os.getenv("FEATURE_VOICE_INPUT", "false").lower() == "true"
    FEATURE_CALENDAR_SYNC: bool = os.getenv("FEATURE_CALENDAR_SYNC", "true").lower() == "true"
    FEATURE_TEAM_SCHEDULING: bool = os.getenv("FEATURE_TEAM_SCHEDULING", "false").lower() == "true"
    FEATURE_RECURRING_MEETINGS: bool = os.getenv("FEATURE_RECURRING_MEETINGS", "true").lower() == "true"
    
    # =============================================================================
    # COMPANY SETTINGS
    # =============================================================================
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Your Company Name")
    COMPANY_EMAIL: str = os.getenv("COMPANY_EMAIL", "contact@yourcompany.com")
    COMPANY_PHONE: str = os.getenv("COMPANY_PHONE", "+1-234-567-8900")
    COMPANY_ADDRESS: str = os.getenv("COMPANY_ADDRESS", "123 Business St, City, State 12345")
    COMPANY_WEBSITE: str = os.getenv("COMPANY_WEBSITE", "https://yourcompany.com")
    
    MEETING_ROOMS: List[str] = os.getenv("MEETING_ROOMS", "Conference Room A,Conference Room B,Board Room").split(",")
    ROOM_CAPACITIES: List[int] = [int(x) for x in os.getenv("ROOM_CAPACITIES", "10,10,20").split(",")]
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.ENVIRONMENT.lower() == "development"
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the appropriate database URL"""
        return cls.DATABASE_URL
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return list of missing required settings"""
        missing = []
        
        # Check required settings for production
        if cls.is_production():
            required_production_settings = [
                ("SECRET_KEY", cls.SECRET_KEY),
                ("JWT_SECRET_KEY", cls.JWT_SECRET_KEY),
            ]
            
            for setting_name, setting_value in required_production_settings:
                if not setting_value or setting_value in ["change-this-in-production", "your-jwt-secret-key"]:
                    missing.append(f"Production requires {setting_name} to be set")
        
        # Check Google Calendar integration
        if cls.FEATURE_CALENDAR_SYNC and not cls.DEV_MOCK_GOOGLE_CALENDAR:
            google_required = [
                ("GOOGLE_CLIENT_ID", cls.GOOGLE_CLIENT_ID),
                ("GOOGLE_CLIENT_SECRET", cls.GOOGLE_CLIENT_SECRET),
                ("GOOGLE_PROJECT_ID", cls.GOOGLE_PROJECT_ID),
            ]
            
            for setting_name, setting_value in google_required:
                if not setting_value:
                    missing.append(f"Google Calendar integration requires {setting_name}")
        
        # Check email configuration
        if cls.ENABLE_EMAIL_NOTIFICATIONS and not cls.DEV_MOCK_EMAIL_SENDING:
            email_required = [
                ("SMTP_USERNAME", cls.SMTP_USERNAME),
                ("SMTP_PASSWORD", cls.SMTP_PASSWORD),
                ("EMAIL_FROM", cls.EMAIL_FROM),
            ]
            
            for setting_name, setting_value in email_required:
                if not setting_value:
                    missing.append(f"Email notifications require {setting_name}")
        
        return missing
    
    @classmethod
    def print_config_summary(cls):
        """Print a summary of current configuration"""
        print(f"🚀 {cls.APP_NAME} v{cls.APP_VERSION}")
        print(f"🌍 Environment: {cls.ENVIRONMENT}")
        print(f"🐛 Debug Mode: {cls.DEBUG}")
        print(f"🗄️  Database: {cls.DATABASE_URL}")
        print(f"📧 Email Notifications: {cls.ENABLE_EMAIL_NOTIFICATIONS}")
        print(f"🤖 AI Recommendations: {cls.FEATURE_AI_RECOMMENDATIONS}")
        print(f"📅 Google Calendar: {cls.FEATURE_CALENDAR_SYNC}")
        
        # Validate configuration
        missing = cls.validate_config()
        if missing:
            print("\n⚠️  Configuration Issues:")
            for issue in missing:
                print(f"   - {issue}")
        else:
            print("\n✅ Configuration is valid!")

# Create global config instance
config = Config()

# Utility functions
def get_config() -> Config:
    """Get the global configuration instance"""
    return config

def reload_config():
    """Reload configuration from environment variables"""
    global config
    load_dotenv(dotenv_path=env_path, override=True)
    config = Config()
    return config

if __name__ == "__main__":
    # Print configuration summary when run directly
    config.print_config_summary()