import sqlite3
# Open the main content (Read only)
conn = sqlite3.connect('file:content.sqlite?mode=ro', uri=True)
cur = conn.cursor()

cur.execute('SELECT pl_name,pl_bmasse,pl_rade,pl_eqt,st_dist FROM Exoplanets')

with open('kbchart.js','w') as fhand:

    fhand.write("kbchart = [")

    first = True
    for row in cur:
        if first :
            fhand.write("[                              'Planet Name',  'Distance'," +
            "        'Mass',  'Temp.',   'Radius']")
            first = False
            continue

        # if Radius and Temperature are not null
        if row[2] == 'null' or row[3] == 'null' : continue
        # Find habitabale planets (similar to Earth)
        if 0.5 < row[2] < 5 and 150 < row[3] < 300:
            fhand.write(",\n['"+row[0].rjust(52)+"', "+str(row[4]).rjust(11)+", " +
            str(row[1]).rjust(13)+", "+str(row[3]).rjust(8)+", "+str(row[2]).rjust(10)+"]")
    # Add Earth to file (on chart) as example with test distance
    fhand.write(",\n['                                               EARTH'," +
    "         3.0,           1.0,      288,        1.0]")
    fhand.write("\n];\n")

print("Output written to kbchart.js")
print("Open kbchart.htm in a browser to see the vizualization")

cur.close()
