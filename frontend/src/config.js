const config = {
  apiUrl: process.env.NODE_ENV === 'production' 
    ? 'https://cover-letter-agent-backend.onrender.com'
    : 'http://localhost:5051'
};

export default config;
