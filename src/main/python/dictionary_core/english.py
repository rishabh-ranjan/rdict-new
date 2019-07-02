#!/usr/bin/env python3

# TODO: support for derivative words

from fbs_runtime.application_context.PyQt5 import ApplicationContext
import json
import string

data, css = None, None

# parse all required resource files into their corresponding variables
def parse():

    global data, css

    appctxt = ApplicationContext()
    datafile = appctxt.get_resource('dictionary_data/english.json')
    cssfile = appctxt.get_resource('styles/english.css')

    with open(datafile) as df:
        raw = df.read()
    data = json.loads(raw)

    with open(cssfile) as cf:
        css = cf.read()

# recursively builds formatted HTML string for val
tabstr = '&nbsp;' * 4
br = '<br/>'
def toHtml(val, indent = 0, res = ''):

    if type(val) == dict:
        for k, v in val.items():

            kc = k.strip().lower()
            for i in range(len(kc)):
                if kc[i] not in string.ascii_lowercase:
                    kc = kc[:i] + '_' + kc[i + 1:]

            res += f'{indent * tabstr}<span class = "label {kc}">{k}</span>{br}\n'
            res += f'<span class = "content {kc}_child">\n'
            res = toHtml(v, indent + 1, res)
            res += '</span>\n'

    elif type(val) == list:
        for v in val:
            res = toHtml(v, indent, res)

    else:
        res += f'{indent * tabstr}<span class = "item">{val}</span>{br}\n'

    return res

# return formatted word definition
def define(word):
    global data

    # binary search
    lo = 0
    hi = len(data) - 1
    res = None
    while hi >= lo:
        mid = (hi + lo) // 2

        if data[mid]['word'] == word:
            res = data[mid]
            break
        
        if data[mid]['word'] < word:
            lo = mid + 1
        else:
            hi = mid - 1

    style = f'<style>\n{css}\n</style>\n'
    if res is None:
        return style + '<span class = "not_found">Sorry! Word not found.</span>'
    else:
        return style + toHtml(res)

