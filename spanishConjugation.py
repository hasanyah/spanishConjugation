import csv
import requests
from lxml import html
import numpy as np
from itertools import cycle

endpoint = "https://www.spanishdict.com/conjugate/"
verbs = ["Estar", "Ser", "Tener", "Haber", "Hacer", "Ir", "Venir", "Decir","Poder","Dar","Ver","Saber","Tomar","Coger","Querer","Llegar","Pasar","Poner","Parecer","Quedar","Hablar","Creer","Llamar","Seguir","Encontrar"]
verbs = list(map(lambda x: x.lower(), verbs))
subjects = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellas/ellos/ustedes"]
tenses = ["present", "preterite", "imperfect", "conditional", "future"]
tenses = np.array([["("+tense+")"] * 6 for tense in tenses]).flatten()
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for verb in verbs:
        print(verb)
        response = requests.get(endpoint+verb)
        if (response.status_code != 200):
            print("There is a problem with the response from {}!".format(endpoint))
            print(response.json())
        else:
            tree = html.fromstring(response.content)
            table = np.array(tree.xpath('(//table[@class="_2WLTGmgs"])[1]//td[@class="_3_AB7VNM"]//a/@aria-label'))
            transposed = np.array(np.split(table, len(table) // 5)).transpose().flatten()
            transposed = list(zip(cycle(subjects), cycle(["("+verb+")"]), cycle(tenses), transposed))
            for tpl in transposed:
                writer.writerow(tpl)
