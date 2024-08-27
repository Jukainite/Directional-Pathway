from unidecode import unidecode
import nltk
from nltk.tokenize import word_tokenize

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