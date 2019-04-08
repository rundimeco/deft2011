#coding:utf-8
import re
import sys
#from bs4 import BeautifulSoup
import glob
import codecs
from tools_karkkainen_sanders import *
from rstr_max import *

def open_utf8(path):
  f = codecs.open(path, "r", "utf-8")
  s = f.read()
  f.close()
  return s

def get_affinites(liste_parts, liste_res):
  rstr = Rstr_max()
  nb_parts = len(liste_parts)
  for part in liste_parts:
    rstr.add_str(part)
  for res in liste_res:
    rstr.add_str(res)
  r = rstr.go()
  longuest = {"chaine":"", "res":-1}
  len_max = 0
  dic_aff = {}
  for (offset_end, nb), (l, start_plage) in r.iteritems():
    is_unique = -1
    ss = rstr.global_suffix[offset_end-l:offset_end]
    s_occur = set()
    for o in xrange(start_plage, start_plage+nb) :
      id_str = rstr.idxString[rstr.res[o]]
      s_occur.add(id_str)
      if id_str >=nb_parts:
        if is_unique!=-1:
          continue
        is_unique =id_str
    if is_unique==-1:
      continue
    is_repeated = [x for x in s_occur if x<nb_parts] 
    if len(is_repeated)>=1:
      real_id_res = is_unique-nb_parts #remettre l'ID reel
      if len(ss)>len_max:
        longuest = {"chaine":ss, "res":real_id_res}
        len_max = len(ss)
      elif len(ss)==len_max:#égalité/indécision
        if type(longuest["chaine"]) is list:
          longuest["chaine"].append(ss)
          longuest["res"].append(real_id_res)
        else:
          l1 = [longuest["chaine"], ss]
          l2 = [longuest["res"], real_id_res]
          longuest = {"chaine":l1, "res":l2}
      dic_aff.setdefault(real_id_res, [])
      dic_aff[real_id_res].append(ss)
  #return N longuest rstr? longuest by res ???
  return {"card_affinites":dic_aff, "max_affinites":longuest}

def get_parts_art_simple(content):
#  soup = BeautifulSoup(content, "xml")
#  texte = soup.findAll("texte")[0].text
  #texte = content
  #TODO:optionner le CUT quelle influence sur les résultats ?
  try:
    elems = re.split("texte>", content)
    content = elems[1]
  except:
    pass
  inter_titres = re.split("<titre>", content)
  if len(inter_titres)>2:
    intro = "<titre>"+inter_titres[0]
    dev = "<titre>"+"<titre>".join(inter_titres[1:-2])
    concl = "<titre>"+inter_titres[-1]
    parts = [intro, dev,concl]
  else:
    fin_intro = int(20*len(content)/100)
    deb_concl = int(80*len(content)/100)
    parts = [content[:fin_intro],content[fin_intro:deb_concl],content[deb_concl:]]
  return parts 

def deft2011(candidat, pretendants, relax):
  parts = get_parts_art_simple(candidat)
  data_affinites = get_affinites(parts, pretendants) 
  data_affinites["diagnostic"] = get_diag(data_affinites, relax)
  return data_affinites 

def get_diag(data_affinites, relax):
  dic_aff = data_affinites["card_affinites"]
  longuest=data_affinites["max_affinites"]
  sorted_aff = sorted([[len(y), x] for x,y in dic_aff.iteritems()],reverse=True)
  id_max = longuest["res"]
  id_card = sorted_aff[0][1]
  try:
    is_equal_card = sorted_aff[0][0]=sorted_aff[1][0]
  except:
    is_equal_card = False
#  if type(id_max) is list or is_equal_card:
#    return {"statut":"unsure","id_result":-1, "id_card":id_card,"id_max":id_max}
  if id_max==id_card:
    return {"statut": "OK", "id_result":id_card, "id_card":id_card,"id_max":id_max}
  elif relax==True:
    return {"statut": "OK", "id_result":id_card, "id_card":id_card,"id_max":id_card}
  else:
    return {"statut":"bad","id_result":-1, "id_card":id_card,"id_max":id_max}

