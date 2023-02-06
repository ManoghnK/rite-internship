import PyPDF2
import textract
import spacy
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict

#%matplotlib inline



pdfFileObj = open('data\Murali Mohan Vamsi_Rite Software_Fusion SCM Cloud Functional.pdf','rb')

# Read file
pdfReader = PyPDF2.PdfReader(pdfFileObj)
writer = PyPDF2.PdfWriter()

# Get total number of pages
num_pages = len(pdfReader.pages)

# Initialize a count for the number of pages
count = 0

# Initialize a text empty etring variable
text = ""

# Extract text from every page on the file
while count < num_pages:
    pageObj = pdfReader.pages[count]
    pageObj.cropbox.lower_left=(80,80)
    pageObj.cropbox.upper_right=(500,700)
    #writer.add_page(pageObj)
    count +=1

    text += pageObj.extract_text()


#text = text.lower()
# Remove numbers
text = re.sub(r'\d+','',text)

# Remove punctuation
text = text.translate(str.maketrans('','',string.punctuation))

text = re.sub(r'\n','$',text)
text = re.sub(r'[^\w\s]', '', text)
text = re.sub(r'\s+', ' ', text)

text = re.sub('Page [0-9] of [0-9]', '', text)
words = text.split('$')


print(text.encode('utf-8'))
print(words)
for i in words:
    if(i==" "):
        words.remove(i)
    else:
        i= re.sub(r'[^\w\s]', '', i)
        i = re.sub(r'\s+', '', i)
print('\n')
print(words)
#name_search = re.search(r'([A-Z][a-z]+) ([A-Z][a-z]+)', tet)
#if name_search:
#    first_name = name_search.group(1)
#    last_name = name_search.group(2)
#    print(f'Name: {first_name} {last_name}')
#else:
#    print("Name not found.")
terms = {'Quality/Six Sigma':['black belt','capability analysis','control charts','doe','dmaic','fishbone',
                              'gage r&r', 'green belt','ishikawa','iso','kaizen','kpi','lean','metrics',
                              'pdsa','performance improvement','process improvement','quality',
                              'quality circles','quality tools','root cause','six sigma',
                              'stability analysis','statistical analysis','tqm'],      
        'Operations management':['automation','bottleneck','constraints','cycle time','efficiency','fmea',
                                 'machinery','maintenance','manufacture','line balancing','oee','operations',
                                 'operations research','optimization','overall equipment effectiveness',
                                 'pfmea','process','process mapping','production','resources','safety',
                                 'stoppage','value stream mapping','utilization'],
        'Supply chain':['abc analysis','apics','customer','customs','delivery','distribution','eoq','epq',
                        'fleet','forecast','inventory','logistic','materials','outsourcing','procurement',
                        'reorder point','rout','safety stock','scheduling','shipping','stock','suppliers',
                        'third party logistics','transport','transportation','traffic','supply chain',
                        'vendor','warehouse','wip','work in progress'],
        'Project management':['administration','agile','budget','cost','direction','feasibility analysis',
                              'finance','kanban','leader','leadership','management','milestones','planning',
                              'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
        'Data analytics':['analytics','api','aws','big data','busines intelligence','clustering','code',
                          'coding','data','database','data mining','data science','deep learning','hadoop',
                          'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                          'predictive','programming','python','r','sql','tableau','text mining',
                          'visualuzation'],
        'Healthcare':['adverse events','care','clinic','cphq','ergonomics','healthcare',
                      'health care','health','hospital','human factors','medical','near misses',
                      'patient','reporting system']}
# Initializie score counters for each area
quality = 0
operations = 0
supplychain = 0
project = 0
data = 0
healthcare = 0

# Create an empty list where the scores will be stored
scores = []

# Obtain the scores for each area
for area in terms.keys():
        
    if area == 'Quality/Six Sigma':
        for word in terms[area]:
            if word in text:
                quality +=1
        scores.append(quality)
        
    elif area == 'Operations management':
        for word in terms[area]:
            if word in text:
                operations +=1
        scores.append(operations)
        
    elif area == 'Supply chain':
        for word in terms[area]:
            if word in text:
                supplychain +=1
        scores.append(supplychain)
        
    elif area == 'Project management':
        for word in terms[area]:
            if word in text:
                project +=1
        scores.append(project)
        
    elif area == 'Data analytics':
        for word in terms[area]:
            if word in text:
                data +=1
        scores.append(data)
        
    else:
        for word in terms[area]:
            if word in text:
                healthcare +=1
        scores.append(healthcare)

summary = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
print(summary.head())
match = max(quality,operations,supplychain,project,data,healthcare)
if (match==quality):print("Quality/Six sigma")
elif(match==operations):print("Operations management")
elif(match==supplychain):print("Supplychain")
elif(match==project):print("Project Management")
elif(match==data):print("Data Analytics")
elif(match==healthcare):print("Health Care")
else: 
    print("No match")

print(match)
