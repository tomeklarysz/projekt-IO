import { useState, useRef } from "react";

type AddModalProps = {
    onClose: () => void;
    onAdd: (firstName: string, lastName: string) => void;
};

export default function AddModal({ onClose, onAdd }: AddModalProps) {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleRegister = async () => {
        try {
            if (!selectedFile) {
                alert("Please select a photo first.");
                return;
            }
            
            setIsLoading(true);

            // Step 1: Upload Photo
            const formData = new FormData();
            formData.append('file', selectedFile);

            const uploadResponse = await fetch('http://localhost:8000/upload', {
                method: 'POST',
                body: formData
            });

            if (!uploadResponse.ok) {
                const errText = await uploadResponse.text();
                throw new Error(`Upload failed: ${errText}`);
            }

            const uploadData = await uploadResponse.json();
            const photoPath = uploadData.file_path;

            // Step 2: Register Employee with Photo Path
            const formDataRegister = new FormData();
            formDataRegister.append('first_name', firstName);
            formDataRegister.append('last_name', lastName);
            formDataRegister.append('photo_path', photoPath);

            const response = await fetch('http://localhost:8000/employees/add', {
                method: 'POST',
                body: formDataRegister,
            });

            if (response.ok) {
                onAdd(firstName, lastName);
                onClose();
            } else {
                const errText = await response.text();
                console.error("Failed to register worker:", errText);
                alert("Failed to register worker: " + errText);
            }
        } catch (error) {
            console.error("Error registering worker:", error);
            alert("Error: " + error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={(e) => {
            if (e.target === e.currentTarget) onClose();
        }}>
            <div className="modal-content">
                <div className="modal-header">
                    <h3 className="modal-title">New Worker Registration</h3>
                    <button type="button" className="btn-close" onClick={onClose} aria-label="close">
                        ✕
                    </button>
                </div>

                <div className="input-group">
                    <label className="input-label">
                        First Name
                    </label>
                    <input
                        className="form-control"
                        type="text"
                        placeholder="Enter first name"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                    />
                </div>

                <div className="input-group">
                    <label className="input-label">
                        Last Name
                    </label>
                    <input
                        className="form-control"
                        type="text"
                        placeholder="Enter last name"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                    />
                </div>

                <div className="input-group" style={{marginTop: '1.5rem', marginBottom: '0'}}>
                    <input 
                        type="file" 
                        ref={fileInputRef} 
                        style={{display: 'none'}} 
                        accept="image/*"
                        onChange={(e) => {
                            if (e.target.files && e.target.files[0]) {
                                setSelectedFile(e.target.files[0]);
                            }
                        }}
                    />
                     <button 
                        type="button" 
                        className="btn btn-secondary" 
                        style={{width: '100%'}}
                        onClick={() => fileInputRef.current?.click()}
                     >
                        {selectedFile ? `📷 Selected: ${selectedFile.name}` : "📷 Upload Worker Photo"}
                    </button>
                    <p style={{fontSize: '0.75rem', color: 'var(--text-light)', marginTop: '0.5rem', textAlign: 'center'}}>
                        Please upload a clear face photo for recognition.
                    </p>
                </div>

                <div className="modal-footer">
                    <button type="button" className="btn btn-secondary" onClick={onClose} disabled={isLoading}>
                        Cancel
                    </button>
                    <button 
                        type="button" 
                        className="btn btn-primary"
                        onClick={handleRegister}
                        disabled={!firstName || !lastName || !selectedFile || isLoading}
                        style={{opacity: (!firstName || !lastName || !selectedFile || isLoading) ? 0.6 : 1}}
                    >
                        {isLoading ? "Processing..." : "Register Worker"}
                    </button>
                </div>
            </div>
        </div>
    );
}
