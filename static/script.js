        document.addEventListener('DOMContentLoaded', function() {
            const generateBtn = document.getElementById('generate-btn');
            const outputContainer = document.getElementById('output-container');
            const outputContent = document.getElementById('output-content');
            const copyBtn = document.getElementById('copy-btn');
            const wordCount = document.getElementById('word-count');
            const charCount = document.getElementById('char-count');
            const quoteContainer = document.getElementById('quote-container');
            
            // Sample quotes
            const quotes = [
                "The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
                "First, solve the problem. Then, write the code. - John Johnson",
                "Code is like humor. When you have to explain it, it's bad. - Cory House",
                "Make it work, make it right, make it fast. - Kent Beck",
                "Programming isn't about what you know; it's about what you can figure out. - Chris Pine"
            ];
            
            generateBtn.addEventListener('click', async function() {
                const language = document.getElementById('language').value;
                const contentType = document.getElementById('content-type').value;
                
                try {
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            topic: language,
                            content_type: contentType,
                            save_file: false
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    
                    const data = await response.json();
                    
                    // Display the content
                    if (contentType === 'code') {
                        outputContent.innerHTML = `<pre class="code-block"><code class="language-${language}">${data.content}</code></pre>`;
                        hljs.highlightAll();
                    } else if (contentType === 'tips') {
                        outputContent.innerHTML = data.content.split('\n').map(line => 
                            `<div class="tip-item">${line}</div>`
                        ).join('');
                    } else {
                        outputContent.textContent = data.content;
                    }
                    
                    // Update metadata
                    wordCount.textContent = `${data.metadata.word_count} words`;
                    charCount.textContent = `${data.metadata.char_count} characters`;
                    
                    // Show a random quote
                    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
                    quoteContainer.textContent = randomQuote;
                    quoteContainer.classList.remove('hidden');
                    
                    // Show the output container
                    outputContainer.classList.remove('hidden');
                } catch (error) {
                    console.error('Error:', error);
                    outputContent.textContent = 'An error occurred while generating content. Please try again.';
                    outputContainer.classList.remove('hidden');
                }
            });
            
            copyBtn.addEventListener('click', function() {
                const range = document.createRange();
                range.selectNode(outputContent);
                window.getSelection().removeAllRanges();
                window.getSelection().addRange(range);
                document.execCommand('copy');
                window.getSelection().removeAllRanges();
                
                // Visual feedback
                const originalText = copyBtn.textContent;
                copyBtn.textContent = 'Copied!';
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                }, 2000);
            });
        });