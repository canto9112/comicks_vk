import os

from dotenv import load_dotenv

import vk_api
import xkdc

if __name__ == '__main__':
    load_dotenv()

    vk_api_version = 5.21
    vk_token = os.getenv('VK_PERSON_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')

    try:
        image_name, author_comment = xkdc.save_random_comics()
        vk_api.post_comics(image_name, author_comment, vk_api_version, vk_token, vk_group_id)
    finally:
        os.remove(image_name)
