// Markdown formatter for Gemini responses
// Add this script to your HTML: <script src="markdown-formatter.js"></script>

// Simple markdown to HTML converter
function formatMarkdown(text) {
    if (!text) return '';

    let html = text;

    // Escape HTML first
    html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Headers
    html = html.replace(/^### (.+)(\r?)$/gm, '<h3 style="color: var(--accent-primary); margin: 12px 0 6px; font-size: 15px;">$1</h3>');
    html = html.replace(/^## (.+)(\r?)$/gm, '<h2 style="color: var(--accent-primary); margin: 14px 0 8px; font-size: 16px; font-weight: 600;">$1</h2>');
    html = html.replace(/^# (.+)(\r?)$/gm, '<h1 style="color: var(--accent-primary); margin: 16px 0 10px; font-size: 18px; font-weight: 700;">$1</h1>');

    // Bold text
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong style="color: var(--accent-primary); font-weight: 600;">$1</strong>');

    // Italic text
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Bullet lists
    html = html.replace(/^[\-\*] (.+)(\r?)$/gm, '<li style="margin-left: 20px; margin-bottom: 4px;">$1</li>');

    // Numbered lists
    html = html.replace(/^\d+\. (.+)(\r?)$/gm, '<li style="margin-left: 20px; margin-bottom: 4px;">$1</li>');

    // Wrap consecutive <li> in <ul>
    html = html.replace(/(<li[^>]*>.*<\/li>\s*)+/g, function (match) {
        return '<ul style="margin: 8px 0; list-style-position: inside;">' + match + '</ul>';
    });

    // Code blocks (triple backticks)
    // We use a placeholder to prevent table parsing from messing up code blocks
    const codeBlocks = [];
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, function (match, lang, code) {
        codeBlocks.push(`<pre style="background: rgba(0, 0, 0, 0.3); padding: 12px; border-radius: 8px; overflow-x: auto; margin: 10px 0;"><code class="language-${lang || ''}">${code}</code></pre>`);
        return `__CODE_BLOCK_${codeBlocks.length - 1}__`;
    });

    // Code inline
    html = html.replace(/`([^`]+)`/g, '<code style="background: rgba(0, 212, 255, 0.1); padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 13px;">$1</code>');

    // Horizontal rules
    html = html.replace(/^---(\r?)$/gm, '<hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 12px 0;">');

    // Tables support
    const lines = html.split('\n');
    let inTable = false;
    let tableHtml = '';
    let processedLines = [];

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();

        if (line.startsWith('|') && line.endsWith('|')) {
            if (!inTable) {
                // Check if next line is a delimiter row
                if (i + 1 < lines.length) {
                    let nextLine = lines[i + 1].trim();
                    if (nextLine.startsWith('|') && nextLine.includes('---')) {
                        inTable = true;
                        tableHtml = '<div style="overflow-x: auto; margin: 12px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 14px; border: 1px solid rgba(255,255,255,0.1);">';

                        // Process header
                        let headers = line.slice(1, -1).split('|').map(h => h.trim());
                        tableHtml += '<thead><tr style="background: rgba(255,255,255,0.05);">';
                        headers.forEach(h => {
                            tableHtml += `<th style="padding: 10px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.2); color: var(--accent-primary);">${h}</th>`;
                        });
                        tableHtml += '</tr></thead><tbody>';

                        // Skip delimiter row
                        i++;
                        continue;
                    }
                }
            } else {
                // Inside table - process body row
                let cells = line.slice(1, -1).split('|').map(c => c.trim());
                tableHtml += '<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">';
                cells.forEach(c => {
                    tableHtml += `<td style="padding: 8px 10px;">${c}</td>`;
                });
                tableHtml += '</tr>';
            }

            // Check if table ends
            if (inTable) {
                if (i + 1 >= lines.length || !lines[i + 1].trim().startsWith('|')) {
                    inTable = false;
                    tableHtml += '</tbody></table></div>';
                    processedLines.push(tableHtml);
                }
            } else {
                processedLines.push(line);
            }
        } else {
            if (inTable) {
                inTable = false;
                tableHtml += '</tbody></table></div>';
                processedLines.push(tableHtml);
            }
            processedLines.push(line);
        }
    }

    html = processedLines.join('\n');

    // Restore code blocks
    codeBlocks.forEach((block, index) => {
        html = html.replace(`__CODE_BLOCK_${index}__`, block);
    });

    // Line breaks
    html = html.replace(/\n/g, '<br>');

    // Cleanup <br> after block elements
    html = html.replace(/(<\/h[1-6]>|<\/ul>|<\/li>|<\/pre>|<\/hr>|<\/table>|<\/div>)<br>/g, '$1');

    return html;
}
