#import sqlite3
conn = sqlite3.connect("health.db")
cur1 = conn.cursor()
cur1.execute("select * from date_line" )
list1 = cur1.fetchall() #id,date

print(len(list1))

for w in range(len(list1)):  ##change date,usr
    a = list1[w][0]
    b = list1[w][1]

    cur2 = conn.cursor()
    cur2.execute("select * from time_line where user = {0} AND date = ?".format(a), (b,))

    list2 = cur2.fetchall() #id,date,time,sleep,heart

    time_ls = [i[2] for i in list2]
    sleep_ls = [i[3] for i in list2]
    time_dict = dict(zip(time_ls,sleep_ls))

    time_ls.sort()
    min_range = time_ls
    print("最小時間t0: ",min_range[0])

    min_day = int((min_range[0]-15)/5)

    time_ls.reverse()
    max_range = time_ls
    print("最大時間t0: ",max_range[0])

    max_day = int((max_range[0]+15)/5)+1

    if min_day >= 0 and max_day <= 1435:
        time_range = [i*5 for i in range(min_day,max_day)]
    else:
        time_range = [i*5 for i in range(3,max_day)]

    day_dict = dict(zip(time_range,[3 for i in range(len(time_range))]))

    day_dict.update(time_dict)
    print(day_dict)

    new = [(a,b,k,v) for k,v in day_dict.items()]
    print(len(new))

    conn.executemany("insert into sleep values(?,?,?,?)", new)

    cur3 = conn.cursor()
    cur3.execute( "select * from sleep" )
    list = cur3.fetchall()
    print( list )

    conn.commit()
conn.close()
