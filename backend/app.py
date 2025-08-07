from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
import tempfile
import shutil
from datetime import datetime
import json
import hashlib
import traceback

# Import our custom modules
from config import Config
from utils.text_extractor import TextExtractor
from utils.validators import InputValidator
from models.resume_parser import ResumeParser
from models.job_analyzer import JobAnalyzer
from models.cover_letter_generator import CoverLetterGenerator
from models.skills_matcher import SkillsMatcher

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
CORS(app, origins=Config.ALLOWED_ORIGINS)

# Initialize components
try:
    text_extractor = TextExtractor()
    resume_parser = ResumeParser()
    job_analyzer = JobAnalyzer()
    cover_letter_generator = CoverLetterGenerator()
    skills_matcher = SkillsMatcher()
    input_validator = InputValidator()
    logger.info("All components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize components: {str(e)}")
    raise

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def generate_file_hash(file_content):
    """Generate hash for file content to avoid reprocessing"""
    return hashlib.md5(file_content.encode()).hexdigest()

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413

@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(e)}")
    logger.error(traceback.format_exc())
    return jsonify({
        'success': False,
        'error': 'An internal server error occurred. Please try again.'
    }), 500

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'AI Cover Letter Generator API is running',
        'version': '1.0.0',
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def api_health():
    """API health check"""
    return jsonify({
        'success': True,
        'api_status': 'operational',
        'components': {
            'text_extractor': 'ready',
            'resume_parser': 'ready',
            'job_analyzer': 'ready',
            'cover_letter_generator': 'ready',
            'skills_matcher': 'ready'
        }
    })

@app.route('/api/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Main endpoint to generate cover letter"""
    try:
        logger.info("Received cover letter generation request")
        
        # Validate request
        if 'resume' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No resume file provided'
            }), 400
        
        if 'job_description' not in request.form:
            return jsonify({
                'success': False,
                'error': 'No job description provided'
            }), 400
        
        resume_file = request.files['resume']
        job_description = request.form['job_description']
        template_style = request.form.get('template_style', 'professional')
        custom_message = request.form.get('custom_message', '')
        
        # Validate inputs
        if resume_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No resume file selected'
            }), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Supported formats: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        if not input_validator.validate_job_description(job_description):
            return jsonify({
                'success': False,
                'error': 'Job description is too short or invalid. Please provide a detailed job description.'
            }), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(resume_file.filename)
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, filename)
        resume_file.save(file_path)
        
        try:
            # Extract text from resume
            logger.info(f"Extracting text from resume: {filename}")
            resume_text = text_extractor.extract_text(file_path)
            
            if not resume_text:
                return jsonify({
                    'success': False,
                    'error': 'Could not extract text from resume. Please ensure the file is not corrupted.'
                }), 400
            
            # Validate resume content
            if not input_validator.validate_resume_text(resume_text):
                return jsonify({
                    'success': False,
                    'error': 'Resume content appears to be insufficient. Please upload a more detailed resume.'
                }), 400
            
            # Parse resume and analyze job description
            logger.info("Parsing resume and analyzing job description")
            resume_data = resume_parser.parse_resume(resume_text)
            job_data = job_analyzer.analyze_job_description(job_description)
            
            # Perform skills matching analysis
            logger.info("Performing skills matching analysis")
            skills_analysis = skills_matcher.get_skill_analysis(
                resume_data.get('skills', []),
                job_data.get('required_skills', [])
            )
            
            # Generate cover letter
            logger.info(f"Generating cover letter with template: {template_style}")
            cover_letter_result = cover_letter_generator.generate_cover_letter(
                resume_data=resume_data,
                job_data=job_data,
                template_style=template_style,
                custom_message=custom_message if custom_message else None
            )
            
            if not cover_letter_result.get('success'):
                return jsonify({
                    'success': False,
                    'error': cover_letter_result.get('error', 'Failed to generate cover letter')
                }), 500
            
            # Prepare response
            response_data = {
                'success': True,
                'cover_letter': cover_letter_result['cover_letter'],
                'analysis': {
                    'resume_data': {
                        'contact_info': resume_data.get('contact_info', {}),
                        'skills_count': len(resume_data.get('skills', [])),
                        'experience_count': len(resume_data.get('experience', [])),
                        'education_count': len(resume_data.get('education', [])),
                        'summary': resume_data.get('summary', '')[:200] + '...' if len(resume_data.get('summary', '')) > 200 else resume_data.get('summary', '')
                    },
                    'job_data': {
                        'job_title': job_data.get('job_title', ''),
                        'company_name': job_data.get('company_info', {}).get('name', ''),
                        'required_skills_count': len(job_data.get('required_skills', [])),
                        'job_type': job_data.get('job_type', ''),
                        'experience_level': job_data.get('experience_level', '')
                    },
                    'skills_matching': skills_analysis
                },
                'metadata': {
                    'template_used': cover_letter_result.get('template_used', template_style),
                    'word_count': cover_letter_result.get('word_count', 0),
                    'generation_timestamp': datetime.now().isoformat(),
                    'recommendations': cover_letter_result.get('recommendations', [])
                }
            }
            
            logger.info("Cover letter generated successfully")
            return jsonify(response_data)
            
        finally:
            # Clean up temporary files
            try:
                shutil.rmtree(temp_dir)
            except Exception as cleanup_error:
                logger.warning(f"Failed to clean up temp directory: {cleanup_error}")
    
    except Exception as e:
        logger.error(f"Error in generate_cover_letter: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request. Please try again.'
        }), 500

@app.route('/api/analyze-skills', methods=['POST'])
def analyze_skills():
    """Endpoint to analyze skill matching without generating cover letter"""
    try:
        data = request.get_json()
        
        if not data or 'resume_skills' not in data or 'job_requirements' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: resume_skills and job_requirements'
            }), 400
        
        resume_skills = data['resume_skills']
        job_requirements = data['job_requirements']
        
        # Perform skills analysis
        skills_analysis = skills_matcher.get_skill_analysis(resume_skills, job_requirements)
        
        return jsonify({
            'success': True,
            'skills_analysis': skills_analysis
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_skills: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to analyze skills'
        }), 500

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """Endpoint to parse resume only"""
    try:
        if 'resume' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No resume file provided'
            }), 400
        
        resume_file = request.files['resume']
        
        if resume_file.filename == '' or not allowed_file(resume_file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file'
            }), 400
        
        # Save and process file
        filename = secure_filename(resume_file.filename)
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, filename)
        resume_file.save(file_path)
        
        try:
            # Extract and parse resume
            resume_text = text_extractor.extract_text(file_path)
            resume_data = resume_parser.parse_resume(resume_text)
            
            return jsonify({
                'success': True,
                'resume_data': resume_data
            })
            
        finally:
            shutil.rmtree(temp_dir)
            
    except Exception as e:
        logger.error(f"Error in parse_resume: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to parse resume'
        }), 500

@app.route('/api/analyze-job', methods=['POST'])
def analyze_job():
    """Endpoint to analyze job description only"""
    try:
        data = request.get_json()
        
        if not data or 'job_description' not in data:
            return jsonify({
                'success': False,
                'error': 'No job description provided'
            }), 400
        
        job_description = data['job_description']
        
        if not input_validator.validate_job_description(job_description):
            return jsonify({
                'success': False,
                'error': 'Job description is too short or invalid'
            }), 400
        
        # Analyze job description
        job_data = job_analyzer.analyze_job_description(job_description)
        
        return jsonify({
            'success': True,
            'job_data': job_data
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_job: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to analyze job description'
        }), 500

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available cover letter templates"""
    templates = {
        'professional': {
            'name': 'Professional',
            'description': 'Traditional, formal cover letter suitable for corporate environments',
            'best_for': 'Corporate positions, traditional industries, formal applications'
        },
        'creative': {
            'name': 'Creative',
            'description': 'Engaging and creative tone while maintaining professionalism',
            'best_for': 'Creative industries, startups, marketing roles'
        },
        'technical': {
            'name': 'Technical',
            'description': 'Focuses on technical skills and achievements',
            'best_for': 'Software development, engineering, technical roles'
        },
        'entry_level': {
            'name': 'Entry Level',
            'description': 'Emphasizes potential, education, and eagerness to learn',
            'best_for': 'Recent graduates, career changers, first-time job seekers'
        }
    }
    
    return jsonify({
        'success': True,
        'templates': templates
    })

if __name__ == '__main__':
    # Validate configuration before starting
    try:
        Config.validate()
        logger.info("Configuration validated successfully")
        
        # Start the application
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise