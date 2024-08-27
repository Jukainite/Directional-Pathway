
def tinh_tien(thansohoc, nhantuonghoc, sinhtrachoc,his,sales=1,ser_sale={},his3=False,count=0):
    cost={
       "thansohoc": 50000,
        "nhantuonghoc": 80000,
        "sinhtrachoc": 100000, 
    }
    value= {
        1:0,
        5:1,
        10:2
    }
    def count_zeros(lst):
        count = 0
        for num in lst:
            if num == 0:
                count += 1
        return count
    bought=[1,1,1]
    if thansohoc == 0:
        bought[0] = 0
    if nhantuonghoc == 0:
        bought[1] = 0
    if sinhtrachoc == 0:
        bought[2] = 0
    
    
    thansohoc_cost= 0
    nhantuonghoc_cost= 0
    sinhtrachoc_cost= 0
    if bought[0]>0:
        
        if value[thansohoc] == 1:
            discount = 0.9
        elif value[thansohoc]==2:
            discount = 0.8
        else:
            discount=1
        temp=1
        if ser_sale['thansohoc'] == 0:
            if ser_sale['nhantuonghoc'] >0:
                if ser_sale['sinhtrachoc'] >0:
                    temp=0.7
                else :
                    temp =0.75
            else:
                temp = 0.8
        elif ser_sale['thansohoc'] ==1:
            temp = 0.9
        thansohoc_cost= thansohoc * cost['thansohoc'] * discount * temp
    if bought[1]>0:
        
        if value[nhantuonghoc] == 1:
            discount = 0.9
        elif value[nhantuonghoc]==2:
            discount = 0.8
        else:
            discount=1
        temp=1
        if ser_sale['nhantuonghoc'] == 0:
            if ser_sale['thansohoc'] >0:
                if ser_sale['sinhtrachoc'] >0:
                    temp=0.7
                else :
                    temp =0.75
            else:
                temp = 0.8
        elif ser_sale['nhantuonghoc'] ==1:
            temp = 0.9
        nhantuonghoc_cost= nhantuonghoc * cost['nhantuonghoc'] * discount * temp
    if bought[2]>0:
        
        if value[sinhtrachoc] == 1:
            discount = 0.9
        elif value[sinhtrachoc]==2:
            discount = 0.8
        else:
            discount=1
        temp=1
        if ser_sale['sinhtrachoc'] == 0:
            if ser_sale['thansohoc'] >0:
                if ser_sale['nhantuonghoc'] >0:
                    temp=0.7
                else :
                    temp =0.75
            else:
                temp = 0.8
        elif ser_sale['sinhtrachoc'] ==1:
            temp = 0.9
        sinhtrachoc_cost= sinhtrachoc * cost['sinhtrachoc'] * discount * temp
    num0= count_zeros(bought)
    tong_tien=thansohoc_cost + nhantuonghoc_cost +sinhtrachoc_cost
    


    if num0 ==0:
        if his3 :
            if count ==1:
                sales= 0.65
        else:
            sales =0.7

    elif num0==1:
        if bought[0]> 0 and bought[1]>0:
            if his['12'] ==1:
                sales=0.75
            elif his['12'] ==0:
                sales=0.8
        if bought[0]> 0 and bought[2]>0:
            if his['13'] ==1:
                sales=0.75
            elif his['13'] ==0:
                sales=0.8
        if bought[2]> 0 and bought[1]>0:
            if his['23'] ==1:
                sales=0.75
            elif his['23'] ==0:
                sales=0.8
    #     sales=0.8
    # else:
        # pass
    

    return round(tong_tien*sales)