from unidecode import unidecode
import nltk
from nltk.tokenize import word_tokenize

def so_su_menh(ten):
    chi_so = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    nguyen_am = ["A", 'O', 'E', 'I', 'U']

    def tinh_tong_chu_so(so):
        tong = 0
        while so > 0:
            tong += so % 10
            so //= 10
        return tong

    ten = unidecode(ten.upper())
    words = word_tokenize(ten)
    temp = []
    chi_so_su_menh = 0
    for word in words:
        hold = 0
        chus = list(word)
        for chu in chus:
            hold += chi_so[chu]
        while hold >= 10:
            hold = tinh_tong_chu_so(hold)
        chi_so_su_menh += hold
    while chi_so_su_menh >= 10:
        if chi_so_su_menh == 11 or chi_so_su_menh == 22:
            return chi_so_su_menh
        chi_so_su_menh = tinh_tong_chu_so(chi_so_su_menh)

    return chi_so_su_menh