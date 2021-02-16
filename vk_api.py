import requests


def get_server_address(token, api_version, group_id):
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id
    }
    response = requests.get('https://api.vk.com/method/photos.getWallUploadServer',
                            params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def uploading_image_to_server(url, image_name):
    with open(image_name, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        server_response = response.json()
        server_hash = server_response['hash']
        photo = server_response['photo']
        server = server_response['server']
    return server_hash, photo, server


def saving_image_in_album_group(server_hash, photo, server, group_id, token, api_version):
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': server_hash
    }
    response = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    response.raise_for_status()
    response = response.json()
    id_image = response['response'][0]['id']
    owner_id = response['response'][0]['owner_id']
    return id_image, owner_id


def posting_image_group_wall(token, api_version, from_group, message, media_id, owner_id):
    params = {
        'access_token': token,
        'v': api_version,
        'owner_id': -int(from_group),
        'attachments': f'photo{owner_id}_{media_id}',
        'message': message
    }
    response = requests.post('https://api.vk.com/method/wall.post', params=params)
    response.raise_for_status()