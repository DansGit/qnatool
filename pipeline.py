import os
import sys
import utils
import process
import analyze
import config


def process_cmd(args):
    """Processes text files and generates
    a database of SVO triplets in output dir.
    """
    # Set parameters in config.py.
    config.name = args.NAME
    if args.SRC and utils.valid_dir(args.SRC):
        config.source_dir = os.path.abspath(args.SRC)
    else:
        print "Source dir error. Exiting."
        sys.exit(1)

    if args.DEST and utils.valid_dir(args.DEST):
        config.output_dir = os.path.join(os.path.abspath(args.DEST),
                                         config.name)
    else:
        print "Destination dir error. Exiting."
        sys.exit(1)

    # Make the destination dir if it doesn't exist
    if not os.path.exists(config.output_dir):
        os.mkdir(config.output_dir)

    # Set database location.
    if config.DB == '':
        config.DB = os.path.join(config.output_dir, '{}.db'.format(config.name))

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


def classify_cmd(args):
    """Uses verbs.txt in output dir to set sentiment
    values for triplets. Allows for manual sentiment
    coding if desired.
    """

    # Set parameters in config.py.
    if utils.valid_dir(args.SRC):
        config.source_dir = args.SRC
        config.output_dir = args.SRC

    print "This does nothing...for now."


def network_cmd(args):
    """Uses database in output dir to make network graph
    files in output dir. Graph files can take the form of
    a png image, a pickled igraph object, or a gexf file.
    """

    # Set parameters in config.py.
    if utils.valid_dir(args.SRC):
        config.source_dir = args.SRC
        config.output_dir = args.SRC

    print 'Generating network graph...'
    G = analyze.network.make_graph(giant=config.giant)

    print "Finding communities."
    analyze.network.community_modularity(G)

    if args.gexf or args.all:
        print "Exporting to gexf..."
        fname = "{}.gexf".format(config.project_name)
        analyze.network.write_gexf(G, os.path.join(config.output_dir, fname))

    if args.png or args.all:
        print "drawing network to png..."
        analyze.draw_network.draw(G, 'fr',
                                  label='name',
                                  name=config.project_name
                                  )

    if args.pickle or args.all:
        print "Pickling network..."
        analyze.network.pickle_graph(G)

    if args.communities:
        H = analyze.network.community_graph(G)

        if H:
            if args.gexf or args.all:
                print "Exporting community network to gexf..."
                fname = "{}_communities.gexf".format(config.project_name)
                fpath = os.path.join(config.output_dir, fname)
                analyze.network.write_gexf(H, fpath)

            if args.png or args.all:
                print "Drawing community network as png file..."
                analyze.draw_network.draw(H,
                                          'fr',
                                          label='label',
                                          name=config.project_name +
                                          '_communities'
                                          )

            if args.pickle or args.all:
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
