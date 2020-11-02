a = "НАЗВАНИЕ :ООО \"Агрохимсибирь+\"\nОГРН : 1202200033287\nИНН : 2207011108\nРЕГИОН : Алтайский край\nАДРЕСС : " \
    "658709, Алтайский край, Каменский район, город Камень-на-Оби, Солнечная улица, дом 1, квартира 7\nДиректор : " \
    "Кашицын Михаил Викторович\n2020-10-29 : 46.75\nУСТАВНОЙ КАПИТАЛ : Торговля оптовая химическими продуктами\nДАТА " \
    "РЕГ : 10000"


class Info:

    def __init__(self, x: str):
        self.para = x.split("\n")
        self.slovo = {
            "НАЗВАНИЕ": self.para[0].split(":")[1].strip()
        }
        self.name = self.para[0].split(":")[1].strip()
        self.ogrn = self.para[1].split(":")[1].strip()
        self.inn = self.para[2].split(":")[1].strip()
        self.region = self.para[3].split(":")[1].strip()
        self.address = self.para[4].split(":")[1].strip()
        self.position = self.para[5].split(":")[1].strip()
        self.data_reg = self.para[6].split(":")[0]
        self.okved = self.para[6].split(":")[1].strip()
        self.okved_info = self.para[7].split(":")[1].strip()
        self.capital = self.para[8].split(":")[1].strip()



print(Info(a).slovo)
