
import React from 'react';

type QRModalProps = {
    isOpen: boolean;
    onClose: () => void;
    qrUrl: string;
    workerName: string;
};

const DownloadIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="7 10 12 15 17 10" />
        <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
);

const PrintIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="6 9 6 2 18 2 18 9" />
        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2" />
        <rect x="6" y="14" width="12" height="8" />
    </svg>
);

const CopyIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>
);

const ShareIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="18" cy="5" r="3" />
        <circle cx="6" cy="12" r="3" />
        <circle cx="18" cy="19" r="3" />
        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
    </svg>
);

const CloseIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
);

const QRModal = ({ isOpen, onClose, qrUrl, workerName }: QRModalProps) => {
    if (!isOpen) return null;

    const handleDownload = async () => {
        try {
            const response = await fetch(qrUrl);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `qr_${workerName.replace(/\s+/g, '_')}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Download failed:', error);
            alert('Failed to download image');
        }
    };

    const handlePrint = () => {
        const printWindow = window.open('', '_blank');
        if (printWindow) {
            printWindow.document.write(`
                <html>
                    <head>
                        <title>Print QR Code - ${workerName}</title>
                        <style>
                            body {
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                alignItems: center;
                                height: 100vh;
                                margin: 0;
                                font-family: 'Segoe UI', sans-serif;
                            }
                            img {
                                max-width: 60%;
                                height: auto;
                                margin-bottom: 2rem;
                            }
                            h1 {
                                font-size: 24px;
                                margin-bottom: 10px;
                                color: #333;
                            }
                            p {
                                color: #666;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>${workerName}</h1>
                        <p>QR Access Code</p>
                        <img src="${qrUrl}" onload="window.print();window.close()" />
                    </body>
                </html>
            `);
            printWindow.document.close();
        }
    };

    const handleCopy = async () => {
        try {
            const response = await fetch(qrUrl);
            const blob = await response.blob();
            await navigator.clipboard.write([
                new ClipboardItem({
                    [blob.type]: blob
                })
            ]);
            alert('QR Code copied to clipboard!');
        } catch (error) {
            console.error('Copy failed:', error);
            alert('Failed to copy image to clipboard');
        }
    };

    const handleShare = async () => {
        try {
            const response = await fetch(qrUrl);
            const blob = await response.blob();
            const file = new File([blob], `qr_${workerName.replace(/\s+/g, '_')}.png`, { type: blob.type });

            if (navigator.canShare && navigator.canShare({ files: [file] })) {
                await navigator.share({
                    title: `QR Code for ${workerName}`,
                    text: `QR access code for ${workerName}`,
                    files: [file]
                });
            } else {
                const subject = `QR Code for ${workerName}`;
                window.location.href = `mailto:?subject=${encodeURIComponent(subject)}`;
            }
        } catch (error) {
            console.error('Share failed:', error);
            const subject = `QR Code for ${workerName}`;
             window.location.href = `mailto:?subject=${encodeURIComponent(subject)}`;
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxWidth: '440px', padding: 0, overflow: 'hidden' }}>
                <div style={{ 
                    padding: '1.25rem 1.5rem', 
                    borderBottom: '1px solid #f0f0f0', 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    background: '#f8fafc'
                }}>
                    <h3 style={{ margin: 0, fontSize: '1.1rem', color: '#1e293b' }}>QR Code Access</h3>
                    <button 
                        onClick={onClose}
                        style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#64748b', padding: '4px', display: 'flex' }}
                        title="Close"
                    >
                        <CloseIcon />
                    </button>
                </div>

                <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <div style={{ 
                        margin: '0 0 2rem 0', 
                        padding: '1.5rem', 
                        background: 'white', 
                        border: '1px solid #e2e8f0', 
                        borderRadius: '12px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)'
                    }}>
                        <img 
                            src={qrUrl} 
                            alt={`QR code for ${workerName}`}
                            style={{ width: '200px', height: '200px', display: 'block' }} 
                        />
                    </div>
                    
                    <h4 style={{ margin: '0 0 1.5rem 0', color: '#334155', fontWeight: 500 }}>{workerName}</h4>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', width: '100%' }}>
                        <button className="btn btn-secondary" onClick={handleDownload} style={{ display: 'flex', gap: '8px', alignItems: 'center', justifyContent: 'center', padding: '0.6rem' }}>
                            <DownloadIcon /> Download
                        </button>
                        <button className="btn btn-secondary" onClick={handlePrint} style={{ display: 'flex', gap: '8px', alignItems: 'center', justifyContent: 'center', padding: '0.6rem' }}>
                            <PrintIcon /> Print
                        </button>
                        <button className="btn btn-secondary" onClick={handleCopy} style={{ display: 'flex', gap: '8px', alignItems: 'center', justifyContent: 'center', padding: '0.6rem' }}>
                            <CopyIcon /> Copy
                        </button>
                        <button className="btn btn-secondary" onClick={handleShare} style={{ display: 'flex', gap: '8px', alignItems: 'center', justifyContent: 'center', padding: '0.6rem' }}>
                            <ShareIcon /> Share
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QRModal;
