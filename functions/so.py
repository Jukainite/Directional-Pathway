from unidecode import unidecode
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
def so_chu_dao(ngay_thang_nam_sinh):
    """Hàm tính số chủ đạo từ ngày tháng năm sinh."""
    # Tách ngày, tháng và năm từ chuỗi ngày tháng năm sinh
    day, month, year = map(int, ngay_thang_nam_sinh.split('/'))

    # Hàm tính tổng các chữ số của một số
    def tong_chu_so(number):
        total = 0
        while number > 0:
            total += number % 10
            number //= 10
        return total

    # Tính tổng các chữ số của ngày, tháng, năm sinh
    tong_chu_so_ngay = tong_chu_so(day)
    tong_chu_so_thang = tong_chu_so(month)
    tong_chu_so_nam = tong_chu_so(year)

    # Tính tổng tổng các chữ số
    tong = tong_chu_so_ngay + tong_chu_so_thang + tong_chu_so_nam

    # Tính số chủ đạo từ tổng
    while tong > 10:
        if tong == 11 or tong == 22 or tong == 33:
            return tong
        tong = tong_chu_so(tong)

    return tong
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
