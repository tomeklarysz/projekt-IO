type LogsProps = {
    onGoToMenu: () => void;
};

export default function Logs({ onGoToMenu }: LogsProps) {
    return (
        <div>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem'}}>
                <h1>Access Logs</h1>
                <button type="button" className="btn btn-secondary" onClick={onGoToMenu}>
                    ← Back to Dashboard
                </button>
            </div>
            
            <div className="card">
                <p style={{color: 'var(--text-light)', textAlign: 'center', padding: '2rem'}}>
                    No logs available to display at this time.
                </p>
                {/* Table placeholder */}
            </div>
        </div>
    );
}
