# Code review
### Code reviewer: Lara Scipio

## READ ME
Probeer nog toe te voegen wat jouw model 'oplost', dus wat je er in principe mee zou kunnen onderzoeken als je echte data zou gebruiken. Dan zit er wat meer nut achter.

<br>

## colony.py
Niet alle dingen je importeert gebruik je (zoals get_distance)
Bij regel 37: checken met true en false hoeft volgens mij niet, ik denk dat je gewoon direct kan checken of een position leeg is, en op basis daarvan kan toevoegen.


place a variable number of traps for every home

--> onduidelijk waar de traps precies geplaatst worden, ik neem aan rond het huis? Maar hoe dan? Dat kan duidelijker.

age = self.random.randrange(150) --> waar komt de 150 vandaan? Voor mij is dit een floating variable (of hoe je dat ook noemt)

In het algemeen kunnen er meer comments bij, ook kleine met bv wat een specifieke functie doet, maar misschien is dat meer persoonlijk.

<br>

## cats.py
Kunnen ook meer comments bij!

Veel getallen (bv HUNGER THRESHOLD) komen beetje zonder context, misschien kun je die uitleggen

if self.trapped --> zet hier even in een comment bij waar dit wordt aangepast 
bij interact() --> beetje onduidelijk hoe de functie is opgebouwd 

<br>

## homes.py
random() beter uitleggen 
"# requirements for new location" regel 57 --> beter formuleren
self.running = False toevoegen! 