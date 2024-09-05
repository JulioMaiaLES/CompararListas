import pandas as pd
import openpyxl  # Explicitly import openpyxl

# Function to determine file extension
def read_file(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename, header=None)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(filename, header=None, engine='openpyxl')  # Specifying engine is optional as 'openpyxl' is default for .xlsx
    else:
        raise ValueError("Unsupported file format")

# Prompting user for filenames
origin_file = input("Arquivo de Leitura: ")
dest_file = input("Arquivo a ser Comparado: ")

# Reading the files provided by the user
listOrigin_df = read_file(origin_file)  
listDest_df = read_file(dest_file)


# Converting the dataframes into lists
listOrigin = listOrigin_df[0].tolist()
listDest = listDest_df[0].tolist()

stringListOrigin = []

# Iterate over each string (line) in listOrigin
for listString in listOrigin:
    currentLine = ""  # Initialize an empty string for the current line
    
    # Loop through each character in the string
    for char in listString:
        currentLine += str(char)  # Convert each character to a string and append to currentLine
    
    # Append the concatenated string to stringListOrigin
    stringListOrigin.append(currentLine)


def write_output(output_data, filename):
    # Determine the output format based on file extension
    if filename.endswith('.csv'):
        # Convert output data to DataFrame for easy CSV writing
        output_df = pd.DataFrame(output_data, columns=["Termos", "Numero de Ocorrencias", "Termo Correspondentes"])
        output_df.to_csv(filename, index=False)
    elif filename.endswith('.xlsx'):
        # Convert output data to DataFrame for easy Excel writing
        output_df = pd.DataFrame(output_data, columns=["Termos", "Numero de Ocorrencias", "Termo Correspondentes"])
        output_df.to_excel(filename, index=False, engine='openpyxl')
    else:
        raise ValueError("Unsupported file format")

# Store the output data
output_data = []

for originTerm in listOrigin:
    matches = []  # Temporary list to store matches found
    
    # Compare each origin term with all terms in listDest
    for destTerm in listDest:
        if originTerm.lower() in destTerm.lower():
            matches.append(destTerm)
    
    # Append the first row with the origin term and the number of matches
    if matches:
        output_data.append([originTerm, len(matches), matches[0]])  # First match
        # Append the rest of the matches, leaving the first two columns empty
        for match in matches[1:]:
            output_data.append(["", "", match])  # Subsequent matches

# Call write_output function with your desired output file name, e.g., 'output.xlsx'
write_output(output_data, "outputs/linesExemplo.csv")

print("Output gravado no arquivo linesExemplo.csv")