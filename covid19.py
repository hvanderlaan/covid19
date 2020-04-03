#!/usr/bin/env python3

""" covid19.py - small python script to generate graphs about the spread
                 of the coronavirus (Covis-19). """

# =========================================================================== #
# File   : covid19.py                                                         #
# Purpose: Small python script to graph the Covid-19 outbreak                 #
#                                                                             #
# Author : Harald van der Laan                                                #
# Date   : 2020-04-03                                                         #
# Version: v1.0.0                                                             #
# =========================================================================== #
# Changelog:                                                                  #
# - v1.0.0: Initial commit                              (Harald van der Laan) #
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
    counter = 0

    data = get_plot_values(url, country)

    # creating a time scale for the x axis.
    for _ in range(0, len(data) - 1):
        xvalues.append(counter)
        counter = counter + 1

    # Filling the y axis lists with the remote values
    for _ in range(0, len(data) - 1):
        infected.append(data[_]['confirmed'])
        deaths.append(data[_]['deaths'])
        recovered.append(data[_]['recovered'])

    # Creating plots for the graphs.
    matplotlib.pyplot.figure(figsize=(10, 7))
    matplotlib.pyplot.subplot(3, 1, 1)
    matplotlib.pyplot.plot(xvalues, infected, '-ob')
    matplotlib.pyplot.xlabel('Dag')
    matplotlib.pyplot.ylabel('Besmettingen')
    matplotlib.pyplot.title(f'Covid-19 in {country}')

    matplotlib.pyplot.subplot(3, 1, 2)
    matplotlib.pyplot.plot(xvalues, deaths, '-or')
    matplotlib.pyplot.xlabel('Dag')
    matplotlib.pyplot.ylabel('Doden')

    matplotlib.pyplot.subplot(3, 1, 3)
    matplotlib.pyplot.plot(xvalues, recovered, '-og')
    matplotlib.pyplot.xlabel('Dag')
    matplotlib.pyplot.ylabel('Genezen')

    if args.export:
        # argument -e is provided save graph to file
        matplotlib.pyplot.savefig(args.export)

    matplotlib.pyplot.show()


if __name__ == "__main__":
    ARGS = get_arguments()
    main(ARGS)
