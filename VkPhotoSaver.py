# -*- coding: utf-8 -*-
import vk_api
import vk
import requests
import jsonReadWrite as jRW


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():    
    session = requests.Session()

    login, password = 'login', 'password'
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    vk_session.auth()

    def photo_uploader(photo_link, filename):
        image = requests.get(photo_link, stream=True)
        with open(filename, 'wb') as fd:
            fd.write(image.content)
        
        photo = upload.photo(filename, album_id=265319479, group_id=158982770)

        return 'photo%s_%s' % (photo[0]['owner_id'], photo[0]['id'])

    film_base = jRW.read_json('films_ready.json')
    result = []
    for film in film_base:
        if 'pic' in film and film['pic']:
            film['pic'] = photo_uploader(film['pic'], 'photos/' + film['name'] + '.jpg')
        result.append(film)
        print(film['name'] + ' done')

    jRW.write_json(result, 'films_ready2.json')



if __name__ == '__main__':
    main()
