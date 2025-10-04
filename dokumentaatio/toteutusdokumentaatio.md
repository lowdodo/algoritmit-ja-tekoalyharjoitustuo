# Ohjelman toteutus

## Ohjelmassa on seuraava rakenne:
- game2048.py ssä luokka Game2048, pelin rakennetta varten
- gameloop.py ssä luokka GameLoop, pelin pyöritykseen
- ai.py ssä luokka AI2048, tekoälyyn
- ui.py ssä luokka UI, kaikki visuaalisuus ja pelin rakenne

Gameloop luo peli-olion. Aluksi pelissä, ja gameloop pitää ai_enabled Falsena. On vain manuaalinen peli, eli pelaaja ohjailee sitä nuolinäppäimin. Mikäli pelaaja painaa käyttöliittymästä nappia, ai_enabled = True, jolloin tekoäly instassi kutsutaan. Sen jälkeen tekoäly ratkaisee pelin, ellei sitä keskeytetä muuttamalla se takaisin manuaaliseksi.

## Saavutetut aika- ja tilavaativuudet
analyysi tulossa

## Työn mahdolliset puutteet ja parannusehdotukset
Tällähetkellä työn ollessa kesken:
- parempi heurestiikka
- tuloksen ilmentäminen


## Laajojen kielimallien käyttö
- Olen käyttänyt ChatGPT esittämällä sille error-viestejä ja debuggauksessa kysynyt, minne kaikkialle koodia kannattaisi asettaa millainenkin debugaus viesti. Tuloksia olen sitten laittanut sille, ja sen perusteella etsinyt virhettä. 
Muita kielimalleja en ole käyttänyt

## Merkitykselliset lähteet: 
- Kurssin luentomateriaalit
- [2048 AI Research Paper: *AI Plays 2048* (Nie, Hou, An)]
- Wikipedia-artikkelit aiheista: _Minimax_, _Expectiminimax_
- [geeksforgeeks expectiminamax for ai](https://www.geeksforgeeks.org/artificial-intelligence/expectimax-search-algorithm-in-ai/)