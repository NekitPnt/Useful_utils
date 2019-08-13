import json
import traceback
import os


# command to download quiz: JSON.stringify(quiz_data);
# command to get post id: jQuery("#quiz_post_id").val();


def converter():
    input_file = input('Input file link: ')
    output_file = input('Output file link: ')
    if output_file == '':
        output_file = input_file.split('.')[0] + '_for_bot.' + input_file.split('.')[1]

    with open(input_file, "r", encoding="utf8") as read_file:
        file = read_file.read()
        file = file.replace('</p>', '')
        file = file.replace('<p>', '')
        file = file.replace('<code>', '')
        file = file.replace('</code>', '')
        file = file.replace('\n', '')
        data = json.loads(json.loads(file))

    converted_data = {"name": data["name"], "shuffle_answers": "0", "id": data["id"], "quiz_post_id": "",
                      "quiz_job_id": data["quiz_job_id"], "quiz_company": data["quiz_company_id"],
                      "quiz_job_url": data["quiz_job_url"], "refuse_email": ["Не хочу оставлять почту"],
                      "after_refuse_message": "Жаль, возможно, именно вас не хватает «КОМПАНИИ НЕЙМ».",
                      "question_prefix": "📝 Вопрос", "quiz_title": "",
                      "activate_command": [data["name"].lower()], "activate_command_for_menu": data["name"].lower(),
                      "menu_descr": "",
                      "stata": {
                          "fields": [],
                          "periodic_fields": [],
                          "activator": "",
                          "url": ""
                      },
                      "ending_keyword": "end", "result_keyword": "results",
                      "error_message": {
                          "text": "Вы, кажется, промазали мимо кнопки. Если просто не знаете, как завершить тест, "
                                  "то вот вам кнопка снизу.",
                          "key_text": "Завершить тест",
                          "color": "red",
                          "next_question_id": "bad_end"
                      },
                      "bad_end_message": "Жаль, ведь вы подавали надежды. Если вдруг передумаете и решите вернуться, "
                                         "просто напишите мне «старт бот».",
                      "useful_call": "", "gift": {}, "feedback": "0", "contacts": data["show_email_form"],
                      "min_result_for_contact": data["show_email_form_min_res"], "right_sym": "✅ ", "wrong_sym": "❌ ",
                      "prefix_result_message": "Поздравляем, вы прошли тест! Результат: ",
                      "first_q_id": data['questions'][0]['id'], 'questions': {}}

    proxy_data = dict([(quest['id'], quest) for quest in data['questions']])
    for k, v in proxy_data.items():
        # proxy_answers = dict([(answer['text'], answer) for answer in v['answers']])
        converted_data['questions'][k] = {}
        converted_data['questions'][k]['text'] = v['text'].rstrip()
        converted_data['questions'][k]['attach'] = []
        converted_data['questions'][k]['quiz_id'] = v['quiz_id']
        converted_data['questions'][k]['next_question_id'] = str(int(v['id']) + 1)
        converted_data['questions'][k]['answers'] = []
        proxy_answers = [answer for answer in v['answers']]
        for answer in range(len(proxy_answers)):
            converted_data['questions'][k]['answers'].append({})
            converted_data['questions'][k]['answers'][answer]['text'] = proxy_answers[answer]['text'].rstrip()
            converted_data['questions'][k]['answers'][answer]['descr'] = proxy_answers[answer]['descr'].rstrip()
            converted_data['questions'][k]['answers'][answer]['attach'] = []
            converted_data['questions'][k]['answers'][answer]['correct'] = proxy_answers[answer]['correct']
            converted_data['questions'][k]['answers'][answer]['color'] = 'white'
            converted_data['questions'][k]['answers'][answer]['for_result'] = proxy_answers[answer]['for_result']
        '''
        for k_a, v_a in proxy_answers.items():
            converted_data['questions'][k]['answers'][k_a] = {}
            converted_data['questions'][k]['answers'][k_a]['descr'] = v_a['descr']
            converted_data['questions'][k]['answers'][k_a]['correct'] = v_a['correct']
            converted_data['questions'][k]['answers'][k_a]['color'] = 'white'
            converted_data['questions'][k]['answers'][k_a]['for_result'] = v_a['for_result']
        '''

    converted_data['questions'][max(converted_data['questions'])]['next_question_id'] = converted_data["ending_keyword"]
    converted_data['result'] = []
    for res in data['result']:
        converted_data['result'].append({'title': res['title'], 'attach': [], 'desc': res['desc'].rstrip()})

    with open(output_file, 'w', encoding="utf8") as outfile:
        json.dump(converted_data, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    while True:
        try:
            converter()
            print('done')
            os.system("pause")
            break
        except:
            print(traceback.format_exc())
