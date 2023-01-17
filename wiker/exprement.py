import requests

class Wiker:
    """Wikipedia API-dan foydalangan holda, malumotlarni olish uchun"""
    def __init__(self, lang = 'en'):
        self.lang = lang # Tanlangan tildagi wikipediadan malumot qidiriladi
        self.url = f'https://{self.lang}.wikipedia.org/w/api.php' # Asosiy URL
        self.params = {
            'action': 'query',
            'format': 'json',
            'titles': '',
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
    
    def search(self, req_text):
        """So'rovga yaqin keladigan maqolalar mavzusini qaytaradi"""
        result = list() # mavzular ro'yhatga yig'ib boriladi
        response = requests.get(
            f"{self.url}?origin=*&action=opensearch&search={req_text}").json()
        for i in range(len(response[1])):
            result.append({'title': response[1][i], 'url': response[3][i]}) # mavzu va havolalar ro'yhatga qo'shiladi
        return result
    
    def summary(self, req_text):
        """So'ralgan mavzuga eng yaqin maqolani topib, maqolani qaytaradi"""
        self.params['titles'] = req_text
        response = requests.get(self.url, params=self.params).json()
        try:
            # so'ralgan mavzu bo'yicha maqola topilsa, maqola matni qaytadi
            return list(response["query"]["pages"].values())[0]["extract"]
        except:
            # so'ralgan mavzu to'pilmasa None qiymat qaytadi
            return None

# foydalanib ko'rish uchun oddiy example
wiki = Wiker(lang='uz')
print(wiki.summary("Telegram"))