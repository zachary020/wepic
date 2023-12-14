import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def change_photo_timestamp(image_path, new_timestamp):
    # 打开图片
    img = Image.open(image_path)

    # 将新的时间戳转换为EXIF时间格式
    new_exif_time = datetime.fromtimestamp(int(new_timestamp) / 1000).strftime('%Y:%m:%d %H:%M:%S')

    # 获取图片的EXIF数据
    exif_data = img.getexif()

    # 如果图片有EXIF数据，则更新时间戳
    if exif_data:
        # 修改EXIF时间戳
        exif_data[36867] = new_exif_time  # DateTimeOriginal
        exif_data[36868] = new_exif_time  # DateTimeDigitized

        # 将修改后的EXIF数据放回图片
        img.save(image_path, exif=exif_data.tobytes())

    # 关闭图片
    img.close()

def batch_update_timestamps(directory):
    # 遍历给定目录下的所有文件
    for filename in os.listdir(directory):
        # 检查文件名是否符合微信图片的时间戳格式
        if filename.startswith('mmexport') and len(filename) >= 23 and filename[8:21].isdigit() and filename.lower().endswith('.jpg'):
            # 获取文件的完整路径
            file_path = os.path.join(directory, filename)
            # 微信图片的时间戳是文件名中'mmexport'后的13个字符
            timestamp = filename[8:21]
            # 更新图片的拍摄时间信息
            change_photo_timestamp(file_path, timestamp)
            print(f"Updated timestamp for {filename}")

# 调用函数，传入包含图片文件的目录路径
batch_update_timestamps('/path/to/your/directory')