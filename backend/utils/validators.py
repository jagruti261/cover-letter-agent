import re
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class InputValidator:
    """Validate user inputs and extracted data"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        # Check if it's a valid length (10-15 digits)
        return 10 <= len(digits) <= 15
    
    @staticmethod
    def validate_job_description(job_text: str) -> bool:
        """Validate job description"""
        if not job_text or not isinstance(job_text, str):
            return False
        
        # Must be at least 50 characters and contain some key job-related words
        if len(job_text.strip()) < 50:
            return False
        
        job_keywords = [
            'position', 'role', 'responsibilities', 'requirements', 
            'experience', 'skills', 'qualifications', 'company',
            'job', 'work', 'candidate', 'team', 'project'
        ]
        
        text_lower = job_text.lower()
        keyword_count = sum(1 for keyword in job_keywords if keyword in text_lower)
        
        return keyword_count >= 3
    
    @staticmethod
    def validate_resume_text(resume_text: str) -> bool:
        """Validate resume text"""
        if not resume_text or not isinstance(resume_text, str):
            return False
        
        # Must be at least 100 characters
        if len(resume_text.strip()) < 100:
            return False
        
        resume_keywords = [
            'experience', 'education', 'skills', 'work', 'university',
            'college', 'degree', 'project', 'achievement', 'responsibility'
        ]
        
        text_lower = resume_text.lower()
        keyword_count = sum(1 for keyword in resume_keywords if keyword in text_lower)
        
        return keyword_count >= 3
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Sanitize text input"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove potentially harmful characters
        text = re.sub(r'[<>"\']', '', text)
        
        return text
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int = 16777216) -> bool:
        """Validate file size (default 16MB)"""
        return 0 < file_size <= max_size