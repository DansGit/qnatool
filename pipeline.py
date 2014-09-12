# TODO better init function.
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
    config.project_name = args.NAME
    if args.SRC and utils.valid_dir(args.SRC):
        config.source_dir = os.path.abspath(args.SRC)
    else:
        print "Source dir error. Exiting."
        sys.exit(1)

    if args.DEST and utils.valid_dir(args.DEST):
        config.output_dir = os.path.join(os.path.abspath(args.DEST),
                                         config.project_name)
    else:
        print "Destination dir error. Exiting."
        sys.exit(1)

    # Make the destination dir if it doesn't exist
    if not os.path.exists(config.output_dir):
        os.mkdir(config.output_dir)


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

    # Set opened project
    set_opened(config.project_name, config.output_dir)


def classify_cmd(args):
    """Uses verbs.txt in output dir to set sentiment
    values for triplets. Allows for manual sentiment
    coding if desired.
    """
    from classify import classify

    # Set parameters in config.py.
    if args.SRC is None:
        name, project_path = get_opened()
        config.project_name = name
        config.source_dir = project_path
        config.output_dir = project_path
    elif utils.valid_dir(args.SRC):
        config.source_dir = args.SRC
        config.output_dir = args.SRC
    else:
        print "Project dir error. Exiting."
        sys.exit(1)

    init()

    verbs = os.path.join(config.source_dir, 'verbs.txt')
    classify(verbs)




def network_cmd(args):
    """Uses database in output dir to make network graph
    files in output dir. Graph files can take the form of
    a png image, a pickled igraph object, or a gexf file.
    """

    # Set parameters in config.py.
    if args.SRC is None:
        name, project_path = get_opened()
        config.project_name = name
        config.source_dir = project_path
        config.output_dir = project_path
    elif utils.valid_dir(args.SRC):
        config.source_dir = args.SRC
        config.output_dir = args.SRC
    else:
        print "Project dir error. Exiting."
        sys.exit(1)

    init()

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


def set_opened(name, path):
    """Records the DEST path to a file so
    the user doesn't have to type it in again."""
    fpath = os.path.join(config.DATA, 'opened.txt')
    f = open(fpath, 'w')
    f.write('{}\n{}'.format(name, path))
    f.close()


def get_opened():
    """Gets the last opned project."""
    data_dir = os.path.join(os.path.expanduser('~'), '.qna')
    fpath = os.path.join(data_dir, 'opened.txt')
    if os.path.exists(fpath):
        f = open(fpath, 'r')
        name = f.readline().strip()
        path = f.readline().strip()
        f.close()
        return name, path
    else:
        print("Error unable to get most recently opened project. " +
              "Please set manually.")
        sys.exit(1)


def init():
    home = os.path.expanduser('~')

    # Set data dir path
    progpath = os.path.join(home, '.qna')
    if not os.path.exists(progpath):
        os.mkdir(progpath)
    config.DATA = progpath

    # Set temp dir path
    temp_path = os.path.join(progpath, 'temp')
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    config.TEMP = temp_path

    # Set/move background db.
    if config.BGDB is None:
        bgdb_path = os.path.join(config.DATA, 'background.db')
        if not os.path.exists(bgdb_path):
            import shutil
            shutil.copy('data/background.db', bgdb_path)
        config.BGDB = bgdb_path

    # Set database location.
    if config.DB == '':
        config.DB = os.path.join(config.output_dir, '{}.db'.format(config.project_name))

    # Make database
    process.database.init_db()

    # clear temp
    for root, dirs, fnames in os.walk(config.TEMP):
        for fname in fnames:
            p = os.path.join(root, fname)
            os.remove(p)

    # clear log file
    logpath = os.path.join(config.DATA, 'corenlp_log.txt')
    f = open(logpath, 'w')
    f.close()
