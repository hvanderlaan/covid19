# covid-19 [![Build Status](https://travis-ci.org/hvanderlaan/covid19.svg?branch=master)](https://travis-ci.org/hvanderlaan/covid19)

This is a small python3 script that can plot all current infections of the corona virus. The graph will show the rate of infections, deaths and recovered persons over the time. Please nite that the dataset that is used, is updated every 8 hours. This could mean that you are seeing older data.

## usage:

``` bash
git clone https://github.com/hvanderlaan/covid19
cd covid19
pip3 install -r requirements.txt

sage: covid19.py [-h] [-c COUNTRY] [-e EXPORT] [-n]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNTRY, --country COUNTRY
                        Country to generate graphs of
  -e EXPORT, --export EXPORT
                        Export graph to filename.png
  -n, --nogui           Do not display a graph in gui

eg:
./covid19.py -c Netherlands
./covid19.py -c Germany -e Germany-2020-04-06.png
./covid19.py -c France -e France-2020-04-06.png -n
```

## Thanks to:

[https://github.com/pomber/covid19](https://github.com/pomber/covid19)
