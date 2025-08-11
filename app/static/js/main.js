/**
 * YouTube Transcriber Frontend JavaScript
 */

class YouTubeTranscriber {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentTranscript = null;
    }

    initializeElements() {
        // Form elements
        this.form = document.getElementById('transcript-form');
        this.urlInput = document.getElementById('youtube-url');
        this.extractBtn = document.getElementById('extract-btn');
        this.btnText = this.extractBtn.querySelector('.btn-text');
        this.spinner = this.extractBtn.querySelector('.spinner');

        // Section elements
        this.loadingSection = document.getElementById('loading-section');
        this.errorSection = document.getElementById('error-section');
        this.resultsSection = document.getElementById('results-section');

        // Result elements
        this.videoTitle = document.getElementById('video-title');
        this.videoDuration = document.getElementById('video-duration');
        this.extractionTime = document.getElementById('extraction-time');
        this.chaptersSection = document.getElementById('chapters-section');
        this.chaptersList = document.getElementById('chapters-list');
        this.transcriptText = document.getElementById('transcript-text');

        // Action buttons
        this.copyBtn = document.getElementById('copy-btn');
        this.downloadBtn = document.getElementById('download-btn');
        this.retryBtn = document.getElementById('retry-btn');

        // Error elements
        this.errorMessage = document.getElementById('error-message');

        // Toast
        this.toast = document.getElementById('toast');
        this.toastMessage = document.getElementById('toast-message');
    }

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.copyBtn.addEventListener('click', () => this.copyTranscript());
        this.downloadBtn.addEventListener('click', () => this.downloadTranscript());
        this.retryBtn.addEventListener('click', () => this.retryExtraction());

        // URL input validation
        this.urlInput.addEventListener('input', () => this.validateUrl());
    }

    validateUrl() {
        const url = this.urlInput.value.trim();
        const isValid = this.isValidYouTubeUrl(url);
        
        if (url && !isValid) {
            this.urlInput.setCustomValidity('Please enter a valid YouTube URL');
        } else {
            this.urlInput.setCustomValidity('');
        }
    }

    isValidYouTubeUrl(url) {
        const patterns = [
            /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/|youtube\.com\/live\/)[\w-]+/,
            /^[\w-]{11}$/ // Direct video ID
        ];
        
        return patterns.some(pattern => pattern.test(url));
    }

    async handleSubmit(event) {
        event.preventDefault();
        
        const url = this.urlInput.value.trim();
        if (!url) return;

        this.showLoading();
        
        try {
            const response = await this.fetchTranscript(url);
            this.showResults(response);
            this.showToast('Transcript extracted successfully!', 'success');
        } catch (error) {
            this.showError(error.message);
            this.showToast('Failed to extract transcript', 'error');
        }
    }

    async fetchTranscript(url) {
        const response = await fetch('/api/transcript', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    }

    showLoading() {
        this.hideAllSections();
        this.loadingSection.classList.remove('hidden');
        this.setButtonLoading(true);
    }

    showError(message) {
        this.hideAllSections();
        this.errorMessage.textContent = message;
        this.errorSection.classList.remove('hidden');
        this.setButtonLoading(false);
    }

    showResults(data) {
        this.hideAllSections();
        this.currentTranscript = data;
        
        // Update video info
        this.videoTitle.textContent = data.title || 'Untitled Video';
        this.videoDuration.textContent = this.formatDuration(data.duration);
        this.extractionTime.textContent = `Extracted ${this.formatDate(data.extracted_at)}`;
        
        // Update transcript
        this.transcriptText.textContent = data.transcript;
        
        // Update chapters
        if (data.chapters && data.chapters.length > 0) {
            this.renderChapters(data.chapters);
            this.chaptersSection.classList.remove('hidden');
        } else {
            this.chaptersSection.classList.add('hidden');
        }
        
        this.resultsSection.classList.remove('hidden');
        this.setButtonLoading(false);
    }

    renderChapters(chapters) {
        this.chaptersList.innerHTML = '';
        
        chapters.forEach((chapter, index) => {
            const chapterElement = document.createElement('div');
            chapterElement.className = 'chapter-item';
            chapterElement.innerHTML = `
                <div class="chapter-timestamp">${chapter.timestamp}</div>
                <div class="chapter-title">${this.escapeHtml(chapter.title)}</div>
            `;
            
            // Add click handler to scroll to chapter in transcript
            chapterElement.addEventListener('click', () => {
                this.scrollToChapter(chapter);
            });
            
            this.chaptersList.appendChild(chapterElement);
        });
    }

    scrollToChapter(chapter) {
        // This is a simplified implementation
        // In a more advanced version, you could highlight specific parts of the transcript
        this.transcriptText.scrollIntoView({ behavior: 'smooth' });
        this.showToast(`Jumped to: ${chapter.title}`, 'success');
    }

    hideAllSections() {
        this.loadingSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        this.resultsSection.classList.add('hidden');
    }

    setButtonLoading(isLoading) {
        if (isLoading) {
            this.extractBtn.disabled = true;
            this.btnText.textContent = 'Extracting...';
            this.spinner.classList.remove('hidden');
        } else {
            this.extractBtn.disabled = false;
            this.btnText.textContent = 'Extract Transcript';
            this.spinner.classList.add('hidden');
        }
    }

    async copyTranscript() {
        if (!this.currentTranscript) return;
        
        try {
            await navigator.clipboard.writeText(this.currentTranscript.transcript);
            this.showToast('Transcript copied to clipboard!', 'success');
        } catch (error) {
            // Fallback for older browsers
            this.fallbackCopyTextToClipboard(this.currentTranscript.transcript);
        }
    }

    fallbackCopyTextToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.top = '0';
        textArea.style.left = '0';
        textArea.style.position = 'fixed';
        
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            this.showToast('Transcript copied to clipboard!', 'success');
        } catch (error) {
            this.showToast('Failed to copy transcript', 'error');
        }
        
        document.body.removeChild(textArea);
    }

    downloadTranscript() {
        if (!this.currentTranscript) return;
        
        const content = this.formatTranscriptForDownload();
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = this.generateFilename();
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        window.URL.revokeObjectURL(url);
        this.showToast('Transcript downloaded!', 'success');
    }

    formatTranscriptForDownload() {
        const data = this.currentTranscript;
        let content = '';
        
        content += `Title: ${data.title || 'Untitled Video'}\n`;
        content += `Video ID: ${data.video_id || 'Unknown'}\n`;
        content += `Duration: ${this.formatDuration(data.duration)}\n`;
        content += `Extracted: ${this.formatDate(data.extracted_at)}\n`;
        content += `URL: https://www.youtube.com/watch?v=${data.video_id || 'unknown'}\n\n`;
        
        if (data.chapters && data.chapters.length > 0) {
            content += 'CHAPTERS:\n';
            content += '=========\n';
            data.chapters.forEach(chapter => {
                content += `${chapter.timestamp} - ${chapter.title}\n`;
            });
            content += '\n';
        }
        
        content += 'TRANSCRIPT:\n';
        content += '===========\n';
        content += data.transcript;
        
        return content;
    }

    generateFilename() {
        const data = this.currentTranscript;
        
        // Handle cases where title might be undefined, null, or empty
        let title = 'Untitled Video';
        if (data && data.title && typeof data.title === 'string' && data.title.trim()) {
            title = data.title.trim()
                // Replace filesystem-unsafe characters with dashes
                .replace(/[<>:"/\\|?*]/g, '-')
                // Remove control characters (ASCII 0-31 and 127)
                .replace(/[\x00-\x1F\x7F]/g, '')
                // Replace multiple consecutive dashes/spaces with single dash
                .replace(/[-\s]+/g, ' ')
                // Trim any leading/trailing dashes or spaces
                .trim()
                .replace(/^-+|-+$/g, '');
        }
        
        // Fallback if title becomes empty after cleaning
        if (!title) {
            title = 'Untitled Video';
        }
        
        // Return clean filename with transcript suffix
        return `${title} - Transcript.txt`;
    }

    retryExtraction() {
        if (this.urlInput.value.trim()) {
            this.handleSubmit(new Event('submit'));
        }
    }

    showToast(message, type = 'info') {
        this.toastMessage.textContent = message;
        this.toast.className = `toast ${type} show`;
        
        setTimeout(() => {
            this.toast.classList.remove('show');
        }, 3000);
    }

    formatDuration(seconds) {
        if (!seconds) return '00:00';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, (m) => map[m]);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new YouTubeTranscriber();
});

// Add some utility functions for debugging
window.debugTranscriber = {
    testAPI: async () => {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            console.log('API Health:', data);
        } catch (error) {
            console.error('API Error:', error);
        }
    }
};