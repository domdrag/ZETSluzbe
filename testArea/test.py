import re

def phone_format(tel):
    tel = f"{tel[:3]}-{tel[3:6]}-{tel[6:]}"
    return str(tel)

print(phone_format("05555555"))
