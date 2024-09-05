import pandas as pd

# Reading the CSV files using pandas
listOrigin_df = pd.read_csv("listOrigin.csv", header=None)
listDest_df = pd.read_csv("listDest.csv", header=None)

# Converting the dataframes into lists
listOrigin = listOrigin_df[0].tolist()
listDest = listDest_df[0].tolist()

# Dictionary to store the results
dicRet = {}

# Algorithm to compare listOrigin with listDest
for originTerm in listOrigin:
    matches = []
    
    # Compare each origin term with all terms in listDest
    for destTerm in listDest:
        if originTerm.lower() in destTerm.lower():
            matches.append(destTerm)
    
    # Store the result in the dictionary
    dicRet[originTerm] = [len(matches)] + matches

# Prepare data for writing to CSV
output_data = []
for term, matches in dicRet.items():
    # Add the origin term, number of matches, and the matched terms to the output list
    output_data.append([term, matches[0], *matches[1:]])

# Convert the output data into a pandas DataFrame
output_df = pd.DataFrame(output_data)

# Writing the output DataFrame to a CSV file
output_df.to_csv("output.csv", index=False, header=["Termos", "Numero de Ocorrencias", "Termos Correspondentes"])

print("Output gravado no arquivo output.csv")
