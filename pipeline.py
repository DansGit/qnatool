import os
import process
import analyze
import config
import progressbar


def run():
    init()
    if config.do_process:
        process.process.batch_process(config.source_dir)
        process.refine.weight()
        process.refine.set_reliable(
                frequency_threshold=config.frequency_threshold,
                weight_threshold=config.weight_threshold,
                unnamed_threshold=config.unnamed_threshold
                )
        process.refine.resolve_corefs()

    if config.do_network:
        print 'Generating network graph...'
        G = analyze.network.make_graph(giant=config.giant)
        print 'Finding communities...'
        analyze.network.community_modularity(G)
        H = analyze.network.community_graph(G)

        # Create network images
        print "drawing networks..."
        analyze.draw_network.draw(G, 'fr',
                label='name',
                name=config.project_name)
        analyze.draw_network.draw(H, 'fr',
                label='label',
                name=config.project_name + '_communities')

        print "Exporting to Gexf..."
        analyze.network.write_gexf(G,
                os.path.join(config.output_dir,
                    "{}.gexf".format(config.project_name)))
        print 'Generating community network graph...'
        if H is not False:
            analyze.network.write_gexf(H,
                    os.path.join(config.output_dir,
                        "{}_communities.gexf".format(config.project_name)))

        print 'Generating .csv files.'
        analyze.csv_export.triplets(G, config.output_dir)
        analyze.csv_export.entities(G, config.output_dir)

        if config.do_charts:
            print 'Making charts...'
            pbar = progressbar.ProgressBar(3)
            pbar.start()
            analyze.chart.auto_scatter(G, threshold=.2)
            pbar.tick()
            analyze.chart.make_bars(G)
            pbar.tick()
            analyze.chart.make_date_lines(G)
            pbar.tick()


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

