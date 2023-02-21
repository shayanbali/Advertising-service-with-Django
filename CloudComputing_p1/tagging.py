import requests

API_KEY = 'acc_0bdc7c87c685220'
API_SECRET = 'c261203818531cdf1663249d843c13b4'


# IMAGE_URL = 'https://wallpapercave.com/wp/wp3503654.jpg'


def tagImage(IMAGE_URL):
    state = 'rejected'
    category = ''
    print(IMAGE_URL, "Image URL")
    if IMAGE_URL is not None:

        response = requests.get(
            'https://api.imagga.com/v2/tags?image_url=%s' % IMAGE_URL, auth=(API_KEY, API_SECRET))

        tags = response.json()
        tags = tags['result']['tags']
        for tag in tags:
            if tag['tag']['en'] == 'vehicle' and tag['confidence'] > 50:
                state = 'confirmed'

        category = tags[0]['tag']['en']

    return state, category
