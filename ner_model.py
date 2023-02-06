import spacy

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Create a new NER pipeline
ner = nlp.get_pipe("ner")


# Add the "EDUCATION" entity label to the NER pipeline
ner.add_label("EDUCATION")

# Annotated training data
training_data = [
    ("Bachelor of Technology in Computer Science", {"entities": [(0, 34, "EDUCATION")]}),
    ("Indian Institute of Technology, Delhi", {"entities": [(0, 33, "EDUCATION")]}),
    ("MBA (Finance), Kakatiya University",{"entities":[(0,31,"EDUCATION")]}),
    ("Osmania University Hyderabad (AP), India",{"entities":[(0,36,"EDUCATION")]}),
    ("Bachelor Of commerce (B. Com) From Mangalore University",{"entities":[(0,48,"EDUCATION")]})    ,
    ("B.Tech in Computer Science & Engineering from Madan Mohan Malaviya Engineering. College, Gorakhpur, Uttar Pradesh.",{"entities":[(0,100,"EDUCATION")]}),
    ("2008: BE (EEE) from Anna University in Tamil Nadu",{"entities":[(0,41,"EDUCATION")]}),
    ("B.Com Computer application from Sri Venkateswara University, Tirupati, AP",{"entities":[(0,65,"EDUCATION")]}),
    ("MBA From Sikkim Manipal University (Finance and Marketing) in 2009",{"entities":[(0,57,"EDUCATION")]}),
    ("MBA From Sikkim Manipal University (Finance and Marketing) in 2009",{"entities":[(0,57,"EDUCATION")]})
    # Add more training data examples...
]
training_data = [spacy.util.minibatch(
    [nlp.make_doc(text) for text, annotations in training_data],
    [annotations for text, annotations in training_data]
)]
training_data = list(training_data)
for batch in training_data:
    nlp.update(batch[0], batch[1], drop=0.2)
# Start the training
nlp.begin_training()
# for i in range(10):
    # for text, annotations in training_data:
        # nlp.update([text], [annotations], drop=0.2)

# Save the trained NER model
nlp.to_disk("nermodel")
