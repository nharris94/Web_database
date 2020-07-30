#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector

def main():
    print("Content-Type: application/json\n\n")
    
    #get the information from the form
    form = cgi.FieldStorage()
    field = form.getvalue('parameter')
    term = form.getvalue('search_term') 

    #connect to server        
    conn = mysql.connector.connect(user='', password='', host='', database='')
    cursor = conn.cursor()

    #Search the database using the parameter and the term
    if field == 'id':
        qry = """
              SELECT id, label, description
                FROM antibiotic_genes
               WHERE id LIKE %s
        """
        cursor.execute(qry, ('%' + term + '%', ))
    elif field  == 'description':
        qry = """
              SELECT id, label, description
                FROM antibiotic_genes
               WHERE description LIKE %s
        """
        cursor.execute(qry, ('%'+ term + '%', ))
    elif field == 'name':
        qry = """
              SELECT id, label, description
                FROM antibiotic_genes
               WHERE label LIKE %s
        """
        cursor.execute(qry, ('%'+ term + '%', ))
    num = 0

    #Add the results to a list
    results = { 'match_count': 0, 'matches': list() }
    for (gene_id, name, description) in cursor:
        results['matches'].append({'gene_id': gene_id, 'name': name, 'description': description})
        results['match_count'] += 1
        num += 1

    #See if the searched name is a synonym and print results
    if field == 'name' and num == 0:
        qry = """
              SELECT a.id, a.label, a.description
                FROM antibiotic_genes a
                   JOIN synonyms s ON s.id = a.id
               WHERE s.synonym LIKE %s
        """
        cursor.execute(qry, ('%'+ term + '%', ))
        for (gene_id, name, description) in cursor:
            results['matches'].append({'gene_id': gene_id, 'name': name, 'description': description})
            results['match_count'] += 1

    conn.close()
    print(json.dumps(results))


if __name__ == '__main__':
    main()
