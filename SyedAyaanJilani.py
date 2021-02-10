import mysql.connector
from prettytable import PrettyTable

#to check whether its connected
try:
    mydb=mysql.connector.connect(host='localhost'
    ,user='root',password=input('Enter Password : '))
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
    mycursor.execute('''create table nett_gross
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
def desc(table_name):

    mycursor.execute(f'desc {table_name}')

    L = []
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for I in (mycursor.fetchall()):
        x.add_row(list(I))
    print(x)

def dates():

    date = input('Enter the year : ')

    try: 
        mycursor.execute(f'''select film_name,release_date,verdict 
        from nett_gross where release_date between '{date}-01-01' 
        and '{date}-12-31' ''')
        L = []
        for I in mycursor.description:
            L.append(I[0])
        x = PrettyTable(L)
        for I in (mycursor.fetchall()):
            x.add_row(list(I))
        print(x)
    except:
        print('The year entered is wrong')

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

    mycursor.executemany('insert into nett_gross values(%s,%s,%s,%s,%s,%s)',rec_list1)
    mycursor.executemany('insert into footfalls values(%s,%s,%s,%s,%s,%s)',rec_list2)
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def delete_movie():

    mycursor.execute(f"delete from nett_gross where film_name='{(name:=input('Enter Film Name : '))}'")
    mycursor.execute(f"delete from footfalls where film_name='{name}'")
    if mycursor.rowcount == 0:
        print('Film Not Found')
        return
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def update(table_name,region):

    name = input('Enter Film Name : ')
    L = table_name.split('_')
    table = ''
    for I in L: 
        table = table + ' ' + I.capitalize()
    value = input(f'Enter{table} {region.capitalize()} : ')
    mycursor.execute(f'''update {table_name} set
    {table_name}_{region}={value}
    where film_name='{name}' ''')
    mycursor.execute(f'''update {table_name} set
    {table_name}_worldwide={table_name}_india+{table_name}_overseas
    where film_name='{name}' ''')
    if mycursor.rowcount == 0:
        print('Film not found')
        return
    print(mycursor.rowcount,'rows affected')
    mydb.commit()

def search():

    mycursor.execute(f'''select N.*,
    footfalls_india,footfalls_overseas,footfalls_worldwide 
    from nett_gross N, footfalls F where N.film_name=F.film_name 
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
    from nett_gross N, footfalls F where N.film_name=F.film_name 
    and N.film_name in
    ('{input('Enter Film 1 : ')}','{input('Enter Film 2 : ')}')''')

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
    
def top10(table_name,region):

    mycursor.execute(f'select * from {table_name} order by {table_name}_{region} desc')
    L = ['rank']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        if J==10:
            break
        x.add_row([J+1]+list(I))
    print(x)

def clean(status):
    
    query = f'''select N.film_name,nett_gross_worldwide,
    footfalls_worldwide,N.verdict from nett_gross N, footfalls 
    F where N.film_name=F.film_name and N.verdict in 
    {status} order by N.verdict'''
    if 'Flop' in status:
        mycursor.execute(query + ' desc')
    else:
        mycursor.execute(query)
    L = ['S.No']
    for I in mycursor.description:
        L.append(I[0])
    x = PrettyTable(L)
    for J,I in enumerate(mycursor.fetchall()):
        x.add_row([J+1]+list(I))
    print(x)

def full(table_name):

    mycursor.execute(f'select * from {table_name}')
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
1) Features of nett_gross
2) Features of footfalls
3) Display movies released in a particular year
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
23) Show full nett_gross table
24) Show full footfalls table
25) Genereate your own query
PRESS # KEY TO EXIT
(Note: All the net_gross figures
and footfalls are in CRORES)''')

while True:
    choice = input('\nEnter your choice number : ')
    print()

    if choice == '1':
        desc('nett_gross')
    elif choice == '2':
        desc('footfalls')
    elif choice == '3':
        dates()
    elif choice == '4':
        add_movies()
    elif choice == '5':
        delete_movie()
    elif choice == '6':
        update('nett_gross','india')
    elif choice == '7':
        update('nett_gross','overseas')
    elif choice == '8':
        update('footfalls','india')
    elif choice == '9':
        update('footfalls','overseas')
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
        top10('nett_gross','india')
    elif choice == '16':
        top10('nett_gross','overseas')
    elif choice == '17':
        top10('nett_gross','worldwide')
    elif choice == '18':
        top10('footfalls','india')
    elif choice == '19':
        top10('footfalls','overseas')
    elif choice == '20':
        top10('footfalls','worldwide')
    elif choice == '21':
        clean("('Hit','Blockbuster','All Time Blockbuster')")
    elif choice == '22':
        clean("('Semi Hit','Flop','Disaster')")
    elif choice == '23':
        full('nett_gross')
    elif choice == '24':
        full('footfalls')
    elif choice == '25':
        own_query()   
    elif choice == '#':
        raise SystemExit