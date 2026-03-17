document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const btnGenerate = document.getElementById('btn-generate');
    const btnKeyword = document.getElementById('btn-keyword');
    const btnSummarize = document.getElementById('btn-summarize');
    const btnCopy = document.getElementById('btn-copy');
    const btnRefreshHistory = document.getElementById('btn-refresh-history');
    
    const uiLoading = document.getElementById('loading-spinner');
    const uiResult = document.getElementById('result-container');
    const uiError = document.getElementById('error-container');
    const resultText = document.getElementById('result-text');
    const errorMessage = document.getElementById('error-message');
    const historyBody = document.getElementById('history-body');

    // Load history on start
    fetchHistory();

    // Event Listeners
    btnGenerate.addEventListener('click', () => handleGeneration('/generate-content'));
    btnKeyword.addEventListener('click', () => handleGeneration('/keyword-content'));
    btnSummarize.addEventListener('click', handleSummarization);
    btnRefreshHistory.addEventListener('click', fetchHistory);

    btnCopy.addEventListener('click', () => {
        resultText.select();
        document.execCommand('copy');
        document.getElementById('copy-feedback').classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('copy-feedback').classList.add('hidden');
        }, 2000);
    });

    function showLoading() {
        uiLoading.classList.remove('hidden');
        uiResult.classList.add('hidden');
        uiError.classList.add('hidden');
    }

    function showResult(text) {
        uiLoading.classList.add('hidden');
        uiResult.classList.remove('hidden');
        resultText.value = text;
        fetchHistory(); // Refresh history automatically
    }

    function showError(msg) {
        uiLoading.classList.add('hidden');
        uiError.classList.remove('hidden');
        errorMessage.textContent = msg;
    }

    async function handleGeneration(endpoint) {
        const topic = document.getElementById('topic').value.trim();
        if (!topic && endpoint !== '/summarize-content') {
            showError("Topic is required.");
            return;
        }

        const tone = document.getElementById('tone').value;
        const wordCount = parseInt(document.getElementById('word_count').value) || 400;
        const keywordsInput = document.getElementById('keywords').value;
        const keywords = keywordsInput.split(',').map(k => k.trim()).filter(k => k);

        let payload = {};
        if (endpoint === '/summarize-content') {
            const text = document.getElementById('source_text').value.trim();
            if(!text) {
                showError("Source text is required for summarization.");
                return;
            }
            const maxLength = parseInt(document.getElementById('max_length').value) || 100;
            payload = { text, max_length: maxLength };
        } else {
            payload = { topic, tone, word_count: wordCount, keywords };
        }

        await sendApiRequest(endpoint, payload);
    }

    async function handleSummarization() {
        await handleGeneration('/summarize-content');
    }

    async function sendApiRequest(endpoint, payload) {
        showLoading();
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            
            if (!response.ok || data.status === 'error') {
                throw new Error(data.message || `HTTP error ${response.status}`);
            }

            showResult(data.data.output);
        } catch (error) {
            showError(`Generation failed: ${error.message}`);
        }
    }

    async function fetchHistory() {
        try {
            const response = await fetch('/history');
            const data = await response.json();
            
            if (data.status === 'success') {
                renderHistoryTable(data.data);
            }
        } catch (error) {
            console.error("Failed to fetch history", error);
        }
    }

    window.reviewResult = function(encodedText) {
        const text = decodeURIComponent(encodedText);
        
        // Populate and select text manually since it's already generated
        uiLoading.classList.add('hidden');
        uiError.classList.add('hidden');
        uiResult.classList.remove('hidden');
        resultText.value = text;
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    function renderHistoryTable(records) {
        historyBody.innerHTML = '';
        if (!records || records.length === 0) {
            historyBody.innerHTML = '<tr><td colspan="4" style="text-align:center; padding: 2rem;">No history found. Generate something!</td></tr>';
            return;
        }

        records.forEach(rec => {
            const tr = document.createElement('tr');
            
            // Format time
            const date = new Date(rec.timestamp);
            const timeStr = date.toLocaleString();
            
            // Format inputs briefly
            let inputsPreview = '';
            if (rec.inputs && rec.inputs.topic) {
                inputsPreview = rec.inputs.topic;
            } else if (rec.inputs && rec.inputs.text_length) {
                inputsPreview = `Text length: ${rec.inputs.text_length}`;
            }

            tr.innerHTML = `
                <td><span style="background: var(--primary); color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">${rec.type}</span></td>
                <td><small>${timeStr}</small></td>
                <td><strong>${inputsPreview}</strong></td>
                <td>
                    <button class="action-btn" onclick="reviewResult('${encodeURIComponent(rec.output)}')">View Result</button>
                </td>
            `;
            historyBody.appendChild(tr);
        });
    }

});
