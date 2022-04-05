"""
Partition dataset of images into training and testing sets

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGEDIR, --imageDir IMAGEDIR
                        Path to the folder where the image dataset is stored. If not specified, the CWD will be used.
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Path to the output folder where the train and test dirs should be created. Defaults to the same directory as IMAGEDIR.
  -r RATIO, --ratio RATIO
                        The ratio of the number of test images over the total number of images. The default is 0.1.
  -x, --xml             Set this flag if you want the xml annotation files to be processed and copied over.
"""
import os
import re, glob
from shutil import copyfile
import argparse
import math
import random


# def iterate_dir(source, dest, ratio, copy_xml):
#     source = source.replace('\\', '/')
#     dest = dest.replace('\\', '/')
#     train_dir = os.path.join(dest, 'train')
#     test_dir = os.path.join(dest, 'test')

#     if not os.path.exists(train_dir):
#         os.makedirs(train_dir)
#     if not os.path.exists(test_dir):
#         os.makedirs(test_dir)

#     images = [f for f in os.listdir(source)
#               if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.jpeg|.png)$', f)]

#     num_images = len(images)
#     num_test_images = math.ceil(ratio*num_images)

#     for i in range(num_test_images):
#         idx = random.randint(0, len(images)-1)
#         filename = images[idx]
#         copyfile(os.path.join(source, filename),
#                  os.path.join(test_dir, filename))
#         if copy_xml:
#             xml_filename = os.path.splitext(filename)[0]+'.xml'
#             copyfile(os.path.join(source, xml_filename),
#                      os.path.join(test_dir,xml_filename))
#         images.remove(images[idx])

#     for filename in images:
#         copyfile(os.path.join(source, filename),
#                  os.path.join(train_dir, filename))
#         if copy_xml:
#             xml_filename = os.path.splitext(filename)[0]+'.xml'
#             copyfile(os.path.join(source, xml_filename),
#                      os.path.join(train_dir, xml_filename))
def data_split(source, dest, ratio, copy_xml):
    train_dir = os.path.join(dest, 'train')
    test_dir = os.path.join(dest, 'test')
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    images= glob.glob(source+'/**/*.jpg',recursive=True)
    num_images=len(images)
    num_test_images = math.ceil(ratio*num_images)
    count = 0
    images.sort()
    # print(images)
    for filedir in images:
        tmp_name = os.path.basename(filedir).split('.')[0].split('_')[0]
        name_num = os.path.basename(filedir).split('.')[0].split('_')[1]
        file_name = filedir.split('/')[-2]
        ch_name = tmp_name+'_'+file_name+'_'+name_num
        # print(ch_name)
        if count < (num_images-num_test_images):
            copyfile(filedir, os.path.join(train_dir, ch_name+'.jpg'))
            if copy_xml:
                xml_filename = os.path.basename(filedir).split('.')[0]+'.xml'
                copyfile(os.path.join(os.path.split(filedir)[0], xml_filename),
                os.path.join(train_dir, ch_name+'.xml'))
            count +=1
        else:
            copyfile(filedir, os.path.join(test_dir, ch_name+'.jpg'))
            if copy_xml:
                xml_filename = os.path.basename(filedir).split('.')[0]+'.xml'
                copyfile(os.path.join(os.path.split(filedir)[0], xml_filename),
                os.path.join(test_dir, ch_name+'.xml'))


def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Partition dataset of images into training and testing sets",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--imageDir',
        help='Path to the folder where the image dataset is stored. If not specified, the CWD will be used.',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to the output folder where the train and test dirs should be created. '
             'Defaults to the same directory as IMAGEDIR.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-r', '--ratio',
        help='The ratio of the number of test images over the total number of images. The default is 0.1.',
        default=0.1,
        type=float)
    parser.add_argument(
        '-x', '--xml',
        help='Set this flag if you want the xml annotation files to be processed and copied over.',
        action='store_true'
    )
    args = parser.parse_args()

    if args.outputDir is None:
        args.outputDir = args.imageDir

    # Now we are ready to start the iteration
    # iterate_dir(args.imageDir, args.outputDir, args.ratio, args.xml)
    data_split(args.imageDir, args.outputDir, args.ratio, args.xml)

if __name__ == '__main__':
    main()