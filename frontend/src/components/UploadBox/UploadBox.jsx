import { useState, useRef } from "react";
import "./UploadBox.css";
import { FaCloudUploadAlt } from "react-icons/fa";

function UploadBox() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setSelectedFile(file);
  };
  const handleRemoveFile = () => {
    setSelectedFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };
  const handleAnalyzeDocument = () => {
    setIsAnalyzing(true);
  };

  return (
    <section className="upload">
      <div className="container">
        <div className="upload-card">
          <div className="upload-icon">
            <FaCloudUploadAlt />
          </div>

          <h2 className="upload-title">Upload Your Document</h2>

          <p className="upload-description">
            Drag & drop your PDF or image here, or browse your files to start
            AI-powered document processing.
          </p>

          <label
            htmlFor="file-upload"
            className="upload-button"
            onClick={() => fileInputRef.current?.click()}
          >
            Browse Files
          </label>

          {selectedFile && (
            <div className="selected-file-container">
              <p className="selected-file">📄 {selectedFile.name}</p>

              <button className="remove-file-button" onClick={handleRemoveFile}>
                Remove File
              </button>
            </div>
          )}
          <button onClick={handleAnalyzeDocument} disabled={isAnalyzing}>
            {isAnalyzing ? "Analyzing..." : "Analyze Document"}
          </button>

          <input
            ref={fileInputRef}
            type="file"
            id="file-upload"
            hidden
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileChange}
          />

          <div className="upload-info">
            <span>Supported: PDF • JPG • PNG</span>

            <span>Max Size: 10 MB</span>
          </div>
        </div>
      </div>
    </section>
  );
}

export default UploadBox;
