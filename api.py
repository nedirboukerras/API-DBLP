from itertools import count
from re import S
import requests
from bottle import *
from lxml import etree as ET
import html.parser
from html.entities import codepoint2name
from bs4 import BeautifulSoup

#fonctions
def htmlCoding(stringToCode):     
    return ''.join( '=%s=' % codepoint2name[ord(oneChar)]                    
                  if ord(oneChar) in codepoint2name                    
                  else oneChar for oneChar in stringToCode) 


#cette fonction a pour but d adapter les accents au format html
def accent(string):
    #accent aigu
    if(string.find('Ã©')!=-1):
        return string.replace('Ã©',htmlCoding('é'))
    
    #accent grave
    if(string.find('Ã¨')!=-1):
        return string.replace('Ã¨',htmlCoding('è'))
    
    if(string.find('Ã¹')!=-1):
        return string.replace('Ã¹',htmlCoding('ù'))
    
     
    #accent circonflexe
    if(string.find('Ã¢')!=-1):
        return string.replace('Ã¢',htmlCoding('â'))
    
    if(string.find('Ãª')!=-1):
        return string.replace('Ãª',htmlCoding('ê'))
        

    if(string.find('Ã®')!=-1):
        return string.replace('Ã®',htmlCoding('î'))
    
    if(string.find('Ã´')!=-1):
        return string.replace('Ã´',htmlCoding('ô'))


    if(string.find('Ã»')!=-1):
        return string.replace('Ã»',htmlCoding('û'))
     
    #o dans le e
    if(string.find('Å')!=-1):
        return string.replace('Å',htmlCoding('œ'))
     
    return(string)

#cette fonction permet d afficher les accents sur une page web
def beautifulWebDisplay(string):
        #accent aigu
    if(string.find('Ã©')!=-1):
        return string.replace('Ã©','é')
    
    #accent grave
    if(string.find('Ã¨')!=-1):
        return string.replace('Ã¨','è')
    
    if(string.find('Ã¹')!=-1):
        return string.replace('Ã¹','ù')
    
     
    #accent circonflexe
    if(string.find('Ã¢')!=-1):
        return string.replace('Ã¢','â')
    
    if(string.find('Ãª')!=-1):
        return string.replace('Ãª','ê')
        

    if(string.find('Ã®')!=-1):
        return string.replace('Ã®','î')
    
    if(string.find('Ã´')!=-1):
        return string.replace('Ã´','ô')


    if(string.find('Ã»')!=-1):
        return string.replace('Ã»','û')
     
    #o dans le e
    if(string.find('Å')!=-1):
        return string.replace('Å','œ')
     
    return(string)


#ouvrir le fichier dblp xml
file="dblp.xml"

#construire l arbre xml
p=ET.XMLParser(recover=True)
tree=ET.parse(file,parser=p)
root=tree.getroot()

#premiere route qui prend un nom d auteur du format : Prenom Nom
@route('/authors/<name>')
def auteurs(name):
    try:
        #en cas de presence d accents dans le nom pour l afficher correctement  
        showName=beautifulWebDisplay(name)
        #adapter les accents pour un traitement html
        name=accent(name)
        #transfomer le nom en une liste pour facilter le traitement
        tempListe=name.split(' ')
        #si taille nom> 2 mots, chercher le nom de le fichier xml
        if(len(tempListe)>2):
                name=accent(name)
                #expression reguliere pour verfier la validité d un nom
                if(re.search("^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",name)):
                    #compteur de nombre de publications
                    cptP=0
                    #compteur de nombre d auteurs
                    cptC=0
                    #parcourir l arbre xml
                    for child in root: 
                        for x in child:
                            #adapter les accents
                            realName=html.unescape(str(x.text))
                            #si la balise contient un auteur et c est l auteur qu on cherche alors
                            if(x.tag=='author' and realName==name):
                                #incrementer le compteur de publications
                                cptP=cptP+1
                                for y in child:
                                   if(y.tag=='author' and html.unescape(str(y.text))!=realName):
                                       #incrementer le compteur de coauteurs
                                       cptC=cptC+1        
                    return '''<center> <p style="background-color:#36A7F0;"> <font size="+70">'''+name+"</font></p></center>  Nombre de publications : "+str(cptP)+" <br /> Nombre de coauteurs : "+str(cptC)
                else: 
                    return '<html><head>false</head><body> Error: 404 Not Found</body></html>'
        #sinon cad la longeur du nom ne depasse pas 2 mots pour recuperer les fichiers xml du web
        #adapter le nom au format necessaire cad Nom:Prenom
        name=tempListe[1]+' '+tempListe[0]
        name=name.replace(" ",":")
        NameAccent=htmlCoding(name)
        #URL pour recuperer le fichier xml de l auteur demende
        URL = 'http://dblp.uni-trier.de/pers/xx/'+name[0].lower()+'/'+NameAccent    
        tree = requests.get(URL)
        xmlFile = ET.fromstring(tree.content)
        #les balises <r> contiennent les publications
        nbrp = len(xmlFile.findall('r'))
        #les balises <coauthors> contiennet les coateurs plus precisiment l attribut n de ces balises
        nbrc = int(xmlFile.find('coauthors').attrib['n'])

        return '''<center> <p style="background-color:#36A7F0;"> <font size="+30">'''+showName+"</font></center></p> <br /> Nombre de publications : "+str(nbrp)+" <br /> Nombre de coauteurs : "+str(nbrc)
    except:
                
        return '<html><head>false</head><body> Error: 404 Not Found</body></html>' 

#Deuxieme route qui prend un nom d auteur au format Prenom Nom pour afficher ses publications
@route('/authors/<name>/publications')
def publications(name):
    try:
        #adapter les accents pour un traitement html
        name=accent(name)
        #transfomer le nom en une liste pour facilter le traitement
        tempListe=name.split(' ')
        #si taille nom> 2 mots, chercher le nom de le fichier xml
        if(len(tempListe)>2):
                name=accent(name)
                #liste qui va contenir les publications de l auteur
                List=[]
                #parcourir l arbre xml
                for child in root: 
                    for x in child:
                        #adapter les accents
                        realName=html.unescape(str(x.text))
                        #si on est bien au niveau de l auteur qu on cherche
                        if(x.tag=='author' and realName==name):
                            for y in child:
                                #les titres de l auteur
                                if(y.tag=='title'):
                                    List.append(y.text)
                                    #trier les publications par ordre alphabetique
                                    List = sorted(List, key=lambda name: name[0])
                Titre='''<table border="3" cellpadding="10" cellspacing="1" width="50%" style="margin-right:auto;margin-left:auto"> '''
                
                #le resultat est une liste donc si la longueur de la liste depasse 100 faut limiter l affichage a 100
                if(len(List)>100):
                    for i in range(100):
                        i=0
                        Titre+='<tr><td>'+List[i]+'</td></tr>' 
                    Titre+='</table>'
                else:
                    for i in List:
                        Titre+='<tr><td>'+i+'</td></tr>' 
                    Titre+='</table>'

                return(Titre)
        #sinon cad la longeur du nom ne depasse pas 2 mots pour recuperer les fichiers xml du web
        #adapter le nom au format necessaire cad Nom:Prenom
        name=tempListe[1]+' '+tempListe[0]
        name=name.replace(" ",":")
        NameAccent=htmlCoding(name)
        #URL pour recuperer le fichier xml de l auteur demende
        URL = 'http://dblp.uni-trier.de/pers/xx/'+name[0].lower()+'/'+NameAccent
        file = requests.get(URL)
        xml_res = ET.fromstring(file.content)
        #liste qui va contenir les publications
        publications = []
        #la balise r contient comme fils la balise titre
        for i in xml_res.findall('r'):
            i=i[0]
            publications.append(i.find('title').text)
            #trier les publications par ordre alphabetique
            publications = sorted(publications, key=lambda name: name[0])
        Titre='''<table border="3" cellpadding="10" cellspacing="1" width="50%" style="margin-right:auto;margin-left:auto"> '''
        #le resultat est une liste donc si la longueur de la liste depasse 100 faut limiter l affichage a 100
        if(len(publications)>100):
            j=0
            for j in range(100):
                Titre+='<tr><td>'+publications[j]+'</td></tr>'
            Titre+='</table>'
        else:
            for j in publications:
                Titre+='<tr><td>'+j+'</td></tr>'
            Titre+='</table>'
        
        return Titre
    except:
        return '<html><body> Error: 404 Not Found </body></html>'  


#Troisieme route qui prend un nom d auteur au format Prenom Nom pour afficher ses coauteurs
@route('/authors/<name>/coauthors')
def coauthors(name):
    try:
        #adapter les accents pour un traitement html
        name=accent(name)
        #transfomer le nom en une liste pour facilter le traitement
        tempListe=name.split(' ')
        #si taille nom> 2 mots, chercher le nom de le fichier xml
        if(len(tempListe)>2):
                name=accent(name)
                #liste qui va contenir les coauteurs de l auteur
                List=[]
                #parcourir l arbre xml
                for child in root: 
                    for x in child:
                        #adapter les accents
                        realName=html.unescape(str(x.text))
                        #si on est bien au niveau de l auteur qu on cherche
                        if(x.tag=='author' and realName==name):
                            for y in child:
                                #les coauteurs de l auteur
                                if(y.tag=='author' and html.unescape(str(y.text))!=realName):
                                    List.append(html.unescape(str(y.text)))
                                    #trier les coauteurs par odre alphabetique
                                    List = sorted(List, key=lambda name: name[0])
                Coauteur='''<table border="3" cellpadding="10" cellspacing="1" width="50%" style="margin-left:auto;margin-right:auto"> '''
                #le resultat est une liste donc si la longueur de la liste depasse 100 faut limiter l affichage a 100
                if(len(List)>100):
                    i=0
                    for i in range(100):
                        Coauteur+='<tr><td>'+List[i]+'</td></tr>' 
                    Coauteur+='</table>'
                else:
                    for i in List:
                        Coauteur+='<tr><td>'+i+'</td></tr>' 
                    Coauteur+='</table>'
                return(Coauteur)
        #sinon cad la longeur du nom ne depasse pas 2 mots pour recuperer les fichiers xml du web
        #adapter le nom au format necessaire cad Nom:Prenom
        name=tempListe[1]+' '+tempListe[0]
        name=name.replace(" ",":")
        NameAccent=htmlCoding(name)
        #URL pour recuperer le fichier xml de l auteur demende
        URL = 'http://dblp.uni-trier.de/pers/xx/'+name[0].lower()+'/'+NameAccent
        file = requests.get(URL)
        tree = ET.fromstring(file.content)
        coauthors = tree.find('coauthors')
        #liste qui va contenir les coauteurs
        resultat = []
        for coau in coauthors.findall('co'):
            resultat.append(coau.find('na').text)
            #trier les coauteurs par odre alphabetique
            resultat = sorted(resultat, key=lambda name: name[0])
        
        string='''<table border="3" cellpadding="10" cellspacing="1" width="50%" style="margin-left:auto;margin-right:auto" > '''
        #le resultat est une liste donc si la longueur de la liste depasse 100 faut limiter l affichage a 100
        if(len(resultat)>100):
            i=0
            for i in range(100):
                string+='<tr><td>'+resultat[i]+'</tr></td>'
            string+='</table>'
        else:
            for i in resultat:
                string+='<tr><td>'+i+'</tr></td>'
            string+='</table>'
        return string
    except:
        return '<html><body>Error: 404 Not Found</body></html>'


#Quatrieme route qui prend une chaine de caracteres comme parametre
@route('/search/authors/<searchString>')
def searchString(searchString):
    #adapter les accents
    searchString=beautifulWebDisplay(searchString)
    #URL qui permet de recuperer le fichier xml des auteurs ayant searchString dans le leurs noms
    URL = 'https://dblp.uni-trier.de/search/author/api?q='+searchString+'&h=1000&format=xml'
    file = requests.get(URL)
    result=[]
    tree = ET.fromstring(file.content)
    #balises hits qui contient comme fils balise author
    hits = tree.find('hits')
    for i in hits:
        for j in i:
            for z in j:
                if(z.tag=="author"):
                    result.append(str(z.text))
                    #trier les auteurs par odre alphabetique
                    result = sorted(result, key=lambda name: name[0])
    s=''
    #le resultat est une liste donc si la longueur de la liste depasse 100 faut limiter l affichage a 100
    if(len(result)>100):
        i=0
        for i in range(100):
            s=s+'<br/>'+result[i]

    else:
        for i in result:
            s=s+'<br/>'+i
    return(s)



#Cinquieme route qui prend deux chaines de caracteres comme arguemnt
@route('/authors/<name_origin>/distance/<name_destination>')
def distance(name_origin,name_destination):
    try:
        #en cas de presence d accents dans le nom pour l afficher correctement 
        showNameOrigin=beautifulWebDisplay(name_origin)
        showNameDistination=beautifulWebDisplay(name_destination)
        #transfomer le nom en une liste pour facilter le traitement
        tempListe=name_origin.split(' ')
        #adapter le nom au format necessaire cad Nom:Prenom
        name=tempListe[1]+' '+tempListe[0]
        name=name.replace(" ",":")
        NameAccent=htmlCoding(name)
        #URL pour recuperer le fichier xml de l auteur demende
        URL = 'http://dblp.uni-trier.de/pers/xx/'+name[0].lower()+'/'+NameAccent    
        file = requests.get(URL)
        root=ET.fromstring(file.content)
        cpt=0
        #liste qui va contenir les coauteurs de maniere recurente
        List=[]
        List.append(name_origin)
        #parcours
        for i in List:
            cpt=cpt+1
            for x in root:
                for y in x:
                    for z in y:
                        #la balise qui contient les coauteurs
                        if(z.tag=='na'):
                            if(z.text==name_destination):
                                return '''<p style="background-color:#36A7F0;"> <font size="+70">La distance entre les deux auteurs '''+str(showNameOrigin)+" et "+str(showNameDistination)+" est : "+str(cpt)+'''</font></p>'''
                            
                            List.append(str(z.text))                
            #refaire jusqu a trouver correspondance
            name=List[0]
            del List[0]
            tempListe=name.split(' ')
            if(len(tempListe)==2 and name.find("-")==-1):
                
                name=tempListe[1]+' '+tempListe[0]
                name=name.replace(" ",":")
                NameAccent=htmlCoding(name)
                URL = 'http://dblp.uni-trier.de/pers/xx/'+name[0].lower()+'/'+NameAccent    
                file = requests.get(URL)
                root=ET.fromstring(file.content)
            if(name_destination in List):
                return '''<p style="background-color:#36A7F0;"> <font size="+70">La distance entre les deux auteurs '''+str(showNameOrigin)+" et "+str(showNameDistination)+" est : "+str(cpt)+'''</font></p>'''
            if(cpt==100):
                return '<html><body>Error: Algorithm Too Complex</body></html>'
               
    except:
        return '<html><body>Error: 404 Not Found</body></html>'

run(host='localhost', port=8080,reloader=True)