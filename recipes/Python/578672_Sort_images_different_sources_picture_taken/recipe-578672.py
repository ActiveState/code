import os
import shutil
import Image
from PIL.ExifTags import TAGS

def print_all_known_exif_tags():
    for k in sorted(TAGS):
        print k, TAGS[k]

def print_all_exif_tags(image):
    try:
        img = Image.open(image)
    except Exception, e:
        print image, "skipping due to", e
    else:
        xf = img._getexif()
        for tag in xf:
            print TAGS.get(tag), xf[tag]
    finally:
        print 'done'


def get_minimum_creation_time(exif_data):
    mtime = "?"
    if 306 in exif_data and exif_data[306] < mtime: # 306 = DateTime
        mtime = exif_data[306]
    if 36867 in exif_data and exif_data[36867] < mtime: # 36867 = DateTimeOriginal
        mtime = exif_data[36867]
    if 36868 in exif_data and exif_data[36868] < mtime: # 36868 = DateTimeDigitized
        mtime = exif_data[36868]
    return mtime


def get_creationdate_with_filename_as_dict(list_of_folders):
    print "Processing all image files in:"

    result = {}
    for folder in list_of_folders:
        print "- " + folder
        counter = 0
        for f in os.listdir(folder):
            counter += 1
            fullFileName = folder + "\\" + f
            try:
                img = Image.open(fullFileName)
            except Exception, e:
                print "    Skipping '%s' due to exception: %s"%(f, e)
                continue
            mtime = get_minimum_creation_time(img._getexif())
            i = 0
            while mtime+"_"*i in result:
                i += 1
            mtime = mtime+"_"*i
            result[mtime] = fullFileName
        print "  Found %s orignal files in %s."%(counter, folder)
    print "Added total of %s to dictionary."%len(result)
    return result


def copy_from_image_dict_to_directory(image_dict, output_dir):
    assert os.path.exists(output_dir)
    for i,key in enumerate(sorted(image_dict)):
        dummy, extension =  os.path.splitext(image_dict[key])
        new_file_name = key.replace(":", "-") + extension
        output_file = output_dir + new_file_name
        shutil.copy2(image_dict[key], output_file)
    print "Copied %s files to %s"%(i+1, output_dir)


if __name__=="__main__":
    source_dir = "/var/tmp/images"
    output_dir = "/var/tmp/output"

    # obtain /var/tmp/images/iPhone, /var/tmp/images/CanonPowerShot, /var/tmp/images/Nikon1
    list_of_folders = [source_dir + subfolder for subfolder in os.listdir(source_dir)]

    all_files = get_creationdate_with_filename_as_dict(list_of_folders)
    copy_from_image_dict_to_directory(all_files, output_dir)
