# you can download PIL from http://www.pythonware.com/products/pil/
from PIL import Image
import os

"""
this class acts as a sequence class
we pass this to Image.putdata()
"""
class MyImageData:
    def __init__(self, image1_data, image2_data):
        self.im1_data = image1_data
        self.im2_data = image2_data

    def are_2rgbs_close_enough(self, rgb1, rgb2):
        upper_rgb = [c + 5 for c in rgb1]
        lower_rgb = [c - 5 for c in rgb1]
        for upper, lower, c in zip(upper_rgb, lower_rgb, rgb2):
            # print str(upper) + ' ' + str(lower) + ' ' + str(c)
            if lower < c < upper:
                return True
        return False

    def __len__(self):
        """
        Image.putdata() will use len(MyImageData)
        """
        return len(self.im1_data)

    def __getitem__(self, key):
        """
        Image.putdata() will use MyImageData[i]
        """
        if self.are_2rgbs_close_enough(self.im1_data[key], self.im2_data[key]):
            return self.im1_data[key]
        else:
            return (0,0,0)

    def __setitem(self, key, value):
        return

    def __delitem__(self, key):
        return

    def __iter__(self):
        return self

    def __reversed__(self):
        return

    def __contains__(self, item):
        return

    def __missing__(self, key):
        return

    def next(self):
        if self.current >= len(self.im):
            raise StopIteration
        else:
            p = self[self.current]
            self.current += 1
            return p


def are_2photos_diff(image_file1, image_file2):
    """
    check if 2 file are different
    it will compare their size and most recent modification date
    """
    file_info1 = os.stat(image_file1)
    file_info2 = os.stat(image_file2)

    # check size
    if file_info1.st_size != file_info2.st_size:
        return True

    # check modification time
    if file_info1.st_mtime != file_info2.st_mtime:
        return True

    return False

def diff(image_file1, image_file2, image_diff_file):
    image1 = Image.open(image_file1)
    image2 = Image.open(image_file2)
    image_diff = Image.new("RGB", image1.size)

    image1_data = image1.getdata()
    image2_data = image2.getdata()

    """
    # this is insufficient, and will raise MemoryError exception
    image_diff_data = []
    index = 0
    try:
        #for i in range(len(image1_data)):
        for p1, p2 in zip(image1_data, image2_data):
            if not are_2rgbs_close_enough(image1_data[i], image2_data[i]):
                image_diff_index.append(i);
            if are_2rgbs_close_enough(image1_data[i], image2_data[i]):
                image_diff_data.append(image1_data[i])
            else:
                image_diff_data.append((0,0,0))
    except MemoryError:
        print 'error' 
    """

    diff_data = MyImageData(image1_data, image2_data)
    image_diff.putdata(diff_data)
    image_diff.save(image_diff_file)

    print 'Created diff file ' + image_diff_file

def to_file_tuple(file_path):
    """
    given a file path c:\a\file\path\file.ext
    returns ['c:\a\file\path\file.ext', 'c:\a\file\path', 'file', 'ext']
    """
    head_tail = os.path.split(file_path)
    name_ext = head_tail[1].split('.')
    return (file_path, head_tail[0], name_ext[0], name_ext[1])

def main():
    dir1 = 'C:\\Users\\ryan\\Desktop\\new'
    dir2 = 'C:\\Users\\ryan\\Desktop\\old'

    # get all .jpg file in the folder
    file_names = [file_name for file_name in os.listdir(dir1) if file_name.endswith(".jpg")]

    for file_name in file_names:
        file_path1 = os.path.join(dir1, file_name)
        file_path2 = os.path.join(dir2, file_name)

        path, head, name, ext = to_file_tuple(file_path1)
        file_diff = os.path.join(head, name + '_diff.' + ext)

        print 'checking file ' + file_name

        # create the diff file if the 2 files are different
        if are_2photos_diff(file_path1, file_path2):
            diff(file_path1, file_path2, file_diff)

main()
