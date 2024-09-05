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
# origin_file = input("Arquivo de Leitura: ")
# dest_file = input("Arquivo a ser Comparado: ")

# Reading the files provided by the user
# listOrigin_df = read_file(origin_file)  
# listDest_df = read_file(dest_file)
listOrigin_df = read_file("listOrigin.csv")  
listDest_df = read_file("listDest.csv")

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

def find_matches_by_char_sequence(stringListOrigin, listDest, char_sequence_length):
    # Initialize a dictionary to store the matches for each string in stringListOrigin
    matches_dict = {}
    output_data = []  # List to store the output rows
    
    # Check if char_sequence_length is 0 to apply the original logic
    if char_sequence_length == 0:
        for originTerm in stringListOrigin:
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
                    output_data.append(["", "", match])
        
        return output_data  # Return the output data for char_sequence_length = 0

    # Logic for substring matching when char_sequence_length > 0
    for origin_string in stringListOrigin:
        matches = set()  # Use a set to store unique matches for the current origin_string

        # Generate all possible substrings of the given length
        for i in range(len(origin_string) - char_sequence_length + 1):
            substring = origin_string[i:i + char_sequence_length]  # Extract a substring
            
            # Iterate over listDest to find matches for the substring
            for dest_string in listDest:
                if substring.lower() in dest_string.lower():  # Case-insensitive match
                    matches.add(dest_string)  # Add the matched string to the set (avoiding duplicates)

        # Convert the set back to a list before storing in the dictionary
        matches_dict[origin_string] = list(matches)

        # Append the first row with the origin string and the number of matches
        if matches_dict[origin_string]:
            output_data.append([origin_string, len(matches_dict[origin_string]), matches_dict[origin_string][0]])  # First match
            # Append the rest of the matches, leaving the first two columns empty
            for match in matches_dict[origin_string][1:]:
                output_data.append(["", "", match])

    return output_data  # Return the output data for char_sequence_length > 0


# TESTES -------------------------------------------------------------------------
# Case when char_sequence_length == 3
# output = find_matches_by_char_sequence(stringListOrigin, listDest, 3)

# for row in output:
#     print(row)

# Case when char_sequence_length == 0 (original logic)
# output = find_matches_by_char_sequence(stringListOrigin, listDest, 0)

# for row in output:
#     print(row)
# TESTES -------------------------------------------------------------------------


# Create a DataFrame and write to CSV
# output_df = pd.DataFrame(output_data, columns=["Termos", "Numero de Ocorrencias", "Termos Correspondentes"])


# Call write_output function with your desired output file name, e.g., 'output.xlsx'
# write_output(output_data, "outputs/exemploSingle.csv")

# print("Output gravado no arquivo exemploSingle.csv")