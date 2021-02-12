import requests
from pprint import pprint


url = 'http://xkcd.com/353/info.0.json'


def get_image_link(url):
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    return response_json['img']


def save_image(url, file_name):
    response = requests.get(url)
    response.raise_for_status()

    with open(f'{file_name}.png', 'wb') as file:
        file.write(response.content)


image_link = get_image_link(url)

save_image(image_link, '1')