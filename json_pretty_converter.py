import json
import traceback
import os


# command to download quiz: JSON.stringify(quiz_data);
def converter():
    input_file = input('Input file link: ')
    output_file = input('Output file link: ')
    if output_file == '':
        output_file = input_file.split('.')[0] + '_converted.' + input_file.split('.')[1]

    with open(input_file, "r", encoding="utf8") as read_file:
        file = read_file.read()
        file = file.replace('</p>', '')
        file = file.replace('<p>', '')
        file = file.replace('\n', '')
        data = json.loads(json.loads(file))

    with open(output_file, 'w', encoding="utf8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


while True:
    try:
        converter()
        print('done')
        os.system("pause")
        break
    except:
        print(traceback.format_exc())
