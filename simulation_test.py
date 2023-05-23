import random

class Haushalt:
    def __init__(self, id):
        self.id = id
        self.erspartes = random.randint(0,100) # zufälliger Wert zwischen 0 und 100	in Euro
        self.schulden = 0 # 
        self.einkommen = random.randint(0,100) # zufälliger Wert zwischen 0 und 100 in Euro
        self.ausgaben = random.randint(0,100) # zufälliger Wert zwischen 0 und 100 in Euro
        self.zinsen = 0.05 # !!!!!Stellschraube!!!!!

    def sparen(self):# Sparen
        if self.einkommen > self.ausgaben:  
            self.erspartes += self.einkommen - self.ausgaben    
        else:
            self.erspartes -= self.ausgaben - self.einkommen
    
    def konsumieren(self):# Konsumieren
        if self.erspartes > 0:
            konsum = min(self.erspartes, self.ausgaben)# Konsumieren bis erspartes oder ausgaben aufgebraucht sind
            self.erspartes -= konsum
            self.ausgaben -= konsum
        else:
            self.ausgaben = 0

    def zinsen_zahlen(self):
        zinszahlung = self.schulden * self.zinsen
        if self.erspartes >= zinszahlung:
            self.erspartes -= zinszahlung
            self.schulden += zinszahlung
        else:
            # Wenn der Haushalt die Zinsen nicht zahlen kann, wird der Kredit als ausgefallen betrachtet
            self.schulden -= self.erspartes
            self.erspartes = 0

    def kredit_aufnehmen(self, bank):
        kredit_betrag = random.randint(0,100) #!!!! Stellschraube !!!!!
        if bank.kredit_vergeben(kredit_betrag): # Wenn die Bank den Kredit vergibt
            self.erspartes += kredit_betrag
            self.schulden += kredit_betrag

    def kredit_zurueckzahlen(self):# Kredit zurückzahlen
        if self.schulden > 0:
            rueckzahlung = min(self.erspartes, self.schulden) # Zurückgezahlt wird das was weniger ist von erspartes und schulden
            self.erspartes -= rueckzahlung
            self.schulden -= rueckzahlung

    def kredit_ausfallen(self):# Kreditausfall
        if self.schulden > 0:
            if random.random() < 0.25:# !!!!!Stellschraube!!!!!
                return True
            else:
                return False
        else:
            return False
        
class Bank:
    def __init__(self, id):
        self.id = id
        self.kapital = random.randint(100,200) # zufälliger Wert zwischen 100 und 200 in Euro
        self.kredite = 0 # Anfangskredite sind 0
        self.risiokoeffizient = random.uniform(0.5,2) # !!!!!Stellschraube!!!!!
        self.zinsen = 0.05 # !!!!!Stellschraube!!!!!

    def kredit_vergeben(self, betrag):# Vergibt einen Kredit
        if self.kapital - betrag > 0 and self.kredite + betrag < self.kapital * self.risiokoeffizient:	
            self.kapital -= betrag
            self.kredite += betrag
            return True
        else:
            return False
        
    
    def zinsen_erheben(self):
        self.kapital += self.kredite * self.zinsen

    def solvenz_pruefen(self):# Prüfe ob die Bank noch solvent ist
        if self.kapital < self.kredite / 2:
            return False
        else:
            return True
        
    def kapital_erhoehen(self): # Zufällige Erhöhung des Kapitals
        if random.choice([True, False]):
            self.kapital += random.randint(0,100)

        
        
haushalte = [Haushalt(i) for i in range(100)] # Erstelle 100 Haushalte
banken = [Bank(i) for i in range(10)] # Erstelle 10 Banken

for t in range(100):# Für 100 Zeitschritte
    for haushalt in haushalte:
        haushalt.sparen()# Sparen
        haushalt.konsumieren()# Konsumieren
        bank = random.choice(banken) # Zufällige Auswahl einer Bank
        haushalt.kredit_aufnehmen(bank)# Kredit aufnehmen
        if haushalt.kredit_ausfallen():# Kreditausfall
            haushalt.schulden = 0
            bank.kredite -= haushalt.schulden
            print(f"Kreditausfall bei Haushalt {haushalt.id} in Zeitschritt {t}")

    
    for bank in banken:# Für jede Bank
        bank.kapital_erhoehen()
        if bank.solvenz_pruefen() == False:
            banken.remove(bank)
            print(f"Bank {bank.id} ist insolvent in Zeitschritt {t}")
            


    
    for haushalt in haushalte:# Für jeden Haushalt
        haushalt.kredit_zurueckzahlen()# Kredit zurückzahlen
    
    print(f"Zeitschritt {t}: {len(banken)} Banken und {len(haushalte)} Haushalte")

    if len(banken) == 0:
        break
