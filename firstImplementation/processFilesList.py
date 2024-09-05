import pandas as pd
import csv

# Reading the CSV files using pandas
listOrigin_df = pd.read_csv("listOrigin.csv", header=None)
listDest_df = pd.read_csv("listDest.csv", header=None)

# Converting the dataframes into lists
listOrigin = listOrigin_df[0].tolist()
listDest = listDest_df[0].tolist()

# Open a CSV file for writing
with open("desiredOutput.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(["Termos", "Numero de Ocorrencias", "Termo Correspondentes"])
    
    # Algorithm to compare listOrigin with listDest directly for output generation
    for originTerm in listOrigin:
        matches = []  # Temporary list to store matches found
        
        # Compare each origin term with all terms in listDest
        for destTerm in listDest:
            if originTerm.lower() in destTerm.lower():
                matches.append(destTerm)
        
        # Convert matches list to a single string with desired separator, e.g., ", "
        matches_str = ", ".join(matches)
        
        # Write the row to the CSV file
        writer.writerow([originTerm, len(matches), matches_str])

print("Output gravado no arquivo desiredOutput.csv")