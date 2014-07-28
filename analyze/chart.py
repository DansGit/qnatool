from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import numpy
import string
import scipy
from os import path
import config
from analyze import get_data, network


DATA_FUNCS = {
        # 'eigenvector': get_data.eigenvector,
        'betweenness': get_data.betweenness,
        'degree': get_data.degree,
        'in degree': get_data.in_degree,
        'out degree': get_data.out_degree,
        'subject/object bias': get_data.sobias,
        'object/subject bias': get_data.osbias,
        'total sentiment': get_data.total_sentiment,
        'in sentiment': get_data.in_sentiment,
        'out sentiment': get_data.out_sentiment
        }


def auto_scatter(G, threshold=.5):
    """Calculates the Pearson Correlation Coefficient for
    data type in DATA_FUNCS and saves scatter plots when
    two data types correlate above a certain threshold.
    +1 = Perfect positive correlation.
    0 = No correlation.
    -1 = Perfect negative correlation.
    """

    for y_data_type, y_function in DATA_FUNCS.iteritems():
        y_dict = y_function(G)
        y_sorted = sort_dict(y_dict, 'greatest', limit=-1)
        y_list = [y[1] for y in y_sorted.items()]
        for x_data_type, x_function in DATA_FUNCS.iteritems():
            if x_data_type.split(' ')[-1] != y_data_type.split(' ')[-1]:
                x_dict = x_function(G)
                x_sorted = correspond(x_dict, y_sorted)
                x_list = [x[1] for x in x_sorted.items()]
                c, p = scipy.stats.pearsonr(x_list, y_list)
                if c >= threshold or c <= threshold * -1:
                    scatter(x_list,
                            x_data_type,
                            y_list,
                            y_data_type,
                            c, p)


def scatter(x, xlabel, y, ylabel, pcc, p):
    # Make the scatter plot
    plt.scatter(x, y)

    # Make the regresssion line
    m, b = numpy.polyfit(x, y, 1)
    plt.plot(x, [m*i+b for i in x])

    # Set labels
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    annotation = "Pearson's r: {}\nP-Value: {}".format(
            numpy.round(pcc, 2),
            numpy.round(p, 2))
    plt.annotate(annotation, xy=(1, 0),
            xycoords='axes fraction',
            fontsize=9,
            horizontalalignment='right',
            verticalalignment='bottom')
    # Save plot
    fname = escape_fname("{} v {}.png".format(ylabel, xlabel))
    p = path.join(config.chart_dir, fname)
    plt.savefig(p)
    plt.close()


def make_bars(G, limit=20, data_types=None):
    """Makes a series of bar charts from chosen data types."""

    if data_types is None:
        data_types = {
            'betweenness': 'greatest',
            'subject/object bias': 'greatest',
            'object/subject bias': 'greatest',
            'total sentiment': 'greatest and least',
            'in sentiment': 'greatest and least',
            'out sentiment': 'greatest and least'}

    for data_type, sort in data_types.iteritems():
        barchart(G, config.chart_dir, data_type, sort, limit)




def barchart(G, save_dir, data_type, group, limit):
    data = DATA_FUNCS[data_type](G)
    data_sorted = sort_dict(data, group, limit)

    bottom_index = numpy.arange(
            start=len(data_sorted),
            stop=0,
            step=-1)
    labels = []
    values = []
    for key, value in data_sorted.iteritems():
        labels.append(key)
        values.append(value)

    # add a very small value to x so that zero values
    # show up on the chart.
    values = [x + .0000000000001 if x == 0 else x for x in values]
    width = .5
    plt.barh(bottom=bottom_index, width=values, height=width)
    plt.yticks(bottom_index+width/2, labels)
    plt.xlabel(data_type)
    plt.title("{} {}".format(group, data_type))
    # plt.grid(True)
    # if group == "greatest and least":
    #     plt.hlines(len(bottom_index)/2 + width * 1.5,
    #             values[-1], values[0], linestyle='dashed')
        # plt.plot(len(bottom_index)/2 + width, 'k-')



    plt.tight_layout()
    plt.autoscale()

    padding = (max(bottom_index) - min(bottom_index)) * .1
    plt.ylim(
            ymin=min(bottom_index) - padding,
            ymax=max(bottom_index) + padding)

    fname = escape_fname("{} {}.png".format(group, data_type))
    p = path.join(save_dir, fname)
    plt.savefig(p)
    plt.close()


def make_date_lines(G, limit=7, data_types=None):
    if data_types is None:
        data_types = {
                'betweenness': 'greatest',
                'degree': 'greatest',
                'subject/object bias': 'greatest',
                'object/subject bias': 'greatest',
                'total sentiment': 'greatest and least',
                'in sentiment': 'greatest and least',
                'out sentiment': 'greatest and least'
                }

        G_date_list = network.get_temporal_graphs()
        for data_type, sort in data_types.iteritems():
            date_line(G, G_date_list, config.chart_dir, data_type, sort, limit)

def date_line(G, G_date_list, save_dir, data_type, group, limit):
    # limt warning
    if limit > 7:
        print "WARNING: Limit is greater than 7. Will reuse colors."

    # find top entities
    data = DATA_FUNCS[data_type](G)
    entities = sort_dict(data, group, limit).keys()

    # prepare chart_dict
    chart_dict = {}
    for entity in entities:
        chart_dict[entity] = {
                'x':[],
                'y':[]
                }

    # cycle through all temporal graphs and populate chart_dict
    for g, d in G_date_list:
        float_date = matplotlib.dates.date2num(d)

        try:
            temporal_data = DATA_FUNCS[data_type](g)
        # no nodes found in this month.
        except KeyError:
            continue

        for entity in entities:
            chart_dict[entity]['x'].append(float_date)
            try:
                # chart_dict[entity]['y'].append(temporal_data[entity])
                data_point = temporal_data[entity]

            # entity does not appear this month
            except KeyError:
                data_point = 0

            if len(chart_dict[entity]['y']) > 0:
                chart_dict[entity]['y'].append(
                        chart_dict[entity]['y'][-1] + data_point)
            else:
                chart_dict[entity]['y'].append(data_point)

    # plot out each of the entities
    fmt_colors = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-']
    count = 0
    for entity, values in chart_dict.iteritems():

        fmt = fmt_colors[count % len(fmt_colors)]
        count += 1
        # color = get_color(mix=(0, 250, 100)) + (1,)

        plt.plot_date(values['x'], values['y'],
            label=entity,
            fmt=fmt
            )

    # set chart properties
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.ylabel(data_type)
    plt.tick_params(labelsize=9)
    fname = escape_fname("{} {} over time".format(group, data_type))
    plt.title("{} {} Over Time".format(group, data_type).title())
    p = path.join(save_dir, fname + ".png")

    # save the chart
    plt.savefig(p, bbox_inches='tight')
    plt.close()


# Utility Functions
def sort_dict(data_dict, group, limit):
    sorted_data = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)

    if group == 'greatest':
        limited_data = sorted_data[0:limit]
    elif group == 'least':
        if limit == -1:
            end_limit = 0
        else:
            end_limit = len(sorted_data) - limit

        limited_data = sorted_data[-1:end_limit:-1]
    elif group == 'greatest and least':
        if limit == -1:
            end_limit = 0
        else:
            end_limit = len(sorted_data) - limit/2
        limited_data = sorted_data[:limit/2] + sorted_data[end_limit:]

    return OrderedDict(limited_data)


def correspond(x_dict, y_dict):
    """Finds the corresponding key in x_dict for each key
    in y_dict. Returns an OrderedDict of x values that corresponding
    to the group and values in y_dict."""
    new_x = OrderedDict()
    for key, value in y_dict.iteritems():
        new_x[key] = x_dict[key]

    return new_x

def escape_fname(fname):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in fname if c in valid_chars)



