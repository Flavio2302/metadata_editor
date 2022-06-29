# Packages
from datetime import datetime
from PIL import Image
from pandas import isnull, notnull
import piexif, os, exifread

# Setting paths to folders
original_path = "C:/Users/flavi/Dropbox/1_Foto/xiaomi up to 24 Apr 2022/IMG-YYYYMMDD-WAXXXX"
target_path = "C:/Users/flavi/Dropbox/1_Foto/00_selected_photos/xiaomi up to 24 Apr 2022/IMG-YYYYMMDD-WAXXXX"

# Loop over files in folder
for filename in os.listdir(original_path):

    # extracting date from name
    year = int(filename[4:8])
    month = int(filename[8:10])
    day = int(filename[10:12])
        
    if filename.endswith("jpg") == 1:
        
        # converting to jpeg
        myimage = Image.open(original_path+"/"+filename)
        myimage.save(target_path+"/"+filename[0:-3]+"jpeg")

        # writing date
        exif_dict = piexif.load(target_path+"/"+filename[0:-3]+"jpeg")
        new_date = datetime(year, month, day, 12, 00, 00).strftime("%Y:%m:%d %H:%M:%S")
        exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, target_path+"/"+filename[0:-3]+"jpeg")
        
        # checking
        print(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
        
    elif filename.endswith("jpeg") == 1 :
        
        exif_dict = piexif.load(original_path+"/"+filename)
        
        if notnull(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]) == 1 and notnull(exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized]) == 1 and notnull(exif_dict['0th'][piexif.ImageIFD.DateTime]) == 1 :
            
            exif_dict_date = exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized]
            print(exif_dict_date)
            
            # extracting time from exif_dict
            # year = int(exif_dict_date[0:4])
            # month = int(exif_dict_date[5:7])
            # day = int(exif_dict_date[8:10])
            hour = int(exif_dict_date[11:13])
            minute = int(exif_dict_date[14:16])
            second = int(exif_dict_date[17:19])
            
            # writing date
            new_date = datetime(year, month, day, hour, minute, second).strftime("%Y:%m:%d %H:%M:%S")
            exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, original_path + "/" + filename)
            
        else :
            
            # writing date
            new_date = datetime(year, month, day, 12, 00, 00).strftime("%Y:%m:%d %H:%M:%S")
            exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, target_path+"/"+filename[0:-3]+"jpeg")