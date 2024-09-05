termOrigin = "Health"

listOrigin = [
    "Medicine", 
    "Learning", 
    "Health",
    "Smart",
    "a"
]

listDest = [
    "Smartphone", 
    "Health technology", 
    "Telemedicine",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Big Data Analytics",
    "Wearable Devices",
    "Electronic Health Records (EHR)",
    "Medical Imaging",
    "Natural Language Processing (NLP)",
    "Robotic Surgery",
    "Predictive Analytics",
    "Blockchain in Healthcare",
    "Virtual Reality in Medicine",
    "Augmented Reality",
    "3D Printing in Medicine",
    "Biotechnology",
    "Precision Medicine",
    "Genomic Data Analysis",
    "Remote Patient Monitoring",
    "Neural Networks",
    "Cognitive Computing",
    "Smart Sensors in Healthcare",
]

# Dicionário que guarda os resultados
dicRet = {}

# Algoritmo que compara listOrigin with listDest
for originTerm in listOrigin:
    matches = []
    
    # Compare each origin term with all terms in listDest
    for destTerm in listDest:
        if originTerm.lower() in destTerm.lower():
            matches.append(destTerm)
    
    # Store the result in the dictionary
    dicRet[originTerm] = [len(matches)] + matches


with open("output3.txt", "w") as f:
    for term, matches in dicRet.items():
        # Write the origin term and the number of matches
        f.write(f"{term}: {matches[0]} correspondencias\n")
        
        # Write each matched term
        for match in matches[1:]:
            f.write(f"    {match}\n")
        
        # Add a new line after each term for readability
        f.write("\n")

print("Output gerado no arquivo output3.txt")


