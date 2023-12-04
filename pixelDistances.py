import math
import csv

# data cleaning function to remove empty values from lists and convert values to int, float
def clean(values):
    values = list(filter(lambda x : x[0], values))
    for row in values:
        row[0] = int(row[0])
        row[1] = float(row[1])
        row[2] = float(row[2])
    return values

# IMPORT CSV
def ingest(readFile):
    greens = []
    purples = []
    print('opening: ',readFile )
    with open(readFile, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # EXTRACT PIXEL DATA
            pixelG,pixelGx,pixelGy = row[0],row[1],row[2]
            pixelP,pixelPx,pixelPy = row[3],row[4],row[5]            
            # ADD PIXEL DATA TO LISTS
            greens.append([pixelG,pixelGx,pixelGy])
            purples.append([pixelP,pixelPx,pixelPy])
    return greens, purples

def calculate(greens,purples):
    # DATA CLEANING

    greens = clean(greens)
    purples = clean(purples)

    newFileData = []

    # ITERATE OVER GREEN PIXEL VALUES
    for i in greens:
        pixelG,pixelGx,pixelGy = i

        # ITERATE OVER PURPLE PIXEL VALUES AND APPEND DISTANCES TO LIST
        distances = []
        for j in purples:
            pixelP,pixelPx,pixelPy = j
            distance = math.sqrt(((pixelGx-pixelPx) ** 2) + ((pixelGy-pixelPy) ** 2))
            distances.append([pixelP, distance])

        # SORT DISTANCES ASCENDING FOR EACH GREEN PIXEL
        distances.sort(key = lambda x: x[1])

        # NEW LINES FOR OUTPUT WITH GREEN PIXELS AND NEAREST NEIGHBOUR
        newFileData.append([pixelG,pixelGx,pixelGy,distances[0][0],distances[0][1]])
    
    return newFileData

def output(sheet,writeFile,newFileData):

    # EXPORT CSV WITH ADDED COLUMN

    with open(writeFile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sheet])
        writer.writerow(['Gpixel','GpixelX','GpixelY','Nearest Ppixel', 'Distance'])
        writer.writerows(newFileData)

    print("saved as:", writeFile)

def process(sheet):
    # FILENAMES
    readFile = f"./{sheet}.csv"
    writeFile = f"./solved/{sheet} Solved.csv"
    # open
    greens, purples = ingest(readFile)
    # calculate
    print('Processing: ', sheet)
    newFileData = calculate(greens, purples)
    # create new file
    output(sheet,writeFile,newFileData)

# FILES TO WORK ON
files = [
    'Cytosol Control 1',
    'Cytosol Control 2',
    'Cytosol Control 3',
    'Cytosol Treat 1',
    'Cytosol Treat 2',
    'Cytosol Treat 3',
    'Vesicle Control 1',
    'Vesicle Control 2',
    'Vesicle Control 3',
    'Vesicle Treat 1',
    'Vesicle Treat 3'
    ]

# WHERE THE ACTION HAPPENS
for file in files:
    process(file)
