# \
# \fixlen = T
# \RowsRetrieved =              3502
# \For detailed descriptions of the columns, go to http://exoplanetarchive.ipac.caltech.edu/docs/documentation.html and choose the appropriate table guide.
# \
# \ pl_name
# \ ___ Planet Common Name
# ...
# \ pl_disc
# \ ___ Year of Discovery
# \
# |                                            pl_name|   pl_bmasse|  pl_rade| pl_eqt|            pl_orbper|   st_dist| pl_disc|
# |                                               char|      double|   double|   long|               double|    double|     int|
# |                                                   |      Mearth|   Rearth|      K|                 days|        pc|        |
# |                                               null|        null|     null|   null|                 null|      null|    null|
#                                            HD 4732 b    753.23000      null    null          360.20000000      56.50     2012

import sqlite3
import time
import ssl
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Create database for data
conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

# Prepare parameters for API query
baseurl = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table="
table = "exoplanets"
col_names = "&select=pl_name,pl_bmasse,pl_rade,pl_eqt,pl_orbper,st_dist,pl_disc"
params = ""
out_format = "&format=ascii"

url = baseurl + table + col_names + params + out_format

# Get data from URL
text = "None"
try:
    # Open with a timeout of 30 seconds
    document = urllib.request.urlopen(url, None, 30, context=ctx)
    text = document.read().decode()
    if document.getcode() != 200 :
        print("Error code=",document.getcode(), url)
except KeyboardInterrupt:
    print('')
    print('Program interrupted by user...')
except Exception as e:
    print("Unable to retrieve or parse page",url)
    print("Error",e)

# Form table with SQLite
cur.execute('''DROP TABLE IF EXISTS Exoplanets ''')
cur.execute('''CREATE TABLE IF NOT EXISTS Exoplanets
    (id INTEGER UNIQUE, pl_name TEXT, pl_bmasse REAL, pl_rade REAL,
    pl_eqt BIGINT, pl_orbper REAL, st_dist REAL, pl_disc INTEGER)''')


# Parse data retrieved by rows
count = 0
rows = 0
columns = []    # list of tuples (name, fullname)
name, fullname = "None", "None"
for line in text.splitlines():
    # Line breaks are not included - "splitlines()"

    line = line.strip()
    # Parse headers
    if line.startswith('\\'):
        # Some meta info
        if not line.startswith('\\ '):
            if line.startswith('\\Rows'):
                pos = line.find('=')
                try:
                    # In Python 3 long int is included to int()
                    rows = int(line[pos+1:].lstrip())
                except:
                    pass
                print("Rows: ", rows)
                print("URL: ", url)
                print('\nFirst 5 rows of data retrieved:')

        # Column names
        else:
            if not line.startswith('\\ ___'):
                if name == "None": name = line.split()[1]
            else:
                if fullname == "None":
                    pos = line.rfind('_') + 1
                    pos2 = line.rfind('[')
                    fullname = line[pos:].strip() if pos2 == -1 else line[pos:pos2-1].strip()

            if name != "None" and fullname != "None":
                columns.append((name, fullname))
                name, fullname = "None", "None"
        continue

    # Parse data after headers
    if line.startswith('|'): continue
    # Split line if delimiter includes 2 or more whitespaces
    s = re.split('  +', line)

    count += 1
    # First 5 rows of data retrieved
    if count <= 5: print(s)

    # Data update for planets with high Planetary habitability
    #1
    if s[0] == 'Kepler-438 b':
        if s[1] == 'null' : s[1] = '1.30000'
        if s[3] == 'null' : s[3] = '276'
    #2
    if s[0] == 'Kepler-296 e':
        if s[1] == 'null' : s[1] = '1.00000'    # mass unknown
        if s[3] == 'null' : s[3] = '267'
    #3
    if s[0] == 'GJ 667 C c':
        if s[1] == 'null' : s[1] = '3.70900'
        if s[3] == 'null' : s[3] = '277'
    #4
    if s[0] == 'Kepler-442 b':
        if s[1] == 'null' : s[1] = '2.30000'
        if s[3] == 'null' : s[3] = '233'
    #5
    if s[0] == 'GJ 832 c':
        if s[2] == 'null' : s[2] = '1.50000'
        if s[3] == 'null' : s[3] = '253'
    #6
    if s[0] == 'Kepler-452 b':
        if s[1] == 'null' : s[1] = '5.00000'
        if s[5] == 'null' : s[5] = '430.00'
    #7
    if s[0] == 'Kepler-1410 b':
        if s[1] == 'null' : s[1] = '2.57000'
        if s[3] == 'null' : s[3] = '274'

    # (To paste values to all columns in right order there is no need to write column names)
    cur.execute('''INSERT OR IGNORE INTO Exoplanets (id, pl_name, pl_bmasse, pl_rade,
                                                    pl_eqt, pl_orbper, st_dist, pl_disc)
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )''', ( count, s[0], s[1], s[2], s[3], s[4], s[5], s[6]))
    # No conversion required: the column type name affects how values are processed before being stored

    if count % 500 == 0 : conn.commit()

conn.commit()
cur.close()
