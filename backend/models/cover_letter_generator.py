import os
import logging
from typing import Dict, Optional
from dotenv import load_dotenv 
import google.generativeai as genai

logger = logging.getLogger(__name__)

load_dotenv()

class CoverLetterGenerator:
    """Generate personalized cover letters using AI"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-pro')
        
        # Template styles
        self.templates = {
            'professional': self._professional_template,
            'creative': self._creative_template,
            'technical': self._technical_template,
            'entry_level': self._entry_level_template
        }
    
    def generate_cover_letter(self, 
                            resume_data: Dict, 
                            job_data: Dict, 
                            template_style: str = 'professional',
                            custom_message: str = None) -> Dict:
        """
        Generate a personalized cover letter
        
        Args:
            resume_data: Parsed resume information
            job_data: Analyzed job description
            template_style: Style of cover letter template
            custom_message: Optional custom message to include
            
        Returns:
            dict: Generated cover letter and metadata
        """
        try:
            # Select template
            template_func = self.templates.get(template_style, self.templates['professional'])
            
            # Create prompt
            prompt = template_func(resume_data, job_data, custom_message)
            
            # Generate cover letter
            response = self.model.generate_content(prompt)
            cover_letter_text = response.text
            
            # Post-process the generated text
            cover_letter_text = self._post_process_cover_letter(cover_letter_text, resume_data, job_data)
            
            return {
                'success': True,
                'cover_letter': cover_letter_text,
                'template_used': template_style,
                'word_count': len(cover_letter_text.split()),
                'recommendations': self._generate_improvement_suggestions(resume_data, job_data)
            }
            
        except Exception as e:
            logger.error(f"Error generating cover letter: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'cover_letter': None
            }
    
    def _professional_template(self, resume_data: Dict, job_data: Dict, custom_message: str = None) -> str:
        """Professional cover letter template"""
        
        # Extract key information
        name = resume_data.get('contact_info', {}).get('name', 'Applicant')
        job_title = job_data.get('job_title', 'the position')
        company_name = job_data.get('company_info', {}).get('name', 'your company')
        skills = resume_data.get('skills', [])[:8]  # Top 8 skills
        experience = resume_data.get('experience', [])
        required_skills = job_data.get('required_skills', [])
        responsibilities = job_data.get('responsibilities', [])[:5]  # Top 5 responsibilities
        
        prompt = f"""
        Create a professional cover letter for {name} applying for the {job_title} position at {company_name}.

        RESUME INFORMATION:
        - Skills: {', '.join(skills)}
        - Experience: {self._format_experience_for_prompt(experience)}
        - Summary: {resume_data.get('summary', 'Experienced professional')}

        JOB REQUIREMENTS:
        - Required Skills: {', '.join(required_skills)}
        - Key Responsibilities: {'; '.join(responsibilities)}
        - Company: {job_data.get('company_info', {}).get('description', 'A leading company')}

        {f"CUSTOM MESSAGE TO INCLUDE: {custom_message}" if custom_message else ""}

        INSTRUCTIONS:
        1. Write a professional, engaging cover letter
        2. Highlight relevant skills that match job requirements
        3. Show enthusiasm for the role and company
        4. Include specific examples from experience when possible
        5. Keep it concise (3-4 paragraphs)
        6. Use professional tone throughout
        7. End with a strong call to action

        FORMAT:
        - Start with proper greeting
        - Include date and company address if company name is provided
        - 3-4 well-structured paragraphs
        - Professional closing

        Generate the cover letter now:
        """
        
        return prompt
    
    def _creative_template(self, resume_data: Dict, job_data: Dict, custom_message: str = None) -> str:
        """Creative cover letter template"""
        
        name = resume_data.get('contact_info', {}).get('name', 'Creative Professional')
        job_title = job_data.get('job_title', 'the position')
        company_name = job_data.get('company_info', {}).get('name', 'your innovative company')
        
        prompt = f"""
        Create a creative and engaging cover letter for {name} applying for the {job_title} position at {company_name}.

        RESUME INFORMATION:
        - Skills: {', '.join(resume_data.get('skills', [])[:8])}
        - Projects: {self._format_projects_for_prompt(resume_data.get('projects', []))}
        - Experience: {self._format_experience_for_prompt(resume_data.get('experience', []))}

        JOB INFORMATION:
        - Position: {job_title}
        - Company: {company_name}
        - Required Skills: {', '.join(job_data.get('required_skills', []))}

        {f"CUSTOM MESSAGE: {custom_message}" if custom_message else ""}

        INSTRUCTIONS:
        1. Use a creative, engaging tone while remaining professional
        2. Start with an attention-grabbing opening
        3. Tell a compelling story about relevant experience
        4. Show personality and passion for the field
        5. Demonstrate creativity in presentation
        6. Keep it engaging but concise
        7. End with memorable closing

        Generate a creative cover letter now:
        """
        
        return prompt
    
    def _technical_template(self, resume_data: Dict, job_data: Dict, custom_message: str = None) -> str:
        """Technical cover letter template"""
        
        technical_skills = [skill for skill in resume_data.get('skills', []) 
                          if any(tech in skill.lower() for tech in ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'react', 'angular', 'node'])]
        
        prompt = f"""
        Create a technical cover letter for a {job_data.get('job_title', 'technical position')} at {job_data.get('company_info', {}).get('name', 'the company')}.

        TECHNICAL BACKGROUND:
        - Technical Skills: {', '.join(technical_skills)}
        - All Skills: {', '.join(resume_data.get('skills', []))}
        - Experience: {self._format_experience_for_prompt(resume_data.get('experience', []))}
        - Projects: {self._format_projects_for_prompt(resume_data.get('projects', []))}

        JOB REQUIREMENTS:
        - Required Technical Skills: {', '.join(job_data.get('required_skills', []))}
        - Responsibilities: {'; '.join(job_data.get('responsibilities', [])[:5])}

        {f"ADDITIONAL CONTEXT: {custom_message}" if custom_message else ""}

        INSTRUCTIONS:
        1. Focus on technical qualifications and achievements
        2. Mention specific technologies and frameworks
        3. Include quantifiable results where possible
        4. Demonstrate problem-solving abilities
        5. Show understanding of technical challenges
        6. Keep professional but show technical depth
        7. Highlight relevant projects or implementations

        Generate a technical cover letter now:
        """
        
        return prompt
    
    def _entry_level_template(self, resume_data: Dict, job_data: Dict, custom_message: str = None) -> str:
        """Entry-level cover letter template"""
        
        education = resume_data.get('education', [])
        projects = resume_data.get('projects', [])
        
        prompt = f"""
        Create an entry-level cover letter for someone applying for {job_data.get('job_title', 'the position')} at {job_data.get('company_info', {}).get('name', 'the company')}.

        CANDIDATE BACKGROUND:
        - Education: {self._format_education_for_prompt(education)}
        - Skills: {', '.join(resume_data.get('skills', []))}
        - Projects: {self._format_projects_for_prompt(projects)}
        - Experience: {self._format_experience_for_prompt(resume_data.get('experience', []))}

        JOB INFORMATION:
        - Position: {job_data.get('job_title', 'Entry-level position')}
        - Required Skills: {', '.join(job_data.get('required_skills', []))}
        - Company: {job_data.get('company_info', {}).get('name', 'the company')}

        {f"PERSONAL MESSAGE: {custom_message}" if custom_message else ""}

        INSTRUCTIONS:
        1. Emphasize eagerness to learn and grow
        2. Highlight relevant coursework and projects
        3. Show enthusiasm and passion for the field
        4. Demonstrate quick learning ability
        5. Mention any internships or relevant experience
        6. Focus on potential and transferable skills
        7. Show research about the company

        Generate an entry-level cover letter now:
        """
        
        return prompt
    
    def _format_experience_for_prompt(self, experience: list) -> str:
        """Format experience data for prompt"""
        if not experience:
            return "No professional experience listed"
        
        formatted = []
        for exp in experience[:3]:  # Top 3 experiences
            title = exp.get('title', 'Position')
            company = exp.get('company', 'Company')
            description = exp.get('description', 'Professional experience')[:100]  # Limit length
            formatted.append(f"{title} at {company}: {description}")
        
        return '; '.join(formatted)
    
    def _format_projects_for_prompt(self, projects: list) -> str:
        """Format projects data for prompt"""
        if not projects:
            return "No projects listed"
        
        formatted = []
        for project in projects[:3]:  # Top 3 projects
            name = project.get('name', 'Project')
            desc = project.get('description', 'Project work')[:80]  # Limit length
            formatted.append(f"{name}: {desc}")
        
        return '; '.join(formatted)
    
    def _format_education_for_prompt(self, education: list) -> str:
        """Format education data for prompt"""
        if not education:
            return "Education information not specified"
        
        formatted = []
        for edu in education:
            degree = edu.get('degree', 'Degree')
            institution = edu.get('institution', 'Institution')
            formatted.append(f"{degree} from {institution}")
        
        return '; '.join(formatted)
    
    def _post_process_cover_letter(self, cover_letter: str, resume_data: Dict, job_data: Dict) -> str:
        """Post-process the generated cover letter"""
        # Basic cleaning
        cover_letter = cover_letter.strip()
        
        # Ensure proper name replacement
        name = resume_data.get('contact_info', {}).get('name')
        if name and '[Your Name]' in cover_letter:
            cover_letter = cover_letter.replace('[Your Name]', name)
        
        # Ensure proper company name
        company_name = job_data.get('company_info', {}).get('name')
        if company_name and '[Company Name]' in cover_letter:
            cover_letter = cover_letter.replace('[Company Name]', company_name)
        
        return cover_letter
    
    def _generate_improvement_suggestions(self, resume_data: Dict, job_data: Dict) -> list:
        """Generate suggestions for improving the application"""
        suggestions = []
        
        # Check skill alignment
        resume_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        required_skills = set(skill.lower() for skill in job_data.get('required_skills', []))
        
        missing_skills = required_skills - resume_skills
        if missing_skills:
            suggestions.append(f"Consider highlighting experience with: {', '.join(list(missing_skills)[:3])}")
        
        # Check experience relevance
        if not resume_data.get('experience'):
            suggestions.append("Consider adding more specific work experience examples")
        
        # Check education alignment
        if not resume_data.get('education'):
            suggestions.append("Ensure educational background is clearly stated")
        
        return suggestions