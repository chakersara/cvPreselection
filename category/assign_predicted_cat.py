from statistics import mode
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
import pickle 
import numpy as np
import json

def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

df=pd.read_csv("../cleaned_resume.csv")
    

word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    stop_words=["english","french"],
    max_features=1500
)

required_text=df.cleaned_resume.values


word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    stop_words=["english","french"],
    max_features=1500
)


word_vectorizer.fit(required_text)

def predict(resumeTxt):
    global word_vectorizer
    model=pickle.load(open("category_model.pkl","rb"))
    categories=json.load(open("code_category.json"))
    resume=word_vectorizer.transform(np.array([
        cleanResume(resumeTxt)
    ]))
    return categories[
            str(model.predict(resume)[0])]
        







