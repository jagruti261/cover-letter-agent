import os
import logging
import requests
from typing import Dict, Optional
from dotenv import load_dotenv 
import google.generativeai as genai

logger = logging.getLogger(__name__)
load_dotenv()

class CoverLetterGenerator:
    """Generate personalized cover letters using Kimi K2, fallback to Gemini AI, then internal template"""

    def __init__(self):
        # Gemini config
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('models/gemini-2.5-pro')

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
        """Generate cover letter with Kimi K2 → Gemini AI → internal fallback"""
        template_func = self.templates.get(template_style, self.templates['professional'])
        prompt = template_func(resume_data, job_data, custom_message)

         # Fallback: Gemini AI
        if self.gemini_api_key:
            try:
                response = self.gemini_model.generate_content(prompt)
                cover_letter_text = response.text
                cover_letter_text = self._post_process_cover_letter(cover_letter_text, resume_data, job_data)
                return self._build_response(cover_letter_text, template_style, resume_data, job_data)
            except Exception as e:
                logger.warning(f"Gemini AI failed: {e}")

        # Last-resort: Internal fallback cover letter
        logger.info("Falling back to internal cover letter generator.")
        cover_letter_text = self._internal_fallback_cover_letter(resume_data, job_data, custom_message)
        return self._build_response(cover_letter_text, template_style, resume_data, job_data)

    def _internal_fallback_cover_letter(self, resume_data: Dict, job_data: Dict, custom_message: str = None) -> str:
        """Generate a polished, professional fallback cover letter"""
        name = resume_data.get('contact_info', {}).get('name', 'Applicant')
        job_title = job_data.get('job_title', 'the position')
        company_name = job_data.get('company_info', {}).get('name', 'your company')

        skills = ', '.join(resume_data.get('skills', [])[:5])
        experience = self._format_experience_for_prompt(resume_data.get('experience', []))
        summary = resume_data.get('summary', 'a motivated and results-driven professional')

        cover_letter = (
            f"Dear Hiring Manager at {company_name},\n\n"
            f"I am writing to express my interest in the {job_title} position at {company_name}. "
            f"With a background in {experience} and skills including {skills}, "
            f"I am confident in my ability to make a meaningful contribution to your team.\n\n"
            f"{summary}. "
            f"I am passionate about driving results and collaborating with talented professionals, "
            f"and I am eager to bring my expertise and enthusiasm to {company_name}.\n\n"
            f"I would welcome the opportunity to discuss how my experience and skills align with your needs "
            f"and how I can contribute to the continued success of your team.\n\n"
            f"Thank you for considering my application.\n\n"
            f"Sincerely,\n{name}"
        )

        if custom_message:
            cover_letter += f"\n\nP.S.: {custom_message}"

        return cover_letter

    def _build_response(self, cover_letter_text, template_style, resume_data, job_data):
        """Helper to standardize the response"""
        return {
            'success': True,
            'cover_letter': cover_letter_text,
            'template_used': template_style,
            'word_count': len(cover_letter_text.split()),
            'recommendations': self._generate_improvement_suggestions(resume_data, job_data)
        }

    # ------------------ Templates ------------------ #
    def _professional_template(self, resume_data: Dict, job_data: Dict, custom_message: str = None) -> str:
        """Professional cover letter template"""
        name = resume_data.get('contact_info', {}).get('name', 'Applicant')
        job_title = job_data.get('job_title', 'the position')
        company_name = job_data.get('company_info', {}).get('name', 'your company')
        skills = resume_data.get('skills', [])[:8]
        experience = resume_data.get('experience', [])
        required_skills = job_data.get('required_skills', [])
        responsibilities = job_data.get('responsibilities', [])[:5]

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

    # ------------------ Helper Formatters ------------------ #
    def _format_experience_for_prompt(self, experience: list) -> str:
        if not experience:
            return "No professional experience listed"
        formatted = []
        for exp in experience[:3]:
            title = exp.get('title', 'Position')
            company = exp.get('company', 'Company')
            description = exp.get('description', 'Professional experience')[:100]
            formatted.append(f"{title} at {company}: {description}")
        return '; '.join(formatted)

    def _format_projects_for_prompt(self, projects: list) -> str:
        if not projects:
            return "No projects listed"
        formatted = []
        for project in projects[:3]:
            name = project.get('name', 'Project')
            desc = project.get('description', 'Project work')[:80]
            formatted.append(f"{name}: {desc}")
        return '; '.join(formatted)

    def _format_education_for_prompt(self, education: list) -> str:
        if not education:
            return "Education information not specified"
        formatted = []
        for edu in education:
            degree = edu.get('degree', 'Degree')
            institution = edu.get('institution', 'Institution')
            formatted.append(f"{degree} from {institution}")
        return '; '.join(formatted)

    # ------------------ Post-processing ------------------ #
    def _post_process_cover_letter(self, cover_letter: str, resume_data: Dict, job_data: Dict) -> str:
        cover_letter = cover_letter.strip()
        name = resume_data.get('contact_info', {}).get('name')
        if name and '[Your Name]' in cover_letter:
            cover_letter = cover_letter.replace('[Your Name]', name)
        company_name = job_data.get('company_info', {}).get('name')
        if company_name and '[Company Name]' in cover_letter:
            cover_letter = cover_letter.replace('[Company Name]', company_name)
        return cover_letter

    def _generate_improvement_suggestions(self, resume_data: Dict, job_data: Dict) -> list:
        suggestions = []
        resume_skills = set(skill.lower() for skill in resume_data.get('skills', []))
        required_skills = set(skill.lower() for skill in job_data.get('required_skills', []))
        missing_skills = required_skills - resume_skills
        if missing_skills:
            suggestions.append(f"Consider highlighting experience with: {', '.join(list(missing_skills)[:3])}")
        if not resume_data.get('experience'):
            suggestions.append("Consider adding more specific work experience examples")
        if not resume_data.get('education'):
            suggestions.append("Ensure educational background is clearly stated")
        return suggestions
