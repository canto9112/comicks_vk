import random

import requests


def get_total_number_comics(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    image_link = response['img']
    image_number = response['num']
    author_comment = response['alt']
    return image_link, image_number, author_comment


def saving_image(url, image_name):
    response = requests.get(url)
    response.raise_for_status()
    with open(image_name, 'wb') as file:
        file.write(response.content)


def saving_random_comics():
    xkdc_last_comics_url = 'http://xkcd.com/info.0.json'
    total_number_comics = get_total_number_comics(xkdc_last_comics_url)
    random_comics = random.randint(1, total_number_comics)
    xkdc_random_comics_url = f'http://xkcd.com/{random_comics}/info.0.json'
    image_link, image_number, author_comment = get_image(xkdc_random_comics_url)
    image_name = f'{image_number}.png'
    saving_image(image_link, image_name)
    return image_name, author_comment