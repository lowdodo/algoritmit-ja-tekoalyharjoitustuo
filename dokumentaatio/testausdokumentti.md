# unittestit

toistaiseksi unittestejä on tehty ai, peli ja gameloopeille. Testit voi suorittaa kirjoittamalla pytest src terminaaliin juuressa, kattavuuden saa coverage report -m. yhteiskattavuus tällähetkellä on 97%

## Name Stmts Miss Cover Missing

src/ai.py 62 3 95% 41, 58, 64
src/game2048.py 74 0 100%
src/gameloop.py 61 2 97% 88-89

---

TOTAL 197 5 97%

## game_test.py – Pelilogiikka

Testattu: rivien liukuminen ja yhdistyminen (slide_and_merge)

Esim. syöte [2, 2, 0, 2] → tulos [4, 2, 0, 0]

Testattu: eri suuntiin liikkuminen (move("left"|"right"|"up"|"down"))

Tarkistetaan, että laatat yhdistyvät oikein ja uusi tila vastaa odotettua.

Testattu: pelin loppumisen tunnistus (is_game_over)

Täynnä oleva taulukko ilman siirtomahdollisuutta palauttaa True.

Tilanteet, joissa siirto on vielä mahdollinen (esim. vierekkäiset samanarvoiset laatat), palauttavat False.

Testattu: uuden laatan lisäys (add_tile)

Varmistetaan, että uusi laatta lisätään tyhjään ruutuun eikä vanhat arvot katoa.

Syötteet: käsin asetetut 4×4-taulukot eri yhdistelminä.
Tarkistus: pelin sisäinen tila (board) vastaa odotettua.

## ai_test.py – Tekoäly (AI2048)

Testattu: best_move() palauttaa aina kelvollisen suunnan (left/right/up/down) tai None, jos peli on ohi.

Testattu: expectiminimax() palauttaa numeerisen arvon ja ei kaadu virhetilanteissa.

Testattu: tilanteet, joissa ei ole siirtoja (täysi lauta ilman yhdistymistä) – AI palauttaa None.

Testattu: tilanteet, joissa on vain yksi järkevä siirto – AI valitsee sen (esim. vasen yhdistäminen).

Testattu: AI toimii myös oletussyvyydellä (depth=3) ilman virheitä.

Syötteet: eri pelitiloja, joissa tekoälyn on tehtävä päätös siirrosta.
Tarkistus: tekoäly palauttaa oikean siirron ja laskettu arvo on numeerinen.

## loop_test.py – Pelisilmukka ja tapahtumien käsittely

Testattu: nuolinäppäimillä tehtävät siirrot (vasen, oikea, ylös, alas).

Simuloidaan Pygamen tapahtumia (pygame.KEYDOWN) ja varmistetaan, että pelilauta päivittyy oikein.

Testattu: tekoälyn kytkeminen päälle ja pois (toggle_ai ja hiiren klikkaus painikkeeseen).

Hiiritapahtuma (pygame.MOUSEBUTTONDOWN) vaihtaa tekoälyn tilaa ja piirtää laudan uudelleen.

Testattu: tekoälyn vuoro pääsilmukassa.

Kun AI on päällä, ai.best_move() kutsutaan ja palautettua suuntaa käytetään siirtoon.

Testattu: väärien suuntien käsittely.

apply_move("invalid_direction") ei muuta pelitilaa.

Testattu: pääsilmukka päättyy hallitusti pygame.QUIT-tapahtumalla.

Syötteet: simuloidut Pygame-tapahtumat (KEYDOWN, MOUSEBUTTONDOWN, QUIT).
Tarkistus: pelin tila (board), tekoälyn tila (ai_enabled) ja ruudunpäivitys (draw_board kutsuttu).
