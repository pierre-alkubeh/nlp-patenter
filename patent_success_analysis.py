import PyPDF2
import textract

import matplotlib.pyplot as plt

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from google import google

#This should be the name/path to the pdf file of your application.
filename = ''

#Extracts patent application from a pdf file into a string
def extract_text():

    #Extracts texts in bytes then converts to string
    text = textract.process(filename, language='eng').decode('utf-8')
    #Turns text all lowercase
    text = text.lower()

    return text

#Finds the patent abstract
def abstractExtract(text):
    abstract = ""
    #Finds where the abstract is. Assumes abstract is placed at the end of the doc
    pos = text.find("abstract")
    abstract = text[pos:]

    abstract = abstract[abstract.find("\n")+1:]
    abstract = abstract.split()
    abstract = " ".join(abstract)
    return abstract

#Finds the word count of the abstract
def abstractWrdCnt(text):
    abstract = abstractExtract(text)

    cnt = len(abstract.split())
    return cnt

#Checks if the abstract follows USPTO rules
def abstractCheck(text):
    cnt = abstractWrdCnt(text)

    if cnt < 50 or cnt > 150:
        return (f"WARNING:The abstract must have a word count between 50 and 150 words for US patents. We counted {cnt}.")
    else:
        return "✓"

#Checks if a section is in the submitted text
def sectionCheck(namesLst, text):
    for name in namesLst:
        if text.find(name.lower()):
            return "✓"
    return "Potentially Essential Section Could Not Be Found"

#Checks if all necessary sections are in the application
def formatCheck(text):
    titles = ["Sections", "Other Common Names","Comment"]

    tech_field = ["Technical Field", "Field of the InventionTechnological Field",
        sectionCheck(["Technical Field", "Field of the Invention", "Technological Field"],text)]
    prior_art = ["Background Art", "Prior ArtRelated ArtDescription of Related Art",
        sectionCheck([" art ", "background"],text)]
    description_drawings = ["Brief Description of Drawings", "N/A",
        sectionCheck(["BRIEF DESCRIPTION OF THE DRAWINGS", "Brief Description of Drawings"],text)]
    description = ["Detailed Description", "N/A",
        sectionCheck(["Detailed Description"],text)]
    claims = ["Claims", "What is Claimed",
        sectionCheck(["Claims", "What is claimed"],text)]
    if sectionCheck(["abstract"],text) == "✓":
        abstract = ["Abstract", "N/A", abstractCheck(text)]
    else:
        abstract = ["Abstract", "N/A", "Potentially Essential Section Could Not Be Found"]


    cellText = [titles, tech_field, prior_art, description_drawings, description, claims, abstract]

    for row in cellText:
        print(row[0], "\t", row[1], "\t", row[2])

#removes duplicates from a list
def remove_lst_duplicates(lst):
    temp = []
    for i in lst:
        if i not in temp:
            temp.append(i)
    return temp

#finds keywords in a string
def tokenize(a_string):
    tokens = word_tokenize(a_string)

    #identifies punctuation to be removed from tokens
    punctuations = ['(',')',';','.','?','!',':','[',']',',']
    #identifies common english words that are not keywords
    stop_words = stopwords.words('english')
    #removes punctuation and stop_words from list of tokens to create keywords.
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
    keywords = remove_lst_duplicates(keywords)

    return keywords

#measures similarity of text with another by percentage of keywords present.
def similarity(keywords, text):
    total = len(keywords)

    text = text.lower()

    cnt = 0
    for word in keywords:
        if word in text:
            cnt += 1
    return (cnt/total)

#Searchs patents.google.com for similar patents
def search(search_terms):

    search_results = google.search(f"{search_terms} AROUND(10) site:patents.google.com")

    return search_results


#Creates a list of the description of similar patents
def search_results_list(search_results):
    desc_lst = []
    link_lst = []

    for result in search_results:
        desc_lst.append(result.description)
        link_lst.append(result.link)

    return desc_lst, link_lst

#Calculates the probability of success based on how novel the patent application is
def prob_success(keywords, desc_list):
    avg_similarity = 0
    for desc in desc_list:
        avg_similarity += similarity(keywords, desc)
    avg_similarity = avg_similarity/len(keywords)

    success = (1-avg_similarity)*0.95

    return success

#Main function code
if __name__ == "__main__":

    patent_app = extract_text()
    formatCheck(patent_app)

    keywords = tokenize(abstractExtract(patent_app))
    search_str = " ".join(keywords)
    descriptions, links = search_results_list(google.search(search_str))

    success_rate = (prob_success(keywords, descriptions))

    if success_rate > 0.9:
        print(f"Congratulations!!! Your application has a {success_rate} success rate.")
        print("Here is a list of the most similar patents we find that you should review to double-check:")
        for link in links:
            print(link)
    elif success_rate > 0.7:
        print(f"Not Bad! Your application has a {success_rate} success rate.")
        print("Here is a list of the most similar patents we find that you should review to double-check:")
        for link in links:
            print(link)
    else:
        print(f"Hmmm... Your application has a {success_rate} success rate.")
        print("Here is a list of the most similar patents we find that you should review to double-check:")
        for link in links:
            print(link)
