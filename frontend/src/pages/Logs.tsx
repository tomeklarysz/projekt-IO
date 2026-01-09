import { useEffect, useState } from "react";

type LogsProps = {
    onGoToMenu: () => void;
};

interface Log {
    id: number;
    worker_name: string;
    timestamp: string;
    action: string;
}

export default function Logs({ onGoToMenu }: LogsProps) {
    const [logs, setLogs] = useState<Log[]>([]);

    useEffect(() => {
        fetch('http://localhost:5000/api/logs')
            .then(res => res.json())
            .then(data => setLogs(data))
            .catch(err => console.error("Error fetching logs:", err));
    }, []);

    return (
        <div>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem'}}>
                <h1>Access Logs</h1>
                <button type="button" className="btn btn-secondary" onClick={onGoToMenu}>
                    ← Back to Dashboard
                </button>
            </div>
            
            <div className="card">
                {logs.length === 0 ? (
                    <p style={{color: 'var(--text-light)', textAlign: 'center', padding: '2rem'}}>
                        No logs available to display at this time.
                    </p>
                ) : (
                    <table style={{width: '100%', borderCollapse: 'collapse'}}>
                        <thead>
                            <tr style={{textAlign: 'left', borderBottom: '1px solid var(--secondary-color)'}}>
                                <th style={{padding: '1rem'}}>Time</th>
                                <th style={{padding: '1rem'}}>Worker</th>
                                <th style={{padding: '1rem'}}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {logs.map(log => (
                                <tr key={log.id} style={{borderBottom: '1px solid #eee'}}>
                                    <td style={{padding: '1rem'}}>{log.timestamp}</td>
                                    <td style={{padding: '1rem'}}>{log.worker_name}</td>
                                    <td style={{padding: '1rem'}}>{log.action}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}
