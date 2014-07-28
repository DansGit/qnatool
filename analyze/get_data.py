import igraph as ig


def betweenness(G):
    betweens = G.betweenness()
    params = zip(G.vs['name'], betweens)
    # return {x[0]:x[1] for x in params}
    return dict(params)


def sobias(G):
    sobias_dict = {}

    for vertex in G.vs:
        in_degree = G.degree(vertex, mode=ig.IN)
        out_degree = G.degree(vertex, mode=ig.OUT)

        # solve divide by zero error
        if in_degree == 0 or type(in_degree) is not int:
            in_degree = 1

        sobias_dict[vertex['name']] = out_degree / float(in_degree)

    return sobias_dict


def osbias(G):
    osbias_dict = {}

    for vertex in G.vs:
        in_degree = G.degree(vertex, mode=ig.IN)
        out_degree = G.degree(vertex, mode=ig.OUT)

        # solve divide by zero error
        if out_degree == 0 or type(out_degree) is not int:
            out_degree = 1

        osbias_dict[vertex['name']] = in_degree / float(out_degree)

    return osbias_dict


def degree(G, mode=ig.ALL):
    degrees = G.vs.degree(mode=mode)
    names = G.vs['name']
    params = zip(names, degrees)
    return dict(params)


def in_degree(G):
    return degree(G, mode=ig.IN)


def out_degree(G):
    return degree(G, mode=ig.OUT)


def in_sentiment(G):
    in_sentiment_dict = {}

    for vertex in G.vs:
        # print G.es.select(_target_eq=vertex.index)['weight']
        sentiment = sum(G.es.select(_target_eq=vertex.index)['sentiment'])

        try:
            sentiment = sentiment / float(vertex.indegree())
        except ZeroDivisionError:
            sentiment = 0

        in_sentiment_dict[vertex['name']] = sentiment

    return in_sentiment_dict


def out_sentiment(G):
    out_sentiment_dict = {}

    for vertex in G.vs:
        sentiment = sum(G.es.select(_source_eq=vertex.index)['sentiment'])

        try:
            sentiment = sentiment / float(vertex.outdegree())
        except ZeroDivisionError:
            sentiment = 0

        out_sentiment_dict[vertex['name']] = sentiment

    return out_sentiment_dict


def total_sentiment(G):
    sentiment_dict = {}

    for vertex in G.vs:
        in_sentiment = sum(G.es.select(_target_eq=vertex.index)['weight'])
        out_sentiment = sum(G.es.select(_source_eq=vertex.index)['weight'])
        sentiment = (in_sentiment + out_sentiment) / float(vertex.degree())
        sentiment_dict[vertex['name']] = sentiment

    return sentiment_dict
