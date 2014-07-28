import os
import sys
import config
import pipeline

def _help():
    print """USAGE: QNATool project_name source_directory output_directory"""
    # todo: better help.

def _valid_path(path):
    if not os.path.exists(path):
        print 'ERROR: "{}" does not exist'.format(path)
        return False
    elif not os.path.isdir(path):
        print 'ERROR: "{}" is not a directory'.format(path)
        return False
    else:
        return True

def QNATool(project_name, source_dir, output_dir):
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
    args = sys.argv[1:]

    # print help
    if args[1] == '-h' or args[1] == '--help':
        _help()
    else:
        QNATool(*args)

