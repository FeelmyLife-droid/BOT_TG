import httpx
from fake_useragent import UserAgent


async def get_name_firm(inn: int):
    ua = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.rusprofile.ru',
        'Referer': 'https://www.rusprofile.ru/',
        'TE': 'Trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.chrome
    }
    async with httpx.AsyncClient(headers=headers) as client:
        r = await client.get(
            f"https://www.rusprofile.ru/ajax.php?=&query={inn}&action=search")
    res = r.json()
    dict_firm = {
        "name_org": res['ul'][0]['name'],
        "ogrn_org": res['ul'][0]['ogrn'],
        "inn_org": str(res['ul'][0]['inn'])[3:13],
        "region_org": res['ul'][0]['region'],
        "address_org": res['ul'][0]['address'],
        "position": res['ul'][0]['ceo_type'],
        "position_fio": res['ul'][0]['snippet_string'],
        "okved_descr": res['ul'][0]['main_okved_id'] ,
        "capital": res['ul'][0]['okved_descr'],
        "date_reg_org": str(res['ul'][0]['authorized_capital']).split(".")[0],
        "okved_org": res['ul'][0]['reg_date'],

    }
    # name_org = res['ul'][0]['name']
    # ogrn_org = res['ul'][0]['ogrn']
    # inn_org = str(res['ul'][0]['inn'])[3:13]
    # region_org = res['ul'][0]['region']
    # address_org = res['ul'][0]['address']
    # position = res['ul'][0]['ceo_type']
    # position_fio = res['ul'][0]['snippet_string']
    # okved_org = res['ul'][0]['main_okved_id']
    # okved_descr = res['ul'][0]['okved_descr']
    # capital = str(res['ul'][0]['authorized_capital']).split(".")[0]
    # date_reg_org = res['ul'][0]['reg_date']
    # reply_text = (f'НАЗВАНИЕ :<b>{name_org}</b>/\n'
    #               f'ОГРН : <b>{ogrn_org}</b>/\n'
    #               f'ИНН : <b>{inn_org}</b>\n'
    #               f'РЕГИОН : <b>{region_org}</b>\n'
    #               f'АДРЕСС : <b>{address_org}</b>\n'
    #               f'{position} : <b>{position_fio}</b>\n'
    #               f'{okved_org} : <b>{okved_descr}</b>\n'
    #               f'УСТАВНОЙ КАПИТАЛ : <b>{capital}</b>\n'
    #               f'ДАТА РЕГ : <b>{date_reg_org}</b>')
    return dict_firm
