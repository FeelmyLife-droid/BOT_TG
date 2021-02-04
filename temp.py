class Info:

    def __init__(self, x: str):
        self.para = x.split("\n")
        self.slovo = {
            "НАЗВАНИЕ": self.para[0].split(":")[1].strip(),
            "ОГРН": self.para[1].split(":")[1].strip(),
            "ИНН": self.para[2].split(":")[1].strip(),
            "РЕГИОН": self.para[3].split(":")[1].strip(),
            "АДРЕСС": self.para[4].split(":")[1].strip(),
            "Директор": self.para[5].split(":")[1].strip(),
            "Дата_Рег": self.para[8].split(":")[1].strip(),
            "ОКВЭД": self.para[6].split(":")[0],
            "ОКВЭД_ИНФО": self.para[6].split(":")[1].strip(),
            "Уставной капитал":self.para[7].split(":")[1].strip()
        }

