import requests

url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSfOMLR-8krFnxhiQcbhvtXWG8c2uVB1YT2r6zoxAFohIgSxrQ/formResponse"

data = {
    "entry.756291279": "12345",              # id_расхода
    "entry.1422320460": "Объект_1",          # id_объекта
    "entry.656508705": "2026-02-15",         # дата (ВАЖНО формат YYYY-MM-DD)
    "entry.577364935": "1500",               # сумма
    "entry.379656384": "материалы"           # категория (строго как в форме)
}

response = requests.post(url, data=data)

print("Статус:", response.status_code)