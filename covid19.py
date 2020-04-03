#!/usr/bin/env python3

""" covid19.py - small python script to generate graphs about the spread
                 of the coronavirus (Covis-19). """

# =========================================================================== #
# File   : covid19.py                                                         #
# Purpose: Small python script to graph the Covid-19 outbreak                 #
#                                                                             #
# Author : Harald van der Laan                                                #
# Date   : 2020-04-03                                                         #
# Version: v1.0.1                                                             #
# =========================================================================== #
# Changelog:                                                                  #
# - v1.0.0: Initial commit                              (Harald van der Laan) #
# - v1.0.1: Update with more graphs                     (Harald van der Laan) #
# =========================================================================== #
# Copyright © 2020 Harald van der Laan                                        #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining       #
# a copy of this software and associated documentation files (the "Software") #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included     #
# in all copies or substantial portions of the Software.                      #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,             #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES             #
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.   #
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM  #
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,               #
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE  #
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                               #
# =========================================================================== #

import sys
import json
import argparse

import requests
import matplotlib.pyplot


def get_arguments():
    """ Function for getting commandline arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--country', default="Netherlands",
                        help="Country to generate graphs of")
    parser.add_argument('-e', '--export',
                        help="Export graph to filename.png")

    return parser.parse_args()


def get_plot_values(url, country):
    """ Function for getting remote dataset of the coronavirus
        This data set is updated every 8 hours, there is a
        possibility that you are seeing old data """
    response = requests.get(url)

    if response.ok:
        jsondata = json.loads(response.text)
    else:
        sys.stderr.write('Could not connect to API.\n')
        sys.exit(1)

    return jsondata[country]


def main(args):
    """ Main python function """
    url = 'https://pomber.github.io/covid19/timeseries.json'
    country = args.country

    xvalues = []
    infected = []
    deaths = []
    recovered = []

    # ipd = infected per day, dpd = deaths per day
    # rpd = recovered per day
    ipd = []
    dpd = []
    rpd = []
    counter = 0

    data = get_plot_values(url, country)

    for entry in data:
        # x axis of the graph
        xvalues.append(counter)

        # y axis of the graphs
        infected.append(entry['confirmed'])
        deaths.append(entry['deaths'])
        recovered.append(entry['recovered'])

        if counter == 0:
            ipd.append(data[counter]['confirmed'] - 0)
            dpd.append(data[counter]['deaths'] - 0)
            rpd.append(data[counter]['recovered'] - 0)
        else:
            ipd.append(data[counter]['confirmed'] - data[counter - 1]['confirmed'])
            dpd.append(data[counter]['deaths'] - data[counter - 1]['deaths'])
            rpd.append(data[counter]['recovered'] - data[counter - 1]['recovered'])

        counter += 1

    # Creating plots for the graphs.
    fig, ((gr1, gr2), (gr3, gr4), (gr5, gr6)) = matplotlib.pyplot.subplots(3, 2, figsize=(14, 7))
    fig.suptitle(f'Covid-19 in {args.country}')

    gr1.plot(xvalues, infected, '-ob')
    gr1.set_title('Totaal aantal besmettingen')

    gr2.plot(xvalues, ipd, '-ob')
    gr2.set_title('Besmettingen per dag')

    gr3.plot(xvalues, deaths, '-or')
    gr3.set_title('Totaal aantal doden')

    gr4.plot(xvalues, dpd, '-or')
    gr4.set_title('Doden per dag')

    gr5.plot(xvalues, recovered, '-og')
    gr5.set_title('Totaal aantal genezingen')

    gr6.plot(xvalues, rpd, '-og')
    gr6.set_title('Genezingen per dag')

    if args.export:
        # argument -e is provided save graph to file
        matplotlib.pyplot.savefig(args.export)

    matplotlib.pyplot.show()


if __name__ == "__main__":
    ARGS = get_arguments()
    main(ARGS)
