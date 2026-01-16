import { useEffect, useState } from "react";

type MenuProps = {
    onGoToLogs: () => void;
    onOpenAddWorker: () => void;
    onGoToDetails: (qr_hash: string) => void;
    refreshKey?: number;
};

interface Worker {
    qr_hash: string;
    first_name: string;
    last_name: string;
    status: string;
}

export default function Menu({ onGoToLogs, onOpenAddWorker, onGoToDetails, refreshKey = 0 }: MenuProps) {
    const [workers, setWorkers] = useState<Worker[]>([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/workers')
            .then(res => res.json())
            .then(data => setWorkers(data))
            .catch(err => console.error("Error fetching workers:", err));
    }, [refreshKey]);

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

            <div style={{marginTop: '3rem'}}>
                <h2 style={{marginBottom: '1rem'}}>Current Workers</h2>
                <div className="card" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                    {workers.length === 0 ? (
                        <p style={{color: 'var(--text-light)', padding: '1rem'}}>No workers found.</p>
                    ) : (
                        <ul style={{listStyle: 'none', padding: 0, margin: 0}}>
                            {workers.map(worker => (
                                <li key={worker.qr_hash} 
                                    onClick={() => onGoToDetails(worker.qr_hash)}
                                    style={{
                                        padding: '1rem', 
                                        borderBottom: '1px solid #eee',
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'center',
                                        cursor: 'pointer'
                                    }}
                                    className="worker-item"
                                >
                                    <span style={{fontWeight: 500}}>{worker.first_name} {worker.last_name}</span>
                                    <span style={{
                                        fontSize: '0.875rem', 
                                        padding: '0.25rem 0.75rem', 
                                        background: worker.status === 'Active' ? '#e6f4ea' : '#f1f3f4',
                                        color: worker.status === 'Active' ? '#1e8e3e' : '#5f6368',
                                        borderRadius: '999px'
                                    }}>
                                        {worker.status}
                                    </span>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        </div>
    );
}