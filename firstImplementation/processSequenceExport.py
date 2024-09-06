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

num_char = 0

# Prompting user for filenames
origin_file = input("Arquivo de Leitura: ")
dest_file = input("Arquivo a ser Comparado: ")
choice = input("Gostaria de seccionar sua cadeia?(S/N) ")
if choice == 'S':
    print("Sequencias inciadas com 0 consideram o termo como um todo")
    num_char=int(input("Tamanho da sequencia: "))
else:
    pass


# Reading the files provided by the user
list_origin_df = read_file(origin_file)  
list_dest_df = read_file(dest_file)


# Converting the dataframes into lists
list_origin = list_origin_df[0].tolist()
list_dest = list_dest_df[0].tolist()

string_list_origin = []

# Iterate over each string (line) in listOrigin
for listString in list_origin:
    currentLine = ""  # Initialize an empty string for the current line
    
    # Loop through each character in the string
    for char in listString:
        currentLine += str(char)  # Convert each character to a string and append to currentLine
    
    # Append the concatenated string to stringListOrigin
    string_list_origin.append(currentLine)


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

def find_matches_by_char_sequence(string_list_origin, list_dest, char_sequence_length):
    # Initialize a dictionary to store the matches for each string in stringListOrigin
    matches_dict = {}
    output_data = []  # List to store the output rows
    
    # Check if char_sequence_length is 0 to apply the original logic
    if char_sequence_length == 0:
        for origin_term in string_list_origin:
            matches = []  # Temporary list to store matches found

            # Compare each origin term with all terms in listDest
            for dest_term in list_dest:
                if origin_term.lower() in dest_term.lower():
                    matches.append(dest_term)

            # Append the first row with the origin term and the number of matches
            if matches:
                output_data.append([origin_term, len(matches), matches[0]])  # First match
                # Append the rest of the matches, leaving the first two columns empty
                for match in matches[1:]:
                    output_data.append(["", "", match])
        
        return output_data  # Return the output data for char_sequence_length = 0

    # Logic for substring matching when char_sequence_length > 0
    for origin_string in string_list_origin:
        matches = set()  # Use a set to store unique matches for the current origin_string

        # Generate all possible substrings of the given length
        for i in range(len(origin_string) - char_sequence_length + 1):
            substring = origin_string[i:i + char_sequence_length]  # Extract a substring
            
            # Iterate over listDest to find matches for the substring
            for dest_string in list_dest:
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

output = find_matches_by_char_sequence(string_list_origin, list_dest, num_char)

# Call write_output function with your desired output file name, e.g., 'output.xlsx'
write_output(output, "outputs/testeExtensoes4.xlsx")

print("Output gravado no arquivo testeExtensoes4.xlsx")