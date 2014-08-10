import os
import sys
import argparse
import config
import pipeline


def _help():
    print """USAGE: QNATool project_name source_directory output_directory"""
    # todo: better help.




def qnatool(cmd, *args):
    pass


def QNATool(cmd, project_name, source_dir, output_dir):
    # Make sure path variables are valid
    if not _valid_path(source_dir) or not _valid_path(output_dir):
        sys.exit(1)

    # Set config.py settings,
    # unless they have been already set.
    if config.project_name == '':
        config.project_name = project_name

    if config.source_dir == '':
        config.source_dir = source_dir

    if config.output_dir == '':
        project_dir = os.path.join(output_dir, project_name)
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
        config.output_dir = project_dir

    if config.chart_dir == '':
        chart_dir = os.path.join(config.output_dir, 'charts')
        if not os.path.exists(chart_dir):
            os.mkdir(chart_dir)
        config.chart_dir = chart_dir

    if config.DB == '':
        config.DB = os.path.join(project_dir, '{}.db'.format(project_name))

    # Run the pipeline
    pipeline.run()


    

if __name__ == '__main__':
    # Create top level parser and subparsers
    parser = argparse.ArgumentParser(prog="qna")
    subparsers = parser.add_subparsers()

    # 'process' command
    process_parser = subparsers.add_parser('process')
    process_parser.set_defaults(func=pipeline.process_cmd)
    process_parser.add_argument('NAME', help='A name for the project.')
    process_parser.add_argument('SRC', help='The path to a directory with ' +
                                'files to process')
    process_parser.add_argument('DEST', help='The path to an directory in ' +
                                'which the output will be placed.')

    # 'classify' command
    classify_parser = subparsers.add_parser('classify')
    classify_parser.set_defaults(func=pipeline.classify_cmd)
    classify_parser.add_argument('SRC', default=None, help='Directory ' +
                                 'containing the output of the "process" ' +
                                 'command. Defaults to last opened project.')
    classify_parser.add_argument('-f', '--f', help="Path to a verbs.txt file " +
                                 "if you don't want to use the one in the SRC" +
                                 " dir.")

    # 'network' command
    network_parser = subparsers.add_parser('network')
    network_parser.set_defaults(func=pipeline.network_cmd)
    network_parser.add_argument('SRC', nargs='?', default=None,
                                help='Directory containing ' +
                                'the output the "process" command. ' +
                                'Defaults to last opened project.')
    network_parser.add_argument('-a', '--all', action='store_true',
                                help='Generate all graph files.')
    network_parser.add_argument('-p', '--png', action='store_true',
                                help='Generate png image.')
    network_parser.add_argument('-g', '--gexf', action='store_true',
                                help='Generate gexf file.')
    network_parser.add_argument('-k', '--pickle', action='store_true',
                                help='Generate pickled ' +
                                'igraph Graph file.')
    network_parser.add_argument('-c', '--communities', action='store_true',
                                help='Generate a' +
                                'graph file for a network in which all ' +
                                'vertices in a community have been ' +
                                'aggregated into a single vertex.')

    args = parser.parse_args()

    #Runs the appropriate function in pipeline.py and passes
    #command line arguemnts to it.
    args.func(args)
