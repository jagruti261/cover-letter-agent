import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class ResumeParser:
    """Parse resume text to extract structured information"""
    
    def __init__(self):
        # Skills database - you can expand this
        self.skills_keywords = [
            # Programming languages
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'typescript', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql',
            
            # Web technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
            'flask', 'spring', 'laravel', 'rails', 'asp.net',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle',
            'sqlite', 'cassandra', 'dynamodb',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
            'ansible', 'git', 'gitlab', 'github',
            
            # Data Science & AI
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter',
            
            # General skills
            'project management', 'agile', 'scrum', 'leadership', 'communication',
            'problem solving', 'analytical thinking'
        ]
        
        self.education_keywords = [
            'university', 'college', 'degree', 'bachelor', 'master', 'phd', 'doctorate',
            'certification', 'diploma', 'graduate', 'undergraduate', 'school',
            'institute', 'academy', 'education'
        ]
        
        self.experience_keywords = [
            'experience', 'work', 'employment', 'job', 'position', 'role',
            'company', 'organization', 'responsibilities', 'achievements',
            'projects', 'developed', 'managed', 'led', 'implemented'
        ]
    
    def parse_resume(self, text: str) -> Dict:
        """
        Parse resume text and extract structured information
        
        Args:
            text (str): Resume text
            
        Returns:
            dict: Structured resume data
        """
        try:
            return {
                'contact_info': self._extract_contact_info(text),
                'skills': self._extract_skills(text),
                'experience': self._extract_experience(text),
                'education': self._extract_education(text),
                'summary': self._extract_summary(text),
                'projects': self._extract_projects(text)
            }
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            return self._get_empty_resume_data()
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        contact_info = {
            'email': None,
            'phone': None,
            'name': None,
            'linkedin': None,
            'github': None
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Extract phone number
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_matches:
            contact_info['linkedin'] = linkedin_matches[0]
        
        # Extract GitHub
        github_pattern = r'github\.com/[\w-]+'
        github_matches = re.findall(github_pattern, text, re.IGNORECASE)
        if github_matches:
            contact_info['github'] = github_matches[0]
        
        # Extract name (assume first line or near email)
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and all(word.replace('.', '').isalpha() for word in line.split()):
                contact_info['name'] = line
                break
        
        return contact_info
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        found_skills = []
        text_lower = text.lower()
        
        # Look for skills in the skills keywords list
        for skill in self.skills_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill.title())
        
        # Look for skills in dedicated skills section
        skills_section_pattern = r'(?:skills?|technical skills?|competencies)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z]|$)'
        skills_matches = re.findall(skills_section_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in skills_matches:
            # Extract individual skills from the skills section
            skills_text = match.strip()
            # Split by common separators
            potential_skills = re.split(r'[,•\-\n\t]+', skills_text)
            for skill in potential_skills:
                skill = skill.strip()
                if skill and len(skill) < 50:  # Reasonable skill name length
                    found_skills.append(skill.title())
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience"""
        experience_list = []
        
        # Look for experience section
        exp_pattern = r'(?:experience|employment|work history)[:]*\s*\n(.*?)(?:\n\s*\n|\n(?:education|skills|projects)|$)'
        exp_matches = re.findall(exp_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in exp_matches:
            exp_text = match.strip()
            
            # Try to extract individual job entries
            # Look for patterns like "Job Title at Company" or "Company - Job Title"
            job_pattern = r'([A-Za-z\s]+(?:Engineer|Developer|Manager|Analyst|Specialist|Coordinator|Director|Lead|Senior|Junior))[,\s]*(?:at|@|-)\s*([A-Za-z\s&.,]+)'
            jobs = re.findall(job_pattern, exp_text, re.IGNORECASE)
            
            for job_title, company in jobs:
                experience_list.append({
                    'title': job_title.strip(),
                    'company': company.strip(),
                    'description': self._extract_job_description(exp_text, job_title, company)
                })
        
        return experience_list
    
    def _extract_job_description(self, text: str, job_title: str, company: str) -> str:
        """Extract job description for a specific role"""
        # This is a simplified version - you could make it more sophisticated
        lines = text.split('\n')
        description_lines = []
        found_job = False
        
        for line in lines:
            line = line.strip()
            if job_title.lower() in line.lower() and company.lower() in line.lower():
                found_job = True
                continue
            
            if found_job:
                if line and (line.startswith('-') or line.startswith('•') or 'responsible' in line.lower()):
                    description_lines.append(line)
                elif line and len(line) > 30:  # Likely a description line
                    description_lines.append(line)
                elif not line:  # Empty line might indicate end of this job
                    break
        
        return ' '.join(description_lines)
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education_list = []
        
        # Look for education section
        edu_pattern = r'(?:education|academic background|qualifications)[:]*\s*\n(.*?)(?:\n\s*\n|\n(?:experience|skills|projects)|$)'
        edu_matches = re.findall(edu_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in edu_matches:
            edu_text = match.strip()
            
            # Look for degree patterns
            degree_pattern = r'(Bachelor|Master|PhD|Doctorate|Diploma|Certificate)[s]?\s+(?:of|in)?\s+([A-Za-z\s]+)(?:\s+(?:from|at)\s+([A-Za-z\s&.,]+))?'
            degrees = re.findall(degree_pattern, edu_text, re.IGNORECASE)
            
            for degree_type, field, institution in degrees:
                education_list.append({
                    'degree': f"{degree_type} in {field}".strip(),
                    'institution': institution.strip() if institution else 'Not specified',
                    'field': field.strip()
                })
        
        return education_list
    
    def _extract_summary(self, text: str) -> str:
        """Extract summary or objective"""
        # Look for summary/objective section
        summary_patterns = [
            r'(?:summary|objective|profile|about)[:]*\s*\n(.*?)(?:\n\s*\n|\n[A-Z]|$)',
            r'^(.*?)(?:\n\s*\n|\nexperience|\neducation|\nskills)'
        ]
        
        for pattern in summary_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                summary = matches[0].strip()
                if len(summary) > 50:  # Reasonable summary length
                    return summary
        
        # If no dedicated summary, extract first meaningful paragraph
        paragraphs = text.split('\n\n')
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if len(paragraph) > 100 and 'experience' in paragraph.lower():
                return paragraph
        
        return "No summary available"
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract project information"""
        projects = []
        
        # Look for projects section
        project_pattern = r'(?:projects?|portfolio)[:]*\s*\n(.*?)(?:\n\s*\n|\n(?:experience|education|skills)|$)'
        project_matches = re.findall(project_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in project_matches:
            project_text = match.strip()
            
            # Simple project extraction - look for bullet points or lines
            lines = project_text.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or len(line) > 30):
                    projects.append({
                        'name': line[:50] + '...' if len(line) > 50 else line,
                        'description': line
                    })
        
        return projects
    
    def _get_empty_resume_data(self) -> Dict:
        """Return empty resume data structure"""
        return {
            'contact_info': {
                'email': None,
                'phone': None,
                'name': None,
                'linkedin': None,
                'github': None
            },
            'skills': [],
            'experience': [],
            'education': [],
            'summary': "Unable to parse resume content",
            'projects': []
        }