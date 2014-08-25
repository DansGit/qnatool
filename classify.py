import sqlite3
import config

def classify(path):
    verbs = open(path, 'r')
    conn = sqlite3.connect(config.DB)
    query = """UPDATE triplets
    SET sentiment = :sentiment
    WHERE predicate = :verb"""

    for line in verbs:
        verb, sentiment = line.split(' = ')
        params = {'verb': verb.strip(), 'sentiment': sentiment.strip()}
        conn.execute(query, params)
    conn.commit()
    conn.close()

