from requests import *
from json import *
import unittest




class TestAPIMethods(unittest.TestCase):
    server_ip, server_port = '127.0.0.1', 8080
    #tester la premiere route /authors/<name>
    def test_authors_name(self):
        #on recupere le resultat de la route
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Sébastien Baey")
        l = r1.text
        #le resultat attendu
        waitedResult='''<center> <p style="background-color:#36A7F0;"> <font size="+30">Sébastien Baey</font></center></p> <br /> Nombre de publications : 17 <br /> Nombre de coauteurs : 22'''
        self.assertEqual(l, waitedResult)
        #on recupere le resultat de la route
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Olivier Fourmaux")
        l = r1.text
        #le resultat attendu
        waitedResult='''<center> <p style="background-color:#36A7F0;"> <font size="+30">Olivier Fourmaux</font></center></p> <br /> Nombre de publications : 36 <br /> Nombre de coauteurs : 36'''
        self.assertEqual(l, waitedResult)

    #tester la deuxieme route /authors/<name>/publications
    def test_authors_name_publications(self):
        #on recupere le resultat de la route
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Aadrika A/publications")
        l = r1.text
        #le resultat attendu
        waitedResult='''<table border="3" cellpadding="10" cellspacing="1" width="50%" style="margin-right:auto;margin-left:auto"> <tr><td>Impact of Dietary Habits and Opinionated Lifestyle during COVID-19 Pandemic : A Case Study on Engineering Students.</td></tr></table>'''
        self.assertEqual(l, waitedResult)
        #on recupere le resultat de la route
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Espen Aarseth/publications")
        l = r1.text
        #le resultat attendu
        waitedResult='''<table border="3" cellpadding="10" cellspacing="1" width="50%" style="margin-right:auto;margin-left:auto"> <tr><td>An Ontological Meta-Model for Game Research.</td></tr><tr><td>A narrative theory of games.</td></tr><tr><td>A multidimensional typology of games.</td></tr><tr><td>Challenges for game addiction as a mental health diagnosis.</td></tr><tr><td>Computer Game Studies, Year One.</td></tr><tr><td>From Hunt the Wumpus to EverQuest: Introduction to Quest Theory.</td></tr><tr><td>Game Studies: How to play - Ten play-tips for the aspiring game-studies scholar.</td></tr><tr><td>Game History: A special issue.</td></tr><tr><td>Game Classification as Game Design: Construction Through Critical Analysis.</td></tr><tr><td>I Fought the Law: Transgressive Play and The Implied Player.</td></tr><tr><td>Just Games.</td></tr><tr><td>Ludic Zombies: An Examination of Zombieism in Games.</td></tr><tr><td>Meta-Game Studies.</td></tr><tr><td>Mapping the game landscape: Locating genres using functional classification.</td></tr><tr><td>Meet Death Jr.: The culture and business of cross-media productions.</td></tr><tr><td>Port or conversion? An ontological framework for classifying game versions.</td></tr><tr><td>Proceedings of the 8th International Conference on the Foundations of Digital Games, FDG 2013, Chania, Crete, Greece, May 14-17, 2013.</td></tr><tr><td>The game itself?: Towards a Hermeneutics of Computer Games.</td></tr><tr><td>The Battle for Open Access Publishing - And how it affects YOU.</td></tr><tr><td>The Word Game: The ontology of an undefinable object.</td></tr><tr><td>Theorizing for design: The case for pure theory.</td></tr><tr><td>The Dungeon and the Ivory Tower: Vive La Difference ou Liaison Dangereuse?</td></tr></table>'''
        self.assertEqual(l, waitedResult)

    #tester la troisieme route /authors/<name>/coauteurs
    def test_authors_name_coauthors(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Wael Abbas/coauthors")
        l = r1.text
        #le resultat attendu
        waitedResult='''<table border="3" cellpadding="10" cellspacing="1" width="50%" style="margin-left:auto;margin-right:auto" > <tr><td>Ahmed Adel Aly</tr></td><tr><td>Hesham M. El-Badawy</tr></td><tr><td>Hussein ElAttar</tr></td></table>'''
        self.assertEqual(l, waitedResult)
        #on recupere le resultat de la route
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Mohammed Ahmed/coauthors")
        l = r1.text
        #le resultat attendu
        waitedResult='''<table border="3" cellpadding="10" cellspacing="1" width="50%" style="margin-left:auto;margin-right:auto" > <tr><td>Ala I. Al-Fuqaha</tr></td><tr><td>Alaa AlZoubi</tr></td><tr><td>Ammar Rayes</tr></td><tr><td>Azhin Tahir Sabir</tr></td><tr><td>Frank Kirchner</tr></td><tr><td>Hongbo Du</tr></td><tr><td>Layth Al-Gebory</tr></td><tr><td>Mohsen Guizani</tr></td><tr><td>Mrinal Khanvilkar</tr></td><tr><td>Naseer Al-Jawad</tr></td><tr><td>Nayyef Talib</tr></td><tr><td>Yong-Ho Yoo</tr></td></table>'''
        self.assertEqual(l, waitedResult)

    #tester la quatrieme route /search/authors/<searchString>
    def test_search_authors_searchstring(self):
        #on recupere le resultat de la route
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Chennubhotla")
        l = r1.text
        #le resultat attendu
        waitedResult='''<br/>Chennubhotla S. Chakravarthy<br/>Chakra Chennubhotla<br/>S. Chakra Chennubhotla<br/>Tejaswi Chennubhotla'''
        self.assertEqual(l, waitedResult)
       #on recupere le resultat de la route
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Tixeuil")
        l = r1.text
        #le resultat attendu
        waitedResult='''<br/>Sébastien Tixeuil'''
        self.assertEqual(l, waitedResult)
        

    def test_distance_authors(self):
        #on recupere le resultat de la route
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Takumi Miyoshi/distance/Kyoko Yamori")
        l = r1.text
        #le resultat attendu
        waitedResult='''<p style="background-color:#36A7F0;"> <font size="+70">La distance entre les deux auteurs Takumi Miyoshi et Kyoko Yamori est : 1</font></p>'''
        self.assertEqual(l, waitedResult)
    


if __name__ == '__main__':
    unittest.main()