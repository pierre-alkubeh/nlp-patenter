# open_patent
Patent application analysis repository for analyzing chances for success and improving the application. Created by Pierre Alkubeh of Leviasec Corporation. The project is open-source, but we can analyze any patent application for you at www.leviasec.com .

# patent_success_analysis.py
This service checks for:

1. Proper formatting of your patent.

2. Prior art search and returns links with most similar patents

3. Novelty analysis and returns a probability of your patent being novel and therefore accepted by the patent office.

How it works: 

The algorithm first extracts the text from the PDF file or submitted text into a string. The string is then analyzed for presence of necessary sections such as a detailed description and for formatting requirements such as the word count for the abstract. A natural-language processing algorithm then extracts  keywords from the application using tokenization and runs a search through the patent office for most similar patents. A final algorithm calculates the similarities between your patent application and the most similar patents to create a novelty score for your patent. 

# COMING SOON: STYLE ANALYSIS & WRITING

Patents need to be written in legalese for best protection in court. This algorithm will analyse the writing style in your patent application and rewrite unsatisfactory parts into iron-clad legalese speak. 

# COMING SOON: CLAIM ANALYSIS

The claims made are the heart of any patent application. The claim analysis service will analyze the argumentation behind your claim analysis to ensure your success in patenting and defending your invention. 
