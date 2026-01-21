import { useEffect, useState, useCallback } from "react";
import AddModal from "../components/AddModal";
import ConfirmModal from "../components/ConfirmModal";
import QRModal from "../components/QRModal";

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
    status: boolean;
}

export default function Details({ qrHash, onGoToMenu }: DetailsProps) {
    const [worker, setWorker] = useState<WorkerDetails | null>(null);
    const [logs, setLogs] = useState<Log[]>([]);
    const [newExpiryDate, setNewExpiryDate] = useState("");
    const [editModalOpen, setEditModalOpen] = useState(false);
    const [qrModalOpen, setQrModalOpen] = useState(false);
    const [deleteModalOpen, setDeleteModalOpen] = useState(false);
    const [deleteSuccess, setDeleteSuccess] = useState(false);

    const handleDeleteWorker = async () => {
        try {
            const response = await fetch(`http://localhost:8000/employees/${qrHash}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                setDeleteSuccess(true);
            } else {
                const errText = await response.text();
                alert("Failed to delete worker: " + errText);
            }
        } catch (error) {
            console.error("Error deleting worker:", error);
            alert("Error: " + error);
        }
    };

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
                <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '2rem', padding: '2.5rem' }}>
                    <div style={{ display: 'flex', gap: '2rem' }}>
                        {/* Avatar Column */}
                        <div style={{ flexShrink: 0 }}>
                            {worker.photo_path ? (
                                <img
                                    src={`http://localhost:8000/${worker.photo_path.replace(/\\/g, '/')}`}
                                    alt={`${worker.first_name} ${worker.last_name}`}
                                    style={{
                                        width: '120px',
                                        height: '120px',
                                        objectFit: 'cover',
                                        borderRadius: '50%',
                                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                                    }}
                                />
                            ) : (
                                <div style={{
                                    width: '120px',
                                    height: '120px',
                                    background: '#f3f4f6',
                                    borderRadius: '50%',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '2.5rem',
                                    color: '#9ca3af'
                                }}>
                                    👤
                                </div>
                            )}
                        </div>

                        {/* Info Column */}
                        <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                                <div>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                        <h2 style={{ margin: 0, fontSize: '1.75rem', fontWeight: 600, color: '#111827' }}>
                                            {worker.first_name} {worker.last_name}
                                        </h2>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#374151', fontSize: '0.9rem', fontWeight: 500, background: '#f9fafb', padding: '0.2rem 0.6rem', borderRadius: '20px', border: '1px solid #f3f4f6' }}>
                                            <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: logs.length > 0 ? '#10b981' : '#d1d5db' }}></span>
                                            {worker.status ? 'Active' : 'Inactive'}
                                        </div>
                                    </div>
                                    <p style={{ margin: '0.5rem 0 0.5rem 0', color: '#6b7280', fontSize: '0.95rem' }}>
                                        Employee
                                    </p>
                                    {/* Employee Stats / Info moved up */}
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', marginBottom: '0.5rem' }}>
                                        <div style={{ color: '#6b7280', fontSize: '0.85rem' }}>
                                            ID: {qrHash}
                                        </div>
                                    </div>
                                </div>

                                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                    {/* Action Buttons - Minimal Icon Style */}
                                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                                        <button
                                            className="btn"
                                            onClick={() => setEditModalOpen(true)}
                                            title="Edit Profile"
                                            style={{
                                                padding: '0.5rem',
                                                background: 'transparent',
                                                border: '1px solid #e5e7eb',
                                                color: '#4b5563',
                                                borderRadius: '6px'
                                            }}
                                            onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#9ca3af'; e.currentTarget.style.color = '#1f2937'; }}
                                            onMouseLeave={(e) => { e.currentTarget.style.borderColor = '#e5e7eb'; e.currentTarget.style.color = '#4b5563'; }}
                                        >
                                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                                        </button>
                                        <button
                                            className="btn"
                                            onClick={() => setDeleteModalOpen(true)}
                                            title="Delete Profile"
                                            style={{
                                                padding: '0.5rem',
                                                background: 'transparent',
                                                border: '1px solid #fee2e2',
                                                color: '#ef4444',
                                                borderRadius: '6px'
                                            }}
                                            onMouseEnter={(e) => { e.currentTarget.style.borderColor = '#fca5a5'; e.currentTarget.style.backgroundColor = '#fef2f2'; }}
                                            onMouseLeave={(e) => { e.currentTarget.style.borderColor = '#fee2e2'; e.currentTarget.style.backgroundColor = 'transparent'; }}
                                        >
                                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Recent Activity Table (Full Width) */}
                    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', borderTop: '1px solid #f3f4f6', paddingTop: '1.5rem' }}>
                        <h3 style={{ fontSize: '0.9rem', textTransform: 'uppercase', color: '#9ca3af', marginBottom: '1rem', letterSpacing: '0.05em' }}>Recent Activity</h3>
                        <div style={{ flex: 1, overflow: 'auto', maxHeight: '300px' }}>
                            {logs.length === 0 ? (
                                <p style={{ color: '#9ca3af', fontStyle: 'italic', fontSize: '0.9rem' }}>No recent logs found.</p>
                            ) : (
                                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                                    <tbody>
                                        {logs.map(log => (
                                            <tr key={log.id} style={{ borderBottom: '1px solid #f9fafb' }}>
                                                <td style={{ padding: '0.5rem 0', color: '#6b7280', width: '40%' }}>{log.timestamp}</td>
                                                <td style={{ padding: '0.5rem 0', color: '#111827', fontWeight: 500 }}>{log.action}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            )}
                        </div>
                    </div>
                </div>

                {/* QR Code Card */}
                <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <h3 style={{ marginTop: 0 }}>QR Access Code</h3>

                    <div
                        style={{
                            width: '100%',
                            aspectRatio: '1',
                            margin: '1.5rem 0 1rem 0',
                            padding: '1rem',
                            background: 'white',
                            border: '1px solid #e5e7eb',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                            transition: 'all 0.2s ease-in-out'
                        }}
                        onClick={() => setQrModalOpen(true)}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.borderColor = 'var(--primary-color)';
                            e.currentTarget.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.borderColor = '#e5e7eb';
                            e.currentTarget.style.boxShadow = 'none';
                        }}
                    >
                        {/* We use .replace to ensure backslashes from Windows paths are converted to forward slashes if present */}
                        <img
                            src={`http://localhost:8000/${worker.qr_path?.replace(/\\/g, '/')}`}
                            alt="Worker QR Code"
                            style={{ display: 'block', maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                        />
                    </div>

                    <button
                        className="btn btn-secondary"
                        onClick={() => setQrModalOpen(true)}
                        style={{ width: '100%', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                    >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="11" cy="11" r="8" />
                            <line x1="21" y1="21" x2="16.65" y2="16.65" />
                        </svg>
                        View Options
                    </button>

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

            <QRModal
                isOpen={qrModalOpen}
                onClose={() => setQrModalOpen(false)}
                qrUrl={worker.qr_path ? `http://localhost:8000/${worker.qr_path}` : ''}
                workerName={`${worker.first_name} ${worker.last_name}`}
            />

            {deleteModalOpen && (
                <ConfirmModal
                    isOpen={deleteModalOpen}
                    onClose={() => {
                        if (deleteSuccess) onGoToMenu();
                        setDeleteModalOpen(false);
                    }}
                    onConfirm={deleteSuccess ? onGoToMenu : handleDeleteWorker}
                    title={deleteSuccess ? "Success" : "Delete Worker"}
                    message={deleteSuccess
                        ? "Worker has been successfully removed from the system."
                        : `Are you sure you want to remove ${worker.first_name} ${worker.last_name} from the system? This action cannot be undone.`
                    }
                    confirmText={deleteSuccess ? "OK" : "Yes, Remove Worker"}
                    cancelText={deleteSuccess ? null : "Cancel"}
                    confirmButtonStyle={deleteSuccess ? { backgroundColor: 'var(--primary-color)', borderColor: 'var(--primary-color)' } : { backgroundColor: '#dc3545', borderColor: '#dc3545' }}
                />
            )}
        </div>
    );
}
