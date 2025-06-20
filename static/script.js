// File: app.js (Theme Fix Integrated)

document.addEventListener('DOMContentLoaded', function () {
    // Element declarations
    const generateBtn = document.getElementById('generate-btn');
    const outputSection = document.getElementById('output-section');
    const outputContent = document.getElementById('output-content');
    const previewBtn = document.getElementById('preview-btn');
    const wordCount = document.getElementById('word-count');
    const charCount = document.getElementById('char-count');
    // const generationTime = document.getElementById('generation-time');
    const quoteContainer = document.getElementById('quote-container');
    const previewModal = document.getElementById('preview-modal');
    const previewIframe = document.getElementById('preview-iframe');
    const previewClose = document.getElementById('preview-close');
    const contentTypeSelect = document.getElementById('content-type');
    const promptSection = document.querySelector('.prompt-section');
    const toggleBtn = document.getElementById('toggle-theme');
    const syntaxToggleBtn = document.getElementById('toggle-syntax-theme');
    const hljsThemeLink = document.getElementById('hljs-theme');
    const downloadBtn = document.getElementById('download-btn');
    const clearBtn = document.getElementById('clear-history-btn');

    const quotes = [
        "💡 The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
        "🎯 First, solve the problem. Then, write the code. - John Johnson",
        "😄 Code is like humor. When you have to explain it, it's bad. - Cory House",
        "⚡ Make it work, make it right, make it fast. - Kent Beck",
        "🔍 Programming isn't about what you know; it's about what you can figure out. - Chris Pine",
        "🚀 The best error message is the one that never shows up. - Thomas Fuchs",
        "🎨 Code is poetry written for computers to execute and humans to read. - Anonymous",
        "🔧 Any fool can write code that a computer can understand. Good programmers write code that humans can understand. - Martin Fowler"
    ];

    if (contentTypeSelect && promptSection) {
        contentTypeSelect.addEventListener('change', function () {
            promptSection.style.display = this.value === 'prompt' ? 'block' : 'none';
        });
    }

    function enhancePrompt(input, language, type) {
        let enhanced = input.trim();
        if (!enhanced.toLowerCase().includes(language)) {
            enhanced += ` in ${language}`;
        }
        if ((type === 'code' || type === 'prompt') && !enhanced.toLowerCase().startsWith("generate")) {
            enhanced = `Generate ${type} that ${enhanced}`;
        }
        return enhanced;
    }

    if (generateBtn) {
        generateBtn.addEventListener('click', async function () {
            const language = document.getElementById('language').value;
            const contentType = document.getElementById('content-type').value;
            const prompt = document.getElementById('prompt').value;
            const enhancedPrompt = enhancePrompt(prompt, language, contentType);

            if (contentType === 'prompt' && !prompt.trim()) {
                alert('Please describe what you want to create in the prompt field.');
                document.getElementById('prompt').focus();
                return;
            }

            generateBtn.classList.add('loading');
            generateBtn.querySelector('.btn-text').textContent = 'Generating...';
            // const startTime = Date.now();

            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: language, content_type: contentType, prompt: enhancedPrompt, save_file: false })
                });
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                // const endTime = Date.now();

                if (contentType === 'code' || contentType === 'prompt') {
                    if (language === 'html' && (contentType === 'prompt' || data.content.includes('<!DOCTYPE html'))) {
                        if (previewBtn) {
                            previewBtn.classList.remove('hidden');
                            previewBtn.onclick = () => showPreview(data.content);
                        }
                    } else {
                        if (previewBtn) previewBtn.classList.add('hidden');
                    }
                    if (outputContent) outputContent.innerHTML = `<pre><code class="language-${language}">${escapeHtml(data.content)}</code></pre>`;
                    if (typeof hljs !== 'undefined' && hljs.highlightAll) hljs.highlightAll();
                } else if (contentType === 'tips') {
                    const tips = data.content.split('\n').filter(line => line.trim());
                    if (outputContent) outputContent.innerHTML = tips.map(tip => `<div class="tip-item">${tip.replace('• ', '')}</div>`).join('');
                } else {
                    if (outputContent) outputContent.innerHTML = `<div style="padding: 1rem; background: #f8fafc; border-radius: 10px; line-height: 1.6;">${data.content}</div>`;
                }

                if (wordCount) wordCount.textContent = `${data.metadata.word_count} words`;
                if (charCount) charCount.textContent = `${data.metadata.char_count} characters`;
                setTimeout(() => {
                    if (outputContent) {
                        const pre = outputContent.querySelector('pre');
                        if (pre && !pre.querySelector('.copy-btn')) {
                            const copyBtn = document.createElement('button');
                            copyBtn.className = 'copy-btn';
                            copyBtn.textContent = 'Copy Code';
                            copyBtn.style.cssText = 'position:absolute;top:8px;right:8px;z-index:2;';
                            pre.style.position = 'relative';
                            pre.appendChild(copyBtn);
                            copyBtn.addEventListener('click', function() {
                                const codeElem = pre.querySelector('code');
                                if (!codeElem) return;
                                const code = codeElem.innerText;
                                if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
                                    navigator.clipboard.writeText(code).then(function() {
                                        copyBtn.textContent = 'Copied!';
                                        setTimeout(() => copyBtn.textContent = 'Copy Code', 1500);
                                    }).catch(function() {
                                        copyBtn.textContent = 'Failed!';
                                        setTimeout(() => copyBtn.textContent = 'Copy Code', 1500);
                                    });
                                }
                            });
                        }
                    }
                }, 100);

                const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
                if (quoteContainer) {
                    quoteContainer.textContent = randomQuote;
                    quoteContainer.classList.add('show');
                }
                if (outputSection) {
                    outputSection.classList.add('show');
                    outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
                outputSection.classList.add('show');
                outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

                const history = JSON.parse(localStorage.getItem('outputHistory')) || [];
                history.unshift({
                    language,
                    type: contentType,
                    prompt,
                    content: data.content,
                    preview: data.content.substring(0, 100) + '...',
                    time: new Date().toLocaleString()
                });
                localStorage.setItem('outputHistory', JSON.stringify(history.slice(0, 20)));
                renderHistory();

            } catch (error) {
                console.error('Error:', error);
                outputContent.innerHTML = '<div style="color: var(--error); padding: 1rem; text-align: center;">❌ An error occurred while generating content. Please try again.</div>';
                outputSection.classList.add('show');
            } finally {
                generateBtn.classList.remove('loading');
                generateBtn.querySelector('.btn-text').textContent = 'Generate Code';
            }
        });
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function showPreview(htmlContent) {
        const blob = new Blob([htmlContent], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        previewIframe.src = url;
        previewModal.classList.add('show');
        previewIframe.onload = () => setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    if (previewClose) {
        previewClose.addEventListener('click', function () {
            previewModal.classList.remove('show');
            previewIframe.src = '';
        });
    }
    if (previewModal) {
        previewModal.addEventListener('click', function (e) {
            if (e.target === previewModal) {
                previewModal.classList.remove('show');
                previewIframe.src = '';
            }
        });
    }

    // Theme Fix: Apply saved theme on load
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            updateIcon();
        });
    }

    function updateIcon() {
        if (!toggleBtn) return;
        toggleBtn.innerHTML = document.body.classList.contains('dark-mode') ? '🌞 Light Mode' : '🌙 Dark Mode';
    }

    // Syntax highlight theme switch
    if (syntaxToggleBtn && hljsThemeLink) {
        syntaxToggleBtn.addEventListener('click', () => {
            const current = localStorage.getItem('syntax-theme') || 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            localStorage.setItem('syntax-theme', next);
            hljsThemeLink.href = next === 'dark'
                ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css'
                : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css';
            updateSyntaxToggleLabel();
        });

        const savedSyntax = localStorage.getItem('syntax-theme') || 'light';
        hljsThemeLink.href = savedSyntax === 'dark'
            ? 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css'
            : 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css';
        updateSyntaxToggleLabel();
    }

    function updateSyntaxToggleLabel() {
        if (!syntaxToggleBtn) return;
        const isDark = localStorage.getItem('syntax-theme') === 'dark';
        syntaxToggleBtn.textContent = isDark ? '🌓 Syntax: Dark' : '🌓 Syntax: Light';
    }

    updateIcon();

    // Render history
    function renderHistory() {
        const historyContainer = document.getElementById('history-list');
        if (!historyContainer) return;
        const stored = JSON.parse(localStorage.getItem('outputHistory')) || [];
        historyContainer.innerHTML = '';
        if (stored.length === 0) {
            historyContainer.innerHTML = '<p>No history yet.</p>';
            return;
        }
        stored.forEach((item, index) => {
            const entry = document.createElement('div');
            entry.className = 'history-entry';
            entry.innerHTML = `
                <div><strong>${item.language}</strong> | ${item.type} | <small>${item.time}</small></div>
                <pre>${escapeHtml(item.preview)}</pre>
                <button class="reuse-btn" data-index="${index}">🔁 Reuse</button>
            `;
            historyContainer.appendChild(entry);

            // Add event listener for reuse button
            entry.querySelector('.reuse-btn').addEventListener('click', () => {
                document.getElementById('language').value = item.language;
                document.getElementById('content-type').value = item.type;
                document.getElementById('prompt').value = item.prompt;
                if (outputContent) outputContent.innerHTML = `<pre><code class="language-${item.language}">${escapeHtml(item.content)}</code></pre>`;
                if (typeof hljs !== 'undefined' && hljs.highlightAll) hljs.highlightAll();
                if (outputSection) {
                    outputSection.classList.add('show');
                    outputSection.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            localStorage.removeItem('outputHistory');
            renderHistory();
        });
    }

    renderHistory();

    // Feedback form logic
    const feedbackForm = document.getElementById('feedback-form');
    const feedbackBtn = document.getElementById('submit-feedback');
    const feedbackThanks = document.getElementById('feedback-thanks');

    if (feedbackForm && feedbackBtn) {
        feedbackForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const rating = feedbackForm.querySelector('input[name="rating"]:checked');
            const comment = feedbackForm.querySelector('#feedback-comment').value;

            if (!rating) {
                alert('Please select a rating.');
                return;
            }

            // Store feedback in localStorage
            const feedbackHistory = JSON.parse(localStorage.getItem('feedbackList')) || [];
            feedbackHistory.unshift({
                stars: rating.value,
                comment,
                time: new Date().toLocaleString()
            });
            localStorage.setItem('feedbackList', JSON.stringify(feedbackHistory.slice(0, 20)));

            feedbackForm.reset();
            feedbackThanks.classList.remove('hidden');
            setTimeout(() => feedbackThanks.classList.add('hidden'), 3000);
        });
    }

    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            // Do NOT toggle dark mode on the preview area
        });
    }
    // Download functionality
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            const content = outputContent.innerText || outputContent.textContent;
            if (!content.trim()) {
                alert('Nothing to download. Please generate content first.');
                return;
            }
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `generated_content_${new Date().toISOString()}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }
});
const htmlInput = document.getElementById('html-input');
const htmlPreview = document.getElementById('html-preview');
if (htmlInput && htmlPreview) {
    htmlInput.addEventListener('input', function() {
        htmlPreview.srcdoc = this.value;
    });
    // Initialize preview
    htmlPreview.srcdoc = htmlInput.value;
}

