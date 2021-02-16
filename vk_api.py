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


def upload_image_to_server(url, image_name):
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


def save_image_in_group_album(server_hash, photo, server, group_id, token, api_version):
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


def post_image_group_wall(token, api_version, from_group, message, media_id, owner_id):
    params = {
        'access_token': token,
        'v': api_version,
        'owner_id': -int(from_group),
        'attachments': f'photo{owner_id}_{media_id}',
        'message': message
    }
    response = requests.post('https://api.vk.com/method/wall.post', params=params)
    response.raise_for_status()


def post_comics(image_name, author_comment, api_version, token, group_id):
    vk_server_address = get_server_address(token, api_version, group_id)
    server_hash, photo, server = upload_image_to_server(vk_server_address, image_name)
    media_id, owner_id = save_image_in_group_album(server_hash, photo, server, group_id, token, api_version)
    post_image_group_wall(token, api_version, group_id, author_comment, media_id, owner_id)
