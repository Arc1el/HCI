# -*- coding: euc-kr -*-

import serial
import mydata
import datetime as dt
port=serial.Serial(port='/dev/serial0', baudrate=9600, write_timeout = 1, timeout=1.0)
eof = b"\xff\xff\xff"
counter = 0

def send_command(commands):
    datas = []
    for i in range(len(commands)):
        str_cmd = commands[i]
        port.write(str_cmd.encode())
        port.write(eof)
        data = port.read()
        datas.append(data)
    return datas

def main_update():
    print("update main data!")
    today = dt.datetime.today()
    year = str(today.year)
    month = str(today.month)
    day = today.day
    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)

    date = year+month+day

    kospi = mydata.kospi(date)[0]
    kosdaq = mydata.kosdaq(date)[0]

    sep = 0x20

    if kospi[2] > 0:
        send_command([
                    't1.txt=\"' + str(kospi[1]) + '\"',
                    't5.txt=\"' + str(kospi[2]) + " " + str(kospi[3]) + "%" + '\"',
                    "t1.pco=63488",
                    "t5.pco=63488",
                    ])
    elif kospi[2] < 0:
        send_command([
                    't1.txt=\"' + str(kospi[1]) + '\"',
                    't5.txt=\"' + str(kospi[2]) + " " + str(kospi[3]) + "%" + '\"',
                    "t1.pco=10591",
                    "t5.pco=10591"
                    ])
    elif kospi[2] == 0:
        send_command([
                    't1.txt=\"' + str(kospi[1]) + '\"',
                    't5.txt=\"' + str(kospi[2]) + " " + str(kospi[3]) + "%" + '\"',
                    "t1.pco=65535",
                    "t5.pco=65535"
                    ])
    if kosdaq[2] > 0:
        send_command([
                    't3.txt=\"' + str(kosdaq[1]) + '\"',
                    't6.txt=\"' + str(kosdaq[2]) + " " + str(kosdaq[3]) + "%" + '\"',
                    "t3.pco=63488",
                    "t6.pco=63488"
                    ])
    elif kosdaq[2] < 0:
        send_command([
                    't3.txt=\"' + str(kosdaq[1]) + '\"',
                    't6.txt=\"' + str(kosdaq[2]) + " " + str(kosdaq[3]) + "%" + '\"',
                    "t3.pco=10591",
                    "t6.pco=10591"
                    ])
    elif kosdaq[2] == 0:
        send_command([
                    't3.txt=\"' + str(kosdaq[1]) + '\"',
                    't6.txt=\"' + str(kosdaq[2]) + " " + str(kosdaq[3]) + "%" + '\"',
                    "t3.pco=65535",
                    "t6.pco=65535"
                    ])

def title_command(command, title):
    print("command : ", command, "title : ", title)
    port.write(command.encode())
    port.write(title.encode("euc-kr"))
    port.write('\"'.encode())
    port.write(eof)
    data = port.read()
    return data
    

def fav_update(favs):
    print(favs)
    for i in range(len(favs)):
        print("update fav data!", i)
        code = favs[i]
        dat = mydata.search(code)
        title = dat[0][0]
        price = dat[0][1]
        prev = dat[0][2]
        percent = dat[0][3]

        title_command('f' + str(i) + 'title.txt=\"', title)
        send_command([
                    'f' + str(i) + 'val.txt=\"' + str(price) + " " + str(prev) + " " + str(percent) + '\"',
                    ])
    
        if float(percent[:-1]) < 0:
            send_command([
                        'f' + str(i) + 'title.pco=10591',
                        'f' + str(i) + 'val.pco=10591'
                        ])
        elif float(percent[:-1]) > 0:
            send_command([
                        'f' + str(i) + 'title.pco=63488',
                        'f' + str(i) + 'val.pco=63488'
                        ]) 
        else:
            send_command([
                        'f' + str(i) + 'title.pco=65535',
                        'f' + str(i) + 'val.pco=65535'
                        ])
        

#init main page
favs = ["하이닉스", "카카오", "LG화학", "NAVER", "이마트"]
#main_update()
#fav_update(favs)
flag = "main"

to_search = b'e\x00\x01\x00\xff\xff\xff'
#search = b'e\x01\x01\x00\xff\xff\xff'
to_fav = b'e\x02\x01\x00\xff\xff\xff'
#favorite = b'e\x03\x01\x00\xff\xff\xff'
back_search = b'e\x02\x02\x00\xff\xff\xff'
code = 0
arr_index = 0
title = ""

while True:
    try:
        counter += 1

        #update main page
        if counter%5 == 0 and flag == "main":
            main_update()
            fav_update(favs)

        if flag == "main" :
            output = port.readline()
            print(output)

        if output == to_search:
            flag = "to_search"
            print("to search button pressed")
            while True:
                output = port.readline()
                if output:
                    print(output.decode())
                    code = output.decode()
                    break

            print("code ok")
            print("display data")

            data = mydata.search(code)
            (anal1, anal2, anal3, anal4) = mydata.analysis_stock(code)
            title = data[0][0]

            title_command('p2txt1.txt=\"', title)
            title_command('p2txt2.txt=\"', anal1)
            title_command('p2txt3.txt=\"', anal2)
            title_command('p2txt4.txt=\"', anal3)
            title_command('p2txt5.txt=\"', anal4)
            
            while True:
                output = port.readline()
                if output:
                    print(output)
                    break

        if output == to_fav:
            flag = "to_fav"
            print("to_fav button pressed")

            #change favorites list
            dat = title_command('t8.txt=\"', favs[0])
            print(dat)
            dat = title_command('t9.txt=\"', favs[1])
            print(dat)
            dat = title_command('t11.txt=\"', favs[2])
            print(dat)
            dat = title_command('t13.txt=\"', favs[3])
            print(dat)
            dat = title_command('t15.txt=\"', favs[4])
            print(dat)


            while True:
                print("wait for confim button")
                output = port.readline()
                if output:
                    break
            
            print(code)
            
            #update favorite
            if output == b'\x00\x00\x00\x00':
                print("index 0 is update")
                favs[0] = str(title)

            elif output == b'\x01\x00\x00\x00':
                print("index 1 is update")
                favs[1] = str(title)

            elif output == b'\x02\x00\x00\x00':
                print("index 2 is update")
                favs[2] = str(title)
                
            elif output == b'\x03\x00\x00\x00':
                print("index 3 is update")
                favs[3] = str(title)
            
            elif output == b'\x04\x00\x00\x00':
                print("index 4 is update")
                favs[4] = str(title)

            flag = "main"
            counter = 3
                
    except:
        pass
