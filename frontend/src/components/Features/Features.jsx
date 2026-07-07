import "./Features.css";
import {
    FaMagic,
    FaFileAlt,
    FaDatabase
} from "react-icons/fa";

function Features() {
    const features = [
    {
        icon: <FaFileAlt />,
        title: "Smart OCR Extraction",
        description:
        "Extract text from PDFs, scanned documents, invoices, and images with high accuracy.",
    },
    {
        icon: <FaMagic />,
        title: "AI-Powered Summaries",
        description:
        "Generate intelligent summaries and key insights from your documents in seconds.",
    },
    {
        icon: <FaDatabase />,
        title: "Structured Data Extraction",
        description:
        "Convert unstructured documents into organized, searchable, and actionable data.",
    },
    ];
    return (
        <section className="features">

            <div className="container">

                <div className="section-header">

                    <span className="section-badge">
                        <FaMagic />
                        Powerful AI Features
                    </span>

                    <h2 className="section-title">
                        Everything You Need to Process Documents
                    </h2>

                    <p className="section-description">
                        Upload PDFs or images and instantly extract text,
                        generate AI-powered summaries, and convert your
                        documents into structured, actionable data.
                    </p>

                </div>

                <div className="features-grid">

                    {features.map((feature, index) => (

                        <div
                            className="feature-card"
                            key={index}
                        >

                            <div className="feature-icon">
                            {feature.icon}
                            </div>

                            <div className="feature-content">

                            <h3 className="feature-title">
                                {feature.title}
                            </h3>

                            <p className="feature-description">
                                {feature.description}
                            </p>

                            </div>

                        </div>

                        ))}

                </div>
            </div>
        </section>
    );
}

export default Features;