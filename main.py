import requests
# from tqdm import tqdm
import time
from tqdm import tqdm 

def vk():
    url_vk = 'https://api.vk.com/method/photos.get'
    with open('token.txt') as file_token:
        for i in file_token:
            token_vk = i
    foto_dict = {}
    params = {'owner_id': 20629072, 'access_token': token_vk, 'album_id': 'profile', 'count': '5', 'extended': '1', 'v': 5.131}
    resp = requests.get(url_vk, params=params)
    json_file = resp.json()
    for foto_list in json_file['response']['items']:
        like = foto_list['likes']['count']
        date = foto_list['date']
        foto_dict[(foto_list['sizes'][-1]['url'])] = [like,date]
    return foto_dict
         
url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
with open('token_ya.txt') as file_token_ya:
    for i in file_token_ya:
        token_ya = i
headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                 'Authorization': f'OAuth {token_ya}'}


def create_folder(path):
    requests.put(f'{url_ya}?path={path}', headers=headers)

create_folder('vk_foto_test')


def upload_file(loadfile, sevefile, replace=False):
    res = requests.get(f'{url_ya}/upload?path={sevefile}&overwrite={replace}', headers=headers).json()
    try:
        requests.put(res['href'], files={'file': loadfile})
    except KeyError:
        print(res)


if __name__ == '__main__':
    foto_dict = vk()
    for i in foto_dict.items():
        file_url = i[0]
        file_name = f' {i[1][0]}_{i[1][1]}.jpg'   
        api = requests.get(file_url) 
        tqdm(upload_file(api.content,  f'vk_foto_test/{file_name}'))
        

            

