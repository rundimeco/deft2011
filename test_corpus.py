import sys
import re

for fic in sys.argv[1:]:
  f = open(fic)
  chaine = f.read()
  f.close()
  elems = re.split("texte>", chaine)
  
  chaine = elems[1]
  titres = re.findall("<titre>.*?</titre>", chaine)
  if len(titres)>1:
    print(titres[0]+ "  "+titres[-1] )
  else:
    print(fic)
    d = input("Next ?")
