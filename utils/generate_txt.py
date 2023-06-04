import glob

#存放图片的地址
train_image_path = r"/home/URPC2019/images/train/"
valid_image_path = r"/home/URPC2019/images/valid/"
test_image_path = r"/home/URPC2019/images/test/"
#生成的txt的路径
txt_path = r"/home/URPC2019/"
def generate_train_and_val(image_path, txt_file):
    with open(txt_file, 'w') as tf:
        for jpg_file in glob.glob(image_path + '*.jpg'):
            tf.write(jpg_file + '\n')

generate_train_and_val(train_image_path, txt_path + 'train.txt')
generate_train_and_val(valid_image_path, txt_path + 'valid.txt')
generate_train_and_val(test_image_path, txt_path + 'test.txt')

