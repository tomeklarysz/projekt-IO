import { useEffect, useState, useCallback } from "react";
import AddModal from "../components/AddModal";

type DetailsProps = {
    qrHash: string;
    onGoToMenu: () => void;
};

interface Log {
    id: number;
    timestamp: string;
    action: string;
}

interface WorkerDetails {
    first_name: string;
    last_name: string; // Made required as per AddModal expectation
    photo_path?: string;
    qr_expiration_date?: string;
    qr_path?: string;
}

export default function Details({ qrHash, onGoToMenu }: DetailsProps) {
    const [worker, setWorker] = useState<WorkerDetails | null>(null);
    const [logs, setLogs] = useState<Log[]>([]);
    const [newExpiryDate, setNewExpiryDate] = useState("");
    const [editModalOpen, setEditModalOpen] = useState(false);

    const fetchWorkerDetails = useCallback(() => {
        fetch(`http://localhost:8000/employees/${qrHash}`)
            .then(res => res.json())
            .then(data => {
                setWorker(data);
                if (data.qr_expiration_date) {
                    setNewExpiryDate(data.qr_expiration_date);
                }
            })
            .catch(err => {
                console.error("Error fetching worker details:", err);
            });
    }, [qrHash]);

    useEffect(() => {
        fetchWorkerDetails();
        // (Optional) Fetch logs for this worker if endpoint exists
        // fetch(`http://localhost:8000/api/workers/${qrHash}/logs`) ...
    }, [fetchWorkerDetails]);

    const handleUpdateExpiry = () => {
        if (!worker) return;

        fetch(`http://localhost:8000/employees/expiry`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ qr_hash: qrHash, new_expiry_date: newExpiryDate })
        })
            .then(async (res) => {
                if (res.ok) {
                    alert("Expiration date updated!");
                } else {
                    const txt = await res.text();
                    alert("Error: " + txt);
                }
            })
            .catch(err => console.error("Error updating expiry:", err));
    };

    if (!worker) {
        return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading worker details...</div>;
    }

    return (
        <div>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2rem' }}>
                <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={onGoToMenu}
                    style={{ marginRight: '1rem' }}
                >
                    ← Back
                </button>
                <h1 style={{ margin: 0 }}>Worker Details</h1>
            </div>

            <div className="dashboard-grid" style={{ gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
                {/* Main Info Card */}
                <div className="card">
                    <h2 style={{ marginTop: 0, borderBottom: '1px solid #eee', paddingBottom: '1rem', marginBottom: '1.5rem' }}>
                        {worker.first_name} {worker.last_name}
                    </h2>

                    <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1rem' }}>
                        <div>
                            <p style={{ color: 'var(--text-light)', marginBottom: '0.25rem' }}>Worker ID</p>
                            <p style={{ fontSize: '0.9rem', fontWeight: 500, wordBreak: 'break-all' }}>{qrHash}</p>
                        </div>
                        <div>
                            <p style={{ color: 'var(--text-light)', marginBottom: '0.25rem' }}>Latest Action</p>
                            <p>{logs.length > 0 && logs[0] ? logs[0].action : 'No recent activity'}</p>
                        </div>
                    </div>

                    <div style={{ marginTop: '2rem' }}>
                        <h3 style={{ fontSize: '1.1rem' }}>Worker Photo</h3>
                        <div style={{ margin: '1rem 0' }}>
                            {worker.photo_path ? (
                                <img
                                    src={`http://localhost:8000/${worker.photo_path.replace(/\\/g, '/')}`}
                                    alt={`${worker.first_name} ${worker.last_name}`}
                                    style={{
                                        width: '150px',
                                        height: '150px',
                                        objectFit: 'cover',
                                        borderRadius: '8px',
                                        border: '1px solid #eee'
                                    }}
                                />
                            ) : (
                                <div style={{ width: '150px', height: '150px', background: '#eee', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                    👤 No Photo
                                </div>
                            )}
                        </div>
                        <button
                            className="btn btn-secondary"
                            onClick={() => setEditModalOpen(true)}
                        >
                            ✏️ Edit Worker Details
                        </button>
                    </div>
                </div>

                {/* QR Code Card */}
                <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <h3 style={{ marginTop: 0 }}>QR Access Code</h3>

                    <div style={{ margin: '1.5rem 0', padding: '1rem', background: 'white', border: '1px solid #eee' }}>
                        {/* We use .replace to ensure backslashes from Windows paths are converted to forward slashes if present */}
                        <img
                            src={`http://localhost:8000/${worker.qr_path?.replace(/\\/g, '/')}`}
                            alt="Worker QR Code"
                            style={{ display: 'block', maxWidth: '100%', width: '250px', height: '250px' }}
                        />
                    </div>

                    <div style={{ width: '100%' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-light)' }}>
                            Expires On
                        </label>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
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
            <div style={{ marginTop: '2rem' }}>
                <h3>Recent Activity</h3>
                <div className="card">
                    {logs.length === 0 ? (
                        <p style={{ color: 'var(--text-light)', padding: '1rem' }}>No recent logs found.</p>
                    ) : (
                        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                            <thead>
                                <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--secondary-color)' }}>
                                    <th style={{ padding: '0.75rem' }}>Time</th>
                                    <th style={{ padding: '0.75rem' }}>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {logs.map(log => (
                                    <tr key={log.id} style={{ borderBottom: '1px solid #eee' }}>
                                        <td style={{ padding: '0.75rem' }}>{log.timestamp}</td>
                                        <td style={{ padding: '0.75rem' }}>{log.action}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            </div>

            {editModalOpen && (
                <AddModal
                    onClose={() => setEditModalOpen(false)}
                    onSuccess={() => {
                        fetchWorkerDetails();
                    }}
                    initialData={{
                        firstName: worker.first_name,
                        lastName: worker.last_name || "",
                        qrHash: qrHash
                    }}
                />
            )}
        </div>
    );
}
