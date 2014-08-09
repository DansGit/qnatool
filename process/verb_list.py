import sqlite3
import os
import config


def write():
    """Writes a texf file to output dir that contains
    every verb in the db and its sentences sentiment.
    This allows the user to manually set sentiment values
    if she chooses to.
    """

    f = open(os.path.join(config.output_dir, 'verbs.txt'),
             mode='w')
    result = _get_verbs()
    for verb, sentiment in result:
        f.write('{} = {}\n'.format(verb, str(sentiment)))

    f.close()


def _get_verbs():
    query = """SELECT DISTINCT predicate, sentiment FROM triplets
                WHERE is_reliable = 1"""

    conn = sqlite3.connect(config.DB)

    return conn.execute(query).fetchall()
