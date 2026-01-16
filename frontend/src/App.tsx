import { useState } from "react";

import AddModal from "./components/AddModal";
import SuccessModal from "./components/SuccessModal";
import Logs from "./pages/Logs";
import Menu from "./pages/Menu";
import Details from "./pages/Details";

type Page = "menu" | "logs" | "details";

export default function App() {
    const [page, setPage] = useState<Page>("menu");
    const [selectedQrHash, setSelectedQrHash] = useState<string | null>(null);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isSuccessModalOpen, setIsSuccessModalOpen] = useState(false);
    const [addedWorkerName, setAddedWorkerName] = useState("");
    const [refreshKey, setRefreshKey] = useState(0);

    function openAddModal() {
        setIsAddModalOpen(true);
    }

    function closeAddModal() {
        setIsAddModalOpen(false);
    }

    function closeSuccessModal() {
        setIsSuccessModalOpen(false);
        setRefreshKey(prev => prev + 1);
    }

    function handleAddWorker(firstName: string, lastName: string) {
        if (!firstName.trim()) {
            return;
        }

        const fullName = `${firstName.trim()} ${lastName.trim()}`.trim();
        setAddedWorkerName(fullName);
        setIsAddModalOpen(false);
        setIsSuccessModalOpen(true);
    }

    function handleGoToDetails(qrHash: string) {
        setSelectedQrHash(qrHash);
        setPage("details");
    }

    return (
        <div className="app-container">
            <header style={{
                background: 'var(--white)', 
                padding: '1rem 2rem', 
                boxShadow: 'var(--shadow)', 
                marginBottom: '3rem', 
                borderBottom: '1px solid var(--secondary-color)'
            }}>
                <div style={{maxWidth: '1200px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                    <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
                        <div style={{width: '32px', height: '32px', background: 'var(--primary-color)', borderRadius: '4px'}}></div>
                        <h2 style={{margin: 0, fontSize: '1.25rem'}}>SecureGate Admin</h2>
                    </div>
                </div>
            </header>
            
            <main className="page-container">
                {page === "menu" ? (
                    <Menu 
                        onGoToLogs={() => setPage("logs")} 
                        onOpenAddWorker={openAddModal} 
                        onGoToDetails={handleGoToDetails}
                        refreshKey={refreshKey}
                    />
                ) : page === "logs" ? (
                    <Logs onGoToMenu={() => setPage("menu")} />
                ) : (
                    <Details 
                        qrHash={selectedQrHash!} 
                        onGoToMenu={() => setPage("menu")} 
                    />
                )}
            </main>

            {isAddModalOpen ? (
                <AddModal onClose={closeAddModal} onAdd={handleAddWorker} />
            ) : null}

            {isSuccessModalOpen ? (
                <SuccessModal workerName={addedWorkerName} onClose={closeSuccessModal} />
            ) : null}
        </div>
    );
}