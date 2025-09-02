<title>JavaScript file</title>
document.getElementById('process-button').addEventListener('click', () => {
    const files = document.getElementById('pdf-upload').files;
    if (files.length === 0) {
        alert('Please select one or more PDF files.');
        return;
    }
    // This is where you would handle the file processing
    alert(`${files.length} PDF(s) selected for processing.`);
});

document.getElementById('query-button').addEventListener('click', () => {
    const query = document.getElementById('query-input').value;
    if (!query) {
        alert('Please enter a question.');
        return;
    }
    // This is where you would send the query to the backend
    document.getElementById('response-text').textContent = `Fetching response for: "${query}"`;
});
