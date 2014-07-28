import csv
from os.path import join

import get_data

def triplets(G, path):
    csv_file = open(join(path, 'triplets.csv'), 'wb')
    writer = csv.writer(csv_file)
    writer.writerow(['SUBJECT', 'PREDICATE', 'OBJECT', 'SENTENCES',
        'ARTICLE_PATH'])
    for edge in G.es:
        subject = G.vs[edge.source]['name']
        obj = G.vs[edge.target]['name']
        writer.writerow([
            subject,
            edge['label'],
            obj,
            edge['sentences'].encode('ascii', 'ignore'),
            edge['article_path']
            ])
    csv_file.close()

def entities(G, path):
    csv_file = open(join(path, 'entities.csv'), 'wb')
    writer = csv.writer(csv_file)

    betweenness = get_data.betweenness(G)
    in_degree = get_data.in_degree(G)
    out_degree = get_data.out_degree(G)
    in_sentiment = get_data.in_sentiment(G)
    out_sentiment = get_data.out_sentiment(G)
    sobias = get_data.sobias(G)
    osbias = get_data.osbias(G)

    writer.writerow(['ENTITY', 'BETWEENNESS', 'IN_DEGREE', 'OUT_DEGREE',
        'IN_SENTIMENT', 'OUT_SENTIMENT', 'SUBJECT/OBJECT BIAS',
        'OBJECT/SUBJECT BIAS'])

    for vertex in G.vs:
        v = vertex['name']
        writer.writerow([v, betweenness[v], in_degree[v], out_degree[v],
            in_sentiment[v], out_sentiment[v], sobias[v], osbias[v]])
    csv_file.close()
