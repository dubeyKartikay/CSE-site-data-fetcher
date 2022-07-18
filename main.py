import logging
from urllib import response
import pandas as pd
import xmltodict
import pprint
import sys
import requests
inputCSVFileName = "facueelty.csv" if len(sys.argv) <2 else sys.argv[1]
outputCSVFileName = "home.csv" if len(sys.argv) <3 else sys.argv[2]

df = pd.read_csv(inputCSVFileName)
df = df.loc[:, df.columns.intersection(['DBLP','DOR','DOJ'])]
print(df)
url = "https://dblp.org/pid/"
dataFormat = "xml"

publicationFilter = ["AAAI","ECCV","CVPR","Trans.","ICML","ICCV"]
def isValidPub(journal,publicationFilter):
    for word in publicationFilter:
        if word in journal:
            return True
    return False

for row in df.values:
    finalURL = f"{url}{row[0]}.{dataFormat}"
    response = requests.get(finalURL) 
    tree = xmltodict.parse(response.content)
    for pub in tree["dblpperson"]["r"]:
        pubData =[","]
        if 'article' in pub.keys():
            if not(isValidPub(pub["article"]["journal"],publicationFilter)):
                continue
            pubData.append(pub["article"]["title"])
            pubData.append(pub["article"]["ee"])
            pubData.append(pub["article"]["journal"])
            authors = ",".join(map(lambda x :x['#text'],pub["article"]["author"]))
            pubData.append(authors)
            pubData.append("publication")
            pubData.append(pub["article"]["year"])
        elif 'inproceedings' in pub.keys():
            if not(isValidPub(pub["inproceedings"]["booktitle"],publicationFilter)):
                continue
            pubData.append(pub["inproceedings"]["title"])
            pubData.append(pub["inproceedings"]["ee"])
            pubData.append(pub["inproceedings"]["booktitle"])
            authors = ",".join(map(lambda x :x['#text'],pub["inproceedings"]["author"]))
            pubData.append(authors)
            pubData.append("publication")
            pubData.append(pub["inproceedings"]["year"])
        pprint.pprint(pub)
        pprint.pprint(pubData)
        print()
    break