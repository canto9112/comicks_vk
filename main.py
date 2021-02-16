import os
import random

from dotenv import load_dotenv

import vk_api
import xkdc

if __name__ == '__main__':
    load_dotenv()

    vk_api_version = 5.21
    vk_token = os.getenv('VK_PERSON_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')

    image_name, author_comment = xkdc.saving_random_comics()

    vk_server_address = vk_api.get_server_address(vk_token, vk_api_version, vk_group_id)
    server_hash, photo, server = vk_api.uploading_image_to_server(vk_server_address, image_name)
    media_id, owner_id = vk_api.saving_image_in_album_group(server_hash, photo, server, vk_group_id, vk_token, vk_api_version)
    vk_api.posting_image_group_wall(vk_token, vk_api_version, vk_group_id, author_comment, media_id, owner_id)
    os.remove(image_name)
