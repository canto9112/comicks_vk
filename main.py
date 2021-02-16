import os
import random

import requests
from dotenv import load_dotenv


def get_total_number_comics(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def get_xkdc_image(url):
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()

    image_link = response_json['img']
    image_number = response_json['num']
    author_comment = response_json['alt']
    return image_link, image_number, author_comment


def xkdc_image_save(url, file_name):
    response = requests.get(url)
    response.raise_for_status()
    with open(f'{file_name}.png', 'wb') as file:
        file.write(response.content)


def get_vk_server_address(token, api_version, group_id):
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id
    }
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer',
                            params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def vk_uploading_image_to_server(url, image_name):
    with open(f'{image_name}.png', 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        server_response = response.json()
        hash = server_response['hash']
        photo = server_response['photo']
        server = server_response['server']
    return hash, photo, server


def vk_saving_photo_in_album_group(hash, photo, server, group_id, token, api_version):
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hash
    }
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    response.raise_for_status()
    response_json = response.json()
    id_image = response_json['response'][0]['id']
    owner_id = response_json['response'][0]['owner_id']
    return id_image, owner_id


def vk_public_image_group_wall(token, api_version, from_group, message, media_id, owner_id):
    params = {
        'access_token': token,
        'v': api_version,
        'owner_id': -int(from_group),
        'attachments': f'photo{owner_id}_{media_id}',
        'message': message
    }
    response = requests.post('https://api.vk.com/method/wall.post', params=params)
    response.raise_for_status()


if __name__ == '__main__':
    load_dotenv()

    vk_api_version = 5.21
    vk_token = os.getenv('VK_PERSON_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')

    xkdc_last_comics_url = 'http://xkcd.com/info.0.json'

    total_number_comics = get_total_number_comics(xkdc_last_comics_url)
    random_comics = random.randint(1, total_number_comics)
    xkdc_random_comics_url = f'http://xkcd.com/{random_comics}/info.0.json'
    image_link, image_name, author_comment = get_xkdc_image(xkdc_random_comics_url)

    xkdc_image_save(image_link, image_name)

    vk_server_address = get_vk_server_address(vk_token, vk_api_version, vk_group_id)
    hash, photo, server = vk_uploading_image_to_server(vk_server_address, image_name)
    media_id, owner_id = vk_saving_photo_in_album_group(hash, photo, server, vk_group_id, vk_token, vk_api_version)
    vk_public_image_group_wall(vk_token, vk_api_version, vk_group_id, author_comment, media_id, owner_id)
    os.remove(f'{image_name}.png')
