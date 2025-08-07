import React from 'react';
import { motion } from 'framer-motion';
import CoverLetterGenerator from './components/CoverLetterGenerator';
import ContactForm from "./components/ContactForm";
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-[#0d1117] text-[#e6edf3] overflow-x-hidden">
      {/* Subtle Background Pattern */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none opacity-30">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0)`,
          backgroundSize: '20px 20px'
        }} />
      </div>

      {/* Header */}
      <motion.header 
        className="relative bg-[#161b22] border-b border-[#30363d] sticky top-0 z-50"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <div className="max-w-7xl mx-auto px-6 py-4">
          <motion.div 
            className="flex items-center justify-between"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <div className="flex items-center space-x-3">
              <motion.div
                className="w-8 h-8 bg-[#f0f6fc] text-[#0d1117] rounded-md flex items-center justify-center"
                whileHover={{ scale: 1.05 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" strokeWidth={1.5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </motion.div>
              <h1 className="text-xl font-semibold text-[#f0f6fc]">
                CoverLetter Generator
              </h1>
            </div>
            
            <motion.div 
              className="hidden md:flex items-center space-x-6"
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3, duration: 0.5 }}
            >
              <nav className="flex space-x-6">
                <a href="#features" className="text-[#7d8590] hover:text-[#f0f6fc] transition-colors duration-200 text-sm font-medium">Features</a>
                <a href="#generator" className="text-[#7d8590] hover:text-[#f0f6fc] transition-colors duration-200 text-sm font-medium">Generator</a>
                <a href="#contact-form" className="text-[#7d8590] hover:text-[#f0f6fc] transition-colors duration-200 text-sm font-medium">Contact</a>
                 </nav>
            </motion.div>
          </motion.div>
        </div>
      </motion.header>

      {/* Hero Section */}
      <section className="relative py-20 px-6 text-center">
        <motion.div
          className="max-w-5xl mx-auto relative z-10"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <motion.div
            className="mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.6 }}
          >
            <h2 className="text-5xl md:text-6xl font-bold mb-6 text-[#f0f6fc] leading-tight">
              Create professional cover letters
              <br />
              <span className="text-[#7c3aed]">powered by AI</span>
            </h2>
          </motion.div>
          
          <motion.p
            className="text-xl text-[#7d8590] max-w-3xl mx-auto mb-8 leading-relaxed"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
          >
            Generate tailored, professional cover letters that help you stand out to employers. 
            Built for job seekers who want to make a great first impression.
          </motion.p>

          <motion.div
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.6 }}
          >
            <motion.a
              href="#generator"
              className="px-6 py-3 bg-[#238636] hover:bg-[#2ea043] text-white font-medium rounded-md transition-all duration-200 flex items-center"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Get started
              <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </motion.a>
          </motion.div>

          {/* Feature Stats */}
          <motion.div
            className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.6 }}
          >
            {[
              { 
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                ), 
                title: "Lightning fast", 
                desc: "Generate in under 30 seconds" 
              },
              { 
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                ), 
                title: "ATS optimized", 
                desc: "Passes applicant tracking systems" 
              },
              { 
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                ), 
                title: "Personalized", 
                desc: "Tailored to each job application" 
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="border border-[#30363d] rounded-lg p-6 bg-[#0d1117] hover:border-[#8b949e] transition-all duration-200"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 + index * 0.1, duration: 0.5 }}
                whileHover={{ y: -2 }}
              >
                <div className="text-[#7c3aed] mb-4 flex justify-center">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-[#f0f6fc] mb-2">{feature.title}</h3>
                <p className="text-[#7d8590] text-sm leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>
      </section>

      {/* Detailed Features Section */}
      <motion.section
        id="features"
        className="relative py-24 px-6 bg-gradient-to-b from-[#0d1117] to-[#161b22]"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true, margin: "-100px" }}
      >
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-[#f0f6fc] mb-4">
              Everything you need to
              <span className="text-[#7c3aed]"> land your dream job</span>
            </h2>
            <p className="text-xl text-[#7d8590] max-w-3xl mx-auto">
              Our AI-powered platform provides all the tools you need to create compelling cover letters that get noticed.
            </p>
          </motion.div>

          {/* Main Features Grid */}
          <div className="grid lg:grid-cols-2 gap-12 mb-20">
            {/* Feature 1: AI-Powered Generation */}
            <motion.div
              className="flex flex-col"
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              viewport={{ once: true }}
            >
              <div className="border border-[#30363d] rounded-lg p-8 bg-[#161b22] h-full hover:border-[#8b949e] transition-all duration-300 group">
                <div className="flex items-center mb-6">
                  <div className="w-12 h-12 bg-[#7c3aed] rounded-lg flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-[#f0f6fc]">Smart AI Generation</h3>
                </div>
                <p className="text-[#7d8590] mb-6 leading-relaxed">
                  Our advanced AI analyzes job descriptions and your experience to create personalized cover letters that highlight your most relevant skills and achievements.
                </p>
                <div className="space-y-3">
                  {[
                    "Contextual job matching",
                    "Keyword optimization",
                    "Industry-specific language",
                    "Achievement highlighting"
                  ].map((feature, index) => (
                    <div key={index} className="flex items-center text-sm">
                      <svg className="w-4 h-4 text-[#238636] mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className="text-[#7d8590]">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>

            {/* Feature 2: Professional Templates */}
            <motion.div
              className="flex flex-col"
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <div className="border border-[#30363d] rounded-lg p-8 bg-[#161b22] h-full hover:border-[#8b949e] transition-all duration-300 group">
                <div className="flex items-center mb-6">
                  <div className="w-12 h-12 bg-[#238636] rounded-lg flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                    <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-[#f0f6fc]">Professional Templates</h3>
                </div>
                <p className="text-[#7d8590] mb-6 leading-relaxed">
                  Choose from a variety of professionally designed templates that are optimized for different industries and career levels, ensuring your application looks polished.
                </p>
                <div className="space-y-3">
                  {[
                    "Multiple design options",
                    "Industry-specific layouts",
                    "ATS-friendly formatting",
                    "Mobile-responsive design"
                  ].map((feature, index) => (
                    <div key={index} className="flex items-center text-sm">
                      <svg className="w-4 h-4 text-[#238636] mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className="text-[#7d8590]">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>

          {/* Additional Features Row */}
          <motion.div
            className="grid md:grid-cols-3 gap-8"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: true }}
          >
            {[
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                ),
                title: "Privacy First",
                description: "Your data is encrypted and never shared. Complete privacy protection for your job search.",
                color: "text-[#f85149]"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                ),
                title: "Export Options",
                description: "Download your cover letters in multiple formats including PDF, Word, and plain text.",
                color: "text-[#f0883e]"
              },
              {
                icon: (
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                ),
                title: "Real-time Preview",
                description: "See your cover letter update in real-time as you make changes, ensuring perfect formatting.",
                color: "text-[#7c3aed]"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="border border-[#30363d] rounded-lg p-6 bg-[#0d1117] hover:border-[#8b949e] transition-all duration-300 group"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index, duration: 0.5 }}
                viewport={{ once: true }}
                whileHover={{ y: -5 }}
              >
                <div className={`${feature.color} mb-4 flex justify-center group-hover:scale-110 transition-transform duration-300`}>
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-[#f0f6fc] mb-3 text-center">{feature.title}</h3>
                <p className="text-[#7d8590] text-sm text-center leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>

          {/* Call to Action */}
          <motion.div
            className="text-center mt-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            viewport={{ once: true }}
          >
            <motion.a
              href="#generator"
              className="inline-flex items-center px-8 py-4 bg-[#7c3aed] hover:bg-[#8b5cf6] text-white font-semibold rounded-lg transition-all duration-200 text-lg"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Start creating your cover letter
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </motion.a>
          </motion.div>
        </div>
      </motion.section>

      {/* Main Generator Section */}
      <motion.main
        id="generator"
        className="relative max-w-5xl mx-auto py-16 px-6"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        viewport={{ once: true, margin: "-50px" }}
      >
        <motion.div
          className="border border-[#30363d] rounded-lg bg-[#161b22] shadow-lg"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          viewport={{ once: true }}
        >
          {/* Header */}
          <div className="border-b border-[#30363d] px-8 py-6">
            <motion.div
              className="text-center"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              viewport={{ once: true }}
            >
              <h3 className="text-2xl font-semibold text-[#f0f6fc] mb-2">
                Cover Letter Generator
              </h3>
              <p className="text-[#7d8590] max-w-2xl mx-auto">
                Enter your information below to generate a professional, personalized cover letter.
              </p>
            </motion.div>
          </div>
          
          {/* Generator Content */}
          <div className="p-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.5 }}
              viewport={{ once: true }}
            >
              <CoverLetterGenerator />
            </motion.div>
          </div>
        </motion.div>
      </motion.main>

      <motion.section
      id="contact-form"
      className="relative py-24 px-6 bg-gradient-to-b from-[#0d1117] to-[#161b22]"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
      viewport={{ once: true, margin: "-100px" }}
    >
      <div className="max-w-3xl mx-auto">
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-[#f0f6fc] mb-4">
            Get in <span className="text-[#7c3aed]">Touch</span>
          </h2>
          <p className="text-xl text-[#7d8590] max-w-2xl mx-auto">
            Have questions or need help? Fill out the form below and we'll get back to you as soon as possible.
          </p>
        </motion.div>

        {/* Contact Form */}
        <ContactForm />
      </div>
    </motion.section>

      {/* Footer */}
      <motion.footer 
        className="relative border-t border-[#30363d] bg-[#161b22] mt-24"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        viewport={{ once: true }}
      >
        <div className="max-w-7xl mx-auto py-16 px-6">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
            <div className="col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-6 h-6 bg-[#f0f6fc] text-[#0d1117] rounded-sm flex items-center justify-center">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" strokeWidth={1.5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <span className="font-semibold text-[#f0f6fc]">CoverLetter Generator</span>
              </div>
              <p className="text-[#7d8590] text-sm max-w-sm leading-relaxed">
                Making job applications easier with AI-powered cover letter generation. 
                Built for developers, by developers.
              </p>
            </div>
            
            <div>
              <h4 className="text-[#f0f6fc] font-semibold mb-3 text-sm">Product</h4>
              <ul className="space-y-2">
                {['Features'].map(item => (
                  <li key={item}>
                    <a href="#" className="text-[#7d8590] hover:text-[#58a6ff] text-sm transition-colors duration-200">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            
            
            
            <div>
              <h4 className="text-[#f0f6fc] font-semibold mb-3 text-sm">Support</h4>
              <ul className="space-y-2">
                {['Help Center', 'Contact'].map(item => (
                  <li key={item}>
                    <a href="##contact-form" className="text-[#7d8590] hover:text-[#58a6ff] text-sm transition-colors duration-200">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          <div className="border-t border-[#30363d] mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-[#7d8590] text-sm">
            © 2024 CoverLetter Generator. Built with React and Gemini AI.
          </p>
          
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <a
              href="https://github.com/jagruti261"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#7d8590] hover:text-[#f0f6fc] transition-colors duration-200"
            >
              <span className="text-sm">GitHub</span>
            </a>

            <a
              href="https://www.linkedin.com/in/jagrutivekariya/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#7d8590] hover:text-[#f0f6fc] transition-colors duration-200"
            >
              <span className="text-sm">LinkedIn</span>
            </a>
          </div>
        </div>

        </div>
      </motion.footer>
    </div>
  );
}

export default App;