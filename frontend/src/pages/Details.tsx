import { useEffect, useState } from "react";

type DetailsProps = {
    workerId: number;
    onGoToMenu: () => void;
};

interface Log {
    id: number;
    timestamp: string;
    action: string;
}

interface WorkerDetails {
    id: number;
    first_name: string;
    last_name: string;
    qr_code_url: string;
    qr_expiration: string;
}

export default function Details({ workerId, onGoToMenu }: DetailsProps) {
    const [worker, setWorker] = useState<WorkerDetails | null>(null);
    const [logs, setLogs] = useState<Log[]>([]);
    const [newExpiryDate, setNewExpiryDate] = useState("");

    useEffect(() => {
        // Fetch worker details
        fetch(`http://localhost:5000/api/workers/${workerId}`)
            .then(res => res.json())
            .then(data => {
                setWorker(data);
                // Initialize new expiry date with current one if available
                if (data.qr_expiration) {
                    setNewExpiryDate(data.qr_expiration.split('T')[0]); // Format for date input
                }
            })
            .catch(err => {
                console.error("Error fetching worker details:", err);
                // Fallback for testing with our hardcoded worker
                if (workerId === 999) {
                    setWorker({
                        id: 999,
                        first_name: "Test",
                        last_name: "Worker",
                        qr_code_url: "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=TestWorker999",
                        qr_expiration: "2026-12-31"
                    });
                    setNewExpiryDate("2026-12-31");
                }
            });

        // Fetch logs for this worker
        fetch(`http://localhost:5000/api/workers/${workerId}/logs`)
            .then(res => res.json())
            .then(data => setLogs(data))
            .catch(err => console.error("Error fetching worker logs:", err));
    }, [workerId]);

    const handleUpdateExpiry = () => {
         fetch(`http://localhost:5000/api/workers/${workerId}/qr/expiry`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expiration_date: newExpiryDate })
        })
        .then(() => alert("Expiration date updated!"))
        .catch(err => console.error("Error updating expiry:", err));
    };

    if (!worker) {
        return <div style={{padding: '2rem', textAlign: 'center'}}>Loading worker details...</div>;
    }

    return (
        <div>
            <div style={{display: 'flex', alignItems: 'center', marginBottom: '2rem'}}>
                <button 
                    type="button" 
                    className="btn btn-secondary" 
                    onClick={onGoToMenu}
                    style={{marginRight: '1rem'}}
                >
                    ← Back
                </button>
                <h1 style={{margin: 0}}>Worker Details</h1>
            </div>

            <div className="dashboard-grid" style={{gridTemplateColumns: '2fr 1fr', gap: '2rem'}}>
                {/* Main Info Card */}
                <div className="card">
                    <h2 style={{marginTop: 0, borderBottom: '1px solid #eee', paddingBottom: '1rem', marginBottom: '1.5rem'}}>
                        {worker.first_name} {worker.last_name}
                    </h2>
                    
                    <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem'}}>
                        <div>
                            <p style={{color: 'var(--text-light)', marginBottom: '0.25rem'}}>Worker ID</p>
                            <p style={{fontSize: '1.1rem', fontWeight: 500}}>{worker.id}</p>
                        </div>
                        
                        <div>
                             <p style={{color: 'var(--text-light)', marginBottom: '0.25rem'}}>Latest Action</p>
                             <p>{logs.length > 0 && logs[0] ? logs[0].action : 'No recent activity'}</p>
                        </div>
                    </div>

                    <div style={{marginTop: '2rem'}}>
                        <h3 style={{fontSize: '1.1rem'}}>Photos</h3>
                        <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', margin: '1rem 0'}}>
                            {/* Placeholder for photos */}
                            <div style={{width: '80px', height: '80px', background: '#eee', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                                👤
                            </div>
                            <div style={{width: '80px', height: '80px', background: '#eee', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                                👤
                            </div>
                        </div>
                        <button className="btn btn-secondary">
                            📷 Update / Add Photos
                        </button>
                    </div>
                </div>

                {/* QR Code Card */}
                <div className="card" style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                    <h3 style={{marginTop: 0}}>QR Access Code</h3>
                    
                    <div style={{margin: '1.5rem 0', padding: '1rem', background: 'white', border: '1px solid #eee'}}>
                        <img 
                            src={worker.qr_code_url} 
                            alt="Worker QR Code" 
                            style={{display: 'block', maxWidth: '100%', width: '150px', height: '150px'}}
                        />
                    </div>

                    <div style={{width: '100%'}}>
                        <label style={{display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-light)'}}>
                            Expires On
                        </label>
                        <div style={{display: 'flex', gap: '0.5rem'}}>
                            <input 
                                type="date" 
                                className="form-control"
                                value={newExpiryDate}
                                onChange={(e) => setNewExpiryDate(e.target.value)}
                            />
                            <button className="btn btn-primary" onClick={handleUpdateExpiry}>
                                Save
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Recent Logs Section */}
            <div style={{marginTop: '2rem'}}>
                <h3>Recent Activity</h3>
                <div className="card">
                    {logs.length === 0 ? (
                        <p style={{color: 'var(--text-light)', padding: '1rem'}}>No recent logs found.</p>
                    ) : (
                        <table style={{width: '100%', borderCollapse: 'collapse'}}>
                            <thead>
                                <tr style={{textAlign: 'left', borderBottom: '1px solid var(--secondary-color)'}}>
                                    <th style={{padding: '0.75rem'}}>Time</th>
                                    <th style={{padding: '0.75rem'}}>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {logs.map(log => (
                                    <tr key={log.id} style={{borderBottom: '1px solid #eee'}}>
                                        <td style={{padding: '0.75rem'}}>{log.timestamp}</td>
                                        <td style={{padding: '0.75rem'}}>{log.action}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            </div>
        </div>
    );
}
