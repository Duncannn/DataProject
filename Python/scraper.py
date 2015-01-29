#!/usr/bin/env python
# Name:
# Student number:
'''
This script scrapes IMDB and outputs a CSV file with highest ranking tv series.
'''
# IF YOU WANT TO TEST YOUR ATTEMPT, RUN THE test-tvscraper.py SCRIPT.
import os
import sys
import csv
import codecs
import cStringIO
import errno

from pattern.web import URL, DOM, plaintext

# ----------------------------------------------------------------------------------------

TARGET_URL = "http://finance.yahoo.com/q/op?s="
stocks = ["AMZN&date=", "AAPL&date=", "BIDU&date=", "CL&date=", "COST&date=", "GS&date=",
          "IBM&date=", "MA&date=", "NTES&date=", "NFLX&date=", "RL&date=", "WYNN&date="]
MATURITY_DATES = [("January 2, 2015", '1420156800'), ("January 9, 2015",'1420761600'), 
                  ("January 17, 2015",'1421452800'), ("January 23, 2015",'1421971200'),
                  ("January 30, 2015", '1422576000')]
SCRIPT_DIR = os.path.split(os.path.realpath(__file__))[0]

# ----------------------------------------------------------------------------------------

class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# ----------------------------------------------------------------------------------------

def create_dir(directory):
    '''
    Create directory if needed.

    Args:
        directory: string, path of directory to be made


    Note: the backup directory is used to save the HTML of the pages you
        crawl.
    '''

    try:
        os.makedirs("/Users/duncanbarker/Desktop")
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Backup directory already exists, no problem for this script,
            # just ignore the exception and carry on.
            pass
        else:
            # All errors other than an already exising backup directory
            # are not handled, so the exception is re-raised and the 
            # script will crash here.
            raise


def save_csv(filename, rows):
    '''
    Save CSV file with the top 250 most popular movies on IMDB.

    Args:
        filename: string filename for the CSV file
        rows: list of rows to be saved (250 movies in this exercise)
    '''
    with open(filename, 'wb') as f:
        writer = UnicodeWriter(f)  # implicitly UTF-8
        writer.writerow([])

        writer.writerows(rows)

# ----------------------------------------------------------------------------------------

def extract_prices(dom):
    call_strike = []
    put_strike = []
    for call in dom.by_id("optionsCallsTable").by_tag("table.details-table quote-table Fz-m")[:]:
        for strike in call.by_tag("tr")[2:]:
            call_strike.append(strike.by_tag("a")[0].content.encode('utf8'))
            call_strike.append(strike.by_tag("div.option_entry Fz-m")[1].content.encode('utf8'))
    for put in dom.by_id("optionsPutsTable").by_tag("table.details-table quote-table Fz-m")[:]:
        for strike in put.by_tag("tr")[2:]:
            put_strike.append(strike.by_tag("a")[0].content.encode('utf8'))
            put_strike.append(strike.by_tag("div.option_entry Fz-m")[1].content.encode('utf8'))
    return call_strike, put_strike

def exparations(stocks, MATURITY_DATES):
    rows = []
    for stock in stocks:
        for date in MATURITY_DATES:
            print "Scraping stock "+ stock + date[1]
            new_URL = TARGET_URL + stock + date[1]
            url = URL(new_URL)
            html = url.download()
            dom = DOM(html)
            prices =  extract_prices(dom)
            rows.append(["CALL " + stock + date[1]] + prices[0])
            rows.append(["PUT " + stock + date[1]] + prices[1])
    print "Saving CSV ..."
    save_csv(os.path.join(SCRIPT_DIR, 'PutCallData.csv'), rows)

# ----------------------------------------------------------------------------------------
    
if __name__ == '__main__':
    # Download the HTML file
    #tvseries = exparations(stocks, MATURITY_DATES)

# Have all those 10 stock charts, click on one of them and given the spread, strike prices and current stock price
# which will then be some time at the 30th of januari, we check what the spread will be worth.
