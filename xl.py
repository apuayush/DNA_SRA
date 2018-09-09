import csv

def search(e, l):
    for i in l:
        if e == i['pno']:
            return i['return']

    return '-'

def make_csv(name, num, data):
    with open('out.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if num == 0:
            spamwriter.writerow(["Num", "VTA", "Air Speed", "Barometer", "ICE", "Latitude", "Vertical Speed", "Compass", "Wind", "Slip"])
        spamwriter.writerow([str(num), search("2", data),search("3", data),search("4", data),search("5", data),search("6", data),search("7", data),search("8", data),search("9", data),search("10", data)])
