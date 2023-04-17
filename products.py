import csv
import os


def read_file(path):
    # create dictionary variable for storing data under string names
    object = {}
    # init array of objects
    objects = []
    # open given file and read data within ';' delimiter
    with open(path, newline="") as file:
        data = csv.reader(file, delimiter=';')
        for i, row in enumerate(data):
            # first row is headers
            if i == 0:
                headers = row
            else:
                # rest of rows are the data
                # nazwa
                object[headers[0]] = row[0]
                # under header[0] there is string "nazwa" so it equals to  object["nazwa"] = row[0]

                # cena brutto
                object[headers[1]] = row[1]
                # cena netto
                object[headers[2]] = row[2]
                # numer zdjecia
                object[headers[3]] = row[3] + ".png"
                # atrybut
                object[headers[4]] = row[4]
                # append object to list
                objects.append(object.copy())

    return objects


def check_if_images_exists(products, image_folder):
    file_list = []
    errors = []
    # go to the images folder and get all the files with .png extension
    for file in os.listdir(image_folder):
        if file.endswith(".png"):
            file_list.append(file)
    # search names from the list within the images in the folder. If there is a picture then create a path
    # if there aren't add error to error list
    for product in products:
        file_name = product["numer zdjecia"]
        if file_name in file_list:
            product["numer zdjecia"] = image_folder + file_name
        else:
            errors.append(file_name)
    # return errors
    return errors
