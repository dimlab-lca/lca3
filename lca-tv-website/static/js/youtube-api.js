// Enhanced YouTube API integration for LCA TV
// YouTube API configuration
const YOUTUBE_API_KEY = 'AIzaSyC-9RCCz6mRrNWbUBhmrp37l3uXN09vXo0';
const YOUTUBE_CHANNEL_ID = 'UCkquZjmd6ubRQh2W2YpbSLQ'; // LCA TV official channel ID

// Function to load LCA TV videos from the official channel
async function loadLCATVVideos() {
    const container = document.getElementById('replay-videos-list');
    
    try {
        console.log('🎬 Loading LCA TV videos from official channel...');
        
        // Show loading state
        container.innerHTML = `
            <div style="text-align: center; padding: 20px; color: #666;">
                <i class="fas fa-spinner fa-spin" style="font-size: 1.5rem; margin-bottom: 10px;"></i>
                <div>Chargement des vidéos LCA TV...</div>
                <div style="font-size: 0.8rem; margin-top: 5px;">Récupération depuis la chaîne officielle...</div>
            </div>
        `;
        
        // Get the uploads playlist ID
        const channelResponse = await fetch(`https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id=${YOUTUBE_CHANNEL_ID}&key=${YOUTUBE_API_KEY}`);
        const channelData = await channelResponse.json();
        
        if (!channelData.items || channelData.items.length === 0) {
            throw new Error('Channel not found');
        }
        
        const uploadsPlaylistId = channelData.items[0].contentDetails.relatedPlaylists.uploads;
        console.log('📋 Uploads playlist ID:', uploadsPlaylistId);
        
        // Get videos from uploads playlist
        const playlistResponse = await fetch(`https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=${uploadsPlaylistId}&maxResults=20&key=${YOUTUBE_API_KEY}`);
        const playlistData = await playlistResponse.json();
        
        if (!playlistData.items || playlistData.items.length === 0) {
            throw new Error('No videos found');
        }
        
        console.log(`✅ Found ${playlistData.items.length} videos from LCA TV`);
        
        // Filter out private/deleted videos
        const validVideos = playlistData.items.filter(item => {
            const title = item.snippet.title;
            return title !== 'Private video' && 
                   title !== 'Deleted video' && 
                   title !== '' && 
                   title !== 'Untitled';
        });
        
        if (validVideos.length > 0) {
            container.innerHTML = validVideos.slice(0, 15).map(item => {
                const video = item.snippet;
                const videoId = video.resourceId.videoId;
                const title = video.title;
                const publishedAt = new Date(video.publishedAt);
                const thumbnail = video.thumbnails.medium ? 
                                video.thumbnails.medium.url : 
                                video.thumbnails.default.url;
                
                return `
                    <div class="replay-video-item" onclick="playInMainPlayer('${videoId}', '${title.replace(/'/g, "\\'")}')">
                        <div class="replay-video-thumbnail">
                            <img src="${thumbnail}" 
                                 alt="${title}" 
                                 onerror="this.src='https://i.ytimg.com/vi/${videoId}/mqdefault.jpg'">
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 12px;">
                                <i class="fas fa-play"></i>
                            </div>
                        </div>
                        <div class="replay-video-info">
                            <div class="replay-video-title">${title}</div>
                            <div class="replay-video-date">${publishedAt.toLocaleDateString('fr-FR')}</div>
                        </div>
                    </div>
                `;
            }).join('');
            
            console.log('🎯 Successfully loaded LCA TV videos');
        } else {
            throw new Error('No valid videos found');
        }
        
    } catch (error) {
        console.error('❌ Error loading LCA TV videos:', error);
        loadFallbackReplayVideos();
    }
}

// Function to load fallback replay videos
function loadFallbackReplayVideos() {
    const container = document.getElementById('replay-videos-list');
    const fallbackVideos = [
        { id: 'yMmuFmjjrCg', title: 'JCI Ouaga golden - Santé mentale', date: '09/07/2025' },
        { id: 'nwHkDCYeQLI', title: 'Femmes impactantes - BUMO 2025', date: '07/07/2025' },
        { id: 'cKCVs2HeLT4', title: 'Un arbre fruitier par ménage', date: '07/07/2025' },
        { id: '6AHk1Nsem0Y', title: 'Femmes et artisanat au Burkina', date: '07/07/2025' },
        { id: 'oPg3xmEaPTs', title: 'Association Tarwende Sida', date: '04/07/2025' },
        { id: 'eSApphrRKWg', title: 'Jeunes dans le monde hyperconnecté', date: '02/07/2025' },
        { id: 'ixQEmhTbvTI', title: 'Diffusion en direct de LCA TV', date: '09/10/2022' },
        { id: 'zjWu0nZyBCY', title: 'Questions de Femmes - Infidélité', date: '13/05/2025' }
    ];
    
    console.log('📺 Loading fallback LCA TV videos');
    
    container.innerHTML = fallbackVideos.map(video => `
        <div class="replay-video-item" onclick="playInMainPlayer('${video.id}', '${video.title}')">
            <div class="replay-video-thumbnail">
                <img src="https://i.ytimg.com/vi/${video.id}/mqdefault.jpg" alt="${video.title}">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-size: 12px;">
                    <i class="fas fa-play"></i>
                </div>
            </div>
            <div class="replay-video-info">
                <div class="replay-video-title">${video.title}</div>
                <div class="replay-video-date">${video.date}</div>
            </div>
        </div>
    `).join('');
}

// Initialize the video loading when DOM is ready
if (typeof window !== 'undefined') {
    window.loadLCATVVideos = loadLCATVVideos;
    window.loadFallbackReplayVideos = loadFallbackReplayVideos;
}