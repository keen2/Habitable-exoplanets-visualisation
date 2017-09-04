import sqlite3
# Open the main content (Read only)
conn = sqlite3.connect('file:content.sqlite?mode=ro', uri=True)
cur = conn.cursor()

cur.execute('SELECT pl_disc FROM Exoplanets')
years = {}
for row in cur:
    years[row[0]] = years.get(row[0],0) + 1
years_list = sorted(years)

fhand = open('khistogram.js','w')
fhand.write("khistogram = [")
first = True
for year in years_list:
    if not first : fhand.write( ",\n")
    first = False
    fhand.write("{year: '"+str(year)+"', amount: "+str(years[year])+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to khistogram.js")
print("Open khistogram.htm in a browser to see the vizualization")

cur.close()
