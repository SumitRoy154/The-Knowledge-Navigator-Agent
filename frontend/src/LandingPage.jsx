import { useState, useEffect } from "react";
import HeroAuroraBackground from "./HeroAuroraBackground";

export default function LandingPage() {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem("theme");
    return saved ? saved === "dark" : true;
  });

  // Initialize theme on mount
  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "light") {
      document.body.classList.add("light-mode");
      document.body.classList.remove("dark-mode");
    } else {
      document.body.classList.add("dark-mode");
      document.body.classList.remove("light-mode");
    }
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark-mode");
      document.body.classList.remove("light-mode");
      localStorage.setItem("theme", "dark");
    } else {
      document.body.classList.add("light-mode");
      document.body.classList.remove("dark-mode");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  return (
    <div className="landing-page">
      <HeroAuroraBackground />
      <button 
        className="theme-toggle landing-theme-toggle" 
        onClick={() => setDarkMode(!darkMode)}
        aria-label="Toggle theme"
      >
        {darkMode ? "☀️" : "🌙"}
      </button>
      <div className="landing-container">
        <div className="landing-icon">🎓</div>
        <h1 className="landing-title">Knowledge Navigator</h1>
        <p className="landing-subtitle">AI-Powered Academic Advisor for Curated Learning Paths</p>
        
        <div className="landing-features">
          <div className="feature">
            <span className="feature-icon">🔍</span>
            <h3>Find Best Courses</h3>
            <p>Real-time course data with prices, ratings, and availability</p>
          </div>
          <div className="feature">
            <span className="feature-icon">📋</span>
            <h3>Personalized Roadmaps</h3>
            <p>Structured learning paths tailored to your goals and budget</p>
          </div>
          <div className="feature">
            <span className="feature-icon">🤖</span>
            <h3>AI-Powered Guidance</h3>
            <p>Expert academic advisor available 24/7</p>
          </div>
        </div>

        <button className="cta-button" onClick={() => window.location.hash = '#/chat'}>
          Ready to Learn →
        </button>
      </div>
    </div>
  );
}
