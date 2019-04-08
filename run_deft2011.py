#coding:utf-8
from deft2011 import *
import os
from tools import *

def get_args():
  import argparse
  parser = argparse.ArgumentParser(description='Deft 2011: appariements')
  parser.add_argument("--articles",type=str,
      default="deft2011_appariements_appr_complets/art/",
      help="Path of the articles", 	metavar="ARTICLES")
  parser.add_argument("--resumes", type=str,
      default="deft2011_appariements_appr_complets/res/",
      help="Path of the abstracts", 	metavar="RESUMES")
  parser.add_argument("--verbose", type=bool,
      default=False,
      help="Verbose mode", 	metavar="VERBOSE")
  args = parser.parse_args()
  return args


options = get_args()

dir_art = options.articles
dir_res = options.resumes

liste_art = glob.glob(dir_art+"*")
liste_res = glob.glob(dir_res+"*")

all_resultats = []
cptDone=0
cptPhase = 0
relax = False
try:
  os.makedirs("tmp/")
except:
  pass

log_file = open("tmp/error_file", "w")

while len(liste_art)>0:
  cptPhase +=1
  left = len(liste_art)
  print("-"*20)
  print("Phase %i NB art left : %i"%(cptPhase, left))
  print("-"*20)
  for num_art, path_art in enumerate(liste_art[:20]):
    print(path_art)
    textes_res = []
    for path_res in liste_res:
      textes_res.append(open_utf8(path_res))
    data_affinites = deft2011(open_utf8(path_art), textes_res, relax) 
    if data_affinites["diagnostic"]["statut"] == "OK":
      cptDone+=1
      id_card = data_affinites["diagnostic"]["id_card"]
      id_max  = data_affinites["diagnostic"]["id_max"]
      print(data_affinites["max_affinites"])
      os.system("gedit '%s'"%path_art)
      os.system("gedit '%s'"%liste_res[id_card])
      name_res = re.split("/", liste_res[id_card])[-1]
      name_art = re.split("/", path_art)[-1]
      resultat = "%s\t%s"%(name_art, name_res)
      all_resultats.append(resultat)
      if options.verbose==True:
        print(resultat)
      d = raw_input("next ?")
      textes_res[id_card]= " "
      liste_art[num_art] = " "
      
  if cptPhase>1:
    if left == len(liste_art):
      print("Phase à vide, relax->True")
      relax=True
  liste_art = [art for art in liste_art if art!=" "]
write_utf8("test.resultats", "\n".join(all_resultats))

log_file.close()
