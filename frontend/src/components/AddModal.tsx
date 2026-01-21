import { useState, useRef, useEffect } from "react";

type WorkerData = {
    firstName: string;
    lastName: string;
    qrHash?: string; // Needed for updates
};

type AddModalProps = {
    onClose: () => void;
    onSuccess: () => void;
    initialData?: WorkerData | null;
};

export default function AddModal({ onClose, onSuccess, initialData }: AddModalProps) {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const isEditMode = !!initialData;

    useEffect(() => {
        if (initialData) {
            setFirstName(initialData.firstName);
            setLastName(initialData.lastName);
        } else {
            setFirstName("");
            setLastName("");
        }
        setSelectedFile(null);
    }, [initialData]);

    const handleSubmit = async () => {
        try {
            if (!isEditMode && !selectedFile) {
                alert("Please select a photo first.");
                return;
            }

            setIsLoading(true);

            let photoPath = null;

            // Step 1: Upload Photo (if selected)
            if (selectedFile) {
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
                photoPath = uploadData.file_path;
            }

            // Step 2: Register or Update Employee
            const formDataEmployee = new FormData();
            formDataEmployee.append('first_name', firstName);
            formDataEmployee.append('last_name', lastName);
            if (photoPath) {
                formDataEmployee.append('photo_path', photoPath);
            }

            let response;
            if (isEditMode && initialData?.qrHash) {
                // UPDATE
                response = await fetch(`http://localhost:8000/employees/${initialData.qrHash}`, {
                    method: 'PUT',
                    body: formDataEmployee,
                });
            } else {
                // CREATE
                // create endpoint requires photo_path
                if (!photoPath) {
                    throw new Error("Photo is required for new registration.");
                }
                response = await fetch('http://localhost:8000/employees/add', {
                    method: 'POST',
                    body: formDataEmployee,
                });
            }

            if (response.ok) {
                onSuccess();
                onClose();
            } else {
                const errText = await response.text();
                console.error("Failed to save worker:", errText);
                alert("Failed to save worker: " + errText);
            }
        } catch (error) {
            console.error("Error saving worker:", error);
            alert("Error: " + error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header">
                    <h3 className="modal-title">{isEditMode ? "Edit Worker" : "New Worker Registration"}</h3>
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

                <div className="input-group" style={{ marginTop: '1.5rem', marginBottom: '0' }}>
                    <input
                        type="file"
                        ref={fileInputRef}
                        style={{ display: 'none' }}
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
                        style={{ width: '100%' }}
                        onClick={() => fileInputRef.current?.click()}
                    >
                        {selectedFile ? `📷 Selected: ${selectedFile.name}` : (isEditMode ? "📷 Update Photo (Optional)" : "📷 Upload Worker Photo")}
                    </button>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-light)', marginTop: '0.5rem', textAlign: 'center' }}>
                        {isEditMode ? "Upload only if you want to replace the current photo." : "Please upload a clear face photo for recognition."}
                    </p>
                </div>

                <div className="modal-footer">
                    <button type="button" className="btn btn-secondary" onClick={onClose} disabled={isLoading}>
                        Cancel
                    </button>
                    <button
                        type="button"
                        className="btn btn-primary"
                        onClick={handleSubmit}
                        disabled={!firstName || !lastName || (!isEditMode && !selectedFile) || isLoading}
                        style={{ opacity: (!firstName || !lastName || (!isEditMode && !selectedFile) || isLoading) ? 0.6 : 1 }}
                    >
                        {isLoading ? "Processing..." : (isEditMode ? "Save Changes" : "Register Worker")}
                    </button>
                </div>
            </div>
        </div>
    );
}

