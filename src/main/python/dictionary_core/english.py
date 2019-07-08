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

    with open(datafile, encoding = 'utf8') as df:
        raw = df.read()
    data = json.loads(raw)

    with open(cssfile, encoding = 'utf8') as cf:
        css = cf.read()

# returns HTML string for data element d
def toHtml(d):

    tab = '&nbsp;' * 4
    br = '<br/>'
    bullet = '•'

    res = f'<span class="word"> {d["word"]} </span>{br * 2}\n'

    for word_type, multiple in d['meaning'].items():
        
        # derivative words can have '' as word_type. eg. ate
        if word_type:
            res += f'<span class="word_type"> {word_type} </span>{br * 2}\n'

        for single in multiple:

            res += f'<span class="bullet"> {bullet} </span>'
            res += f'<span class="definition"> {single["definition"]} </span>{br}\n'
            
            if 'example' in single:
                res += f'{tab}<span class="example_label"> example: </span>{br}\n'
                res += f'{tab * 2}<span class="example"> "{single["example"]}" </span>{br}\n'

            if 'synonyms' in single:
                res += f'{tab}<span class="synonyms_label"> synonyms: </span>{br}\n'
                res += f'{tab * 2}<span class="synonyms"> '
                for sy in single['synonyms'][:-1]:
                    res += f'{sy}, '
                res += f'{single["synonyms"][-1]}.</span>{br}\n'

            res += f'{br}'

    return res

# return formatted word definition
def define(word):

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

    style = f'<style>\n{css}</style>\n'
    if res is None:
        # TODO: .not_found CSS
        return style + '<span class="not_found"> Sorry! Word not found. </span>'
    else:
        return style + toHtml(res)

