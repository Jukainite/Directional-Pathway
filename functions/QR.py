

import qrcode
from qr_pay import QRPay

def QR(content, amount):
    # Tạo đối tượng QRPay
    data = {
        "bin_id": "970436",
        "consumer_id": "1016266506",
        'purpose_of_transaction':content,
        "transaction_amount": amount
    }
    qr_pay = QRPay(**data)
    # Lấy mã QR
    qr_code_data = qr_pay.code

    # Tạo mã QR
    qr = qrcode.make(qr_code_data)
    return qr
# # Hiển thị mã QR
# qr.show()
bank_data = [
    ("VietcomBank", "970436"),
    ("VietinBank", "970415"),
    ("Techcombank", "970407"),
    ("BIDV", "970418"),
    ("AgriBank", "970405"),
    ("Navibank", "970419"),
    ("Sacombank", "970403"),
    ("ACB", "970416"),
    ("MBBank", "970422"),
    ("TPBank", "970423"),
    ("Shinhan Bank", "970424"),
    ("VIB Bank", "970441"),
    ("VPBank", "970432"),
    ("SHB", "970443"),
    ("Eximbank", "970431"),
    ("BaoVietBank", "970438"),
    ("VietcapitalBank", "970454"),
    ("SCB", "970429"),
    ("VietNam - Russia Bank", "970421"),
    ("ABBank", "970425"),
    ("PVCombank", "970412"),
    ("OceanBank", "970414"),
    ("NamA bank", "970428"),
    ("HDBank", "970437"),
    ("HDBank", "970420"),
    ("VietBank", "970433"),
    ("VietCredit", "970460"),
    ("Public bank", "970439"),
    ("Hongleong Bank", "970442"),
    ("PG Bank", "970430"),
    ("Co.op Bank", "970446"),
    ("CIMB", "422589"),
    ("Indovina", "970434"),
    ("DongABank", "970406"),
    ("GPBank", "970408"),
    ("BacABank", "970409"),
    ("VietABank", "970427"),
    ("SaigonBank", "970400"),
    ("Maritime Bank", "970426"),
    ("LienVietPostBank", "970449"),
    ("KienLongBank", "970452"),
    ("IBK - Ha Noi", "970455"),
    ("IBK - TP.HCM", "970456"),
    ("Woori bank", "970457"),
    ("SeABank", "970440"),
    ("UOB", "970458"),
    ("OCB", "970448"),
    ("Mirae Asset", "970468"),
    ("Keb Hana - Ho Chi Minh", "970466"),
    ("Keb Hana - Ha Noi", "970467"),
    ("Standard Chartered", "970410"),
    ("CAKE", "546034"),
    ("Ubank", "546035"),
    ("Nonghyup Bank - HN", "801011"),
    ("Kookmin - HN", "970462"),
    ("Kookmin - HCM", "970463"),
    ("DBS - HCM", "796500"),
    ("CBBank", "970444"),
    ("KBank - HCM", "668888"),
    ("HSBC", "458761"),
    ("Timo", "")
]

bank_dict = {name: bin_card for name, bin_card in bank_data}





def QRforadmin(bin_id,consumer_id,content, amount):
    data = {
        "bin_id":bank_dict[bin_id],
        "consumer_id": consumer_id,
        'purpose_of_transaction':content,
        "transaction_amount": amount
    }
    qr_pay = QRPay(**data)
    # Lấy mã QR
    qr_code_data = qr_pay.code

    # Tạo mã QR
    qr = qrcode.make(qr_code_data)
    return qr