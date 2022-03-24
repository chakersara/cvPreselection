import docx2txt as d2t
from matplotlib.pyplot import stem
from pdfminer.high_level import extract_text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from pprint import pprint
import re
from langdetect import detect
import sys
sys.path.append('../category')
sys.path.append('../database')
"""from  assign_predicted_cat import predict"""
from database.data import SkillsData
from nltk.stem import PorterStemmer
from nltk.stem.snowball import FrenchStemmer
import goslate
import string

class ResExtract:
    stopWords=set(stopwords.words("english")).union(set(stopwords.words('french')))
    punctuation=string.punctuation
    countriesFrEn={'afghanistan': 'afghanistan', 'albania': 'albanie', 'algeria': 'algérie', 'andorra': 'andorre', 'angola': 'angola', 'antigua & deps': 'antigua & deps', 'argentina': 'argentine', 'armenia': 'arménie', 'australia': 'australie', 'austria': 'autriche', 'azerbaijan': 'azerbaïdjan', 'bahamas': 'bahamas', 'bahrain': 'bahreïn', 'bangladesh': 'bangladesh', 'barbados': 'barbade', 'belarus': 'bélarus', 'belgium': 'belgique', 'belize': 'belize', 'benin': 'bénin', 'bhutan': 'bhoutan', 'bolivia': 'bolivie', 'bosnia herzegovina': 'bosnie-herzégovine', 'botswana': 'botswana', 'brazil': 'brésil', 'brunei': 'brunei', 'bulgaria': 'bulgarie', 'burkina': 'burkina', 'burundi': 'burundi', 'cambodia': 'cambodge', 'cameroon': 'cameroun', 'canada': 'canada', 'cape verde': 'cap-vert', 'central african rep': 'central african rep', 'chad': 'tchad', 'chile': 'chili', 'china': 'chine', 'colombia': 'colombie', 'comoros': 'comores', 'congo': 'congo', 'congo {democratic rep}': 'congo {république démocratique}', 'costa rica': 'costa rica', 'croatia': 'croatie', 'cuba': 'cuba', 'cyprus': 'chypre', 'czech republic': 'république tchèque', 'denmark': 'danemark', 'djibouti': 'djibouti', 'dominica': 'dominique', 'dominican republic': 'dominicaine (république)', 'east timor': 'timor oriental', 'ecuador': 'équateur', 'egypt': 'égypte', 'el salvador': 'el salvador', 'equatorial guinea': 'guinée équatoriale', 'eritrea': 'érythrée', 'estonia': 'estonie', 'ethiopia': 'éthiopie', 'fiji': 'fidji', 'finland': 'finlande', 'france': 'france', 'gabon': 'gabon', 'gambia': 'gambie', 'georgia': 'géorgie', 'germany': 'allemagne', 'ghana': 'ghana', 'greece': 'grèce', 'grenada': 'grenade', 'guatemala': 'guatemala', 'guinea': 'guinée', 'guinea-bissau': 'guinée-bissau', 'guyana': 'guyana', 'haiti': 'haïti', 'honduras': 'honduras', 'hungary': 'hongrie', 'iceland': 'islande', 'india': 'inde', 'indonesia': 'indonésie', 'iran': 'iran', 'iraq': 'irak', 'ireland': 'irlande', 'palestine': 'palestine', 'italy': 'italie', 'ivory coast': "côte d'ivoire", 'jamaica': 'jamaïque', 'japan': 'japon', 'jordan': 'jordanie', 'kazakhstan': 'kazakhstan', 'kenya': 'kenya', 'kiribati': 'kiribati', 'korea north': 'corée du nord', 'korea south': 'corée du sud', 'kosovo': 'kosovo', 'kuwait': 'koweït', 'kyrgyzstan': 'kirghizistan', 'laos': 'laos', 'latvia': 'lettonie', 'lebanon': 'liban', 'lesotho': 'lesotho', 'liberia': 'liberia', 'libya': 'libye', 'liechtenstein': 'liechtenstein', 'lithuania': 'lituanie', 'luxembourg': 'luxembourg', 'macedonia': 'macédoine', 'madagascar': 'madagascar', 'malawi': 'malawi', 'malaysia': 'malaisie', 'maldives': 'maldives', 'mali': 'mali', 'malta': 'malte', 'marshall islands': 'marshall (îles)', 'mauritania': 'mauritanie', 'mauritius': 'maurice', 'mexico': 'mexique', 'micronesia': 'micronésie', 'moldova': 'moldavie', 'monaco': 'monaco', 'mongolia': 'mongolie', 'montenegro': 'monténégro', 'morocco': 'maroc', 'mozambique': 'mozambique', 'myanmar, {burma}': 'myanmar, {burma}', 'namibia': 'namibie', 'nauru': 'nauru', 'nepal': 'népal', 'netherlands': 'pays-bas', 'new zealand': 'nouvelle-zélande', 'nicaragua': 'nicaragua', 'niger': 'niger', 'nigeria': 'nigeria', 'norway': 'norvège', 'oman': 'oman', 'pakistan': 'pakistan', 'palau': 'palau', 'panama': 'panama', 'papua new guinea': 'papouasie-nouvelle-guinée', 'paraguay': 'paraguay', 'peru': 'pérou', 'philippines': 'philippines', 'poland': 'pologne', 'portugal': 'portugal', 'qatar': 'qatar', 'romania': 'roumanie', 'russian federation': 'fédération de russie', 'rwanda': 'rwanda', 'st kitts & nevis': 'st kitts & nevis', 'st lucia': 'sainte-lucie', 'saint vincent & the grenadines': 'saint vincent et les grenadines', 'samoa': 'samoa', 'san marino': 'saint-marin', 'sao tome & principe': 'sao tome & principe', 'saudi arabia': 'arabie saoudite', 'senegal': 'sénégal', 'serbia': 'serbie', 'seychelles': 'seychelles', 'sierra leone': 'sierra leone', 'singapore': 'singapour', 'slovakia': 'slovaquie', 'slovenia': 'slovénie', 'solomon islands': 'salomon (îles)', 'somalia': 'somalie', 'south africa': 'afrique du sud', 'south sudan': 'sud-soudan', 'spain': 'espagne', 'sri lanka': 'sri lanka', 'sudan': 'soudan', 'suriname': 'suriname', 'swaziland': 'swaziland', 'sweden': 'suède', 'switzerland': 'suisse', 'syria': 'syrie', 'taiwan': 'taïwan', 'tajikistan': 'tadjikistan', 'tanzania': 'tanzanie', 'thailand': 'thaïlande', 'togo': 'togo', 'tonga': 'tonga', 'trinidad & tobago': 'trinité-et-tobago', 'tunisia': 'tunisie', 'turkey': 'turquie', 'turkmenistan': 'turkménistan', 'tuvalu': 'tuvalu', 'uganda': 'ouganda', 'ukraine': 'ukraine', 'united arab emirates': 'emirats arabes unis', 'united kingdom': 'royaume-uni', 'united states': 'états-unis', 'uruguay': 'uruguay', 'uzbekistan': 'ouzbékistan', 'vanuatu': 'vanuatu', 'vatican city': 'vatican city', 'venezuela': 'venezuela', 'vietnam': 'vietnam', 'yemen': 'yémen', 'zambia': 'zambie', 'zimbabwe': 'zimbabwe'}

    def __init__(self,path) :
        self.path=path

    def __docxExtract(self):
        try:
            txt=d2t.process(self.path)
            return  txt.replace("\t"," ") if txt else None
        except:
            return None

    def __pdfExtract(self):
        return extract_text(self.path).replace("\t"," ")

    @property
    def text(self):
        fileType=self.path.split('.')[-1]
        if fileType == 'pdf' :
            return self.__pdfExtract()
        if fileType == "docx":
            return self.__docxExtract()

    @property
    def language(self):
        return detect(self.text)

    @property
    def category(self):
        pass
    @property
    def filtered_token(self):
        txt_tok=word_tokenize(self.text)
        return {w for w in txt_tok if w not in self.stopWords.union(self.punctuation)}

    @property 
    def composed_filtered_token(self):
        return set(map(' '.join, nltk.everygrams(self.filtered_token, 2, 4)))
    
    @property
    def all_filtered_tokens(self):
        return self.filtered_token.union(self.composed_filtered_token)
    
    def __file_list(self,fileName):
        return list(set(map(lambda x:x.strip("\n").lower(),open(fileName).readlines())))

    def __intersection_text_set(self,givenSet):
        oneTofour_token=self.filtered_token.union(self.composed_filtered_token)
        return {elem.lower() for elem in oneTofour_token if elem.lower() in givenSet}

    def __stemmedList(self,toStem):
        return list(map(lambda w: PorterStemmer().stem(w).lower(),toStem))

    def __english_to_french(self,w):
        gs = goslate.Goslate()
        frenchWord = gs.translate(w,'fr')
        return frenchWord

    def getSkills(self):
        skills=SkillsData().allSkillsLower()
        return self.__intersection_text_set(skills)

    def getCountry(self):
        countries_list=self.__file_list("countries.txt")
        stemmed_countries=self.__stemmedList(countries_list)
        stemmed_resume=self.__stemmedList(self.all_filtered_tokens)
        for w in stemmed_resume:
            if w in stemmed_countries:
                country=countries_list[stemmed_countries.index(w)] 
                return  self.countriesFrEn.get(country,country)
        return None

    def getEmail(self):
        return re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",self.text)

    def getPhoneNumber(self):
        return list(set(re.findall("[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]",self.text)))
    
    def __addEducation(self,educList,title,regex,resume):
        if re.compile(regex).findall(resume):
            educList.append(title)

    def getEducation(self):
        res=self.text.lower()
        educ=[]
        self.__addEducation(educ,"Ingénierie","ingéni.* | engineer*",res)
        self.__addEducation(educ,"Licence","bachelor | b?[.]s|licence",res)
        self.__addEducation(educ,"Mastère","mast[eéè]re | master| m?[.]s",res)
        return educ
        
    def getCategory(self):
        return predict(self.text)
        
if __name__=="__main__":
    a=ResExtract("/home/sarra/Documents/projects/projetGlsi2/app/static/resumes/pdf_docx/Chaker_Sarra.pdf")
    print(a.getPhoneNumber())
