#!/usr/local/bin/python3

import re
import os
import mysql.connector

#open connection to database
conn = mysql.connector.connect(user='', password= '', host= '', database= '')
cursor = conn.cursor()

#variables
genes_file = open("aro.owl")
genes = list()
gene_id = ""
gene_label = ""
gene_info = ""
list_of_syn = list()
synonym = list()
i = 0
x = 0

#extract id, label, synonyms and description from file and enter into tables
for line in genes_file:
    line = line.replace("&apos;", "'")
    m = re.search(".+:id .+>(.+)<", line)
    m2 = re.search(".+:label .+>(.+)<", line)
    m3 = re.search(".+:annotatedTarget .+>(.+)<", line)
    m4 = re.search(".+:hasExactSynonym .+>(.+)<", line)
    if m:
        gene_id = m.group(1)
        if x == 1:
            for syn in synonym:
                list_of_syn.append(gene_id + ";" + syn)
            synonym = list()
            x = 0
    elif m4:
        synonym.append(m4.group(1))
        x = 1
    elif m2:
        gene_label = m2.group(1)
    elif m3:
        gene_info = m3.group(1)
        genes.append(gene_id + ";;" + gene_label + ",," + gene_info)

#Enter the genes into the genes table
for gene in genes:
    m = re.search("(.+);;(.+),,(.+)", gene)
    gene_id = m.group(1)
    gene_label = m.group(2)
    gene_info = m.group(3)
    qry = "INSERT INTO antibiotic_genes(id, label, description) VALUES (%s, %s, %s)"
    cursor.execute(qry, (gene_id, gene_label, gene_info))

#Enter the synonyms into the synonyms table
for syn in list_of_syn:
    m = re.search("(.+);(.+)", syn)
    gene_id = m.group(1)
    syn_name = m.group(2)
    qry = "INSERT INTO synonyms(id, synonym) VALUES (%s, %s)"
    cursor.execute(qry, (gene_id, syn_name))


conn.close()


