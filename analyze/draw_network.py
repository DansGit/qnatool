import igraph as ig
import config
import os

def draw(G, layout, label='name', name=None):
    if name is None:
        name = config.project_name

    style = {
            'vertex_label': [l for l in G.vs[label]],
            # I'm not sure why igraph isn't using the color attribute by
            # default, but this line seems to fix that problem.
            'vertex_color': ["{}, {}, {}".format(*color) for color in G.vs['color']],
            #'vertex_size': [20 + i * 60 for i in G.evcent(scale=True)],
            'vertex_size': [20 + i * 60 for i in _scale(G.pagerank())],
            # I made the edge colors a little too bright in the make_graph
            # function, so this line is a bit of a bandaid to darken them up.
            'edge_color': ["{}, {}, {}".format(*(y / 1.5 for y in x)) for x in G.es['color']],
            'margin': 100,
            'bbox': (2000, 2000)
            }

    fname = '{}.png'.format(name)
    l = G.layout(layout)

    try:
        ig.plot(G,
                os.path.join(config.output_dir, fname),
                layout=l,
                **style)
    except TypeError:
        # Plotting is not available
        print "Error: Plotting is not available. You probably don't have cairolib or py2cairo installed."

def _scale(seq):
    return [(x-min(seq))/(max(seq)-min(seq)) for x in seq]
