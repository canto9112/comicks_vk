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


def get_upload_url(url, token, api_version, group_id):
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_json = response.json()
    upload_url = response_json['response']['upload_url']
    return upload_url


def upload_image(url, image_name):
    with open(image_name, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        pprint(response.json())


if __name__ == '__main__':
    load_dotenv()

    xkdc_url = 'http://xkcd.com/353/info.0.json'
    api_vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'

    vk_api_version = 5.21
    token_vk = os.getenv('PERSON_TOKEN_VK')
    user_id_vk = os.getenv('USER_ID_VK')
    group_id_vk = os.getenv('GROUP_ID_VK')

    # image_link, image_name, author_comment = get_image_link(xkdc_url)
    # print(author_comment)
    # save_image(image_link, image_name)
    upload_url = get_upload_url(api_vk_url, token_vk, vk_api_version, group_id_vk)
    print(upload_url)
    upload_image(upload_url, '353.png')