from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
from math import *
from pandas import DataFrame , read_json, read_excel ,ExcelWriter
import datetime as dt
from openpyxl import load_workbook
def rev(s):
    return s[::-1]

def add_underscore(s):
    l = s.split(' ')
    out = ""
    for i in l:
        out = out + "_" + i
    return out

def homepage(request):
    return render(request , 'homepage.html')

def success(request):
    return render(request , 'success.html')

def arith_mean(l):
    return sum(l)/float(len(l))

def geo_mean(l):
    temp = [log((x + 100) , 2) for x in  l]
    ans = arith_mean(temp)
    return (pow(2 , ans)-100)


def st_dev(am , l):
    l_temp = [(x - am) * (x-am) for x in l]
    return sqrt(arith_mean(l_temp))

def geo_st_dev(gm , l):
    l_temp = [(x+100)/100.0 for x in l]
    gm_norm = (gm + 100)/100.0
    l_div = list(map(lambda x: log((x/gm_norm) ,e) * log((x/gm_norm) , e) , l_temp))
    avg = arith_mean(l_div)
    ans_sub = sqrt(avg)
    return ((exp(ans_sub) - 1) * 100)

def calculate_stuff(request):
        sheet1 = read_excel('FINAL MASTERLIST-DEC30.xlsx')
        db1 = DataFrame(sheet1)
        option = request.POST['options']
        start_date = request.POST['str']
        end_date = request.POST['end']

        temp_1 = start_date_obj = dt.datetime.strptime(start_date , "%Y-%m-%d")
        temp_2 = end_date_obj = dt.datetime.strptime(end_date , "%Y-%m-%d")
        #temp_1-=dt.timedelta(days=29)
        scheme_numbers = sheet1['Serial Number']
        scheme_names = sheet1['Scheme Name']
        dict_schemes = dict(zip(scheme_names , scheme_numbers))
        #start_date_obj-=dt.timedelta(days=29)
        dict_nav = {}

        sheet2 = read_excel(str(dict_schemes[option]) + '.xlsx')
        df = DataFrame(sheet2)
        l_nav = l_dates = []
        #print(len(df.axes[0]))
        #print(df.loc[0 , 'date'])
        temp_str = temp_str_obj = temp_1 = df.loc[len(df.axes[0])-1 , 'Date']
        temp_end = temp_end_obj = temp_2 = df.loc[0 , 'Date']

        while(temp_str<=temp_end):
            dict_nav[temp_str]=0
            temp_str+=dt.timedelta(days=1)

        df.set_index('Date' , inplace = True)
        while(temp_str_obj<=temp_end_obj):
            temp = temp_str_obj
            try:
                dict_nav[temp] = float(df.loc[temp, 'Close'])
            except KeyError:
                pass
            temp_str_obj+=dt.timedelta(days=1)

        while(temp_1<=temp_2):
            temp = temp_1
            if(dict_nav[temp]==0):
                temp_1-=dt.timedelta(days=1)
                dict_nav[temp]=dict_nav[temp_1]
                temp_1+=dt.timedelta(days=1)
            temp_1+=dt.timedelta(days=1)

            #print(len((list(dict_nav.values()))))
        l_nav = list(dict_nav.values())
        l_dates = list(dict_nav.keys())

        start_index = l_dates.index(start_date_obj)
        end_index = l_dates.index(end_date_obj)
            #print(start_index)
            #print(end_index)
        l_thirty = []
        l_yearly = []
            #for i in range(len(dict_nav)):
            #    print(str(l_nav[i]) + " " +  str(l_dates[i]))

        for i in range(end_index , start_index+28 , -1):
                #print(str(l_nav[i]) + " " + str(l_nav[i-29]))
            l_thirty.append((l_nav[i] - l_nav[i-29])/(l_nav[i-29]) * 100)

        for i in range(end_index , start_index+1093 , -1):
                #print(str(l_nav[i]) + " " + str(l_nav[i-364]))
            l_yearly.append((l_nav[i]-l_nav[i-1094])/(l_nav[i-1094]) * 100)


        am_30 = arith_mean(l_thirty)
            #gm_30 = gmean(df_2.loc[: , 'values'])
            #print(gm_30)
        gm_30 = geo_mean(l_thirty)
        am_std_30 = st_dev(am_30 , l_thirty)
        gm_std_30 = geo_st_dev(gm_30 , l_thirty)

        am_1095 = arith_mean(l_yearly)
        gm_1095 = geo_mean(l_yearly)
        am_std_1095 = st_dev(am_1095 , l_yearly)
        gm_std_1095 = geo_st_dev(gm_1095 , l_yearly)
            #print(gm_1095)
            #print(am_1095)
            #print(am_std_1095)
            #print(gm_std_1095)
        gm_coeff_var_30 = pow(gm_std_30 , 1/float(gm_30))
        gm_coeff_var_1095 = pow(gm_std_1095 , 1/float(gm_1095))

        sharpe_am_30 = (am_30 - 0.5)/am_std_30
        annual_ratio_am = sharpe_am_30 * sqrt(12)
        sharpe_am_1095 = (am_1095 - 6)/am_std_1095

        sharpe_gm_30 = (gm_30 - 0.5)/gm_std_30
        annual_ratio_gm = sharpe_gm_30 * sqrt(12)
        sharpe_gm_1095 = (gm_1095 - 6)/gm_std_1095

        down_period_30 = len(list(filter(lambda x:x<=0 , l_thirty)))/float(len(l_thirty))
        down_period_1095 = len(list(filter(lambda x:x<=0 , l_yearly)))/float(len(l_yearly))

        under_period_30 = len(list(filter(lambda x:x<=0.5 , l_thirty)))/float(len(l_thirty))
        under_period_1095 = len(list(filter(lambda x:x<=6 , l_yearly)))/float(len(l_yearly))

        mar_thirty = [0 , 0.5 , 0.67 , gm_30]
        mar_yearly = [0 , 19.10 , 25.97 , gm_1095]

        down_deviation_30 = []
        down_deviation_1095 = []

        for i in mar_thirty:
            temp = [pow(min(0 , x-i) , 2) for x in l_thirty]
            down_deviation_30.append(sqrt(arith_mean(temp)))

        for i in mar_yearly:
            temp = [pow(min(0 , x-i) , 2) for x in l_yearly]
            down_deviation_1095.append(sqrt(arith_mean(temp)))

        sortino_30 = []
        sortino_1095 = []

        for i in range(4):
            if(down_deviation_30[i]==0):
                sortino_30.append('NAN')
            else:
                sortino_30.append(gm_30 - (mar_thirty[i]/down_deviation_30[i]) - mar_thirty[i])
            if(down_deviation_1095[i]==0):
                sortino_1095.append('NAN')
            else:
                sortino_1095.append(gm_1095 - (mar_yearly[i]/down_deviation_1095[i]) - mar_yearly[i])

        omega_ratio_1095 = []

        for i in mar_yearly:
            temp = [(x-i) for x in l_yearly]
            num = sum(list(filter((lambda x:x>0) , temp)))
                #print(list(filter((lambda x:x>i) , l_yearly)))
            den = sum(list(filter((lambda x:x<0) , temp)))
                #print(num)
                #print(den)
            if(den==0):
                omega_ratio_1095.append('NAN')
            else:
                omega_ratio_1095.append(num/float(-den))

        omega_ratio_30 = []
        for i in mar_thirty:
            temp = [(x-i) for x in l_thirty]
            num = sum(list(filter((lambda x:x>0) , temp)))
                #print(list(filter((lambda x:x>i) , l_yearly)))
            den = sum(list(filter((lambda x:x<0) , temp)))
                #print(num)
                #print(den)
            if(den==0):
                omega_ratio_30.append('NAN')
            else:
                omega_ratio_30.append(num/float(-den))

        wb1 = load_workbook("COVER SHEET - KS.xlsx")
        sheet = wb1.active
        c1 = sheet['E2']
        c1.value = dict_schemes[option]

        name = sheet['E1']
        name.value = option

        st_1 = sheet['H1']
        en_1 = sheet['H2']

        st_1.value = start_date
        en_1.value = end_date

        a_mean_cell_1 = sheet['G5']
        a_mean_cell_2 = sheet['G6']

        a_mean_cell_1.value = am_30
        a_mean_cell_2.value = am_1095

        geo_mean_cell_1 = sheet['I5']
        geo_mean_cell_2 = sheet['I6']

        geo_mean_cell_1.value = gm_30
        geo_mean_cell_2.value = gm_1095

        std_dev_cell_1 = sheet['H5']
        std_dev_cell_2 = sheet['H6']

        std_dev_cell_1.value = am_std_30
        std_dev_cell_2.value = am_std_1095

        geo_sg_cell_1 = sheet['J5']
        geo_sg_cell_2 = sheet['J6']

        geo_sg_cell_1.value = gm_std_30
        geo_sg_cell_2.value = gm_std_1095

        Sharpe_cell_am_1 = sheet['K5']
        Sharpe_cell_am_1.value = sharpe_am_30

        Sharpe_cell_am_2 = sheet['K6']
        Sharpe_cell_am_2.value = sharpe_am_1095

        Sharpe_gm_cell_1 = sheet['L5']
        Sharpe_gm_cell_1.value = sharpe_gm_30
        Sharpe_gm_cell_2 = sheet['L6']
        Sharpe_gm_cell_2.value = sharpe_gm_1095

        Coefficient_cell_1 = sheet['M6']
        Coefficient_cell_1.value = gm_coeff_var_1095
        Coefficient_cell_2 = sheet['M5']
        Coefficient_cell_2.value = gm_coeff_var_30
        #omega_ratio
        gm_omega_cell_30 = sheet['F11']
        gm_omega_cell_30.value = omega_ratio_30[3]

        zero_omega_cell_30 = sheet['G11']
        zero_omega_cell_30.value = omega_ratio_30[0]

        five_omega_cell_30 = sheet['H11']
        five_omega_cell_30.value = omega_ratio_30[1]

        six_seven_cell_omega_30 = sheet['I11']
        six_seven_cell_omega_30.value = omega_ratio_30[2]

            #Sortino
        gm_sortino_cell_30 = sheet['F12']
        gm_sortino_cell_30.value = '-'

        zero_sortino_cell_30 = sheet['G12']
        zero_sortino_cell_30.value = sortino_30[0]

        five_sortino_cell_30 = sheet['H12']
        five_sortino_cell_30.value = sortino_30[1]

        six_seven_cell_sortino_30 = sheet['I12']
        six_seven_cell_sortino_30.value = sortino_30[2]
            #Dd
        gm_dd_cell_30 = sheet['F13']
        gm_dd_cell_30.value = down_deviation_30[3]

        zero_dd_cell_30 = sheet['G13']
        zero_dd_cell_30.value = down_deviation_30[0]

        five_dd_cell_30 = sheet['H13']
        five_dd_cell_30.value = down_deviation_30[1]

        six_seven_cell_dd_30 = sheet['I13']
        six_seven_cell_dd_30.value = down_deviation_30[2]

        downperiod_30_cell = sheet['J11']
        downperiod_30_cell.value = down_period_30

        underperiod_30_cell = sheet['K11']
        underperiod_30_cell.value =under_period_30

            #omega
        gm_omega_cell_1095 = sheet['F17']
        gm_omega_cell_1095.value = omega_ratio_1095[3]

        zero_omega_cell_1095 = sheet['G17']
        zero_omega_cell_1095.value = omega_ratio_1095[0]

        five_omega_cell_1095 = sheet['H17']
        five_omega_cell_1095.value = omega_ratio_1095[1]

        six_seven_cell_omega_1095 = sheet['I17']
        six_seven_cell_omega_1095.value = omega_ratio_1095[2]

            #sortino_1095
        gm_sortino_cell_1095 = sheet['F18']
        gm_sortino_cell_1095.value = '-'

        zero_sortino_cell_1095 = sheet['G18']
        zero_sortino_cell_1095.value = sortino_1095[0]

        five_sortino_cell_1095 = sheet['H18']
        five_sortino_cell_1095.value = sortino_1095[1]

        six_seven_cell_sortino_1095 = sheet['I18']
        six_seven_cell_sortino_1095.value = sortino_1095[2]

            #dd
        gm_dd_cell_1095 = sheet['F19']
        gm_dd_cell_1095.value = down_deviation_1095[3]

        zero_dd_cell_1095 = sheet['G19']
        zero_dd_cell_1095.value = down_deviation_1095[0]

        five_dd_cell_1095 = sheet['H19']
        five_dd_cell_1095.value = down_deviation_1095[1]

        six_seven_cell_dd_1095 = sheet['I19']
        six_seven_cell_dd_1095.value = down_deviation_1095[2]

        downperiod_1095_cell = sheet['J17']
        underperiod_1095_cell = sheet['K17']

        downperiod_1095_cell.value = down_period_1095
        underperiod_1095_cell.value = under_period_1095

        filename = 'Performance_' + option + '.xlsx'
        filename = add_underscore(filename)
        wb1.save(filename)
        with open(filename, 'rb') as fh:
            response = HttpResponse(fh.read() , content_type = "application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline ; filename=' + filename
            return response
