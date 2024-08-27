from unidecode import unidecode
import nltk
from nltk.tokenize import word_tokenize

def so_linh_hon(ten):
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

    def check_Y(words, place):
        if words[place] != 'Y':
            return False
        else:
            if place == len(words) - 1:
                if words[place - 1] not in nguyen_am:

                    return True
                else:
                    return False
            else:
                if words[place - 1] not in nguyen_am:
                    if words[place + 1] not in nguyen_am:
                        return True
                else:
                    return False

    words = word_tokenize(ten)
    temp = []
    chi_so_linh_hon = 0
    for word in words:
        chus = list(word)

        for i in range(len(chus)):
            if check_Y(chus, i) or (chus[i] in nguyen_am):
                temp.append(chus[i])
                chi_so_linh_hon += chi_so[chus[i]]

    while chi_so_linh_hon >= 10:
        if chi_so_linh_hon == 11 or chi_so_linh_hon == 22:
            return chi_so_linh_hon
        chi_so_linh_hon = tinh_tong_chu_so(chi_so_linh_hon)

    return chi_so_linh_hon