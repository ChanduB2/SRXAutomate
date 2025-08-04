/**
 * SRX Automation Web Interface JavaScript
 * Handles all frontend interactions and API communications
 */

// Global variables
let currentConnection = null;
let configurationInProgress = false;
let loadingProgressInterval = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('SRX Automation Interface Loaded');
    initializeInterface();
    updateMockModeVisibility();
});

/**
 * Initialize the interface with event listeners and default state
 */
function initializeInterface() {
    // Mock mode toggle handler
    const mockModeSelect = document.getElementById('mockMode');
    if (mockModeSelect) {
        mockModeSelect.addEventListener('change', updateMockModeVisibility);
    }
    
    // Auto-check connection when device IP changes
    const deviceIPInput = document.getElementById('deviceIP');
    if (deviceIPInput) {
        let debounceTimer;
        deviceIPInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                if (this.value && this.value.length > 7) {
                    checkConnection();
                }
            }, 1000);
        });
    }
    
    // Form validation
    setupFormValidation();
    
    // Load initial status
    setTimeout(() => {
        checkConnection();
        loadConfigurationHistory();
    }, 500);
}

/**
 * Update interface based on mock mode selection
 */
function updateMockModeVisibility() {
    const mockMode = document.getElementById('mockMode').value === 'true';
    const credentialsRow = document.getElementById('credentialsRow');
    
    if (mockMode) {
        credentialsRow.style.opacity = '0.5';
        credentialsRow.querySelectorAll('input').forEach(input => {
            input.disabled = true;
        });
        
        // Update status to show mock mode
        updateConnectionStatus('Mock mode enabled - simulated device ready', 'info');
    } else {
        credentialsRow.style.opacity = '1';
        credentialsRow.querySelectorAll('input').forEach(input => {
            input.disabled = false;
        });
        
        updateConnectionStatus('Real device mode - please test connection', 'warning');
    }
}

/**
 * Test connection to SRX device
 */
async function checkConnection() {
    if (configurationInProgress) {
        showNotification('Configuration in progress, please wait...', 'warning');
        return;
    }
    
    const deviceIP = document.getElementById('deviceIP').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const mockMode = document.getElementById('mockMode').value;
    
    if (!deviceIP) {
        showNotification('Please enter device IP address', 'warning');
        return;
    }
    
    updateConnectionStatus('Testing connection...', 'info');
    
    try {
        const response = await fetch(`/api/status?device_ip=${encodeURIComponent(deviceIP)}&username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&mock_mode=${mockMode}`);
        const data = await response.json();
        
        if (data.connected) {
            updateConnectionStatus('Connected successfully', 'success');
            updateDeviceInfo(data.device_info);
            currentConnection = data;
        } else {
            updateConnectionStatus(`Connection failed: ${data.error}`, 'danger');
            updateDeviceInfo(null);
            currentConnection = null;
        }
    } catch (error) {
        console.error('Connection test error:', error);
        updateConnectionStatus(`Connection error: ${error.message}`, 'danger');
        updateDeviceInfo(null);
        currentConnection = null;
    }
}

/**
 * Update connection status display
 */
function updateConnectionStatus(message, type) {
    const statusElement = document.getElementById('connectionStatus');
    
    // Remove existing alert classes
    statusElement.className = 'alert';
    
    // Add new alert class
    statusElement.classList.add(`alert-${type}`);
    
    // Update content with appropriate icon
    let icon = 'fas fa-circle-notch fa-spin';
    switch (type) {
        case 'success':
            icon = 'fas fa-check-circle';
            break;
        case 'danger':
            icon = 'fas fa-exclamation-triangle';
            break;
        case 'warning':
            icon = 'fas fa-exclamation-circle';
            break;
        case 'info':
            icon = 'fas fa-info-circle';
            break;
    }
    
    statusElement.innerHTML = `<i class="${icon} me-2"></i>${message}`;
    statusElement.classList.add('fade-in');
}

/**
 * Update device information panel
 */
function updateDeviceInfo(deviceInfo) {
    const deviceInfoElement = document.getElementById('deviceInfo');
    
    if (!deviceInfo) {
        deviceInfoElement.innerHTML = '<p class="text-muted">No device information available</p>';
        return;
    }
    
    const infoHTML = `
        <div class="device-info">
            <h6><i class="fas fa-server me-2"></i>Device Information</h6>
            <div class="info-item">
                <span>Hostname:</span>
                <span>${deviceInfo.hostname || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span>Model:</span>
                <span>${deviceInfo.model || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span>Version:</span>
                <span>${deviceInfo.version || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span>Serial:</span>
                <span>${deviceInfo.serial || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <span>Uptime:</span>
                <span>${deviceInfo.uptime || 'Unknown'}</span>
            </div>
        </div>
    `;
    
    deviceInfoElement.innerHTML = infoHTML;
    deviceInfoElement.classList.add('slide-in');
}

/**
 * Apply configuration to SRX device
 */
async function applyConfiguration() {
    if (configurationInProgress) {
        showNotification('Configuration already in progress', 'warning');
        return;
    }
    
    if (!validateConfigurationForm()) {
        return;
    }
    
    configurationInProgress = true;
    showLoadingOverlay('Applying configuration...');
    
    const configData = {
        device_ip: document.getElementById('deviceIP').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        mock_mode: document.getElementById('mockMode').value === 'true',
        interface_name: document.getElementById('interfaceName').value,
        interface_ip: document.getElementById('interfaceIP').value,
        security_zone: document.getElementById('securityZone').value
    };
    
    try {
        // Simulate progress steps
        const steps = [
            'Connecting to device...',
            'Creating configuration backup...',
            'Loading interface configuration...',
            'Configuring IP address...',
            'Assigning security zone...',
            'Creating security policies...',
            'Validating configuration...',
            'Committing changes...'
        ];
        
        let currentStep = 0;
        const progressInterval = setInterval(() => {
            if (currentStep < steps.length) {
                updateLoadingMessage(steps[currentStep]);
                updateLoadingProgress(((currentStep + 1) / steps.length) * 90); // 90% for steps
                currentStep++;
            }
        }, 1000);
        
        const response = await fetch('/api/configure', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(configData)
        });
        
        clearInterval(progressInterval);
        updateLoadingProgress(100);
        
        const result = await response.json();
        
        setTimeout(() => {
            hideLoadingOverlay();
            displayConfigurationResults(result);
            configurationInProgress = false;
            
            if (result.success) {
                showNotification('Configuration applied successfully!', 'success');
                loadConfigurationHistory(); // Refresh history
            } else {
                showNotification(`Configuration failed: ${result.message}`, 'danger');
            }
        }, 1000);
        
    } catch (error) {
        console.error('Configuration error:', error);
        hideLoadingOverlay();
        configurationInProgress = false;
        showNotification(`Configuration error: ${error.message}`, 'danger');
        
        displayConfigurationResults({
            success: false,
            message: `Network error: ${error.message}`,
            details: {}
        });
    }
}

/**
 * Validate configuration form
 */
function validateConfigurationForm() {
    const deviceIP = document.getElementById('deviceIP').value;
    const interfaceName = document.getElementById('interfaceName').value;
    const interfaceIP = document.getElementById('interfaceIP').value;
    
    if (!deviceIP) {
        showNotification('Please enter device IP address', 'warning');
        document.getElementById('deviceIP').focus();
        return false;
    }
    
    if (!interfaceName) {
        showNotification('Please enter interface name', 'warning');
        document.getElementById('interfaceName').focus();
        return false;
    }
    
    if (!interfaceIP) {
        showNotification('Please enter interface IP address', 'warning');
        document.getElementById('interfaceIP').focus();
        return false;
    }
    
    // Validate IP address format (basic check)
    const ipRegex = /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;
    if (!ipRegex.test(interfaceIP)) {
        showNotification('Please enter IP address in CIDR format (e.g., 192.168.10.1/24)', 'warning');
        document.getElementById('interfaceIP').focus();
        return false;
    }
    
    return true;
}

/**
 * Display configuration results
 */
function displayConfigurationResults(result) {
    const resultsPanel = document.getElementById('resultsPanel');
    const resultsContent = document.getElementById('resultsContent');
    
    let resultHTML = '';
    
    if (result.success) {
        resultHTML = `
            <div class="alert alert-success">
                <h5><i class="fas fa-check-circle me-2"></i>Configuration Applied Successfully</h5>
                <p>${result.message}</p>
            </div>
            
            <div class="config-results">
                <h6><i class="fas fa-cog me-2"></i>Configuration Details</h6>
                <div class="row">
                    <div class="col-md-6">
                        <strong>Interface:</strong> ${result.details.interface}<br>
                        <strong>IP Address:</strong> ${result.details.ip_address}<br>
                        <strong>Security Zone:</strong> ${result.details.security_zone}<br>
                        <strong>Timestamp:</strong> ${new Date(result.details.timestamp).toLocaleString()}
                    </div>
                </div>
            </div>
        `;
        
        // Add applied commands if available
        if (result.details.simulated_commands) {
            resultHTML += `
                <div class="mt-3">
                    <h6><i class="fas fa-terminal me-2"></i>Applied Commands</h6>
                    <div class="code-block">
            `;
            
            result.details.simulated_commands.forEach(cmd => {
                resultHTML += `<div class="config-command config-success">${cmd}</div>`;
            });
            
            resultHTML += '</div></div>';
        }
        
    } else {
        resultHTML = `
            <div class="alert alert-danger">
                <h5><i class="fas fa-exclamation-triangle me-2"></i>Configuration Failed</h5>
                <p>${result.message}</p>
            </div>
        `;
        
        if (result.details && result.details.completed_steps) {
            resultHTML += `
                <div class="config-results">
                    <h6><i class="fas fa-list me-2"></i>Completed Steps</h6>
                    <ul class="list-group">
            `;
            
            result.details.completed_steps.forEach(step => {
                resultHTML += `<li class="list-group-item"><i class="fas fa-check text-success me-2"></i>${step}</li>`;
            });
            
            if (result.details.failed_step) {
                resultHTML += `<li class="list-group-item list-group-item-danger"><i class="fas fa-times text-danger me-2"></i>${result.details.failed_step} (FAILED)</li>`;
            }
            
            resultHTML += '</ul></div>';
        }
    }
    
    resultsContent.innerHTML = resultHTML;
    resultsPanel.style.display = 'block';
    resultsPanel.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Create configuration backup
 */
async function createBackup() {
    if (configurationInProgress) {
        showNotification('Configuration in progress, please wait...', 'warning');
        return;
    }
    
    showLoadingOverlay('Creating configuration backup...');
    
    const backupData = {
        device_ip: document.getElementById('deviceIP').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        mock_mode: document.getElementById('mockMode').value === 'true'
    };
    
    try {
        const response = await fetch('/api/backup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(backupData)
        });
        
        const result = await response.json();
        
        hideLoadingOverlay();
        
        if (result.success) {
            showNotification('Configuration backup created successfully!', 'success');
            
            // Show backup details
            const backupInfo = `
                Backup created at: ${new Date(result.backup.timestamp).toLocaleString()}
                Device: ${result.backup.device_ip}
                Mode: ${result.backup.mock_mode ? 'Mock' : 'Real Device'}
            `;
            
            alert(`Backup Success!\n\n${backupInfo}`);
        } else {
            showNotification(`Backup failed: ${result.message}`, 'danger');
        }
    } catch (error) {
        console.error('Backup error:', error);
        hideLoadingOverlay();
        showNotification(`Backup error: ${error.message}`, 'danger');
    }
}

/**
 * Validate configuration (dry run)
 */
async function validateConfig() {
    if (!validateConfigurationForm()) {
        return;
    }
    
    showNotification('Configuration validation is a premium feature. In mock mode, validation is always successful.', 'info');
    
    setTimeout(() => {
        if (document.getElementById('mockMode').value === 'true') {
            showNotification('Mock configuration validation: PASSED', 'success');
        } else {
            showNotification('Real device validation requires connection to device', 'warning');
        }
    }, 2000);
}

/**
 * Show network topology
 */
function showTopology() {
    const topologyModal = new bootstrap.Modal(document.getElementById('topologyModal'));
    topologyModal.show();
}

/**
 * Show configuration history
 */
async function showHistory() {
    const historyModal = new bootstrap.Modal(document.getElementById('historyModal'));
    historyModal.show();
    
    // Load history will be called automatically
    loadConfigurationHistory();
}

/**
 * Load configuration history
 */
async function loadConfigurationHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        const historyContent = document.getElementById('historyContent');
        
        if (data.history && data.history.length > 0) {
            let historyHTML = '<div class="history-timeline">';
            
            data.history.reverse().forEach(entry => {
                const statusClass = entry.result && entry.result.success ? 'success' : 'error';
                const statusIcon = entry.result && entry.result.success ? 'fas fa-check-circle text-success' : 'fas fa-times-circle text-danger';
                
                historyHTML += `
                    <div class="history-item ${statusClass}">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="mb-1">
                                <i class="${statusIcon} me-2"></i>
                                ${entry.interface_name} Configuration
                            </h6>
                            <small class="text-muted">${new Date(entry.timestamp).toLocaleString()}</small>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <small>
                                    <strong>Device:</strong> ${entry.device_ip}<br>
                                    <strong>IP:</strong> ${entry.interface_ip}<br>
                                    <strong>Zone:</strong> ${entry.security_zone}
                                </small>
                            </div>
                            <div class="col-md-6">
                                <small>
                                    <strong>Mode:</strong> ${entry.mock_mode ? 'Mock' : 'Real Device'}<br>
                                    <strong>Status:</strong> ${entry.result ? (entry.result.success ? 'Success' : 'Failed') : 'Unknown'}
                                </small>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            historyHTML += '</div>';
            historyContent.innerHTML = historyHTML;
        } else {
            historyContent.innerHTML = '<p class="text-muted text-center">No configuration history available</p>';
        }
    } catch (error) {
        console.error('History loading error:', error);
        const historyContent = document.getElementById('historyContent');
        historyContent.innerHTML = '<div class="alert alert-danger">Failed to load configuration history</div>';
    }
}

/**
 * Show logs (placeholder)
 */
function showLogs() {
    showNotification('Log viewing feature coming soon. Check browser console for current logs.', 'info');
    console.log('SRX Automation Logs:');
    console.log('Current connection:', currentConnection);
    console.log('Configuration in progress:', configurationInProgress);
}

/**
 * Setup form validation
 */
function setupFormValidation() {
    // Add real-time validation feedback
    const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
        
        input.addEventListener('input', function() {
            // Clear previous validation state
            this.classList.remove('is-valid', 'is-invalid');
        });
    });
}

/**
 * Validate individual input
 */
function validateInput(input) {
    const value = input.value.trim();
    
    if (input.hasAttribute('required') && !value) {
        input.classList.add('is-invalid');
        return false;
    }
    
    // IP address validation
    if (input.id === 'interfaceIP' && value) {
        const ipRegex = /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;
        if (!ipRegex.test(value)) {
            input.classList.add('is-invalid');
            return false;
        }
    }
    
    input.classList.add('is-valid');
    return true;
}

/**
 * Show loading overlay
 */
function showLoadingOverlay(message = 'Processing...') {
    const overlay = document.getElementById('loadingOverlay');
    const messageElement = document.getElementById('loadingMessage');
    const progressBar = document.getElementById('loadingProgress');
    
    messageElement.textContent = message;
    progressBar.style.width = '0%';
    overlay.style.display = 'flex';
    
    // Start progress animation
    updateLoadingProgress(10);
}

/**
 * Update loading message
 */
function updateLoadingMessage(message) {
    const messageElement = document.getElementById('loadingMessage');
    if (messageElement) {
        messageElement.textContent = message;
    }
}

/**
 * Update loading progress
 */
function updateLoadingProgress(percentage) {
    const progressBar = document.getElementById('loadingProgress');
    if (progressBar) {
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
    }
}

/**
 * Hide loading overlay
 */
function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'none';
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info', duration = 5000) {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">
                    <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
                    ${getNotificationTitle(type)}
                </strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: duration
    });
    
    bsToast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

/**
 * Get notification icon based on type
 */
function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Get notification title based on type
 */
function getNotificationTitle(type) {
    const titles = {
        success: 'Success',
        danger: 'Error',
        warning: 'Warning',
        info: 'Information'
    };
    return titles[type] || 'Notification';
}

/**
 * Utility function to format timestamps
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

/**
 * Utility function to copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success', 2000);
    } catch (err) {
        console.error('Failed to copy to clipboard:', err);
        showNotification('Failed to copy to clipboard', 'danger');
    }
}

// Export functions for global access
window.checkConnection = checkConnection;
window.applyConfiguration = applyConfiguration;
window.createBackup = createBackup;
window.validateConfig = validateConfig;
window.showTopology = showTopology;
window.showHistory = showHistory;
window.showLogs = showLogs;
