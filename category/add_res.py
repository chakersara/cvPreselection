import sys
sys.path.insert(1,'extract_resume')

import extract
import csv
import re

def removePage(text):
    res=text.split("\n")
    reg = re.compile("Page . of .")
    pl= list(filter(reg.match, res)) 
    for page in pl: 
        res.pop(res.index(page))
    return "\n".join(res)


def addcsv(category,paths,csvFile):
    csvWriter=csv.writer(csvFile)
    for path in paths:
        try:
            text=extract.ResExtract(path).text
            text=removePage(text)
            csvWriter.writerow([category,text])
        except:
            print(paths.index(path))
            continue


js=['/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/1553041042-mariusz-bachurski-developer-resume.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/amir-ardalan-resume.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/Ankit_3_yrs_react_node_mindtree.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/CV-Alexander-Zubko-Mobile-Web.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/cv.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/harish4.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/ichrak_azzouz.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/islem_abid.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/Joshua_Dick-Resume.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/Kashish Jain - Resume.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/kellie_petersen_resume.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/Khalil-Stemmler-Resume-2019.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/maher_fadhlaoui.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/Rajesh-Royal-ReactJS-developer-CV.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/resume-2020.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/resume2.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/Resume-Of-Node.js-Developer.docx-1.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/Resume-Of-React-Native-Developer.docx.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/resume.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/TcallsenResume2020v0710-aem-react.pdf', '/home/sarra/Documents/projects/projetGlsi2/Resume_Job_Description/linkedin/JavaScript Developer/Terrence-Crossdale-Resume.pdf']



with open("resume.csv","a") as csvFile:
    addcsv("JavaScript Developer",js,csvFile)