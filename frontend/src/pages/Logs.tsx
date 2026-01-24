import { useEffect, useState } from "react";

/**
 * Component Props Definition
 * @param onGoToMenu - Callback function to navigate back to the main dashboard
 * @param qrHash - Optional hash to filter logs for a specific employee
 */
type LogsProps = {
    onGoToMenu: () => void;
    qrHash?: string;
};

interface Log {
    first_name: string;
    last_name: string;
    status: boolean;
    event_time: string;
    reason: string;
}

export default function Logs({ onGoToMenu, qrHash }: LogsProps) {
    const [logs, setLogs] = useState<Log[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const url = qrHash
            ? `http://localhost:8000/api/employees/logs/${qrHash}`
            : `http://localhost:8000/api/logs/all`;

        setIsLoading(true);

        fetch(url)
            .then(res => res.json())
            .then(data => {
                setLogs(Array.isArray(data) ? data : []);
                setIsLoading(false);
            })
            .catch(err => {
                console.error("Fetch error:", err);
                setIsLoading(false);
            });
    }, [qrHash]);

    const downloadLogs = () => {
        if (logs.length === 0) return;

        let content = "ACCESS CONTROL ACTIVITY REPORT\n";
        content += `Generated on: ${new Date().toLocaleString()}\n`;
        content += "====================================================\n\n";

        logs.forEach((log, index) => {
            const date = new Date(log.event_time).toLocaleString();
            const status = log.status ? "VERIFIED" : "DENIED";
            
            content += `${index + 1}. [${date}]\n`;
            content += `   Employee: ${log.first_name} ${log.last_name?.toUpperCase()}\n`;
            content += `   Status:   ${status}\n`;
            content += `   Details:  ${log.reason || "No additional information"}\n`;
            content += "----------------------------------------------------\n";
        });

        const blob = new Blob([content], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        
        link.href = url;
        link.download = `Access_Logs_${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(link);
        link.click();
        
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="logs-container">
            {/* Header section with title and navigation buttons */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1><i className="fas fa-history"></i> Access Logs</h1>
                
                <div style={{ display: 'flex', gap: '10px' }}>
                    {/* Download Button */}
                    {!isLoading && logs.length > 0 && (
                        <button 
                            type="button" 
                            className="btn btn-primary" 
                            onClick={downloadLogs}
                            style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
                        >
                            <i className="fas fa-file-download"></i> Download Logs
                        </button>
                    )}

                    <button type="button" className="btn btn-secondary" onClick={onGoToMenu}>
                        ← Back to Dashboard
                    </button>
                </div>
            </div>

            <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
                {/* State-based rendering: Loading vs Empty vs Data Table */}
                {isLoading ? (
                    <p style={{ textAlign: 'center', padding: '2rem' }}>Loading historical records...</p>
                ) : logs.length === 0 ? (
                    <p style={{ color: 'var(--text-light)', textAlign: 'center', padding: '2rem' }}>
                        No activity records found in the database.
                    </p>
                ) : (
                    <div style={{ overflowX: 'auto', maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                            <thead>
                                <tr style={{ textAlign: 'left', background: '#374151', color: 'white', position: 'sticky', top: 0, zIndex: 10 }}>
                                    <th style={{ padding: '1rem' }}>Timestamp</th>
                                    <th style={{ padding: '1rem' }}>Employee</th>
                                    <th style={{ padding: '1rem' }}>Status</th>
                                    <th style={{ padding: '1rem' }}>Reason / Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                {logs.map((log, index) => {
                                    const dateObj = new Date(log.event_time);
                                    const formattedDate = isNaN(dateObj.getTime())
                                        ? "Unknown Date"
                                        : dateObj.toLocaleString();

                                    return (
                                        <tr key={index} style={{ borderBottom: '1px solid #eee' }}>
                                            <td style={{ padding: '1rem', whiteSpace: 'nowrap' }}>
                                                {formattedDate}
                                            </td>
                                            <td style={{ padding: '1rem', fontWeight: 'bold' }}>
                                                {log.first_name} {log.last_name?.toUpperCase()}
                                            </td>
                                            <td style={{ padding: '1rem' }}>
                                                <span style={{
                                                    padding: '4px 12px',
                                                    borderRadius: '20px',
                                                    fontSize: '0.85rem',
                                                    fontWeight: 'bold',
                                                    backgroundColor: log.status ? '#dcfce7' : '#fee2e2',
                                                    color: log.status ? '#166534' : '#991b1b',
                                                    border: `1px solid ${log.status ? '#bbf7d0' : '#fecaca'}`
                                                }}>
                                                    {log.status ? '✓ VERIFIED' : '✗ DENIED'}
                                                </span>
                                            </td>
                                            <td style={{ padding: '1rem', color: '#666', fontSize: '0.9rem' }}>
                                                {log.reason || "No details provided"}
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}