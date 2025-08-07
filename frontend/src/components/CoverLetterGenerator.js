import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const CoverLetterGenerator = () => {
    const [resumeFile, setResumeFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');
    const [templateStyle, setTemplateStyle] = useState('professional');
    const [customMessage, setCustomMessage] = useState('');
    const [coverLetter, setCoverLetter] = useState('');
    const [analysis, setAnalysis] = useState(null);
    const [metadata, setMetadata] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [templates, setTemplates] = useState({});
    const [activeTab, setActiveTab] = useState('generate');

    // Get API URL from environment
    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5051';

    // Load templates on component mount
    React.useEffect(() => {
        loadTemplates();
    }, []);

    const loadTemplates = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/templates`);
            if (response.data.success) {
                setTemplates(response.data.templates);
            }
        } catch (error) {
            console.error('Failed to load templates:', error);
        }
    };

    // File dropzone configuration
    const onDrop = useCallback((acceptedFiles) => {
        const file = acceptedFiles[0];
        if (file) {
            // Validate file size (16MB)
            const maxSize = parseInt(process.env.REACT_APP_MAX_FILE_SIZE) || 16777216;
            if (file.size > maxSize) {
                setError('File size too large. Maximum size is 16MB.');
                return;
            }
            setResumeFile(file);
            setError('');
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
            'application/msword': ['.doc'],
            'text/plain': ['.txt']
        },
        multiple: false
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!resumeFile) {
            setError('Please upload a resume file.');
            return;
        }
        
        if (!jobDescription.trim()) {
            setError('Please provide a job description.');
            return;
        }

        setLoading(true);
        setError('');
        
        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('job_description', jobDescription);
        formData.append('template_style', templateStyle);
        if (customMessage.trim()) {
            formData.append('custom_message', customMessage);
        }
      
        try {
            const response = await axios.post(
                `${API_URL}/api/generate-cover-letter`,
                formData,
                { 
                    headers: { 
                        'Content-Type': 'multipart/form-data' 
                    },
                    timeout: 60000 // 60 second timeout
                }
            );
            
            if (response.data.success) {
                setCoverLetter(response.data.cover_letter);
                setAnalysis(response.data.analysis);
                setMetadata(response.data.metadata);
                setActiveTab('result');
            } else {
                setError(response.data.error || 'Failed to generate cover letter');
            }
        } catch (error) {
            console.error('Error:', error);
            if (error.response?.data?.error) {
                setError(error.response.data.error);
            } else if (error.code === 'ECONNABORTED') {
                setError('Request timed out. Please try again.');
            } else {
                setError('An error occurred. Please check your connection and try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = async () => {
        try {
            await navigator.clipboard.writeText(coverLetter);
            alert('Cover letter copied to clipboard!');
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    };

    const downloadCoverLetter = () => {
        const element = document.createElement('a');
        const file = new Blob([coverLetter], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = 'cover-letter.txt';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    const resetForm = () => {
        setResumeFile(null);
        setJobDescription('');
        setCustomMessage('');
        setCoverLetter('');
        setAnalysis(null);
        setMetadata(null);
        setError('');
        setActiveTab('generate');
    };

    return (
        <div className="w-full">
            {/* Tabs Navigation */}
            <div className="mb-6">
                <nav className="flex space-x-8 border-b border-[#30363d]">
                    <button
                        onClick={() => setActiveTab('generate')}
                        className={`py-3 px-1 border-b-2 text-sm font-medium transition-colors duration-200 ${
                            activeTab === 'generate'
                                ? 'border-[#7c3aed] text-[#f0f6fc]'
                                : 'border-transparent text-[#7d8590] hover:text-[#f0f6fc] hover:border-[#8b949e]'
                        }`}
                    >
                        Generate Cover Letter
                    </button>
                    {coverLetter && (
                        <button
                            onClick={() => setActiveTab('result')}
                            className={`py-3 px-1 border-b-2 text-sm font-medium transition-colors duration-200 ${
                                activeTab === 'result'
                                    ? 'border-[#7c3aed] text-[#f0f6fc]'
                                    : 'border-transparent text-[#7d8590] hover:text-[#f0f6fc] hover:border-[#8b949e]'
                            }`}
                        >
                            View Result
                        </button>
                    )}
                    {analysis && (
                        <button
                            onClick={() => setActiveTab('analysis')}
                            className={`py-3 px-1 border-b-2 text-sm font-medium transition-colors duration-200 ${
                                activeTab === 'analysis'
                                    ? 'border-[#7c3aed] text-[#f0f6fc]'
                                    : 'border-transparent text-[#7d8590] hover:text-[#f0f6fc] hover:border-[#8b949e]'
                            }`}
                        >
                            Skills Analysis
                        </button>
                    )}
                </nav>
            </div>

            {/* Error Alert */}
            {error && (
                <div className="mb-6 border border-[#d1242f] bg-[#0d1117] rounded-md p-4">
                    <div className="flex items-start">
                        <svg className="h-5 w-5 text-[#f85149] mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        <p className="text-sm text-[#f85149]">{error}</p>
                    </div>
                </div>
            )}

            {/* Generate Tab */}
            {activeTab === 'generate' && (
                <div className="space-y-6">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Resume Upload Section */}
                        <div>
                            <label className="block text-sm font-medium text-[#f0f6fc] mb-3">
                                Upload Resume
                            </label>
                            <div
                                {...getRootProps()}
                                className={`border-2 border-dashed rounded-md p-8 text-center cursor-pointer transition-all duration-200 ${
                                    isDragActive
                                        ? 'border-[#7c3aed] bg-[#7c3aed]/10'
                                        : resumeFile
                                        ? 'border-[#238636] bg-[#238636]/10'
                                        : 'border-[#30363d] hover:border-[#8b949e] bg-[#0d1117]'
                                }`}
                            >
                                <input {...getInputProps()} />
                                <div className="space-y-3">
                                    <svg className="mx-auto h-12 w-12 text-[#7d8590]" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                                        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                    {resumeFile ? (
                                        <div>
                                            <p className="text-sm text-[#238636] font-medium flex items-center justify-center">
                                                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                                </svg>
                                                {resumeFile.name}
                                            </p>
                                            <p className="text-xs text-[#7d8590]">
                                                {(resumeFile.size / 1024 / 1024).toFixed(2)} MB
                                            </p>
                                        </div>
                                    ) : isDragActive ? (
                                        <p className="text-sm text-[#7c3aed] font-medium">Drop the file here...</p>
                                    ) : (
                                        <div>
                                            <p className="text-sm text-[#f0f6fc]">
                                                <span className="font-medium text-[#58a6ff]">Click to upload</span> or drag and drop
                                            </p>
                                            <p className="text-xs text-[#7d8590] mt-1">
                                                PDF, DOCX, DOC, or TXT (max 16MB)
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Job Description */}
                        <div>
                            <label className="block text-sm font-medium text-[#f0f6fc] mb-3">
                                Job Description
                            </label>
                            <textarea
                                value={jobDescription}
                                onChange={(e) => setJobDescription(e.target.value)}
                                rows={12}
                                className="w-full bg-[#0d1117] border border-[#30363d] rounded-md p-3 text-[#f0f6fc] placeholder-[#7d8590] focus:border-[#58a6ff] focus:ring-1 focus:ring-[#58a6ff] focus:outline-none resize-none"
                                placeholder="Paste the complete job description here including requirements, responsibilities, and company information..."
                                required
                            />
                            <div className="mt-2 text-xs text-[#7d8590]">
                                {jobDescription.length} characters (minimum 50 recommended)
                            </div>
                        </div>

                        {/* Template Selection */}
                        <div>
                            <label className="block text-sm font-medium text-[#f0f6fc] mb-3">
                                Cover Letter Style
                            </label>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {Object.entries(templates).map(([key, template]) => (
                                    <div
                                        key={key}
                                        className={`border rounded-md p-4 cursor-pointer transition-all duration-200 ${
                                            templateStyle === key
                                                ? 'border-[#7c3aed] bg-[#7c3aed]/10'
                                                : 'border-[#30363d] hover:border-[#8b949e] bg-[#0d1117]'
                                        }`}
                                        onClick={() => setTemplateStyle(key)}
                                    >
                                        <div className="flex items-center mb-3">
                                            <div className={`w-4 h-4 rounded-full border-2 mr-3 flex items-center justify-center ${
                                                templateStyle === key 
                                                    ? 'border-[#7c3aed] bg-[#7c3aed]' 
                                                    : 'border-[#7d8590]'
                                            }`}>
                                                {templateStyle === key && (
                                                    <div className="w-2 h-2 bg-white rounded-full"></div>
                                                )}
                                            </div>
                                            <label className="text-sm font-medium text-[#f0f6fc] cursor-pointer">
                                                {template.name}
                                            </label>
                                        </div>
                                        <p className="text-xs text-[#7d8590] mb-2">{template.description}</p>
                                        <p className="text-xs text-[#58a6ff] font-medium">
                                            Best for: {template.best_for}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Custom Message */}
                        <div>
                            <label className="block text-sm font-medium text-[#f0f6fc] mb-3">
                                Custom Message (Optional)
                            </label>
                            <textarea
                                value={customMessage}
                                onChange={(e) => setCustomMessage(e.target.value)}
                                rows={3}
                                className="w-full bg-[#0d1117] border border-[#30363d] rounded-md p-3 text-[#f0f6fc] placeholder-[#7d8590] focus:border-[#58a6ff] focus:ring-1 focus:ring-[#58a6ff] focus:outline-none"
                                placeholder="Add any specific points you'd like to include in your cover letter..."
                            />
                        </div>

                        {/* Action Buttons */}
                        <div className="flex justify-between items-center pt-4">
                            <button
                                type="button"
                                onClick={resetForm}
                                className="px-4 py-2 text-sm font-medium text-[#f0f6fc] bg-[#21262d] border border-[#30363d] rounded-md hover:bg-[#30363d] hover:border-[#8b949e] focus:outline-none focus:ring-2 focus:ring-[#58a6ff] focus:ring-offset-2 focus:ring-offset-[#0d1117] transition-all duration-200"
                            >
                                Reset Form
                            </button>
                            <button
                                type="submit"
                                disabled={loading || !resumeFile || !jobDescription.trim()}
                                className="px-6 py-2 bg-[#238636] hover:bg-[#2ea043] disabled:bg-[#21262d] disabled:text-[#7d8590] disabled:border-[#30363d] text-white text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-[#2ea043] focus:ring-offset-2 focus:ring-offset-[#0d1117] disabled:cursor-not-allowed flex items-center transition-all duration-200"
                            >
                                {loading ? (
                                    <>
                                        <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Generating...
                                    </>
                                ) : (
                                    'Generate Cover Letter'
                                )}
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {/* Results Tab */}
            {activeTab === 'result' && coverLetter && (
                <div className="space-y-6">
                    {/* Header with Actions */}
                    <div className="flex justify-between items-center">
                        <h2 className="text-xl font-semibold text-[#f0f6fc]">Generated Cover Letter</h2>
                        <div className="flex space-x-3">
                            <button
                                onClick={copyToClipboard}
                                className="px-3 py-2 bg-[#238636] hover:bg-[#2ea043] text-white text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-[#2ea043] focus:ring-offset-2 focus:ring-offset-[#0d1117] transition-all duration-200 flex items-center"
                            >
                                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                                Copy
                            </button>
                            <button
                                onClick={downloadCoverLetter}
                                className="px-3 py-2 border border-[#30363d] hover:border-[#8b949e] hover:bg-[#21262d] text-[#f0f6fc] text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-[#58a6ff] focus:ring-offset-2 focus:ring-offset-[#0d1117] transition-all duration-200 flex items-center"
                            >
                                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                Download
                            </button>
                        </div>
                    </div>

                    {/* Metadata */}
                    {metadata && (
                        <div className="border border-[#30363d] rounded-md p-4 bg-[#0d1117]">
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                <div className="flex justify-between">
                                    <span className="text-[#7d8590]">Template:</span>
                                    <span className="text-[#f0f6fc] capitalize font-medium">{metadata.template_used}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-[#7d8590]">Word Count:</span>
                                    <span className="text-[#f0f6fc] font-medium">{metadata.word_count}</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-[#7d8590]">Generated:</span>
                                    <span className="text-[#f0f6fc] font-medium">
                                        {new Date(metadata.generation_timestamp).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Cover Letter Content */}
                    <div className="border border-[#30363d] rounded-md p-6 bg-[#161b22]">
                        <pre className="whitespace-pre-wrap text-[#f0f6fc] leading-relaxed font-mono text-sm">
                            {coverLetter}
                        </pre>
                    </div>

                    {/* Recommendations */}
                    {metadata?.recommendations && metadata.recommendations.length > 0 && (
                        <div className="border border-[#1f6feb] bg-[#0d1117] rounded-md p-4">
                            <h3 className="text-sm font-medium text-[#58a6ff] mb-3 flex items-center">
                                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                                </svg>
                                Recommendations for Improvement
                            </h3>
                            <ul className="space-y-2">
                                {metadata.recommendations.map((rec, index) => (
                                    <li key={index} className="flex items-start text-sm text-[#7d8590]">
                                        <span className="text-[#58a6ff] mr-2 mt-0.5">•</span>
                                        <span>{rec}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}

            {/* Analysis Tab */}
            {activeTab === 'analysis' && analysis && (
                <div className="space-y-8">
                    <h2 className="text-xl font-semibold text-[#f0f6fc]">Skills Analysis & Job Match</h2>

                    {/* Match Score */}
                    <div className="border border-[#30363d] rounded-md p-6 bg-[#161b22]">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-lg font-medium text-[#f0f6fc]">Overall Match Score</h3>
                            <span className={`text-2xl font-bold ${
                                analysis.skills_matching.match_score >= 70 ? 'text-[#238636]' :
                                analysis.skills_matching.match_score >= 50 ? 'text-[#d29922]' : 'text-[#da3633]'
                            }`}>
                                {analysis.skills_matching.match_score}%
                            </span>
                        </div>
                        <div className="w-full bg-[#21262d] rounded-full h-2 mb-3">
                            <div
                                className={`h-2 rounded-full transition-all duration-300 ${
                                    analysis.skills_matching.match_score >= 70 ? 'bg-[#238636]' :
                                    analysis.skills_matching.match_score >= 50 ? 'bg-[#d29922]' : 'bg-[#da3633]'
                                }`}
                                style={{ width: `${analysis.skills_matching.match_score}%` }}
                            ></div>
                        </div>
                        <p className="text-sm text-[#7d8590]">
                            {analysis.skills_matching.total_matched} of {analysis.skills_matching.total_required} required skills matched
                        </p>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Matching Skills */}
                        <div className="border border-[#30363d] rounded-md p-6 bg-[#161b22]">
                            <h3 className="text-lg font-medium text-[#f0f6fc] mb-4 flex items-center">
                                <svg className="w-5 h-5 text-[#238636] mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                </svg>
                                Matching Skills ({analysis.skills_matching.matching_skills.length})
                            </h3>
                            <div className="space-y-2 max-h-60 overflow-y-auto">
                                {analysis.skills_matching.matching_skills.map((skill, index) => (
                                    <div key={index} className="flex items-center p-2 bg-[#238636]/10 border border-[#238636]/20 rounded text-sm">
                                        <div className="w-2 h-2 bg-[#238636] rounded-full mr-3 flex-shrink-0"></div>
                                        <span className="text-[#f0f6fc]">{skill}</span>
                                    </div>
                                ))}
                                {analysis.skills_matching.matching_skills.length === 0 && (
                                    <p className="text-sm text-[#7d8590] italic">No matching skills found</p>
                                )}
                            </div>
                        </div>

                        {/* Missing Skills */}
                        <div className="border border-[#30363d] rounded-md p-6 bg-[#161b22]">
                            <h3 className="text-lg font-medium text-[#f0f6fc] mb-4 flex items-center">
                                <svg className="w-5 h-5 text-[#da3633] mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                                </svg>
                                Missing Skills ({analysis.skills_matching.missing_skills.length})
                            </h3>
                            <div className="space-y-2 max-h-60 overflow-y-auto">
                                {analysis.skills_matching.missing_skills.map((skill, index) => (
                                    <div key={index} className="flex items-center p-2 bg-[#da3633]/10 border border-[#da3633]/20 rounded text-sm">
                                        <div className="w-2 h-2 bg-[#da3633] rounded-full mr-3 flex-shrink-0"></div>
                                        <span className="text-[#f0f6fc]">{skill}</span>
                                    </div>
                                ))}
                                {analysis.skills_matching.missing_skills.length === 0 && (
                                    <p className="text-sm text-[#238636] italic">Great! No missing required skills.</p>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Recommendations */}
                    {analysis.skills_matching.recommendations && (
                        <div className="border border-[#1f6feb] bg-[#0d1117] rounded-md p-6">
                            <h3 className="text-lg font-medium text-[#58a6ff] mb-4 flex items-center">
                                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                                Recommendations
                            </h3>
                            <ul className="space-y-3">
                                {analysis.skills_matching.recommendations.map((rec, index) => (
                                    <li key={index} className="flex items-start text-sm text-[#7d8590]">
                                        <span className="text-[#58a6ff] mr-2 mt-0.5 text-base">💡</span>
                                        <span>{rec}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {/* Resume & Job Summary */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Resume Summary */}
                        <div className="border border-[#30363d] rounded-md p-6 bg-[#161b22]">
                            <h3 className="text-lg font-medium text-[#f0f6fc] mb-4">Resume Summary</h3>
                            <div className="space-y-3 text-sm">
                                <div className="flex justify-between items-center">
                                    <span className="text-[#7d8590]">Skills Found:</span>
                                    <span className="text-[#f0f6fc] font-medium">{analysis.resume_data.skills_count}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-[#7d8590]">Experience Entries:</span>
                                    <span className="text-[#f0f6fc] font-medium">{analysis.resume_data.experience_count}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-[#7d8590]">Education Entries:</span>
                                    <span className="text-[#f0f6fc] font-medium">{analysis.resume_data.education_count}</span>
                                </div>
                                {analysis.resume_data.summary && (
                                    <div className="mt-4 pt-3 border-t border-[#30363d]">
                                        <span className="text-[#7d8590] text-xs font-medium">Summary:</span>
                                        <p className="text-[#f0f6fc] mt-1 text-xs leading-relaxed">
                                            {analysis.resume_data.summary}
                                        </p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Job Summary */}
                        <div className="border border-[#30363d] rounded-md p-6 bg-[#161b22]">
                            <h3 className="text-lg font-medium text-[#f0f6fc] mb-4">Job Summary</h3>
                            <div className="space-y-3 text-sm">
                                <div className="flex justify-between items-center">
                                    <span className="text-[#7d8590]">Position:</span>
                                    <span className="text-[#f0f6fc] font-medium text-right">
                                        {analysis.job_data.job_title || 'Not specified'}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-[#7d8590]">Company:</span>
                                    <span className="text-[#f0f6fc] font-medium text-right">
                                        {analysis.job_data.company_name || 'Not specified'}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-[#7d8590]">Required Skills:</span>
                                    <span className="text-[#f0f6fc] font-medium">{analysis.job_data.required_skills_count}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-[#7d8590]">Job Type:</span>
                                    <span className="text-[#f0f6fc] font-medium">{analysis.job_data.job_type}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-[#7d8590]">Experience Level:</span>
                                    <span className="text-[#f0f6fc] font-medium">{analysis.job_data.experience_level}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CoverLetterGenerator;