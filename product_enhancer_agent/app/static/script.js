document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadSection = document.getElementById('upload-section');
    const previewSection = document.getElementById('preview-section');
    const originalImage = document.getElementById('original-image');
    const enhancedImage = document.getElementById('enhanced-image');
    const loader = document.getElementById('loader');
    const resultDetails = document.getElementById('result-details');
    const generatedTitle = document.getElementById('generated-title');
    const copyBtn = document.getElementById('copy-btn');
    const resetBtn = document.getElementById('reset-btn');

    // Drag & Drop handlers
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    async function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }

        // Show preview UI
        const reader = new FileReader();
        reader.onload = (e) => {
            originalImage.src = e.target.result;
            // Clear previous results
            enhancedImage.src = '';
            enhancedImage.style.display = 'none'; // Hide broken image icon
            uploadSection.classList.add('hidden');
            previewSection.classList.remove('hidden');
            loader.style.display = 'flex';
            resultDetails.classList.add('hidden');
        };
        reader.readAsDataURL(file);

        // Send to API
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Processing failed');
            }

            const data = await response.json();

            // Update UI with results
            enhancedImage.src = `data:image/png;base64,${data.enhanced_image}`;
            enhancedImage.style.display = 'block';
            generatedTitle.textContent = data.title;

            loader.style.display = 'none';
            resultDetails.classList.remove('hidden');

        } catch (error) {
            console.error(error);
            alert('An error occurred while processing the image. Please check your API keys and try again.');
            resetUI();
        }
    }

    // Copy Title
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(generatedTitle.textContent);
        const originalIcon = copyBtn.innerHTML;
        copyBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
        setTimeout(() => {
            copyBtn.innerHTML = originalIcon;
        }, 2000);
    });

    // Reset
    resetBtn.addEventListener('click', resetUI);

    function resetUI() {
        fileInput.value = '';
        previewSection.classList.add('hidden');
        uploadSection.classList.remove('hidden');
        loader.style.display = 'flex';
        resultDetails.classList.add('hidden');
    }
});
