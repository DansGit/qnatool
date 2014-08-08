import os
import process
import analyze
import config


def process_cmd():
    """Processes text files and generates
    a database of SVO triplets in output dir.
    """
    init()
    # Parses with corenlp and extracts triplets.
    process.process.batch_process(config.source_dir)

    # Compares corpus with background database.
    process.refine.weight()

    # Determines which triplets should be included
    # in the graph and which should be filtered out.
    process.refine.set_reliable(
        frequency_threshold=config.frequency_threshold,
        weight_threshold=config.weight_threshold,
        unnamed_threshold=config.unnamed_threshold
        )

    # Reesolve corefs among entities in db.
    process.refine.resolve_corefs()

    #  Make verbs.txt files in output dir.
    process.verb_list.write()


def classify_cmd():
    """Uses verbs.txt in output dir to set sentiment
    values for triplets. Allows for manual sentiment
    coding if desired.
    """
    print "This does nothing...for now."


def network_cmd(gexf, png, pickle, communities):
    """Uses database in output dir to make network graph
    files in output dir. Graph files can take the form of
    a png image, a pickled igraph object, or a gexf file.
    """

    print 'Generating network graph...'
    G = analyze.network.make_graph(giant=config.giant)

    print "Finding communities."
    analyze.network.community_modularity(G)

    if gexf:
        print "Exporting to gexf..."
        fname = "{}.gexf".format(config.project_name)
        analyze.network.write_gexf(G, os.path.join(config.output_dir, fname))

    if png:
        print "drawing network to png..."
        analyze.draw_network.draw(G, 'fr',
                                  label='name',
                                  name=config.project_name
                                  )

    if pickle:
        print "Pickling network..."
        analyze.network.pickle_graph(G)

    if communities:
        H = analyze.network.community_graph(G)

        if H:
            if gexf:
                print "Exporting community network to gexf..."
                fname = "{}_communities.gexf".format(config.Project_name)
                fpath = os.path.join(config.output_dir, fname)
                analyze.network.write_gexf(H, fpath)

            if png:
                print "Drawing community network as png file..."
                analyze.draw_network.draw(H,
                                          'fr',
                                          label='label',
                                          name=config.project_name +
                                          '_communities'
                                          )

            if pickle:
                print "pickling network graph..."
                analyze.network.pickle_graph(G)

        else:
            print "Error: Community detection failed."


def init():
    # Make database
    process.database.init_db()

    # Make temp dir if it doesn't exist
    if not os.path.exists(config.TEMP):
        os.mkdir(config.TEMP)

    # clear temp
    for root, dirs, fnames in os.walk(config.TEMP):
        for fname in fnames:
            p = os.path.join(root, fname)
            os.remove(p)

    # clear log file
    f = open('data/corenlp_log.txt', 'w')
    f.close()
