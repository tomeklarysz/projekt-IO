type MenuProps = {
    onGoToLogs: () => void;
    onOpenAddWorker: () => void;
};

export default function Menu({ onGoToLogs, onOpenAddWorker }: MenuProps) {
    return (
        <div>
            <h1 style={{marginBottom: '2rem'}}>Dashboard</h1>
            <div className="dashboard-grid">
                <div className="dashboard-card" onClick={onGoToLogs}>
                    <div className="dashboard-icon">📋</div>
                    <h3 className="dashboard-title">Access Logs</h3>
                    <p style={{color: 'var(--text-light)', margin: '0.5rem 0 0'}}>View entry and exit history</p>
                </div>

                <div className="dashboard-card" onClick={onOpenAddWorker}>
                    <div className="dashboard-icon">👤</div>
                    <h3 className="dashboard-title">Add Worker</h3>
                    <p style={{color: 'var(--text-light)', margin: '0.5rem 0 0'}}>Register new personnel</p>
                </div>
            </div>
        </div>
    );
}