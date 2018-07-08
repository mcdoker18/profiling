import collections

from profiling.stats import FrozenStatistics


def _connect_traces(parent, child):
    if child is None:
        child = 'kek'

    if parent:
        return parent + ";" + child
    else:
        return child


def _spread_stats(root):
    d = collections.deque(
        ((root.regular_name, child) for child in root.children))

    while d:
        name, stats = d.popleft()
        children = stats.children

        if children:
            d.extend(
                (_connect_traces(name, stats.regular_name), child) for child in
                children
            )

        yield "{} {}".format(_connect_traces(name, stats.regular_name),
                             stats.own_hits)


def convert(stats):
    # type: (FrozenStatistics) -> str
    """Convert a stats to the flamegraph format"""

    return '\n'.join(_spread_stats(stats))
