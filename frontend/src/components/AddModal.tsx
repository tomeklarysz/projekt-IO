import { useState } from "react";

type AddModalProps = {
    onClose: () => void;
    onAdd: (firstName: string, lastName: string) => void;
};

export default function AddModal({ onClose, onAdd }: AddModalProps) {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");

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
                     <button type="button" className="btn btn-secondary" style={{width: '100%'}}>
                        📷 Upload Worker Photos
                    </button>
                    <p style={{fontSize: '0.75rem', color: 'var(--text-light)', marginTop: '0.5rem', textAlign: 'center'}}>
                        Please upload at least 3 clear face photos for recognition.
                    </p>
                </div>

                <div className="modal-footer">
                    <button type="button" className="btn btn-secondary" onClick={onClose}>
                        Cancel
                    </button>
                    <button 
                        type="button" 
                        className="btn btn-primary"
                        onClick={() => onAdd(firstName, lastName)}
                        disabled={!firstName || !lastName}
                        style={{opacity: (!firstName || !lastName) ? 0.6 : 1}}
                    >
                        Register Worker
                    </button>
                </div>
            </div>
        </div>
    );
}
