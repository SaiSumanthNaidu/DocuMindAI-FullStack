import "./UploadBox.css";
import { FaCloudUploadAlt } from "react-icons/fa";

function UploadBox() {
    return (
        <section className="upload">

            <div className="container">

                <div className="upload-card">

                    <div className="upload-icon">
                        <FaCloudUploadAlt />
                    </div>

                    <h2 className="upload-title">
                        Upload Your Document
                    </h2>

                    <p className="upload-description">
                        Drag & drop your PDF or image here, or browse your files to start AI-powered document processing.
                    </p>

                    <label
                        htmlFor="file-upload"
                        className="upload-button"
                    >
                        Browse Files
                    </label>

                    <input
                        id="file-upload"
                        type="file"
                        hidden
                    />

                    <div className="upload-info">

                        <span>
                            Supported: PDF • JPG • PNG
                        </span>

                        <span>
                            Max Size: 10 MB
                        </span>

                    </div>

                </div>

            </div>

        </section>
    );
}

export default UploadBox;