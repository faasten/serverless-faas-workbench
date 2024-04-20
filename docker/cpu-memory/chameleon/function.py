from time import time, perf_counter
# import six
import json
from chameleon import PageTemplate


BIGTABLE_ZPT = """\
<table xmlns="http://www.w3.org/1999/xhtml"
xmlns:tal="http://xml.zope.org/namespaces/tal">
<tr tal:repeat="row python: options['table']">
<td tal:repeat="c python: row.values()">
<span tal:define="d python: c + 1"
tal:attributes="class python: 'column-' + %s(d)"
tal:content="python: d" />
</td>
</tr>
</table>""" % "str"


def main(event):
    latencies = {}
    timestamps = {}
    timestamps["starting_time"] = perf_counter()
    num_of_rows = event['num_of_rows']
    num_of_cols = event['num_of_cols']
    metadata = event['metadata']

    start = perf_counter()
    # tmpl = PageTemplate(BIGTABLE_ZPT)

    # data = {}
    # for i in range(num_of_cols):
    #     data[str(i)] = i

    # table = [data for x in range(num_of_rows)]
    # options = {'table': table}

    # data = tmpl.render(options=options)
    latency = perf_counter() - start
    latencies["function_execution"] = latency
    timestamps["finishing_time"] = perf_counter()

    return {"latencies": latencies, "timestamps": timestamps, "metadata": metadata, "version": 0.1}
