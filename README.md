# 🎮 Maze Chomp

A complete Pac-Man-style game built with Python and Pygame. Features full game mechanics including power-pellets, ghost AI with state machines, pathfinding, and collision detection.

![Game Status](https://img.shields.io/badge/Status-Playable-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-orange)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/maze_chomp.git
cd maze_chomp

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## 🎯 Game Preview

**Maze Chomp** is a fully functional Pac-Man clone featuring:
- 🟡 Classic Pac-Man gameplay with modern Python implementation
- 👻 Smart ghost AI with 4 different personalities (Blinky, Pinky, Clyde, Inky)
- ⚡ Power-pellets that turn ghosts blue and edible
- 🎵 Sound effects and smooth animations
- 📈 Progressive difficulty across 6 levels
- 🏆 Complete scoring system with bonus points

## Ominaisuudet

### Vaihe 1 (MVP)
- **Ruudukkopohjainen liike**: Pelaaja liikkuu 16x16 pikselien ruudukossa
- **Seinätörmäykset**: Ei voi liikkua seinien läpi
- **Pisteiden syönti**: Kerää pellettejä (10 pistettä) ja power-pellettejä (50 pistettä)
- **HUD**: Näyttää pisteet, elämät ja tason numeron
- **Tunneli**: Liiku vasemmasta reunasta oikeaan ja päinvastoin
- **Tason eteneminen**: Kun kaikki pelletit syöty, siirrytään seuraavaan tasoon (5% nopeampi)

### Vaihe 2 (Täydellinen pelimekaniikka)
- **Power-pelletit**: Käynnistävät FRIGHTENED-tilan kaikille haamuille
- **Haamujen tilakone**: SCATTER ↔ CHASE globaali ajastin, FRIGHTENED power-pelletistä, EATEN kun syöty
- **Reitinhaku**: BFS-ruudukossa seuraava askel kohti kohdetta
- **Törmäyslogiikka**: Pelaaja vs haamu - normaalisti kuolema, FRIGHTENED-tilassa haamu syödään
- **HUD päivittyy**: Pisteet, elämät, taso, jäljellä olevat pelletit, nykyinen moodi
- **Haamujen persoonat**: Blinky (jahtaa suoraan), Pinky (4 ruutua eteenpäin)
- **Ghost-ketjupisteet**: 200→400→800→1600 ketjussa, resetoi FRIGHTENED loppuessa

## 📦 Installation

### Method 1: Quick Start (Recommended)
```bash
git clone https://github.com/yourusername/maze_chomp.git
cd maze_chomp
pip install -r requirements.txt
python main.py
```

### Method 2: With Virtual Environment
```bash
git clone https://github.com/yourusername/maze_chomp.git
cd maze_chomp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## 🎮 How to Play

## Ohjaimet

- **Liikkuminen**: Nuolinäppäimet tai WASD
- **Tauko**: SPACE
- **Valikko/Poistu**: ESC
- **Valitse/Jatka**: ENTER

## Projektirakenne

```
maze_chomp/
├── main.py              # Pääsilmukka ja pelin alustus
├── constants.py         # Vakiot (värit, mitat, nopeudet)
├── game_state.py        # Tilakone (menu, pelaaminen, game over)
├── level.py             # Tason lataus ja hallinta
├── player.py            # Pelaajan liike ja logiikka
├── ghost.py             # Haamujen placeholder-AI
├── hud.py               # Käyttöliittymän näyttö
├── utils.py             # Apufunktiot ruudukkokäsittelyyn
├── level1/
│   └── level1.txt       # ASCII-kartta
├── requirements.txt     # Python-riippuvuudet
└── README.md           # Tämä tiedosto
```

## Koodin rakenne

### Moduulit

- **constants.py**: Kaikki pelin vakiot (värit, mitat, nopeudet, pisteet)
- **utils.py**: Apufunktiot koordinaattimuunnoksiin ja vektorilaskentaan
- **level.py**: ASCII-kartan lataus, seinätarkistukset, pellettien hallinta
- **player.py**: Pelaajan syötteiden käsittely ja liike ruudukossa
- **ghost.py**: Haamujen placeholder-AI ja liike (valmistelu tulevaa AI:ta varten)
- **hud.py**: Pisteiden, elämien ja muun UI:n piirtäminen
- **game_state.py**: Tilakone eri pelitiloille (menu, pelaaminen, game over)
- **main.py**: Pääsilmukka, Pygame-alustus ja tapahtumien käsittely

### Teknisiä yksityiskohtia

- **Ruudukko**: 16x16 pikselin ruudut, skaalattu 4x renderöintiin (64x64 pikseliä näytöllä)
- **Delta-aika**: Kaikki liike käyttää delta-aikaa tasaisen pelituntuman varmistamiseksi
- **Koordinaattijärjestelmät**: Sekä ruutukoordinaatit (logiikka) että pikselikoordinaatit (renderöinti)
- **Suunnanvaihto**: Tapahtuu vain ruudun keskellä, snap-toiminnolla
- **Törmäystarkistus**: Tarkistaa seuraavan ruudun ennen liikkumista

## Kartan merkitykset (level1/level1.txt)

- `#` = Seinä
- `.` = Pelletti (10 pistettä)
- `o` = Power-pelletti (50 pistettä)
- `P` = Pelaajan aloituspaikka
- `G` = Haamun aloituspaikka
- ` ` = Tyhjä tila

## Kehitysideoita

Vaihe 2:n jälkeen voidaan lisätä:

1. **Lisää haamujen persoonia**: Clyde ja Inky täydellisillä AI:lla
2. **Äänet**: Syömis-, kuolema- ja voittoäänet
3. **Animaatiot**: Hahmojen liikkumisanimaatiot
4. **Lisää tasoja**: Erilaisia karttoja
5. **Bonus-pisteet**: Hedelmät ja muut bonukset
6. **Parempi grafiikka**: Sprite-kuvat yksinkertaisten muotojen sijaan
7. **Tasojen vaikeus**: Eri nopeudet ja haamujen käyttäytyminen

## Vaatimukset

- Python 3.11+
- Pygame 2.6+

## Lisenssi

Tämä on harjoitusprojekti. Käytä vapaasti oppimis- ja kehitystarkoituksiin.
