import requests


def get_total_number_comics(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def get_xkdc_image(url):
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()

    image_link = response['img']
    image_number = response['num']
    author_comment = response['alt']
    return image_link, image_number, author_comment


def saving_image_xkdc(url, image_name):
    response = requests.get(url)
    response.raise_for_status()
    with open(image_name, 'wb') as file:
        file.write(response.content)