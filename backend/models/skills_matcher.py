import re
from typing import List, Dict, Tuple
import logging
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

class SkillsMatcher:
    """Match resume skills with job requirements"""
    
    def __init__(self):
        # Skill synonyms for better matching
        self.skill_synonyms = {
            'javascript': ['js', 'node.js', 'nodejs'],
            'python': ['py'],
            'machine learning': ['ml', 'artificial intelligence', 'ai'],
            'user interface': ['ui', 'frontend'],
            'user experience': ['ux'],
            'database': ['db', 'databases'],
            'sql': ['mysql', 'postgresql', 'sqlite'],
            'cloud computing': ['aws', 'azure', 'gcp', 'cloud'],
            'react': ['reactjs', 'react.js'],
            'angular': ['angularjs', 'angular.js'],
            'vue': ['vuejs', 'vue.js']
        }
    
    def calculate_match_score(self, resume_skills: List[str], job_requirements: List[str]) -> float:
        """
        Calculate overall match score between resume skills and job requirements
        
        Args:
            resume_skills: List of skills from resume
            job_requirements: List of required skills from job
            
        Returns:
            float: Match score between 0 and 1
        """
        if not job_requirements:
            return 0.0
        
        matched_skills = self.find_matching_skills(resume_skills, job_requirements)
        return len(matched_skills) / len(job_requirements)
    
    def find_matching_skills(self, resume_skills: List[str], job_requirements: List[str]) -> List[str]:
        """
        Find skills that match between resume and job requirements
        
        Args:
            resume_skills: List of skills from resume
            job_requirements: List of required skills from job
            
        Returns:
            List[str]: List of matching skills
        """
        matching_skills = []
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        
        for req_skill in job_requirements:
            req_skill_lower = req_skill.lower()
            
            # Direct match
            if req_skill_lower in resume_skills_lower:
                matching_skills.append(req_skill)
                continue
            
            # Synonym match
            if self._check_synonym_match(req_skill_lower, resume_skills_lower):
                matching_skills.append(req_skill)
                continue
            
            # Partial match (fuzzy matching)
            if self._check_fuzzy_match(req_skill_lower, resume_skills_lower):
                matching_skills.append(req_skill)
        
        return matching_skills
    
    def get_missing_skills(self, resume_skills: List[str], job_requirements: List[str]) -> List[str]:
        """
        Get skills that are required but missing from resume
        
        Args:
            resume_skills: List of skills from resume
            job_requirements: List of required skills from job
            
        Returns:
            List[str]: List of missing skills
        """
        matching_skills = self.find_matching_skills(resume_skills, job_requirements)
        return [skill for skill in job_requirements if skill not in matching_skills]
    
    def get_skill_analysis(self, resume_skills: List[str], job_requirements: List[str]) -> Dict:
        """
        Get comprehensive skill analysis
        
        Args:
            resume_skills: List of skills from resume
            job_requirements: List of required skills from job
            
        Returns:
            dict: Comprehensive skill analysis
        """
        matching_skills = self.find_matching_skills(resume_skills, job_requirements)
        missing_skills = self.get_missing_skills(resume_skills, job_requirements)
        match_score = self.calculate_match_score(resume_skills, job_requirements)
        
        # Categorize skills
        technical_skills = self._categorize_technical_skills(matching_skills)
        soft_skills = self._categorize_soft_skills(matching_skills)
        
        return {
            'match_score': round(match_score * 100, 1),  # Convert to percentage
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'total_required': len(job_requirements),
            'total_matched': len(matching_skills),
            'technical_skills': technical_skills,
            'soft_skills': soft_skills,
            'recommendations': self._generate_recommendations(missing_skills, match_score)
        }
    
    def _check_synonym_match(self, req_skill: str, resume_skills: List[str]) -> bool:
        """Check if skill matches through synonyms"""
        # Check if req_skill has synonyms
        for main_skill, synonyms in self.skill_synonyms.items():
            if req_skill == main_skill or req_skill in synonyms:
                # Check if any synonym is in resume skills
                if main_skill in resume_skills:
                    return True
                if any(synonym in resume_skills for synonym in synonyms):
                    return True
        
        return False
    
    def _check_fuzzy_match(self, req_skill: str, resume_skills: List[str], threshold: float = 0.8) -> bool:
        """Check for fuzzy/partial matches"""
        for resume_skill in resume_skills:
            # Use sequence matcher for similarity
            similarity = SequenceMatcher(None, req_skill, resume_skill).ratio()
            if similarity >= threshold:
                return True
            
            # Check if one skill contains the other
            if req_skill in resume_skill or resume_skill in req_skill:
                return True
        
        return False
    
    def _categorize_technical_skills(self, skills: List[str]) -> List[str]:
        """Categorize technical skills"""
        technical_keywords = [
            'programming', 'language', 'framework', 'library', 'database', 'cloud',
            'devops', 'api', 'web', 'mobile', 'software', 'system', 'network',
            'security', 'testing', 'deployment', 'version control'
        ]
        
        technical_skills = []
        for skill in skills:
            skill_lower = skill.lower()
            if any(keyword in skill_lower for keyword in technical_keywords):
                technical_skills.append(skill)
            # Add common technical skills
            elif any(tech in skill_lower for tech in ['python', 'java', 'javascript', 'react', 'sql', 'aws', 'docker']):
                technical_skills.append(skill)
        
        return technical_skills
    
    def _categorize_soft_skills(self, skills: List[str]) -> List[str]:
        """Categorize soft skills"""
        soft_keywords = [
            'communication', 'leadership', 'teamwork', 'problem solving',
            'analytical', 'creative', 'management', 'organization', 'time management',
            'adaptability', 'collaboration', 'presentation', 'negotiation'
        ]
        
        soft_skills = []
        for skill in skills:
            skill_lower = skill.lower()
            if any(keyword in skill_lower for keyword in soft_keywords):
                soft_skills.append(skill)
        
        return soft_skills
    
    def _generate_recommendations(self, missing_skills: List[str], match_score: float) -> List[str]:
        """Generate recommendations based on skill analysis"""
        recommendations = []
        
        if match_score < 0.3:
            recommendations.append("Consider gaining more of the required skills before applying")
        elif match_score < 0.6:
            recommendations.append("You have some matching skills. Consider highlighting transferable experience")
        else:
            recommendations.append("Strong skill match! Emphasize your relevant experience")
        
        if missing_skills:
            top_missing = missing_skills[:3]  # Top 3 missing skills
            recommendations.append(f"Consider learning: {', '.join(top_missing)}")
        
        if match_score > 0.8:
            recommendations.append("Excellent match! You're well-qualified for this position")
        
        return recommendations

    def get_skill_priority_ranking(self, job_requirements: List[str], job_text: str) -> List[Tuple[str, int]]:
        """
        Rank skills by their priority/importance in the job description
        
        Args:
            job_requirements: List of required skills
            job_text: Full job description text
            
        Returns:
            List[Tuple[str, int]]: List of (skill, priority_score) tuples
        """
        skill_priorities = []
        job_text_lower = job_text.lower()
        
        for skill in job_requirements:
            skill_lower = skill.lower()
            priority_score = 0
            
            # Count mentions
            mentions = job_text_lower.count(skill_lower)
            priority_score += mentions * 10
            
            # Check if in title or early in description
            if skill_lower in job_text[:200].lower():
                priority_score += 20
            
            # Check if marked as required/essential
            required_context = re.findall(rf'(?:required|essential|must have|critical).*?{re.escape(skill_lower)}', job_text_lower)
            if required_context:
                priority_score += 30
            
            skill_priorities.append((skill, priority_score))
        
        # Sort by priority score (descending)
        return sorted(skill_priorities, key=lambda x: x[1], reverse=True)