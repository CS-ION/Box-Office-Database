import mysql.connector
from prettytable import PrettyTable

#to check whether its connected
try:
    mydb=mysql.connector.connect(host='localhost',user='root',password=input('Enter Password : '))
except:
    print('Error establishing connection')
    raise SystemExit

if mydb.is_connected()==False:
    print('not connected')
    raise SystemExit

#creating a cursor object
mycursor=mydb.cursor()

#creating/using database
try:
    mycursor.execute('create database Project')
    mycursor.execute('use Project')
except:
    mycursor.execute('use Project')

#creating table
try:
    mycursor.execute('''create table net_gross
    (film_name varchar(30) primary key,
    release_date date, nett_gross_india decimal(6,2),
    nett_gross_overseas decimal(6,2),
    nett_gross_worldwide decimal(6,2),
    verdict varchar(30))''')
    mycursor.execute('''create table footfalls
    (film_name varchar(30) primary key,
    release_date date, footfalls_india decimal(6,2),
    footfalls_overseas decimal(6,2),
    footfalls_worldwide decimal(6,2),
    verdict varchar(30))''')
except:
    pass

#menu_driven_functions
def desc_net():

    mycursor.execute(f'desc net_gross')

    L = []
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for I in (mycursor.fetchall()):
        x.add_row(list(I))
    print(x)

def desc_footfalls():

    mycursor.execute(f'desc footfalls')

    L = []
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for I in (mycursor.fetchall()):
        x.add_row(list(I))
    print(x)

def add_movie():

    mycursor.execute(f'''insert into net_gross values
    ('{(name:= input('Enter movie name : '))}',
    '{(date:= input('Enter release date : '))}', 
    {(net_ind:= input('Enter Nett Gross India : '))},
    {(net_world:= input('Enter Nett Gross Overseas : '))},
    {(float(net_ind) + float(net_world))},
    '{(verdict:= input('Enter Verdict : '))}')''')

    mycursor.execute(f'''insert into footfalls values('{name}',
    '{date}',{(foot_ind:= input('Enter Footfalls India : '))},
    {(foot_world:= input('Enter Footfalls Overseas : '))},
    {(float(foot_ind) + float(foot_world))},'{verdict}')''')

    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def add_movies():

    rec_list1 = []
    rec_list2 = []

    for I in range(int(input('Enter the no of movies : '))):

        rec_list1.append(((name:= input('Enter movie name : ')),
        (date:= input('Enter release date : ')),
        (net_ind:= float(input('Enter Nett Gross India : '))),
        (net_world:= float(input('Enter Nett Gross Overseas : '))),
        net_ind + net_world,(verdict:= input('Enter Verdict : '))))

        rec_list2.append((name,date,
        (foot_ind:= float(input('Enter Footfalls India : '))),
        (foot_world:= float(input('Enter Footfalls Overseas : '))),
        foot_ind + foot_world,verdict))

        print()

    mycursor.executemany('insert into net_gross values(%s,%s,%s,%s,%s,%s)',rec_list1)
    mycursor.executemany('insert into footfalls values(%s,%s,%s,%s,%s,%s)',rec_list2)
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def delete_movie():

    mycursor.execute(f"delete from net_gross where film_name='{(name:=input('Enter Film Name : '))}'")
    mycursor.execute(f"delete from footfalls where film_name='{name}'")
    if mycursor.rowcount == 0:
        print('Film Not Found')
        return
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def update_nett_gross_ind():

    name = input('Enter Film Name : ')
    mycursor.execute(f'''update net_gross set
    nett_gross_india={input('Enter Nett Gross India : ')}
    where film_name='{name}' ''')
    mycursor.execute(f'''update net_gross set
    nett_gross_worldwide=nett_gross_india+nett_gross_overseas
    where film_name='{name}' ''')
    if mycursor.rowcount == 0:
        print('Film not found')
        return
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def update_nett_gross_ovr():

    name = input('Enter Film Name : ')
    mycursor.execute(f'''update net_gross set
    nett_gross_overseas={input('Enter Nett Gross Overseas : ')}
    where film_name='{name}' ''')
    mycursor.execute(f'''update net_gross set
    nett_gross_worldwide=nett_gross_india+nett_gross_overseas
    where film_name='{name}' ''')
    if mycursor.rowcount == 0:
        print('Film not found')
        return
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def update_footfalls_ind():

    name = input('Enter Film Name : ')
    mycursor.execute(f'''update footfalls set
    footfalls_india={input('Enter Footfalls India : ')}
    where film_name='{name}' ''')
    mycursor.execute(f'''update footfalls set
    footfalls_worldwide=footfalls_india+footfalls_overseas
    where film_name='{name}' ''')
    if mycursor.rowcount == 0:
        print('Film not found')
        return
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def update_footfalls_ovr():

    name = input('Enter Film Name : ')
    mycursor.execute(f'''update footfalls set
    footfalls_overseas={input('Enter Footfalls Overseas : ')}
    where film_name='{name}' ''')
    mycursor.execute(f'''update footfalls set
    footfalls_worldwide=footfalls_india+footfalls_overseas
    where film_name='{name}' ''')
    if mycursor.rowcount == 0:
        print('Film not found')
        return
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def search():

    mycursor.execute(f'''select N.*,
    footfalls_india,footfalls_overseas,footfalls_worldwide 
    from net_gross N, footfalls F where N.film_name=F.film_name 
    and N.film_name='{input('Enter FilmName : ')}'
    ''')

    result = mycursor.fetchall()
    if result == []:
        print('No movies found')
        return
    
    L = []
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for I in result:
        x.add_row(I)
    print(x)

def compare():

    mycursor.execute(f'''select N.*,
    footfalls_india,footfalls_overseas,footfalls_worldwide 
    from net_gross N, footfalls F where N.film_name=F.film_name 
    and N.film_name in
    ('{input('Enter Film 1 : ')}','{input('Enter Film 2 : ')}')
    ''')

    result = mycursor.fetchall()

    if len(result) != 2:
        print('Movies not found')
        return

    L = []
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for I in result:
        x.add_row(I)
    print(x)

def add_coloumn():

    try:
        mycursor.execute(f'''alter table
        {input('Enter the table to add coloum : ')} 
        add {input('Enter coloumn name and its features : ')} after
        {input('You want to add the coloumn after which coloumn : ')}''')
        print(mycursor.rowcount,'rows affected')
    except:
        print('Error. There is something wrong with the info entered')
    mydb.commit()

def modify_coloumn():
    
    try:
        mycursor.execute(f'''alter table {input('Enter the table : ')} 
        modify {input('Enter coloumn name and its modified features : ')} after
        {input('You want to position the coloumn after which coloumn : ')} ''')
        print(mycursor.rowcount,'rows affected')
    except:
        print('Error. There is something wrong with the info entered')
    mydb.commit()

def delete_coloumn():

    try:
        mycursor.execute(f'''alter table {input('Enter the table : ')}
        drop column {input('Enter coloumn name to be deleted : ')}''')
        print(mycursor.rowcount,'rows affected')
    except:
        print('Error. There is something wrong with the info entered')
    mydb.commit()
    
def top10_gross_ind():

    mycursor.execute('select * from net_gross order by nett_gross_india desc')
    L = ['rank']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        if J==10:
            break
        x.add_row([J+1]+list(I))
    print(x)

def top10_gross_ovr():

    mycursor.execute('select * from net_gross order by nett_gross_overseas desc')
    L = ['rank']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        if J==10:
            break
        x.add_row([J+1]+list(I))
    print(x)

def top10_gross_worldwide():

    mycursor.execute('select * from net_gross order by nett_gross_worldwide desc')
    L = ['rank']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        if J==10:
            break
        x.add_row([J+1]+list(I))
    print(x)

def top10_footfalls_ind():

    mycursor.execute('select * from footfalls order by footfalls_india desc')
    L = ['rank']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        if J==10:
            break
        x.add_row([J+1]+list(I))
    print(x)

def top10_footfalls_ovr():

    mycursor.execute('select * from footfalls order by footfalls_overseas desc')
    L = ['rank']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        if J==10:
            break
        x.add_row([J+1]+list(I))
    print(x)

def top10_footfalls_worldwide():

    mycursor.execute('select * from footfalls order by footfalls_worldwide desc')
    L = ['rank']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        if J==10:
            break
        x.add_row([J+1]+list(I))
    print(x)

def clean_hits():

    mycursor.execute(f'''select N.*,
    footfalls_india,footfalls_overseas,footfalls_worldwide 
    from net_gross N, footfalls F where N.film_name=F.film_name 
    and N.verdict in ('Hit','Blockbuster','All Time Blockbuster')
    order by N.verdict''')
    L = ['S.No']
    D={}
    for I in mycursor.description:
        L.append(I[0])
        D[I[0]] = 3
    x = PrettyTable(L)
    x._max_width = D
    for J,I in enumerate(mycursor.fetchall()):
        x.add_row([J+1]+list(I))
    print(x)

def clean_flops():

    mycursor.execute(f'''select N.*,
    footfalls_india,footfalls_overseas,footfalls_worldwide 
    from net_gross N, footfalls F where N.film_name=F.film_name 
    and N.verdict in ('Semi Hit','Flop','Disaster')
    order by N.verdict desc''')
    L = ['S.No']
    D={}
    for I in mycursor.description:
        L.append(I[0])
        D[I[0]] = 3
    x = PrettyTable(L)
    x._max_width = D
    for J,I in enumerate(mycursor.fetchall()):
        x.add_row([J+1]+list(I))
    print(x)

def full_net_gross():

    mycursor.execute('select * from net_gross')
    L = ['S.No']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        x.add_row([J+1]+list(I))
    print(x)

def full_footfalls():

    mycursor.execute('select * from footfalls')
    L = ['S.No']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        x.add_row([J+1]+list(I))
    print(x)

def own_query():
    print('Enter your own query')
    query = input()
    try:
        mycursor.execute(f'{query}')
    except:
        print('Wrong query')
        return
    try:
        L = []
        for I in mycursor.description:
            L.append(I[0])
        x = PrettyTable(L)
        for I in (mycursor.fetchall()):
            x.add_row(list(I))
        print(x)
    except:
        if mycursor.rowcount == 0:
            print('Wrong query')
            return
        print(mycursor.rowcount,'rows affected')
    mydb.commit()

#menu
print('''\nCHOOSE YOUR OPTION
1) Features of net_gross
2) Features of footfalls
3) Add a movie
4) Add many movies
5) Delete movie
6) Update net gross India
7) Update net gross Overseas
8) Update footfalls India
9) Update footfalls Overseas
10) Search movie details
11) Compare two movies 
12) Add coloumn
13) Modify coloumn
14) Delete coloumn
15) Top 10 grossing movies India
16) Top 10 grossing movies Overseas
17) Top 10 grossing movies Worldwide
18) Top 10 footfalls India
19) Top 10 footfalls Overseas
20) Top 10 footfalls Worldwide
21) Show all Clean Hits
22) Show all average/flops 
23) Show full net_gross table
24) Show full footfalls table
25) Genereate your own query
PRESS # KEY TO EXIT
(Note: All the net_gross figures
and footfalls are in CRORES)''')

while True:
    choice = input('\nEnter your choice number : ')
    print()

    if choice == '1':
        desc_net()
    elif choice == '2':
        desc_footfalls()
    elif choice == '3':
        add_movie()
    elif choice == '4':
        add_movies()
    elif choice == '5':
        delete_movie()
    elif choice == '6':
        update_nett_gross_ind()
    elif choice == '7':
        update_nett_gross_ovr()
    elif choice == '8':
        update_footfalls_ind()
    elif choice == '9':
        update_footfalls_ovr()
    elif choice == '10':
        search()
    elif choice == '11':
        compare()
    elif choice == '12':
        add_coloumn()
    elif choice == '13':
        modify_coloumn()
    elif choice == '14':
        delete_coloumn()
    elif choice == '15':
        top10_gross_ind()
    elif choice == '16':
        top10_gross_ovr()
    elif choice == '17':
        top10_gross_worldwide()
    elif choice == '18':
        top10_footfalls_ind()
    elif choice == '19':
        top10_footfalls_ovr()
    elif choice == '20':
        top10_footfalls_worldwide()
    elif choice == '21':
        clean_hits()
    elif choice == '22':
        clean_flops()
    elif choice == '23':
        full_net_gross()
    elif choice == '24':
        full_footfalls()
    elif choice == '25':
        own_query()   
    elif choice=='#':
        raise SystemExit
