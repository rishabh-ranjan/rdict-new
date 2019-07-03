#!/usr/bin/env python3

from fbs_runtime.application_context.PyQt5 import ApplicationContext

data, css = None, None

# parse all required resource files into their corresponding variables
def parse():

    global data, css

    appctxt = ApplicationContext()
    datafile = appctxt.get_resource('dictionary_data/hindi.txt')
    cssfile = appctxt.get_resource('styles/hindi.css')

    with open(datafile) as df:
        dlim = '\t'
        ilim = ','
        data = {}
        for line in df:
            l = line.split(dlim)
            data[l[0]] = l[1].split(ilim)

    with open(cssfile) as cf:
        css = cf.read()

# returns HTML string for data element d (key, value pair)
def toHtml(d):

    br = '<br/>'
    bullet = '•'

    res = f'<span class="word"> {d[0]} </span>{br * 2}\n'

    for defn in d[1]:
        res += f'<span class="bullet"> {bullet} </span>'
        res += f'<span class="definition"> {defn} </span>{br}\n'

    return res

# return formatted word definition
def define(word):

    style = f'<style>\n{css}</style>\n'

    # hash-table retrieve
    if word in data:
        return style + toHtml((word, data[word]))
    else:
        return style + '<span class="not_found"> Sorry! Word not found. </span>'

