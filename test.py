import spacy

# Load the spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Load the resume text
resume_text = "Raman Kumar\n12/3, New Delhi, India\nramank@email.com\n(111) 222-3333\n\nSummary\nHighly motivated and detail-oriented software engineer with 5 years of experience developing applications in a variety of industries.\n\nEducation\nBachelor of Technology in Computer Science\nIndian Institute of Technology, Delhi\nGraduated May 2013\n\nWork Experience\nSoftware Engineer\nDEF Ltd.\nJune 2018 - Present\n- Developed and maintained software applications for clients in the finance and healthcare industries\n- Implemented new features and improved system performance through regular software updates\n\nSoftware Developer\nGHI Pvt. Ltd.\nMay 2013 - June 2018\n- Designed and implemented software applications for clients in the retail and manufacturing industries\n- Collaborated with cross-functional teams to identify and resolve software issues\n\nSkills\n- Python\n- Java\n- SQL\n- Agile methodologies\n"

# Run the NER model on the resume text
doc = nlp(resume_text)

# Extract named entities from the document
entities = {}
for ent in doc.ents:
    if ent.label_ not in entities:
        entities[ent.label_] = []
    entities[ent.label_].append(ent.text)

# Store the extracted information in a structured format
resume_data = {
    "Name": entities.get("PERSON", [""])[0],
    "Email": entities.get("EMAIL", [""])[0],
    "Phone": entities.get("PHONE", [""])[0],
    "Education": entities.get("EDUCATION", []),
    "Work Experience": entities.get("ORG", [])
}

# Print the extracted information
print(resume_data)