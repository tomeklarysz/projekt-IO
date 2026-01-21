type ConfirmModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string | null;
  confirmButtonStyle?: React.CSSProperties;
};

export default function ConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = "Delete",
  cancelText = "Cancel",
  confirmButtonStyle = { backgroundColor: '#dc3545', borderColor: '#dc3545' }
}: ConfirmModalProps) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content" style={{ maxWidth: '400px' }}>
        <div className="modal-header">
          <h3 className="modal-title" style={{ color: confirmButtonStyle.backgroundColor === '#dc3545' ? 'var(--danger-color)' : 'var(--text-color)' }}>
            {title}
          </h3>
          <button type="button" className="btn-close" onClick={onClose} aria-label="close">
            ✕
          </button>
        </div>

        <div style={{ padding: '1.5rem', textAlign: 'center' }}>
          <p style={{ fontSize: '1rem', color: 'var(--text-color)', margin: 0 }}>
            {message}
          </p>
        </div>

        <div className="modal-footer" style={{ justifyContent: 'center', gap: '1rem' }}>
          {cancelText && (
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              {cancelText}
            </button>
          )}
          <button
            type="button"
            className="btn btn-primary"
            style={confirmButtonStyle}
            onClick={onConfirm}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
