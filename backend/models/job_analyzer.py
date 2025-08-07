import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class JobAnalyzer:
    """Analyze job descriptions to extract key information"""
    
    def __init__(self):
        self.requirement_keywords = [
            'required', 'must have', 'essential', 'mandatory', 'minimum',
            'necessary', 'should have', 'experience with', 'proficient in',
            'knowledge of', 'familiar with', 'expertise in'
        ]
        
        self.skills_patterns = [
            r'(?:experience|proficiency|skills?)\s+(?:in|with|using)\s+([^,.]+)',
            r'(?:knowledge|understanding)\s+of\s+([^,.]+)',
            r'(?:proficient|expert)\s+in\s+([^,.]+)',
            r'(\d+\+?\s*years?)\s+(?:of\s+)?(?:experience\s+)?(?:with|in)\s+([^,.]+)'
        ]
    
    def analyze_job_description(self, job_text: str) -> Dict:
        """
        Analyze job description and extract structured information
        
        Args:
            job_text (str): Job description text
            
        Returns:
            dict: Structured job analysis data
        """
        try:
            return {
                'company_info': self._extract_company_info(job_text),
                'job_title': self._extract_job_title(job_text),
                'required_skills': self._extract_required_skills(job_text),
                'preferred_skills': self._extract_preferred_skills(job_text),
                'responsibilities': self._extract_responsibilities(job_text),
                'qualifications': self._extract_qualifications(job_text),
                'benefits': self._extract_benefits(job_text),
                'job_type': self._extract_job_type(job_text),
                'experience_level': self._extract_experience_level(job_text),
                'key_requirements': self._extract_key_requirements(job_text)
            }
        except Exception as e:
            logger.error(f"Error analyzing job description: {str(e)}")
            return self._get_empty_job_data()
    
    def _extract_company_info(self, text: str) -> Dict:
        """Extract company information"""
        company_info = {
            'name': None,
            'description': None,
            'industry': None
        }
        
        # Look for company name patterns
        company_patterns = [
            r'(?:company|organization|employer)[:]\s*([A-Za-z\s&.,]+)',
            r'^([A-Z][A-Za-z\s&.,]+)(?:\s+is\s+)',
            r'(?:join|work at|employment with)\s+([A-Z][A-Za-z\s&.,]+)'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            if matches:
                company_info['name'] = matches[0].strip()
                break
        
        # Extract company description
        desc_patterns = [
            r'(?:about us|company description|who we are)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z])',
            r'([A-Z][^.]*(?:company|organization|business|firm)[^.]*\.)'
        ]
        
        for pattern in desc_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                company_info['description'] = matches[0].strip()
                break
        
        return company_info
    
    def _extract_job_title(self, text: str) -> str:
        """Extract job title"""
        # Look for job title patterns at the beginning
        lines = text.split('\n')
        for line in lines[:3]:  # Check first 3 lines
            line = line.strip()
            if line and any(word in line.lower() for word in ['engineer', 'developer', 'manager', 'analyst', 'specialist', 'director', 'coordinator', 'lead', 'senior', 'junior']):
                return line
        
        # Fallback: look for position/role keywords
        title_pattern = r'(?:position|role|job title)[:]\s*([^\n]+)'
        matches = re.findall(title_pattern, text, re.IGNORECASE)
        if matches:
            return matches[0].strip()
        
        return "Position title not specified"
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills and technologies"""
        skills = []
        
        # Look for requirements section
        req_patterns = [
            r'(?:required|requirements|must have|essential)[:]*\s*\n(.*?)(?:\n\s*\n|\n(?:preferred|nice|benefits)|$)',
            r'(?:you must have|minimum requirements)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z])',
            r'(?:required skills?|technical requirements)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z])'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Extract skills from the requirements section
                req_text = match.strip()
                skills.extend(self._parse_skills_from_text(req_text))
        
        # Use skill patterns to find more skills
        for pattern in self.skills_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    skills.append(match[-1].strip())  # Take the last part (skill name)
                else:
                    skills.append(match.strip())
        
        return list(set(skill.title() for skill in skills if skill.strip()))
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred/nice-to-have skills"""
        skills = []
        
        # Look for preferred skills section
        pref_patterns = [
            r'(?:preferred|nice to have|bonus|plus|additional)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'(?:nice if you have|would be great)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z])',
            r'(?:preferred qualifications|desired skills)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z])'
        ]
        
        for pattern in pref_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                pref_text = match.strip()
                skills.extend(self._parse_skills_from_text(pref_text))
        
        return list(set(skill.title() for skill in skills if skill.strip()))
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []
        
        # Look for responsibilities section
        resp_patterns = [
            r'(?:responsibilities|duties|you will|what you\'ll do)[:]*\s*\n(.*?)(?:\n\s*\n|\n(?:requirements|qualifications)|$)',
            r'(?:key responsibilities|main duties)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z])',
            r'(?:in this role|as a .+, you will)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z])'
        ]
        
        for pattern in resp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                resp_text = match.strip()
                # Split by bullet points or new lines
                resp_items = re.split(r'[•\-\n]+', resp_text)
                for item in resp_items:
                    item = item.strip()
                    if item and len(item) > 10:  # Filter out very short items
                        responsibilities.append(item)
        
        return responsibilities
    
    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract required qualifications"""
        qualifications = []
        
        qual_patterns = [
            r'(?:qualifications|education|degree)[:]*\s*\n(.*?)(?:\n\s*\n|\n(?:experience|skills)|$)',
            r'(?:minimum qualifications|educational requirements)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z])',
            r'(?:bachelor|master|phd|degree)([^.]+\.)'
        ]
        
        for pattern in qual_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                qual_text = match.strip()
                if len(qual_text) > 5:
                    qualifications.append(qual_text)
        
        return qualifications
    
    def _extract_benefits(self, text: str) -> List[str]:
        """Extract job benefits"""
        benefits = []
        
        benefit_patterns = [
            r'(?:benefits|perks|we offer|compensation)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'(?:health insurance|401k|vacation|remote work|flexible)',
            r'(?:competitive salary|stock options|bonus)'
        ]
        
        for pattern in benefit_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if isinstance(match, str) and len(match.strip()) > 5:
                    benefits.append(match.strip())
        
        return benefits
    
    def _extract_job_type(self, text: str) -> str:
        """Extract job type (full-time, part-time, contract, etc.)"""
        job_types = ['full-time', 'part-time', 'contract', 'freelance', 'temporary', 'internship', 'remote']
        
        text_lower = text.lower()
        for job_type in job_types:
            if job_type in text_lower:
                return job_type.title()
        
        return "Not specified"
    
    def _extract_experience_level(self, text: str) -> str:
        """Extract required experience level"""
        exp_patterns = [
            r'(\d+\+?)\s*years?\s*(?:of\s*)?experience',
            r'(?:senior|junior|entry.level|mid.level|experienced)',
            r'(?:minimum|at least)\s*(\d+)\s*years?'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return str(matches[0]) + " years" if matches[0].isdigit() else matches[0]
        
        return "Not specified"
    
    def _extract_key_requirements(self, text: str) -> List[str]:
        """Extract the most important requirements"""
        requirements = []
        
        # Look for bullet points or numbered lists in requirements
        req_text = text.lower()
        
        # Find sections that likely contain requirements
        if 'requirements' in req_text:
            req_section = re.search(r'requirements[:]*\s*(.*?)(?:\n\s*\n|\Z)', text, re.IGNORECASE | re.DOTALL)
            if req_section:
                req_content = req_section.group(1)
                # Extract bullet points
                bullets = re.findall(r'[•\-]\s*([^\n•\-]+)', req_content)
                requirements.extend([bullet.strip() for bullet in bullets if len(bullet.strip()) > 10])
        
        return requirements[:10]  # Return top 10 requirements
    
    def _parse_skills_from_text(self, text: str) -> List[str]:
        """Parse individual skills from a text block"""
        skills = []
        
        # Common skill separators
        separators = r'[,;•\-\n\t]+'
        potential_skills = re.split(separators, text)
        
        for skill in potential_skills:
            skill = skill.strip()
            # Filter out common non-skill phrases
            skip_phrases = [
                'experience', 'knowledge', 'understanding', 'proficiency',
                'years', 'minimum', 'required', 'preferred', 'must have',
                'should have', 'ability to', 'strong', 'excellent'
            ]
            
            if (skill and 
                len(skill) > 2 and 
                len(skill) < 50 and 
                not any(phrase in skill.lower() for phrase in skip_phrases) and
                not skill.isdigit()):
                skills.append(skill)
        
        return skills
    
    def _get_empty_job_data(self) -> Dict:
        """Return empty job data structure"""
        return {
            'company_info': {'name': None, 'description': None, 'industry': None},
            'job_title': "Not specified",
            'required_skills': [],
            'preferred_skills': [],
            'responsibilities': [],
            'qualifications': [],
            'benefits': [],
            'job_type': "Not specified",
            'experience_level': "Not specified",
            'key_requirements': []
        }