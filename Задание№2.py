
from pprint import pprint

import requests

TOKEN = ''


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)
                   }
        return headers

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(url=files_url, headers=headers)

        if response.status_code == 200:
            print('Connected -> OK')
        elif response.status_code == 400:
            print('Некорректные данные')
        elif response.status_code == 401:
            print('Не авторизован')
        elif response.status_code == 403:
            print('Не достаточно прав для изменения данных в общей папке')
        elif response.status_code == 404:
            print('Не удалось найти запрошенный ресурс')
        elif response.status_code == 404:
            print('Не удалось найти запрошенный ресурс')
        elif response.status_code == 429:
            print('Слишком много запросов')
        elif response.status_code == 503:
            print('Сервис временно недоступен.')
        elif response.status_code == 406:
            print('Ресурс не может быть представлен в запрошенном формате.')

        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(url=upload_url, headers=headers, params=params)
        pprint(response)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, path_filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(path_filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            return response.status_code


if __name__ == '__main__':
    uploader = YaUploader(token=TOKEN)
    print(uploader.get_files_list())
    uploader.upload_file_to_disk(disk_file_path="you_folder_on_yandex_disk/text.txt", path_filename="test.txt")