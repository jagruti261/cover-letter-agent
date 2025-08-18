# Cover Letter Agent

<div align="center">
  <h3>🚀 Generate tailored, professional cover letters that help you stand out to employers</h3>
  <p>Built for job seekers who want to make a great first impression</p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
  [![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![GitHub issues](https://img.shields.io/github/issues/jagruti261/cover-letter-agent)](https://github.com/jagruti261/cover-letter-agent/issues)
  [![GitHub stars](https://img.shields.io/github/stars/jagruti261/cover-letter-agent)](https://github.com/jagruti261/cover-letter-agent/stargazers)
</div>

## ✨ Features

- 🤖 **AI-Powered Generation** - Leverages advanced language models for personalized content
- 📄 **Smart Resume Analysis** - Automatically extracts skills and experience from uploaded resumes
- 🎯 **Job Matching** - Intelligently aligns your qualifications with job requirements
- 📝 **Professional Templates** - Clean, ATS-friendly cover letter formats
- ✅ **Skills Validation** - Ensures skill-job requirement alignment
- 🌐 **Modern Web Interface** - Intuitive React-based user experience

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask/FastAPI
- OpenAI API / LangChain
- PyPDF2 / python-docx
- pandas

**Frontend:**
- React 18+
- Tailwind CSS
- Axios
- Modern ES6+

## 📦 Installation

### Prerequisites

Make sure you have the following installed:
- Python 3.8+
- Node.js 14+
- npm or yarn

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/jagruti261/cover-letter-agent.git
   cd cover-letter-agent
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   cd backend
   pip install -r requirements.txt
   
   # Configure environment
   cp config.py.example config.py
   # Edit config.py with your API keys
   
   # Start backend server
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   # In a new terminal
   cd frontend
   
   # Install dependencies
   npm install
   
   # Configure environment
   echo "REACT_APP_API_URL=http://localhost:5000" > .env.local
   
   # Start development server
   npm start
   ```

4. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:5000`

## ⚙️ Configuration

### Environment Variables

**Backend** (create `.env` in `/backend`):
```env
GEMINI_API_KEY=your_openai_api_key_here
DEBUG=True
PORT=5000
```

**Frontend** (create `.env.local` in `/frontend`):
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENVIRONMENT=development
```

## 🎯 Usage

1. **Upload Resume** 📤  
   Upload your resume in PDF or DOCX format

2. **Add Job Description** 📋  
   Paste the job description you're applying for

3. **Review & Match** 🔍  
   Review extracted skills and job requirements

4. **Generate Cover Letter** ✨  
   AI generates a tailored cover letter

5. **Download & Apply** 📄  
   Download your professional cover letter

## 📋 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload-resume` | Upload and parse resume file |
| `POST` | `/api/analyze-job` | Analyze job description |
| `POST` | `/api/generate-cover-letter` | Generate personalized cover letter |
| `GET` | `/api/skills` | Retrieve extracted skills |
| `POST` | `/api/validate-skills` | Validate skill matches |

### Example Request

```javascript
// Generate cover letter
const response = await fetch('/api/generate-cover-letter', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    resume_data: resumeData,
    job_description: jobDescription,
    user_preferences: preferences
  })
});
```

## 🏗️ Project Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Models     │
│   (React)       │◄──►│   (Python)      │◄──►│   (OpenAI)      │
│                 │    │                 │    │                 │
│ • File Upload   │    │ • Resume Parser │    │ • GPT Models    │
│ • Job Input     │    │ • Job Analyzer  │    │ • Text Gen      │
│ • UI/UX         │    │ • Skills Match  │    │ • Analysis      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```


## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add: amazing new feature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write tests for new features
- Update documentation as needed

## 🔗 Links

- **Live Demo**: [Cover Letter Agent](https://cover-letter-agent-frontend.onrender.com/)
- **Issues**: [GitHub Issues](https://github.com/jagruti261/cover-letter-agent/issues)

## 🆘 Support

Having trouble? Here are some resources:

- 🐛 [Report a Bug](https://github.com/jagruti261/cover-letter-agent/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/jagruti261/cover-letter-agent/issues/new?template=feature_request.md)
- 💬 [Discussions](https://github.com/jagruti261/cover-letter-agent/discussions)

## 🎖️ Acknowledgments

- [OpenAI](https://openai.com) for providing powerful language models
- [React](https://reactjs.org) team for the amazing frontend framework
- [Tailwind CSS](https://tailwindcss.com) for beautiful, utility-first styling

## 🔮 Roadmap

- [ ] Multiple cover letter templates
- [ ] Integration with job boards (LinkedIn, Indeed)
- [ ] A/B testing for effectiveness tracking
- [ ] Multi-language support
- [ ] Advanced customization options
- [ ] Mobile application
- [ ] Chrome extension for quick generation

---

<div align="center">
  <p><strong>⭐ If this project helped you land your dream job, please star the repository! ⭐</strong></p>
  <p>Made with ❤️ by <a href="https://github.com/jagruti261">Jagruti</a></p>
</div>
