pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js';
let pdfDoc = null;
let currentPage = 1;
let scale = 1.0;
let currentUsername = '';

async function startAnalysis() {
    const username = document.getElementById('username').value.trim();
    const loader = document.getElementById('loader');
    const error = document.getElementById('error');
    
    if (!username) {
        error.textContent = 'Please enter a username';
        return;
    }

    currentUsername = username;
    loader.style.display = 'block';
    error.textContent = '';
    document.getElementById('reportSection').style.display = 'none';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}`
        });

        const result = await response.json();
        
        if (result.status === 'processing') {
            checkReportStatus(username);
        } else {
            error.textContent = result.message;
            loader.style.display = 'none';
        }
    } catch (err) {
        error.textContent = 'Error connecting to server';
        loader.style.display = 'none';
    }
}

function checkReportStatus(username) {
    const checkInterval = setInterval(async () => {
        try {
            const response = await fetch(`/report/${username}`);
            if (response.status === 200) {
                clearInterval(checkInterval);
                showPreview(username);
            }
        } catch (err) {
            console.error('Error checking report status:', err);
        }
    }, 3000);
}

async function showPreview(username) {
    const container = document.getElementById('pdf-viewer');
    container.innerHTML = '';
    document.getElementById('loader').style.display = 'none';
    document.getElementById('reportSection').style.display = 'block';

    // Add cache-buster to URL
    const url = `/preview/${username}?t=${Date.now()}`;
    
    try {
        // Load PDF document using PDF.js
        pdfDoc = await pdfjsLib.getDocument(url).promise;
        
        // Update page count
        document.getElementById('page-count').textContent = pdfDoc.numPages;
        
        // Load first page
        renderPage(currentPage);
    } catch (error) {
        console.error('Error loading PDF:', error);
        document.getElementById('error').textContent = 'Failed to load report preview';
    }
}

async function renderPage(num) {
    const container = document.getElementById('pdf-viewer');
    container.innerHTML = '<div class="loading-text">Loading page...</div>';
    
    try {
        const page = await pdfDoc.getPage(num);
        const viewport = page.getViewport({ scale: scale });
        
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        
        await page.render({
            canvasContext: context,
            viewport: viewport
        }).promise;
        
        container.innerHTML = '';
        container.appendChild(canvas);
        document.getElementById('page-num').textContent = currentPage;
        document.getElementById('pdf-fallback').style.display = 'none';
    } catch (error) {
        console.error('Error rendering page:', error);
        container.innerHTML = '';
        document.getElementById('pdf-fallback').style.display = 'block';
    }
}

function changePage(offset) {
    const newPage = currentPage + offset;
    if (newPage > 0 && newPage <= pdfDoc.numPages) {
        currentPage = newPage;
        renderPage(currentPage);
    }
}

function downloadReport() {
    if (currentUsername) {
        window.open(`/report/${currentUsername}`, '_blank');
    }
}