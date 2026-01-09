
document.addEventListener('DOMContentLoaded', () => {
    // Flash message auto-dismiss
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 3000);
    });
});

// Clipboard Functionality
async function copyToClipboard(text, element) {
    if (!text) return;

    try {
        await navigator.clipboard.writeText(text);
        showToast('Password copied to clipboard!');
        
        // Visual feedback on button
        const originalText = element.innerHTML;
        element.innerHTML = '<i class="fas fa-check"></i> Copied';
        element.classList.add('btn-success');
        
        // Clear clipboard after 10 seconds
        setTimeout(async () => {
            try {
                // Only clear if the current clipboard content is what we wrote
                const currentText = await navigator.clipboard.readText();
                if (currentText === text) {
                    await navigator.clipboard.writeText('');
                    showToast('Clipboard cleared for security.');
                }
            } catch (err) {
                console.log('Clipboard read permission denied or error', err);
            }
            
            // Reset button
            element.innerHTML = originalText;
            element.classList.remove('btn-success');
        }, 10000);

    } catch (err) {
        console.error('Failed to copy:', err);
        showToast('Failed to copy to clipboard', 'error');
    }
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Trigger reflow
    toast.offsetHeight;
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Password Visibility Toggle
function togglePassword(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}
