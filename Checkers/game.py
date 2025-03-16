from tkinter import *
import random
import time
import copy
import tkinter.messagebox

root=Tk()
root.title('Шашки')
board=Canvas(root, width=800,height=800,bg='#FFFFFF')
board.pack()

n2_spisok=()
ur=3
k_rez=0
o_rez=0
poz1_x=-1
f_hi=True

def image_checker():
    global checkers
    i1=PhotoImage(file="res\\1b.gif")
    i2=PhotoImage(file="res\\1bk.gif")
    i3=PhotoImage(file="res\\1h.gif")
    i4=PhotoImage(file="res\\1hk.gif")
    checkers=[0,i1,i2,i3,i4]


def new_game():
    global pole
    pole=[[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]

def output(x_poz_1,y_poz_1,x_poz_2,y_poz_2):
    global checkers
    global pole
    global kr_ramka,zel_ramka
    k=100
    x=0
    board.delete('all')
    kr_ramka=board.create_rectangle(-5, -5, -5, -5,outline="red",width=5)
    zel_ramka=board.create_rectangle(-5, -5, -5, -5,outline="green",width=5)

    while x<8*k:#рисуем доску
        y=1*k
        while y<8*k:
            board.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    x=1*k
    while x<8*k:#рисуем доску
        y=0
        while y<8*k:
            board.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k

    for y in range(8):
        for x in range(8):
            z=pole[y][x]
            if z:
                if (x_poz_1,y_poz_1)!=(x,y):
                    board.create_image(x*k,y*k, anchor=NW, image=checkers[z])
    z=pole[y_poz_1][x_poz_1]
    if z:
        board.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image=checkers[z],tag='ani')
    #вычисление коэф. для анимации
    kx = 1 if x_poz_1<x_poz_2 else -1
    ky = 1 if y_poz_1<y_poz_2 else -1
    for i in range(abs(x_poz_1-x_poz_2)):
        for ii in range(33):
            board.move('ani',0.03*k*kx,0.03*k*ky)
            board.update()#обновление
            time.sleep(0.01)

def soobsenie(s):
    global f_hi
    z='Игра завершена'
    if s==1:
        tkinter.messagebox.askyesno(title=z, message='Вы победили!\nНажми "Да" что бы начать заново.',icon='info')
        i = True
    if s==2:
        tkinter.messagebox.askyesno(title=z, message='Вы проиграли!\nНажми "Да" что бы начать заново.',icon='info')
        i = True
    if s==3:
        tkinter.messagebox.askyesno(title=z, message='Ходов больше нет.\nНажми "Да" что бы начать заново.',icon='info')
        i = True
    if i:
        new_game()
        output(-1,-1,-1,-1)
        f_hi=True

def pozici_1(event):
    x,y=(event.x)//100,(event.y)//100
    board.coords(zel_ramka,x*100,y*100,x*100+100,y*100+100)

def pozici_2(event):
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    x,y=(event.x)//100,(event.y)//100
    if pole[y][x]==1 or pole[y][x]==2:
        board.coords(kr_ramka,x*100,y*100,x*100+100,y*100+100)
        poz1_x,poz1_y=x,y
    else:
        if poz1_x!=-1:
            poz2_x,poz2_y=x,y
            if f_hi:
                hod_igroka()
                if not(f_hi):
                    time.sleep(0.5)
                    move_ai()
            poz1_x=-1
            board.coords(kr_ramka,-5,-5,-5,-5)

def move_ai():
    global f_hi
    global n2_spisok
    proverka_hk(1,(),[])
    if n2_spisok:
        kh=len(n2_spisok)
        th=random.randint(0,kh-1)
        dh=len(n2_spisok[th])
        for h in n2_spisok:
            h=h
        for i in range(dh-1):
            #выполняем ход
            spisok=hod(1,n2_spisok[th][i][0],n2_spisok[th][i][1],n2_spisok[th][1+i][0],n2_spisok[th][1+i][1])
        n2_spisok=[]#очищаем список ходов
        f_hi=True

    #определяем победителя
    s_k,s_i=skan()
    if not(s_i):
            soobsenie(2)
    elif not(s_k):
            soobsenie(1)
    elif f_hi and not(spisok_hi()):
            soobsenie(3)
    elif not(f_hi) and not(spisok_hk()):
            soobsenie(3)

def spisok_hk():#составляем список ходов компьютера
    spisok=check_moves([])#здесь проверяем обязательные ходы
    if not(spisok):
        spisok=prosmotr_hodov_k2([])#здесь проверяем оставшиеся ходы
    return spisok

def proverka_hk(tur,n_spisok,spisok):
    global pole
    global n2_spisok
    global l_rez,k_rez,o_rez
    if not(spisok):#если список ходов пустой
        spisok=spisok_hk()#заполняем

    if spisok:
        k_pole=copy.deepcopy(pole)#копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проходим все ходы по списку
            t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:#если существует ещё ход
                proverka_hk(tur,(n_spisok+((poz1_x,poz1_y),)),t_spisok)
            else:
                proverka_hi(tur,[])
                if tur==1:
                    t_rez=o_rez/k_rez
                    if not(n2_spisok):
                        n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        l_rez=t_rez#сохряняем наилучший результат
                    else:
                        if t_rez==l_rez:
                            n2_spisok=n2_spisok+(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        if t_rez>l_rez:
                            n2_spisok=()
                            n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                            l_rez=t_rez#сохряняем наилучший результат
                    o_rez=0
                    k_rez=0

            pole=copy.deepcopy(k_pole)#возвращаем поле
    else:
        s_k,s_i=skan()#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def spisok_hi():#составляем список ходов игрока
    spisok=prosmotr_hodov_i1([])#здесь проверяем обязательные ходы
    if not(spisok):
        spisok=prosmotr_hodov_i2([])#здесь проверяем оставшиеся ходы
    return spisok

def proverka_hi(tur,spisok):
    global pole,k_rez,o_rez
    global ur
    if not(spisok):
        spisok=spisok_hi()

    if spisok:#проверяем наличие доступных ходов
        k_pole=copy.deepcopy(pole)#копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:
            t_spisok=hod(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:#если существует ещё ход
                proverka_hi(tur,t_spisok)
            else:
                if tur<ur:
                    proverka_hk(tur+1,(),[])
                else:
                    s_k,s_i=skan()#подсчёт результата хода
                    o_rez+=(s_k-s_i)
                    k_rez+=1

            pole=copy.deepcopy(k_pole)#возвращаем поле
    else:#доступных ходов нет
        s_k,s_i=skan()#подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def skan():
    global pole
    s_i=0
    s_k=0
    for i in range(8):
        for ii in pole[i]:
            if ii==1:s_i+=1
            if ii==2:s_i+=3
            if ii==3:s_k+=1
            if ii==4:s_k+=3
    return s_k,s_i

def hod_igroka():
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    f_hi=False#считаем ход игрока выполненным
    spisok=spisok_hi()
    if spisok:
        if ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проверяем ход на соответствие правилам игры
            t_spisok=hod(1,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_spisok:
                f_hi=True#считаем ход игрока невыполненным
        else:
            f_hi=True#считаем ход игрока невыполненным
    board.update()#!!!обновление

def hod(f,poz1_x,poz1_y,poz2_x,poz2_y):
    global pole
    if f:output(poz1_x,poz1_y,poz2_x,poz2_y)#рисуем игровое поле
    #превращение
    if poz2_y==0 and pole[poz1_y][poz1_x]==1:
        pole[poz1_y][poz1_x]=2
    #превращение
    if poz2_y==7 and pole[poz1_y][poz1_x]==3:
        pole[poz1_y][poz1_x]=4
    #делаем ход
    pole[poz2_y][poz2_x]=pole[poz1_y][poz1_x]
    pole[poz1_y][poz1_x]=0

    kx=ky=1
    if poz1_x<poz2_x:kx=-1
    if poz1_y<poz2_y:ky=-1
    x_poz,y_poz=poz2_x,poz2_y
    while (poz1_x!=x_poz) or (poz1_y!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if pole[y_poz][x_poz]!=0:
            pole[y_poz][x_poz]=0
            if f:output(-1,-1,-1,-1)#рисуем игровое поле
            if pole[poz2_y][poz2_x]==3 or pole[poz2_y][poz2_x]==4:
                return check_movesp([],poz2_x,poz2_y)
            elif pole[poz2_y][poz2_x]==1 or pole[poz2_y][poz2_x]==2:
                return prosmotr_hodov_i1p([],poz2_x,poz2_y)
    if f:output(poz1_x,poz1_y,poz2_x,poz2_y)

def check_moves(spisok):#проверка наличия обязательных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=check_movesp(spisok,x,y)
    return spisok

def check_movesp(spisok,x,y):
    if pole[y][x]==3:#шашка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
    if pole[y][x]==4:#дамка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                        if osh>0:spisok.pop()#удаление хода из списка
                        break
    return spisok

def prosmotr_hodov_k2(spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if pole[y][x]==3:#шашка
                for ix,iy in (-1,1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
            if pole[y][x]==4:#дамка
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or osh==2:
                                break
    return spisok

def prosmotr_hodov_i1(spisok):#проверка наличия обязательных ходов
    spisok=[]#список ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            spisok=prosmotr_hodov_i1p(spisok,x,y)
    return spisok

def prosmotr_hodov_i1p(spisok,x,y):
    if pole[y][x]==1:#шашка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                    if pole[y+iy+iy][x+ix+ix]==0:
                        spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
    if pole[y][x]==2:#дамка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                        osh+=1
                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                        if osh>0:spisok.pop()#удаление хода из списка
                        break
    return spisok

def prosmotr_hodov_i2(spisok):#проверка наличия остальных ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            if pole[y][x]==1:#шашка
                for ix,iy in (-1,-1),(1,-1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if pole[y+iy][x+ix]==0:
                            spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                        if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if pole[y+iy*2][x+ix*2]==0:
                                    spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка
            if pole[y][x]==2:#дамка
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if pole[y+iy*i][x+ix*i]==0:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4:
                                osh+=1
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or osh==2:
                                break
    return spisok

image_checker()
new_game()#начинаем новую игру
output(-1,-1,-1,-1)#рисуем игровое поле
board.bind("<Motion>", pozici_1)
board.bind("<Button-1>", pozici_2)
mainloop()
