import requests

class Wiker:
    def __init__(self, lang = 'en'):
        self.lang = lang
        self.url = f'https://{self.lang}.wikipedia.org/w/api.php'
        self.params = {
            'action': 'query',
            'format': 'json',
            'titles': '',
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
    
    def search(self, req_text):
        result = list()
        response = requests.get(
            f"{self.url}?origin=*&action=opensearch&search={req_text}").json()
        for i in range(len(response[1])):
            result.append({'title': response[1][i], 'url': response[3][i]})
        return result

wiki = Wiker(lang='uz')
print(wiki.search("Turkiston"))