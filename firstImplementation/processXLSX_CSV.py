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
    
    # Combine all matches into a single string => Wrong behavior
    # I want to create a new line for every match
    matches_str = ", ".join(matches)
    
    # Append the result to the output data list
    # You must change this line below aswell, to make the new logic
    output_data.append([originTerm, len(matches), matches_str])

# Call write_output function with your desired output file name, e.g., 'output.xlsx'
write_output(output_data, "outputs/exemplo.csv")

print("Output gravado no arquivo exemplo.csv")