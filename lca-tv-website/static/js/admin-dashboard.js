/**
 * LCA TV Admin Dashboard JavaScript
 * Complete functionality for backend management
 */

// Global variables
let currentSection = 'overview';
let selectedMedia = [];
let currentUser = null;
let currentSubscription = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    setupTabNavigation();
    loadOverviewData();
    setupEventListeners();
    setupModals();
}

// Tab Navigation
function setupTabNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    const contentSections = document.querySelectorAll('.content-section');
    
    navTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all tabs and sections
            navTabs.forEach(t => t.classList.remove('active'));
            contentSections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Show corresponding section
            const targetSection = this.getAttribute('data-tab') + '-section';
            const section = document.getElementById(targetSection);
            if (section) {
                section.classList.add('active');
                currentSection = this.getAttribute('data-tab');
                
                // Load section data
                loadSectionData(currentSection);
            }
        });
    });
}

function loadSectionData(section) {
    switch(section) {
        case 'overview':
            loadOverviewData();
            break;
        case 'users':
            loadUsers();
            break;
        case 'publicity':
            loadPublicityData();
            break;
        case 'videos':
            loadVideos();
            break;
        case 'articles':
            loadArticles();
            break;
        case 'media':
            loadMedia();
            break;
        case 'settings':
            loadSettings();
            break;
        case 'analytics':
            loadAnalytics();
            break;
    }
}

// Overview Section
function loadOverviewData() {
    fetch('/api/admin/overview')
        .then(response => response.json())
        .then(data => {
            updateOverviewStats(data);
            loadRecentActivity();
        })
        .catch(error => {
            console.error('Error loading overview:', error);
            showNotification('Erreur lors du chargement des statistiques', 'error');
        });
}

function updateOverviewStats(data) {
    document.getElementById('total-users').textContent = data.total_users || 0;
    document.getElementById('total-videos').textContent = data.total_videos || 0;
    document.getElementById('total-ads').textContent = data.total_ads || 0;
    document.getElementById('total-articles').textContent = data.total_articles || 0;
}

function loadRecentActivity() {
    fetch('/api/admin/recent-activity')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('recent-activity');
            container.innerHTML = data.map(activity => `
                <div class="activity-item">
                    <i class="fas fa-${activity.icon}"></i>
                    <span>${activity.description}</span>
                    <small>${activity.time}</small>
                </div>
            `).join('');
        })
        .catch(error => console.error('Error loading recent activity:', error));
}

// User Management
function loadUsers() {
    const tbody = document.querySelector('#users-table tbody');
    tbody.innerHTML = '<tr><td colspan="7" class="loading"><i class="fas fa-spinner fa-spin"></i> Chargement...</td></tr>';
    
    fetch('/api/admin/users')
        .then(response => response.json())
        .then(users => {
            tbody.innerHTML = users.map(user => `
                <tr>
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td><span class="status-badge status-${user.role}">${user.role}</span></td>
                    <td>${user.full_name || '-'}</td>
                    <td>${user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Jamais'}</td>
                    <td><span class="status-badge status-${user.is_active ? 'active' : 'inactive'}">${user.is_active ? 'Actif' : 'Inactif'}</span></td>
                    <td>
                        <button class="action-btn edit" onclick="editUser(${user.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="deleteUser(${user.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading users:', error);
            tbody.innerHTML = '<tr><td colspan="7">Erreur de chargement</td></tr>';
        });
}

function openUserModal(userId = null) {
    currentUser = userId;
    const modal = document.getElementById('user-modal');
    const form = document.getElementById('user-form');
    const title = document.getElementById('user-modal-title');
    
    if (userId) {
        title.textContent = 'Modifier Utilisateur';
        // Load user data
        fetch(`/api/admin/users/${userId}`)
            .then(response => response.json())
            .then(user => {
                document.getElementById('user-username').value = user.username;
                document.getElementById('user-email').value = user.email;
                document.getElementById('user-role').value = user.role;
                document.getElementById('user-fullname').value = user.full_name || '';
                document.getElementById('user-phone').value = user.phone || '';
                document.getElementById('user-active').checked = user.is_active;
                document.getElementById('user-password').required = false;
            })
            .catch(error => console.error('Error loading user:', error));
    } else {
        title.textContent = 'Nouvel Utilisateur';
        form.reset();
        document.getElementById('user-password').required = true;
    }
    
    modal.classList.add('show');
}

function saveUser(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    data.is_active = formData.has('is_active');
    
    const url = currentUser ? `/api/admin/users/${currentUser}` : '/api/admin/users';
    const method = currentUser ? 'PUT' : 'POST';
    
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            closeModal('user-modal');
            loadUsers();
            showNotification('Utilisateur sauvegardé avec succès', 'success');
        } else {
            showNotification(result.error || 'Erreur lors de la sauvegarde', 'error');
        }
    })
    .catch(error => {
        console.error('Error saving user:', error);
        showNotification('Erreur lors de la sauvegarde', 'error');
    });
}

function editUser(userId) {
    openUserModal(userId);
}

function deleteUser(userId) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
        fetch(`/api/admin/users/${userId}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadUsers();
                    showNotification('Utilisateur supprimé avec succès', 'success');
                } else {
                    showNotification('Erreur lors de la suppression', 'error');
                }
            })
            .catch(error => {
                console.error('Error deleting user:', error);
                showNotification('Erreur lors de la suppression', 'error');
            });
    }
}

// Publicity Management
function loadPublicityData() {
    setupPublicityTabs();
    loadSubscriptions();
}

function setupPublicityTabs() {
    const tabBtns = document.querySelectorAll('.publicity-tabs .tab-btn');
    const tabContents = document.querySelectorAll('#publicity-section .tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            this.classList.add('active');
            const target = document.getElementById(this.getAttribute('data-target') + '-tab');
            if (target) {
                target.classList.add('active');
                
                switch(this.getAttribute('data-target')) {
                    case 'subscriptions':
                        loadSubscriptions();
                        break;
                    case 'advertisements':
                        loadAdvertisements();
                        break;
                    case 'packages':
                        loadPackages();
                        break;
                }
            }
        });
    });
}

function loadSubscriptions() {
    const tbody = document.querySelector('#subscriptions-table tbody');
    tbody.innerHTML = '<tr><td colspan="8" class="loading"><i class="fas fa-spinner fa-spin"></i> Chargement...</td></tr>';
    
    fetch('/api/admin/subscriptions')
        .then(response => response.json())
        .then(subscriptions => {
            tbody.innerHTML = subscriptions.map(sub => `
                <tr>
                    <td>${sub.client_name}</td>
                    <td>${sub.package_type}</td>
                    <td>${sub.duration_months} mois</td>
                    <td>${sub.price.toLocaleString()} FCFA</td>
                    <td>${new Date(sub.start_date).toLocaleDateString()}</td>
                    <td>${new Date(sub.end_date).toLocaleDateString()}</td>
                    <td><span class="status-badge status-${sub.status}">${sub.status}</span></td>
                    <td>
                        <button class="action-btn view" onclick="viewSubscription(${sub.id})">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn edit" onclick="editSubscription(${sub.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading subscriptions:', error);
            tbody.innerHTML = '<tr><td colspan="8">Erreur de chargement</td></tr>';
        });
}

function loadAdvertisements() {
    const tbody = document.querySelector('#advertisements-table tbody');
    tbody.innerHTML = '<tr><td colspan="9" class="loading"><i class="fas fa-spinner fa-spin"></i> Chargement...</td></tr>';
    
    fetch('/api/admin/advertisements')
        .then(response => response.json())
        .then(ads => {
            tbody.innerHTML = ads.map(ad => `
                <tr>
                    <td>${ad.title}</td>
                    <td>${ad.client_name || '-'}</td>
                    <td>${ad.position}</td>
                    <td>${new Date(ad.start_date).toLocaleDateString()}</td>
                    <td>${new Date(ad.end_date).toLocaleDateString()}</td>
                    <td>${ad.impressions || 0}</td>
                    <td>${ad.clicks || 0}</td>
                    <td><span class="status-badge status-${ad.status}">${ad.status}</span></td>
                    <td>
                        <button class="action-btn view" onclick="viewAdvertisement(${ad.id})">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn edit" onclick="editAdvertisement(${ad.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading advertisements:', error);
            tbody.innerHTML = '<tr><td colspan="9">Erreur de chargement</td></tr>';
        });
}

function loadPackages() {
    const container = document.getElementById('packages-grid');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Chargement...</div>';
    
    fetch('/api/admin/packages')
        .then(response => response.json())
        .then(packages => {
            container.innerHTML = packages.map(pkg => `
                <div class="package-card">
                    <h4>${pkg.name}</h4>
                    <div class="package-price">${pkg.price_monthly.toLocaleString()} FCFA/mois</div>
                    <p>${pkg.description}</p>
                    <ul class="package-features">
                        ${pkg.features.map(feature => `<li>${feature}</li>`).join('')}
                    </ul>
                    <div class="package-actions">
                        <button class="action-btn edit" onclick="editPackage(${pkg.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading packages:', error);
            container.innerHTML = '<div>Erreur de chargement</div>';
        });
}

function openSubscriptionModal() {
    const modal = document.getElementById('subscription-modal');
    
    // Load packages for selection
    fetch('/api/admin/packages')
        .then(response => response.json())
        .then(packages => {
            const container = document.getElementById('packages-selection');
            container.innerHTML = packages.map(pkg => `
                <div class="package-option" onclick="selectPackage(${pkg.id}, ${pkg.price_monthly})">
                    <input type="radio" name="package_id" value="${pkg.id}">
                    <div class="package-name">${pkg.name}</div>
                    <div class="package-price">${pkg.price_monthly.toLocaleString()} FCFA/mois</div>
                    <div class="package-features">${pkg.features.slice(0, 2).join(', ')}</div>
                </div>
            `).join('');
        });
    
    // Set default start date to today
    document.getElementById('start-date').value = new Date().toISOString().split('T')[0];
    
    modal.classList.add('show');
}

function selectPackage(packageId, monthlyPrice) {
    // Update selected package
    document.querySelectorAll('.package-option').forEach(opt => opt.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
    
    // Update radio button
    document.querySelector(`input[value="${packageId}"]`).checked = true;
    
    // Update price display
    document.getElementById('monthly-price').textContent = monthlyPrice.toLocaleString() + ' FCFA';
    
    calculateTotal();
}

function calculateTotal() {
    const monthlyPrice = parseInt(document.getElementById('monthly-price').textContent.replace(/[^\d]/g, '')) || 0;
    const duration = parseInt(document.getElementById('duration-months').value) || 1;
    
    // Calculate discount
    let discount = 0;
    if (duration >= 12) discount = 0.15;
    else if (duration >= 6) discount = 0.10;
    else if (duration >= 3) discount = 0.05;
    
    const subtotal = monthlyPrice * duration;
    const discountAmount = subtotal * discount;
    const total = subtotal - discountAmount;
    
    document.getElementById('duration-display').textContent = duration + ' mois';
    document.getElementById('discount-amount').textContent = discountAmount.toLocaleString() + ' FCFA';
    document.getElementById('total-price').textContent = total.toLocaleString() + ' FCFA';
}

function saveSubscription(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Get selected package
    const selectedPackage = document.querySelector('input[name="package_id"]:checked');
    if (!selectedPackage) {
        showNotification('Veuillez sélectionner un package', 'error');
        return;
    }
    data.package_id = selectedPackage.value;
    
    fetch('/api/admin/subscriptions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            closeModal('subscription-modal');
            loadSubscriptions();
            showNotification('Souscription créée avec succès', 'success');
        } else {
            showNotification(result.error || 'Erreur lors de la création', 'error');
        }
    })
    .catch(error => {
        console.error('Error saving subscription:', error);
        showNotification('Erreur lors de la sauvegarde', 'error');
    });
}

// Video Management
function loadVideos() {
    const container = document.getElementById('videos-grid');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Chargement...</div>';
    
    fetch('/api/admin/videos')
        .then(response => response.json())
        .then(videos => {
            container.innerHTML = videos.map(video => `
                <div class="video-card">
                    <div class="video-thumbnail">
                        <img src="${video.thumbnail_url || '/static/images/default-video.jpg'}" alt="${video.title}">
                        <div class="video-overlay">
                            <button class="action-btn view" onclick="viewVideo('${video.youtube_id || video.id}')">
                                <i class="fas fa-play"></i>
                            </button>
                        </div>
                    </div>
                    <div class="video-info">
                        <h4>${video.title}</h4>
                        <p class="video-category">${video.category}</p>
                        <div class="video-meta">
                            <span><i class="fas fa-eye"></i> ${video.view_count || 0}</span>
                            <span><i class="fas fa-calendar"></i> ${new Date(video.created_at).toLocaleDateString()}</span>
                        </div>
                        <div class="video-actions">
                            <button class="action-btn edit" onclick="editVideo(${video.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="action-btn delete" onclick="deleteVideo(${video.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading videos:', error);
            container.innerHTML = '<div>Erreur de chargement</div>';
        });
}

function openVideoModal() {
    const modal = document.getElementById('video-modal');
    modal.classList.add('show');
    
    // Set default published date
    document.getElementById('published-date').value = new Date().toISOString().slice(0, 16);
}

function switchVideoSource(source) {
    // Update tabs
    document.querySelectorAll('.source-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelector(`[data-source="${source}"]`).classList.add('active');
    
    // Update content
    document.querySelectorAll('.source-content').forEach(content => content.classList.remove('active'));
    document.getElementById(`${source}-source`).classList.add('active');
}

function fetchYouTubeInfo() {
    const url = document.getElementById('youtube-url').value;
    if (!url) return;
    
    // Extract video ID from URL
    const videoId = extractYouTubeVideoId(url);
    if (!videoId) {
        showNotification('URL YouTube invalide', 'error');
        return;
    }
    
    // Mock YouTube API call (implement with real API)
    const mockData = {
        title: 'Titre de la vidéo YouTube',
        description: 'Description de la vidéo...',
        thumbnail: `https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`,
        duration: '15:30'
    };
    
    // Update form
    document.getElementById('video-title').value = mockData.title;
    document.getElementById('video-description').value = mockData.description;
    
    // Show preview
    const preview = document.getElementById('youtube-preview');
    document.getElementById('preview-thumbnail').src = mockData.thumbnail;
    document.getElementById('preview-title').textContent = mockData.title;
    document.getElementById('preview-description').textContent = mockData.description;
    document.getElementById('preview-duration').textContent = mockData.duration;
    preview.style.display = 'flex';
}

function extractYouTubeVideoId(url) {
    const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

function saveVideo(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    fetch('/api/admin/videos', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            closeModal('video-modal');
            loadVideos();
            showNotification('Vidéo ajoutée avec succès', 'success');
        } else {
            showNotification(result.error || 'Erreur lors de l\'ajout', 'error');
        }
    })
    .catch(error => {
        console.error('Error saving video:', error);
        showNotification('Erreur lors de la sauvegarde', 'error');
    });
}

function syncYouTubeVideos() {
    showNotification('Synchronisation en cours...', 'info');
    
    fetch('/api/admin/youtube/sync', { method: 'POST' })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                loadVideos();
                showNotification('Synchronisation terminée', 'success');
            } else {
                showNotification('Erreur lors de la synchronisation', 'error');
            }
        })
        .catch(error => {
            console.error('Error syncing YouTube:', error);
            showNotification('Erreur lors de la synchronisation', 'error');
        });
}

// Media Management
function loadMedia() {
    const container = document.getElementById('media-grid');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Chargement...</div>';
    
    const fileType = document.getElementById('media-type-filter').value;
    const url = fileType ? `/api/admin/media?file_type=${fileType}` : '/api/admin/media';
    
    fetch(url)
        .then(response => response.json())
        .then(media => {
            container.innerHTML = media.map(file => `
                <div class="media-item" onclick="selectMediaItem(${file.id})" data-id="${file.id}">
                    <div class="media-item-preview">
                        ${file.file_type === 'image' ? 
                            `<img src="${file.url}" alt="${file.original_filename}">` :
                            `<i class="fas fa-${getFileIcon(file.file_type)}"></i>`
                        }
                        <div class="media-item-overlay">
                            <div class="media-item-actions">
                                <button class="media-action-btn" onclick="event.stopPropagation(); viewMediaDetail(${file.id})">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="media-action-btn" onclick="event.stopPropagation(); deleteMediaItem(${file.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="media-item-info">
                        <div class="media-item-name">${file.original_filename}</div>
                        <div class="media-item-meta">${formatFileSize(file.file_size)} • ${file.file_type}</div>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading media:', error);
            container.innerHTML = '<div>Erreur de chargement</div>';
        });
}

function openMediaUpload() {
    const modal = document.getElementById('media-modal');
    modal.classList.add('show');
    
    setupMediaUpload();
}

function setupMediaUpload() {
    const uploadArea = document.getElementById('media-upload-area');
    const fileInput = document.getElementById('media-files');
    
    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        handleFileUpload(files);
    });
    
    // Click to upload
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', function() {
        handleFileUpload(this.files);
    });
}

function handleFileUpload(files) {
    const uploadQueue = document.getElementById('upload-queue');
    const uploadItems = document.getElementById('upload-items');
    
    uploadQueue.style.display = 'block';
    
    Array.from(files).forEach(file => {
        const uploadItem = createUploadItem(file);
        uploadItems.appendChild(uploadItem);
        
        uploadFile(file, uploadItem);
    });
}

function createUploadItem(file) {
    const item = document.createElement('div');
    item.className = 'upload-item';
    item.innerHTML = `
        <div class="upload-item-preview">
            <i class="fas fa-${getFileIcon(file.type)}"></i>
        </div>
        <div class="upload-item-info">
            <div class="upload-item-name">${file.name}</div>
            <div class="upload-item-progress">
                <div class="upload-progress-bar"></div>
            </div>
            <div class="upload-item-status">En cours...</div>
        </div>
    `;
    return item;
}

function uploadFile(file, uploadItem) {
    const formData = new FormData();
    formData.append('files', file);
    
    const xhr = new XMLHttpRequest();
    
    xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            const progressBar = uploadItem.querySelector('.upload-progress-bar');
            progressBar.style.width = percentComplete + '%';
        }
    });
    
    xhr.addEventListener('load', function() {
        const status = uploadItem.querySelector('.upload-item-status');
        if (xhr.status === 200) {
            status.textContent = 'Terminé';
            status.style.color = '#28a745';
            
            // Reload media after upload
            setTimeout(() => {
                loadMedia();
            }, 1000);
        } else {
            status.textContent = 'Erreur';
            status.style.color = '#dc3545';
        }
    });
    
    xhr.open('POST', '/api/admin/media/upload');
    xhr.send(formData);
}

function getFileIcon(fileType) {
    const icons = {
        'image': 'image',
        'video': 'video',
        'audio': 'music',
        'document': 'file-alt',
        'application/pdf': 'file-pdf'
    };
    
    return icons[fileType] || 'file';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function selectMediaItem(mediaId) {
    const item = document.querySelector(`[data-id="${mediaId}"]`);
    
    if (selectedMedia.includes(mediaId)) {
        selectedMedia = selectedMedia.filter(id => id !== mediaId);
        item.classList.remove('selected');
    } else {
        selectedMedia.push(mediaId);
        item.classList.add('selected');
    }
    
    updateSelectedCount();
}

function updateSelectedCount() {
    document.getElementById('selected-count').textContent = `${selectedMedia.length} fichier(s) sélectionné(s)`;
    
    const deleteBtn = document.getElementById('delete-btn');
    const insertBtn = document.getElementById('insert-btn');
    
    deleteBtn.disabled = selectedMedia.length === 0;
    insertBtn.disabled = selectedMedia.length === 0;
}

// Settings Management
function loadSettings() {
    // Settings are already loaded in the template
    // This function can be used to reload if needed
}

function saveSettings() {
    const forms = ['general-settings', 'contact-settings', 'youtube-settings', 'system-settings'];
    const allSettings = {};
    
    forms.forEach(formId => {
        const form = document.getElementById(formId);
        if (form) {
            const formData = new FormData(form);
            for (let [key, value] of formData.entries()) {
                if (form.querySelector(`[name="${key}"]`).type === 'checkbox') {
                    allSettings[key] = formData.has(key) ? 'true' : 'false';
                } else {
                    allSettings[key] = value;
                }
            }
        }
    });
    
    fetch('/api/admin/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(allSettings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Paramètres sauvegardés avec succès', 'success');
        } else {
            showNotification('Erreur lors de la sauvegarde', 'error');
        }
    })
    .catch(error => {
        console.error('Error saving settings:', error);
        showNotification('Erreur lors de la sauvegarde', 'error');
    });
}

// Modal Management
function setupModals() {
    // Close modal when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });
    
    // Close modal on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                closeModal(openModal.id);
            }
        }
    });
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
        
        // Reset forms
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
        }
        
        // Reset global variables
        if (modalId === 'user-modal') {
            currentUser = null;
        } else if (modalId === 'subscription-modal') {
            currentSubscription = null;
        }
    }
}

// Utility Functions
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'times' : 'info'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#d4edda' : type === 'error' ? '#f8d7da' : '#d1ecf1'};
        color: ${type === 'success' ? '#155724' : type === 'error' ? '#721c24' : '#0c5460'};
        border: 1px solid ${type === 'success' ? '#c3e6cb' : type === 'error' ? '#f5c6cb' : '#bee5eb'};
        border-radius: 6px;
        padding: 15px 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 10000;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

function setupEventListeners() {
    // Add any additional event listeners here
    
    // Duration change for subscription modal
    const durationSelect = document.getElementById('duration-months');
    if (durationSelect) {
        durationSelect.addEventListener('change', calculateTotal);
    }
    
    // Media type filter
    const mediaTypeFilter = document.getElementById('media-type-filter');
    if (mediaTypeFilter) {
        mediaTypeFilter.addEventListener('change', loadMedia);
    }
}

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification button {
        background: none;
        border: none;
        color: inherit;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    }
`;
document.head.appendChild(notificationStyles);