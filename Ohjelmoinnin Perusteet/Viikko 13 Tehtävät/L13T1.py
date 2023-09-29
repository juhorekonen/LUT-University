######################################################################
# CT60A0203 Ohjelmoinnin perusteet
# Tekijä: Juho Rekonen
# Opiskelijanumero:441410
# Päivämäärä: 6.12.2022
# Kurssin oppimateriaalien lisäksi työhön ovat vaikuttaneet seuraavat
# lähteet ja henkilöt, ja se näkyy tehtävässä seuraavalla tavalla:
#
# Mahdollisen vilppiselvityksen varalta vakuutan, että olen tehnyt itse
# tämän tehtävän ja vain yllä mainitut henkilöt sekä lähteet ovat
# vaikuttaneet siihen yllä mainituilla tavoilla.
######################################################################
# Tehtävä L13T1.py

# eof

import L13T1Kirjasto

def valikko():
    print("1) Anna tiedoston nimi")
    print("2) Lue tiedosto")
    print("3) Tulosta tiedot")
    print("4) Kirjoita tiedosto")
    print("0) Lopeta")

    while True:
        try:
            valinta = int(input("Anna valintasi: ").strip())
        except ValueError:
            print("Anna valinta kokonaislukuna.")
        else:
            break
    
    return valinta


def paaohjelma():
    Henkilot = []
    print("Tämä ohjelma lukee tiedoston ja tulostaa sen tiedot näytölle.")
    while True:
        
        valinta = valikko()

        if valinta == 1:
            tiedosto = L13T1Kirjasto.kysyTiedosto("luettavan")

        elif valinta == 2:
            Henkilot.clear()
            Henkilot = L13T1Kirjasto.analysoiTiedot(tiedosto, Henkilot)
        
        elif valinta == 3:
            if len(Henkilot) < 1:
                print("Ei tietoja tulostettavaksi, analysoi tiedot ennen tulostusta.")
            else:
                L13T1Kirjasto.tulostaTiedot(Henkilot)
        
        elif valinta == 4:
            if len(Henkilot) < 1:
                print("Ei tietoja kirjoitettavaksi, analysoi tiedot ennen tulostusta.")
            else:
                L13T1Kirjasto.kirjoitaTiedot(Henkilot)
        
        elif valinta == 0:
            Henkilot.clear()
            print("Lopetetaan.")
            break

        else:
            print("Tuntematon valinta, yritä uudelleen.")
        
        print()
    print()
    print("Kiitos ohjelman käytöstä.")
    return None

paaohjelma()

