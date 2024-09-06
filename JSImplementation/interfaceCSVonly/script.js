function processFiles() {
    const listOriginFile = document.getElementById('listOrigin').files[0];
    const listDestFile = document.getElementById('listDest').files[0];
    const sequenceLength = parseInt(document.getElementById('sequenceLength').value);

    if (!listOriginFile || !listDestFile) {
        alert('Por favor, faça o upload de ambos os arquivos.');
        return;
    }

    const readerOrigin = new FileReader();
    const readerDest = new FileReader();

    readerOrigin.onload = function(e) {
        const listOriginContent = e.target.result.split('\n').map(line => line.trim());
        readerDest.onload = function(e) {
            const listDestContent = e.target.result.split('\n').map(line => line.trim());
            const result = matchSequences(listOriginContent, listDestContent, sequenceLength);
            displayOutput(result);
        };
        readerDest.readAsText(listDestFile);
    };

    readerOrigin.readAsText(listOriginFile);
}

function matchSequences(listOrigin, listDest, charSequenceLength) {
    let output = [];

    if (charSequenceLength === 0) {
        listOrigin.forEach(originTerm => {
            let matches = [];
            listDest.forEach(destTerm => {
                if (destTerm.toLowerCase().includes(originTerm.toLowerCase())) {
                    matches.push(destTerm);
                }
            });

            if (matches.length > 0) {
                output.push([originTerm, matches.length, matches[0]]);
                matches.slice(1).forEach(match => {
                    output.push(['', '', match]);
                });
            }
        });
    } else {
        listOrigin.forEach(originTerm => {
            let matches = [];
            for (let i = 0; i <= originTerm.length - charSequenceLength; i++) {
                const substring = originTerm.substring(i, i + charSequenceLength);
                listDest.forEach(destTerm => {
                    if (destTerm.toLowerCase().includes(substring.toLowerCase()) && !matches.includes(destTerm)) {
                        matches.push(destTerm);
                    }
                });
            }

            if (matches.length > 0) {
                output.push([originTerm, matches.length, matches[0]]);
                matches.slice(1).forEach(match => {
                    output.push(['', '', match]);
                });
            }
        });
    }

    return output;
}

function displayOutput(result) {
    // Convert result array to CSV format
    let csvContent = "data:text/csv;charset=utf-8,";

    // Add headers
    csvContent += "Termos,Numero de Ocorrencias,Termo Correspondentes\n";

    // Add each result row to CSV content
    result.forEach(row => {
        const rowContent = row.map(field => `"${field}"`).join(","); // Escape fields and join them with commas
        csvContent += rowContent + "\n"; // Add new line at the end of each row
    });

    // Encode CSV content as a URI
    const encodedUri = encodeURI(csvContent);

    // Create a download link for the CSV file
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "teste_seguranca.csv");

    // Append the link to the body and click it to trigger the download
    document.body.appendChild(link);
    link.click();

    // Remove the link from the document after the download
    document.body.removeChild(link);
}

// function displayOutput(result) {
//     // Convert result array to CSV format
//     let csvContent = "data:text/csv;charset=utf-8,";

//     // Add headers
//     csvContent += "Termos,Numero de Ocorrencias,Termo Correspondentes\n";

//     // Add each result row to CSV content, without quotes unless necessary
//     result.forEach(row => {
//         const rowContent = row.map(field => {
//             // Only add quotes if the field contains a comma or newline
//             if (field.includes(",") || field.includes("\n")) {
//                 return `"${field}"`;
//             }
//             return field; // No quotes needed for simple fields
//         }).join(","); // Join the fields with commas
//         csvContent += rowContent + "\n"; // Add new line at the end of each row
//     });

//     // Encode CSV content as a URI
//     const encodedUri = encodeURI(csvContent);

//     // Create a download link for the CSV file
//     const link = document.createElement("a");
//     link.setAttribute("href", encodedUri);
//     link.setAttribute("download", "teste_sem_aspas.csv"); // Set file name

//     // Append the link to the body and click it to trigger the download
//     document.body.appendChild(link);
//     link.click();

//     // Remove the link from the document after the download
//     document.body.removeChild(link);
// }
