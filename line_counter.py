import os
import traceback

directory = input('Choose source directory: ')

try:
    tree = [(d, files) for d, dirs, files in os.walk(directory) if '.git' not in d and '.idea' not in d and 'data' not in d]
    files_dir = [i[0] + '\\' + j for i in tree for j in i[1]]
    counter = sum(1 for f in files_dir for line in open(f, 'r', encoding='utf-8'))

    print('Lines in your project: %d' % counter)
    os.system("pause")
except:
    print(traceback.format_exc())
    os.system("pause")
