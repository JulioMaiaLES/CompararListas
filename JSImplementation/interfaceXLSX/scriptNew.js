function processFiles() {
    const listOriginFile = document.getElementById('listOrigin').files[0];
    const listDestFile = document.getElementById('listDest').files[0];
    const sequenceLength = parseInt(document.getElementById('sequenceLength').value, 10);

    if (!listOriginFile || !listDestFile) {
        alert('Por favor, faça o upload de ambos os arquivos.');
        return;
    }

    const listOriginPromise = readFile(listOriginFile);
    const listDestPromise = readFile(listDestFile);

    Promise.all([listOriginPromise, listDestPromise])
        .then(filesContent => {
            const listOrigin = filesContent[0];
            const listDest = filesContent[1];

            const result = compareFiles(listOrigin, listDest, sequenceLength);
            downloadFile(result);
        })
        .catch(error => console.error('Erro ao processar os arquivos:', error));
}

// Function to read CSV/XLSX files
function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = function(event) {
            const data = event.target.result;
            let parsedData = [];

            if (file.name.endsWith('.csv')) {
                // Parse CSV file
                parsedData = data.split('\n').map(row => row.split(','));
            } else if (file.name.endsWith('.xlsx')) {
                // Parse XLSX file
                const workbook = XLSX.read(data, { type: 'binary' });
                const sheetName = workbook.SheetNames[0];
                const sheet = workbook.Sheets[sheetName];
                parsedData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
            }

            resolve(parsedData.map(row => row[0])); // Return the first column
        };

        if (file.name.endsWith('.csv')) {
            reader.readAsText(file);
        } else if (file.name.endsWith('.xlsx')) {
            reader.readAsBinaryString(file);
        } else {
            reject(new Error('Formato de arquivo inválido'));
        }
    });
}

// Function to compare two lists based on sequence length
function compareFiles(listOrigin, listDest, sequenceLength) {
    const output = [];

    if (sequenceLength === 0) {
        // Original logic: compare full terms
        listOrigin.forEach(originTerm => {
            const matches = listDest.filter(destTerm => destTerm.toLowerCase().includes(originTerm.toLowerCase()));
            if (matches.length) {
                output.push([originTerm, matches.length, matches[0]]);
                matches.slice(1).forEach(match => output.push(["", "", match]));
            }
        });
    } else {
        // Sequence matching logic
        listOrigin.forEach(originTerm => {
            const matches = [];
            for (let i = 0; i <= originTerm.length - sequenceLength; i++) {
                const sequence = originTerm.substring(i, i + sequenceLength).toLowerCase();
                matches.push(...listDest.filter(destTerm => destTerm.toLowerCase().includes(sequence)));
            }
            const uniqueMatches = [...new Set(matches)]; // Remove duplicates
            if (uniqueMatches.length) {
                output.push([originTerm, uniqueMatches.length, uniqueMatches[0]]);
                uniqueMatches.slice(1).forEach(match => output.push(["", "", match]));
            }
        });
    }

    return output;
}

function downloadFile(result) {
    const isXLSXSelected = document.getElementById('xlsxOption').checked;

    if (isXLSXSelected) {
        // If XLSX is selected, generate XLSX file
        generateXLSX(result);
    } else {
        // If CSV is selected, generate CSV file
        generateCSV(result);
    }
}

// Function to display results as CSV
function generateCSV(result) {
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Termos,Numero de Ocorrencias,Termo Correspondentes\n";

    result.forEach(row => {
        const rowContent = row.map(field => `"${field}"`).join(",");
        csvContent += rowContent + "\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "current_mixed_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function generateXLSX(result) {
    // Create a workbook and a worksheet
    let wb = XLSX.utils.book_new();
    let ws_data = [["Termos", "Numero de Ocorrencias", "Termo Correspondentes"]]; // Headers

    // Add result data to the worksheet
    result.forEach(row => {
        ws_data.push(row);
    });

    // Create the worksheet and add to workbook
    let ws = XLSX.utils.aoa_to_sheet(ws_data);
    XLSX.utils.book_append_sheet(wb, ws, "Resultados");

    // Write the workbook and download as XLSX
    XLSX.writeFile(wb, "current_mixed_results.xlsx");
}