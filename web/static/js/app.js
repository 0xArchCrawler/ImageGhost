// ImageGhost v3.0 - Premium Web Dashboard JavaScript
// Production-Ready - Supports 50+ Image Batch Processing

// WebSocket connection
const socket = io();

// State management
let currentFiles = {
    scrub: [],
    encrypt: [],
    decrypt: [],
    pipeline: []
};

let stats = {
    totalProcessed: 0,
    activeJobs: 0
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    console.log('[ImageGhost] Initializing dashboard...');
    initializeNavigation();
    initializeUploadZones();
    initializeButtons();
    initializeThemeSelector();
    initializeWebSocket();
    initializeSettings();
    loadJobs();
    updateStats();
    console.log('[ImageGhost] Dashboard ready');
});

// Navigation
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');

            // Remove active from all
            navItems.forEach(nav => nav.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add active to clicked
            this.classList.add('active');
            const targetPane = document.getElementById(`${tabName}-tab`);
            if (targetPane) {
                targetPane.classList.add('active');
            }

            // Load jobs when jobs tab is opened
            if (tabName === 'jobs') {
                loadJobs();
            }
        });
    });
}

// Upload zones with drag & drop
function initializeUploadZones() {
    const zones = ['scrub', 'encrypt', 'decrypt', 'pipeline'];

    zones.forEach(zone => {
        const uploadZone = document.getElementById(`${zone}-upload`);
        const fileInput = document.getElementById(`${zone}-files`);

        if (!uploadZone || !fileInput) return;

        // Click to upload
        uploadZone.addEventListener('click', () => fileInput.click());

        // File selection
        fileInput.addEventListener('change', function() {
            handleFiles(this.files, zone);
        });

        // Drag and drop
        uploadZone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });

        uploadZone.addEventListener('dragleave', function() {
            this.classList.remove('dragover');
        });

        uploadZone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            handleFiles(e.dataTransfer.files, zone);
        });
    });
}

// Handle file selection (supports 50+ images)
function handleFiles(files, zone) {
    const fileArray = Array.from(files);

    if (fileArray.length > 100) {
        addLog('warning', `Selected ${fileArray.length} files. Processing batches over 100 may take longer.`);
    }

    currentFiles[zone] = fileArray;
    displayFileGrid(zone);
    showActionPanel(zone);

    addLog('info', `${fileArray.length} file(s) selected for ${zone}`);
}

// Display files in grid
function displayFileGrid(zone) {
    const grid = document.getElementById(`${zone}-file-grid`);
    if (!grid) return;

    grid.innerHTML = '';

    if (currentFiles[zone].length === 0) {
        return;
    }

    currentFiles[zone].forEach((file, index) => {
        const card = document.createElement('div');
        card.className = 'file-card';
        card.innerHTML = `
            <button class="remove-btn" data-index="${index}">×</button>
            <div class="filename">${file.name}</div>
            <div class="filesize">${formatFileSize(file.size)}</div>
        `;

        const removeBtn = card.querySelector('.remove-btn');
        removeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const idx = parseInt(this.getAttribute('data-index'));
            currentFiles[zone].splice(idx, 1);
            displayFileGrid(zone);

            if (currentFiles[zone].length === 0) {
                hideActionPanel(zone);
            } else {
                updateFileCount(zone);
            }
        });

        grid.appendChild(card);
    });

    updateFileCount(zone);
}

// Show/hide action panel
function showActionPanel(zone) {
    const panel = document.getElementById(`${zone}-actions`);
    if (panel) {
        panel.style.display = 'flex';
    }
}

function hideActionPanel(zone) {
    const panel = document.getElementById(`${zone}-actions`);
    if (panel) {
        panel.style.display = 'none';
    }
}

// Update file count
function updateFileCount(zone) {
    const countElement = document.querySelector(`#${zone}-actions .file-count`);
    if (countElement) {
        const count = currentFiles[zone].length;
        countElement.textContent = `${count} file${count !== 1 ? 's' : ''} selected`;
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
}

// Initialize buttons
function initializeButtons() {
    // Scrub
    const scrubStart = document.getElementById('scrub-start');
    if (scrubStart) {
        scrubStart.addEventListener('click', () => startScrubJob());
    }

    const scrubClear = document.getElementById('scrub-clear');
    if (scrubClear) {
        scrubClear.addEventListener('click', () => clearFiles('scrub'));
    }

    // Encrypt
    const encryptStart = document.getElementById('encrypt-start');
    if (encryptStart) {
        encryptStart.addEventListener('click', () => startEncryptJob());
    }

    const encryptGenerate = document.getElementById('encrypt-generate');
    if (encryptGenerate) {
        encryptGenerate.addEventListener('click', () => {
            const passField = document.getElementById('encrypt-password');
            passField.value = generatePassword(16);
        });
    }

    // Decrypt
    const decryptStart = document.getElementById('decrypt-start');
    if (decryptStart) {
        decryptStart.addEventListener('click', () => startDecryptJob());
    }

    // Pipeline
    const pipelineStart = document.getElementById('pipeline-start');
    if (pipelineStart) {
        pipelineStart.addEventListener('click', () => startPipelineJob());
    }

    const pipelineGenerate = document.getElementById('pipeline-generate');
    if (pipelineGenerate) {
        pipelineGenerate.addEventListener('click', () => {
            const passField = document.getElementById('pipeline-password');
            passField.value = generatePassword(16);
        });
    }

    // Settings
    const saveSettings = document.getElementById('save-settings');
    if (saveSettings) {
        saveSettings.addEventListener('click', () => saveSettings());
    }

    // Clear logs
    const clearLogs = document.getElementById('clear-logs');
    if (clearLogs) {
        clearLogs.addEventListener('click', () => {
            document.getElementById('log-output').innerHTML = '';
        });
    }

    // Quality slider
    const qualitySlider = document.getElementById('quality');
    if (qualitySlider) {
        qualitySlider.addEventListener('input', function() {
            document.getElementById('quality-value').textContent = this.value;
        });
    }
}

// Clear files for a zone
function clearFiles(zone) {
    currentFiles[zone] = [];
    displayFileGrid(zone);
    hideActionPanel(zone);
    addLog('info', `Cleared ${zone} file selection`);
}

// Generate secure password
function generatePassword(length = 16) {
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?';
    let password = '';
    const array = new Uint8Array(length);
    window.crypto.getRandomValues(array);

    for (let i = 0; i < length; i++) {
        password += charset[array[i] % charset.length];
    }

    return password;
}

// Start scrub job
async function startScrubJob() {
    if (currentFiles.scrub.length === 0) {
        addLog('error', 'No files selected');
        return;
    }

    const formData = new FormData();
    currentFiles.scrub.forEach(file => {
        formData.append('files', file);
    });

    try {
        addLog('info', `Starting scrub job with ${currentFiles.scrub.length} files...`);
        const response = await fetch('/api/scrub', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.job_id) {
            addLog('success', `Job started: ${data.job_id}`);
            clearFiles('scrub');
            stats.activeJobs++;
            updateStats();
        } else {
            addLog('error', data.error || 'Failed to start job');
        }
    } catch (error) {
        addLog('error', `Failed to start job: ${error.message}`);
    }
}

// Start encrypt job
async function startEncryptJob() {
    const password = document.getElementById('encrypt-password').value;

    if (currentFiles.encrypt.length === 0) {
        addLog('error', 'No files selected');
        return;
    }

    if (password.length < 12) {
        addLog('error', 'Password must be at least 12 characters');
        return;
    }

    const formData = new FormData();
    currentFiles.encrypt.forEach(file => {
        formData.append('files', file);
    });
    formData.append('password', password);

    try {
        addLog('info', `Starting encryption job with ${currentFiles.encrypt.length} files...`);
        const response = await fetch('/api/encrypt', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.job_id) {
            addLog('success', `Job started: ${data.job_id}`);
            clearFiles('encrypt');
            document.getElementById('encrypt-password').value = '';
            stats.activeJobs++;
            updateStats();
        } else {
            addLog('error', data.error || 'Failed to start job');
        }
    } catch (error) {
        addLog('error', `Failed to start job: ${error.message}`);
    }
}

// Start decrypt job
async function startDecryptJob() {
    const password = document.getElementById('decrypt-password').value;

    if (currentFiles.decrypt.length === 0) {
        addLog('error', 'No files selected');
        return;
    }

    if (!password) {
        addLog('error', 'Password required');
        return;
    }

    const formData = new FormData();
    currentFiles.decrypt.forEach(file => {
        formData.append('files', file);
    });
    formData.append('password', password);

    try {
        addLog('info', `Starting decryption job with ${currentFiles.decrypt.length} files...`);
        const response = await fetch('/api/decrypt', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.job_id) {
            addLog('success', `Job started: ${data.job_id}`);
            clearFiles('decrypt');
            document.getElementById('decrypt-password').value = '';
            stats.activeJobs++;
            updateStats();
        } else {
            addLog('error', data.error || 'Failed to start job');
        }
    } catch (error) {
        addLog('error', `Failed to start job: ${error.message}`);
    }
}

// Start pipeline job
async function startPipelineJob() {
    const password = document.getElementById('pipeline-password').value;
    const shredMethod = document.getElementById('shred-method').value;

    if (currentFiles.pipeline.length === 0) {
        addLog('error', 'No files selected');
        return;
    }

    if (password.length < 12) {
        addLog('error', 'Password must be at least 12 characters');
        return;
    }

    const formData = new FormData();
    currentFiles.pipeline.forEach(file => {
        formData.append('files', file);
    });
    formData.append('password', password);
    formData.append('shred_method', shredMethod);

    try {
        addLog('info', `Starting pipeline job with ${currentFiles.pipeline.length} files...`);
        const response = await fetch('/api/pipeline', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.job_id) {
            addLog('success', `Job started: ${data.job_id}`);
            clearFiles('pipeline');
            document.getElementById('pipeline-password').value = '';
            stats.activeJobs++;
            updateStats();
        } else {
            addLog('error', data.error || 'Failed to start job');
        }
    } catch (error) {
        addLog('error', `Failed to start job: ${error.message}`);
    }
}

// WebSocket handlers
function initializeWebSocket() {
    socket.on('connected', function(data) {
        addLog('success', 'Connected to ImageGhost server');
        document.getElementById('system-status').textContent = 'Connected';
    });

    socket.on('disconnect', function() {
        addLog('warning', 'Disconnected from server');
        document.getElementById('system-status').textContent = 'Disconnected';
    });

    socket.on('log', function(data) {
        addLog(data.level, data.message);
    });

    socket.on('job_update', function(job) {
        updateJobCard(job);
        if (job.status === 'completed') {
            stats.totalProcessed += job.results.success?.length || 0;
            updateStats();
        }
    });
}

// Add log entry
function addLog(level, message) {
    const logOutput = document.getElementById('log-output');
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${level}`;

    const timestamp = new Date().toLocaleTimeString();
    let prefix = '';

    switch(level) {
        case 'info': prefix = '[*]'; break;
        case 'success': prefix = '[+]'; break;
        case 'error': prefix = '[-]'; break;
        case 'warning': prefix = '[!]'; break;
    }

    logEntry.innerHTML = `
        <span class="log-timestamp">${timestamp}</span>
        <span>${prefix} ${message}</span>
    `;

    logOutput.appendChild(logEntry);
    logOutput.scrollTop = logOutput.scrollHeight;
}

// Update stats
function updateStats() {
    document.getElementById('total-processed').textContent = stats.totalProcessed;
    document.getElementById('active-jobs').textContent = stats.activeJobs;
}

// Load jobs
async function loadJobs() {
    try {
        const response = await fetch('/api/jobs');
        const jobs = await response.json();

        const jobsGrid = document.getElementById('jobs-grid');
        const activeTab = document.getElementById('jobs-tab');

        if (!activeTab.classList.contains('active')) return;

        // Count actual active jobs
        const active = jobs.filter(j => j.status === 'running' || j.status === 'pending').length;
        stats.activeJobs = active;
        updateStats();

        if (jobs.length === 0) {
            jobsGrid.innerHTML = `
                <div class="empty-state">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                    <h3>No Active Jobs</h3>
                    <p>Start processing images to see jobs here</p>
                </div>
            `;
            return;
        }

        jobsGrid.innerHTML = '';
        jobs.forEach(job => {
            createJobCard(job);
        });
    } catch (error) {
        addLog('error', `Failed to load jobs: ${error.message}`);
    }
}

// Create job card
function createJobCard(job) {
    const jobsGrid = document.getElementById('jobs-grid');

    let existingCard = document.getElementById(`job-${job.id}`);
    if (existingCard) {
        updateJobCard(job);
        return;
    }

    const jobCard = document.createElement('div');
    jobCard.className = 'job-card';
    jobCard.id = `job-${job.id}`;

    const percentage = job.total > 0 ? Math.round((job.progress / job.total) * 100) : 0;

    jobCard.innerHTML = `
        <div class="job-header">
            <span class="job-id">${job.id}</span>
            <span class="job-status ${job.status}">${job.status}</span>
        </div>
        <div class="job-info">Type: ${job.type} | Progress: ${job.progress}/${job.total}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${percentage}%"></div>
        </div>
        <div class="job-actions">
            ${job.status === 'completed' ? `<button class="btn-secondary" onclick="downloadResults('${job.id}')">Download Results</button>` : ''}
        </div>
    `;

    jobsGrid.appendChild(jobCard);
}

// Update job card
function updateJobCard(job) {
    let jobCard = document.getElementById(`job-${job.id}`);

    if (!jobCard) {
        createJobCard(job);
        return;
    }

    const percentage = job.total > 0 ? Math.round((job.progress / job.total) * 100) : 0;

    const statusElem = jobCard.querySelector('.job-status');
    if (statusElem) {
        statusElem.className = `job-status ${job.status}`;
        statusElem.textContent = job.status;
    }

    const infoElem = jobCard.querySelector('.job-info');
    if (infoElem) {
        infoElem.textContent = `Type: ${job.type} | Progress: ${job.progress}/${job.total}`;
    }

    const progressFill = jobCard.querySelector('.progress-fill');
    if (progressFill) {
        progressFill.style.width = `${percentage}%`;
    }

    const actionsElem = jobCard.querySelector('.job-actions');
    if (actionsElem && job.status === 'completed' && !actionsElem.querySelector('button')) {
        actionsElem.innerHTML = `<button class="btn-secondary" onclick="downloadResults('${job.id}')">Download Results</button>`;
    }
}

// Download results
function downloadResults(jobId) {
    window.location.href = `/api/download/${jobId}`;
    addLog('success', `Downloading results for ${jobId}`);
}

// Theme selector
function initializeThemeSelector() {
    const themeSelect = document.getElementById('theme-select');
    if (!themeSelect) return;

    // Load saved theme
    const savedTheme = localStorage.getItem('imageghost-theme') || 'arch_blue';
    themeSelect.value = savedTheme;
    applyTheme(savedTheme);

    themeSelect.addEventListener('change', function() {
        const theme = this.value;
        applyTheme(theme);
        localStorage.setItem('imageghost-theme', theme);
        addLog('info', `Theme changed to: ${theme}`);
    });
}

// Apply theme
function applyTheme(theme) {
    document.body.className = `theme-${theme}`;
}

// Settings management
function initializeSettings() {
    // Load settings from backend
    fetch('/api/config')
        .then(response => response.json())
        .then(config => {
            if (config.scrubber) {
                const useExiftool = document.getElementById('use-exiftool');
                const stripStego = document.getElementById('strip-stego');
                const reencode = document.getElementById('reencode');
                const quality = document.getElementById('quality');
                const qualityValue = document.getElementById('quality-value');

                if (useExiftool) useExiftool.checked = config.scrubber.use_exiftool;
                if (stripStego) stripStego.checked = config.scrubber.strip_steganography;
                if (reencode) reencode.checked = config.scrubber.reencode_images;
                if (quality) quality.value = config.scrubber.default_output_quality;
                if (qualityValue) qualityValue.textContent = config.scrubber.default_output_quality;
            }

            if (config.crypto) {
                const argonTime = document.getElementById('argon-time');
                const argonMemory = document.getElementById('argon-memory');
                const minPassLength = document.getElementById('min-pass-length');

                if (argonTime) argonTime.value = config.crypto.argon2_time_cost;
                if (argonMemory) argonMemory.value = config.crypto.argon2_memory_cost;
                if (minPassLength) minPassLength.value = config.crypto.min_password_length;
            }

            if (config.performance) {
                const maxThreads = document.getElementById('max-threads');
                if (maxThreads) maxThreads.value = config.performance.max_threads;
            }
        })
        .catch(error => {
            addLog('warning', `Could not load settings: ${error.message}`);
        });
}

// Save settings
async function saveSettings() {
    const settings = {
        scrubber: {
            use_exiftool: document.getElementById('use-exiftool')?.checked || false,
            strip_steganography: document.getElementById('strip-stego')?.checked || false,
            reencode_images: document.getElementById('reencode')?.checked || false,
            default_output_quality: parseInt(document.getElementById('quality')?.value || 95)
        },
        crypto: {
            argon2_time_cost: parseInt(document.getElementById('argon-time')?.value || 4),
            argon2_memory_cost: parseInt(document.getElementById('argon-memory')?.value || 65536),
            min_password_length: parseInt(document.getElementById('min-pass-length')?.value || 12)
        },
        performance: {
            max_threads: parseInt(document.getElementById('max-threads')?.value || 4)
        }
    };

    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });

        const data = await response.json();
        addLog('success', 'Settings saved successfully');
    } catch (error) {
        addLog('error', `Failed to save settings: ${error.message}`);
    }
}

// Refresh jobs every 2 seconds when on jobs tab
setInterval(function() {
    const jobsTab = document.getElementById('jobs-tab');
    if (jobsTab && jobsTab.classList.contains('active')) {
        loadJobs();
    }
}, 2000);

// Console log for debugging
console.log('[ImageGhost] Premium Web Dashboard v3.0');
console.log('[ImageGhost] Arch Linux Blue Theme');
console.log('[ImageGhost] Batch Processing: 50+ images supported');
console.log('[ImageGhost] Privacy-First • Zero Trust • Zero Metadata');
