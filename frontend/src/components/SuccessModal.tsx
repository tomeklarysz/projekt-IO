type SuccessModalProps = {
    workerName: string;
    onClose: () => void;
};

export default function SuccessModal({ workerName, onClose }: SuccessModalProps) {
    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{maxWidth: '400px', textAlign: 'center'}}>
                <div className="success-message">
                    <div className="success-icon">✓</div>
                    <h3 style={{marginBottom: '0.5rem', color: 'var(--text-color)'}}>Registration Successful</h3>
                    <p style={{color: 'var(--text-light)', marginBottom: '1.5rem'}}>
                        Worker <strong>{workerName}</strong> has been successfully added to the system.
                    </p>
                    <button type="button" className="btn btn-primary" onClick={onClose} style={{width: '100%'}}>
                        Return to Dashboard
                    </button>
                </div>
            </div>
        </div>
    );
}
