import urllib.request
import urllib
import re
import webbrowser
import os
import platform
import html
import math
import datetime as dt
import sys

try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

import datetime

def julianDate(my_date):
    # Takes a date string MM-DD-YYYY and
    # returns Julian Date
    date = my_date.split("-")

    month = int(date[0])
    day   = int(date[1])
    year  = int(date[2])

    month=(month-14)/12
    year=year+4800
    JDate=1461*(year+month)/4+367*(month-2-12*month)/12-(3*((year+month+100)/100))/4+day-32075
    return JDate

# Function from:  https://gist.github.com/jiffyclub/1294443
def date_to_jd(year,month,day):
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)
    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)

    D = math.trunc(30.6001 * (monthp + 1))

    jd = B + C + D + day + 1720994.5
    return jd

# Function from:  https://gist.github.com/jiffyclub/1294443
def jd_to_date(jd):
    jd = jd + 0.5
    F, I = math.modf(jd)
    I = int(I)
    A = math.trunc((I - 1867216.25)/36524.25)
    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I
    C = B + 1524
    D = math.trunc((C - 122.1) / 365.25)
    E = math.trunc(365.25 * D)
    G = math.trunc((C - E) / 30.6001)
    day = C - E + F - math.trunc(30.6001 * G)
    if G < 13.5:
        month = G - 1
    else:
        month = G - 13
    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715
    return year, month, day

# Clear screen
def cls():
    if platform.system() == "Windows":
        os.system('cls')  # for Windows
    else:
        os.system('clear')  # for Linux/OS X

# Find string between 2 strings
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Download image to location
def downloadImage( url, fileName ):
    with urllib.request.urlopen(url) as f:
        htmlSource = str(f.read())
        imageURL = find_between( htmlSource, "data-image=", "data-date=" )
        urlNoQuotes = imageURL.replace('"', '').strip()
        #print("Image URL: " + str(urlNoQuotes))
        #webbrowser.open(urlNoQuotes)
        urllib.request.urlretrieve(urlNoQuotes, fileName)

def downloadImageTo( url, fileName ):
    urllib.request.urlretrieve(url, fileName)

def getImageHTML ( url ):
    with urllib.request.urlopen(url) as f:
        htmlSource = str(f.read())
        return htmlSource

def getImageURL ( html ):
    imageURL = find_between( html, "data-image=", "data-date=" )
    return imageURL.replace('"', '').strip()

def getImageTitle ( html ):
    imageTitle = find_between( html, "data-title=", "data-tags=" )
    h = HTMLParser()
    imageTitle = h.unescape(imageTitle)
    #print(h.unescape(imageTitle))
    return imageTitle.replace('"', '').strip()

def clearSplash ():
    cls()
    print("  ###                           ###")
    print(" # Dilbert Downloader - CorpNewt #")
    print("###                           ###")
    print("")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Start of script                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

response1 = ""
response2 = ""
tooMany = 100

# Get some preliminary values
todayDate = dt.datetime.today().strftime("%m-%d-%Y")
tDate = todayDate.split("-")
tJDate = date_to_jd(int(tDate[2]), int(tDate[0]), int(tDate[1]))

firstDate = "04-16-1989"
fDate = firstDate.split("-")
fJDate = date_to_jd(int(fDate[2]), int(fDate[0]), int(fDate[1]))

clearSplash()
print("First Dilbert Comic:  04-16-1989")
print("")
print("Just press [enter] for today")
print("")
response1 = input("Enter the start date (MM-DD-YYYY): ")

if response1 == "":
    response1=dt.datetime.today().strftime("%m-%d-%Y")
    response2=response1

try:
    startDate = response1.split("-")
except ValueError:
    print("Not valid date.")
    sys.exit()

if response2 == "":
    clearSplash()
    print("Start date: " + response1)
    print("")
    response2 = input("Enter the end date (MM-DD-YYY): ")
    if response2 == "":
        response2=dt.datetime.today().strftime("%m-%d-%Y")

try:
    endDate = response2.split("-")
except ValueError:
    print("Not valid date.")
    sys.exit()

startJDate = date_to_jd(int(startDate[2]), int(startDate[0]), int(startDate[1]))
endJDate = date_to_jd(int(endDate[2]), int(endDate[0]), int(endDate[1]))

outOfRange = False

# Check date ranges
if startJDate < fJDate:
    outOfRange = True
if startJDate > tJDate:
    outOfRange = True
if endJDate < fJDate:
    outOfRange = True
if endJDate > tJDate:
    outOfRange = True

if outOfRange:
    clearSplash()
    print("Date(s) out of range. Must be between " + firstDate + " and " + todayDate)
    print("")
    sys.exit()

difference = endJDate - startJDate

if difference < 0:
    # We've got our dates backwards - reverse them
    tempJ = startJDate
    startJDate = endJDate
    endJDate = tempJ
    # Flip the difference polarity
    difference *= -1

# Increment difference to include the end date
difference += 1

clearSplash()

if (difference >= tooMany):
    warning = input("Are you SURE you want to download " + str(int(difference)) + " comics? (y/n): ")
    if warning[0:1].lower() != "y".lower():
        # We didn't get "y" as our response - exit
        sys.exit()

if (difference == 1):
    print("Downloading " + response1)
else:
    print("Downloading from " + response1 + " to " + response2)
    print(str(int(difference)) + " day(s) to download...")

print("")

dlCount = 0
currentImage = 1
skippedImages = 0

while (startJDate <= endJDate):
    # Let's get the date - and parse/download our image
    gDate = jd_to_date(startJDate)

    # Prep dir names
    yDir = str(gDate[0])
    mDir = str(gDate[1])
    dName = str(int(gDate[2]))

    if (gDate[1] < 10):
        mDir = "0"+mDir

    if (gDate[2] < 10):
        dName = "0"+dName

    dirPath = "./Dilbert/" + yDir + "/" + mDir

    # Check directories
    if not os.path.isdir(dirPath):
        os.makedirs(dirPath)

    # Get URL
    getURL = "http://dilbert.com/strip/" + str(gDate[0]) + "-" + mDir + "-" + dName

    clearSplash()

    dateString = "{}-{}-{}".format(mDir, dName, yDir)

    print("Image " + str(currentImage) + " of " + str(int(difference)) + " - " + dateString)
    print("")
    print("Getting source from: " + getURL)

    # Retrieve HTML and other info
    imageHTML = getImageHTML(getURL)
    imageURL  = getImageURL(imageHTML)
    imageName = dName + " - " + getImageTitle(imageHTML) + ".jpg"
    imageDest = dirPath + "/" + imageName

    print("Image located at: " + imageURL)
    print("Downloading to: " + imageName)

    # Check if image exists
    if os.path.isfile(imageDest):
        print("ERROR:  Already Exists - skipping.")
        skippedImages += 1
    else:
        # Download image
        downloadImageTo( imageURL, imageDest)
        dlCount += 1

    # Increment Counter
    startJDate += 1
    currentImage += 1

    # Print newline
    print("\n")

clearSplash()
print(str(dlCount) + " of " + str(int(difference)) + " images downloaded.")
print(str(skippedImages) + " image(s) skipped.")
print("")
print("Done.")
print("")
