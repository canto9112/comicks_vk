import requests
from pprint import pprint
from dotenv import load_dotenv
import os


def get_image_link(url):
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    image_link = response_json['img']
    image_num = response_json['num']
    author_comment = response_json['alt']

    return image_link, image_num, author_comment


def save_image(url, file_name):
    response = requests.get(url)
    response.raise_for_status()

    with open(f'{file_name}.png', 'wb') as file:
        file.write(response.content)


def get_upload_url(token, api_version, group_id):
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id
    }
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer',
                            params=params)
    response.raise_for_status()
    response_json = response.json()
    upload_url = response_json['response']['upload_url']
    return upload_url


def upload_image_to_server_vk(url, image_name):
    with open(f'{image_name}.png', 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        response_json = response.json()
        hash = response_json['hash']
        photo = response_json['photo']
        server = response_json['server']
        return hash, photo, server


def upload_image_in_wall(hash, photo, server, group_id, token, api_version):
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hash
    }
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto',
                             params=params)
    response.raise_for_status()
    response_json = response.json()
    id_image = response_json['response'][0]['id']
    owner_id = response_json['response'][0]['owner_id']
    return id_image, owner_id


def public_image_wall_vk(token, api_version, from_group, message, media_id, owner_id):
    params = {
        'access_token': token,
        'v': api_version,
        'owner_id': -int(from_group),
        'attachments': f'photo{owner_id}_{media_id}',
        'message': message
    }
    response = requests.post('https://api.vk.com/method/wall.post',
                             params=params)
    response.raise_for_status()
    response_json = response.json()


if __name__ == '__main__':
    load_dotenv()

    xkdc_url = 'http://xkcd.com/353/info.0.json'
    api_vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'

    vk_api_version = 5.21
    token_vk = os.getenv('PERSON_TOKEN_VK')
    user_id_vk = os.getenv('USER_ID_VK')
    group_id_vk = os.getenv('GROUP_ID_VK')

    image_link, image_name, author_comment = get_image_link(xkdc_url)
    print(author_comment)
    save_image(image_link, image_name)
    upload_url = get_upload_url(token_vk, vk_api_version, group_id_vk)

    hash, photo, server = upload_image_to_server_vk(upload_url, image_name)
    media_id, owner_id = upload_image_in_wall(hash, photo, server, group_id_vk, token_vk, vk_api_version)
    print(media_id, owner_id)
    print(-int(group_id_vk))
    public_image_wall_vk(token_vk, vk_api_version, group_id_vk, author_comment, media_id, owner_id)
