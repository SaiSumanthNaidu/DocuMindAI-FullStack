import "./Hero.css";
import {
  FaMagic,
  FaFilePdf,
  FaRobot,
  FaCheckCircle,
  FaClipboardList,
  FaTable,
} from "react-icons/fa";
import { NavLink } from "react-router-dom";

function Hero() {
  return (
    <section className="hero">
      <div className="container">
        <div className="hero-container">

          {/* =========================
              HERO CONTENT
          ========================= */}
          <div className="hero-content">

            <span className="hero-badge">
              <FaMagic />
              AI Powered OCR
            </span>

            <h1 className="hero-title">
              Transform Documents Into{" "}
              <span className="text-gradient">
                Structured Data
              </span>{" "}
              With AI
            </h1>

            <p className="hero-description">
              Upload PDFs or images and instantly extract structured data,
              AI-powered summaries, and key insights with enterprise-grade
              accuracy.
            </p>

            <div className="hero-actions">
              <NavLink
                to="/analyze"
                className="primary-btn"
              >
                Get Started
              </NavLink>

              <button className="secondary-btn">
                Watch Demo
              </button>
            </div>

          </div>

          {/* =========================
              HERO IMAGE
          ========================= */}
          <div className="hero-image">

            {/* Upload Card */}
            <div className="upload-card">

              {/* File Preview */}
              <div className="file-preview">

                <div className="file-icon">
                  <FaFilePdf />
                </div>

                <div className="file-info">
                  <h4>invoice.pdf</h4>
                  <p>PDF • 2.4 MB</p>
                </div>

              </div>

              {/* Processing Status */}
              <div className="processing-status">

                <div className="processing-header">
                  <span>AI Processing...</span>
                  <span>92%</span>
                </div>

                <div className="progress-bar">
                  <div className="progress-fill"></div>
                </div>

              </div>

              {/* Result List */}
              <div className="result-list">

              <div className="result-item">
                  <FaCheckCircle />
                  <span>OCR Complete</span>
              </div>

              <div className="result-item">
                  <FaClipboardList />
                  <span>AI Summary Ready</span>
              </div>

              <div className="result-item">
                  <FaTable />
                  <span>Structured Data</span>
              </div>

              </div>

            </div>

            {/* Floating Elements */}
            <div className="floating floating-pdf">
                <FaFilePdf />
            </div>

            <div className="floating floating-ai">
                <FaRobot />
            </div>

            <div className="floating floating-sparkle">
                <FaMagic />
            </div>

          </div>

        </div>
      </div>
    </section>
  );
}

export default Hero;