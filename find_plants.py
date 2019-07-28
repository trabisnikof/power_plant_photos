from GPSPhoto import gpsphoto
from haversine import haversine, Unit
from glob import glob
import os
import csv
cutoff_km = 1.0
photo_dir = 'photos/'

# Open the CSV with Plant Info
with open('plants.csv', 'rU') as f:
    reader = csv.reader(f)
    headers = next(reader, None)
    plants = list(reader)

#Finds the closest plant using a simple brute force. Could be optimized....
def closest_plant(photo_path):
    data = gpsphoto.getGPSData(photo_path)
    try:
        photo_gps = (float(data['Latitude']), float(data['Longitude']))
        closest = None
        for i in plants:
            plant_gps = (float(i[9]),float(i[10]))
            if closest is None:
                closest = [haversine(plant_gps, photo_gps)] + i
            if closest[0] > haversine(plant_gps, photo_gps):
                closest = [haversine(plant_gps, photo_gps)] + i
        return closest
        # Catch KeyError so we can ignore photos without any GPS.
    except KeyError:
        return None


def at_plant(photo_path):
    closest = closest_plant(photo_path)
    if closest is None:
        return None
    elif closest[0] < cutoff_km:
        return closest
    else:
        return None

def output_csv(list):
    with open('output.csv','a') as output:
        for i in list:
            writer = csv.writer(output)
            writer.writerow(i)

def process_photos(photo_dir_path):
    result_list = []
    # A bit hacky, but gets the job done of dealing with folder trees. Could be expanded to include other extensions.
    photos = [y for x in os.walk(photo_dir_path) for y in glob(os.path.join(x[0], '*.JPG'))]
    print("Number of Photos: {}".format( len(photos)))
    for i in photos:
        result = at_plant(i)
        if result is not None:
            print (result)
            result_list.append(result)
    output_csv(result_list)
    return result_list

print process_photos(photo_dir)
