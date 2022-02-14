from bottle import route, request, run
from json import *
from requests import get
from html.entities import codepoint2name

server_ip = "127.0.0.1"
server_port = 8080

#fonctions
def htmlCoding(stringToCode):     
    return ''.join( '=%s=' % codepoint2name[ord(oneChar)]                    
                  if ord(oneChar) in codepoint2name                    
                  else oneChar for oneChar in stringToCode) 


#chemin racine
@route("/")
def input():
 #ouvrir fichier index.html et l afficher
 return open('htdocs/index.html','rb')

#chemin /route1
@route("/route1.html")
def route1():
 #ouvrir fichier route1.html et l afficher
 return open('htdocs/route1.html','rb')

#chemin /route1 apres avoir rempli le formulaire
@route("/route1.html", method='POST')
def do_route1():
  #recuperer la donnee saisie dans le formulaire
  nameAuthor = request.forms['nameAuthor']

  #resultat de la route /authors/<name>
  r = get(f"http://{server_ip}:{server_port}/authors/{nameAuthor}")
  l1 = r.text
  
  #resulat de la route /search/authors/<searchString> qui se trouve dans le fichier route3.xml
  if(l1.find('false')!=-1):
    r = get(f"http://{server_ip}:{server_port}/search/authors/{nameAuthor}")
    l1 = r.text
    List=l1.split('<br/>')
    file=open('htdocs/route3.html','w')
    del List[0]
    file.writelines('<html><body>')
    for i in List:
      file.writelines(f'''
      <form action = "http://localhost:8081/route1.html" method = "post">
         <p><input type = "text" name = "nameAuthor" value="{i}" /></p>
         <p><input type = "submit" value = "valider" /></p>
      </form>    
      ''')

    file.writelines(' </body> </html>')  
    file.close()
    """
    s=''
    for i in List:
      s=s+f'''<h1><a href="route3.html">{i}</a></h1>'''
    """
    return open('htdocs/route3.html','rb') 
  
  #resultat de la route /authors/<name>/publications
  r = get(f"http://{server_ip}:{server_port}/authors/{nameAuthor}/publications")
  l2=r.text
  
  #resultat de la route /authors/<name>/coauthors
  r = get(f"http://{server_ip}:{server_port}/authors/{nameAuthor}/coauthors")
  l3=r.text
  
  return f'''<h1>{l1} <br /> <br /> <br /><center><p style="background-color:#36A7F0;">Les publications</center> </p> {l2} <br /><center> <p style="background-color:#36A7F0;">Les coauteurs </p> </center> {l3} <br /> </h1>'''



#chemin /route2.html
@route("/route2.html")
def route2():
 #ouvrir fichier route2.html et l afficher
 return open('htdocs/route2.html','rb')

#chemin /route2.html apres avoir rempli le formulaire
@route("/route2.html", method='POST')
def do_route2():
  #recuperer les donnees saisies dans le formualire
  name_origin = request.forms['name_origin']
  name_destination = request.forms['name_destination']
  #resulat de la route /authors/<name_origin>/distance/<name_destination>
  r = get(f"http://{server_ip}:{server_port}/authors/{name_origin}/distance/{name_destination}")
  l = r.text
  return f"<h1>{l}</h1>"




run(host='localhost', port=8081)