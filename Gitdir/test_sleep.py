#import sqlite3
conn = sqlite3.connect("health.db")

cur5 = conn.cursor()
cur5.execute("select * from date_line" )
list5 = cur5.fetchall() #id,date

print(len(list5))

for w in range(len(list5)):  ##change date,usr
    a = list5[w][0]
    b = list5[w][1]

    cur1 = conn.cursor()
    cur1.execute("select * from sleep where user = {0} AND date = ?".format(a),(b,))
    list1 = cur1.fetchall() #id,date

    heart_array = [] #usr,date,time,heart
    for i in list1:
#       print(i[2])
        cur3 = conn.cursor()
        cur3.execute("select * from heart where user = {0} AND time = {1} AND date = ?".format(a,i[2]), (b,))
        list3 = cur3.fetchall()
        if list3 != []:
            heart_array.append(list3[0])

    print("心臓時間帯数",len(heart_array))

    #############
    ###DICT HEART
    heart_dict = dict(zip([t[2] for t in heart_array],[t[3] for t in heart_array]))
    print("HEART",len(heart_dict))


    print(heart_dict)

    heart_time = [t[2] for t in heart_array]
    min_heart = min(heart_time)
    max_heart = max(heart_time)

    print("心臓最小時間: ",min_heart)
    print("心臓最大時間: ",max_heart)

    max_sleep = max_heart
    min_sleep = min_heart

    cur4 = conn.cursor()
    cur4.execute("select * from sleep where user = {0} AND time BETWEEN {1} and {2} AND date = ?".format(a,min_sleep,max_sleep),(b,))
    list4 = cur4.fetchall()

    print(list4) #target sleep

    ###############
    #######DICT SLEEP
    sleep_dict = dict(zip([t[2] for t in list4],[t[3] for t in list4]))
    print(sleep_dict)
    print("SLEEP",len(sleep_dict))


    ############
    FINAL = []
    if len(heart_dict) == len(sleep_dict):
        new_array = [(heart_array[i][3],list4[i][3]) for i in range(len(sleep_dict))] 
        #0:heart , 1:sleep
        print(new_array)
        for i in range(3,len(new_array)-3):
            goal = (new_array[i-3][0],new_array[i-2][0],new_array[i-1][0],new_array[i][1],new_array[i+1][0],new_array[i+2][0],new_array[i+3][0])
            print(goal)
            FINAL.append(goal)
    elif len(heart_dict) < len(sleep_dict):
         ls = [k for k,v in sleep_dict.items() if k not in heart_dict.keys()]
         for t in ls:
             del sleep_dict[t]
         
         print(len(heart_dict) , len(sleep_dict))
         old_array = [(heart_array[i][3],list4[i][3]) for i in range(len(sleep_dict))]
         #0:heart , 1:sleep
         print(old_array)
         for i in range(3,len(old_array)-3):
             goal2 = (old_array[i-3][0],old_array[i-2][0],old_array[i-1][0],old_array[i][1],old_array[i+1][0],old_array[i+2][0],old_array[i+3][0])
             print(goal2)
             FINAL.append(goal2)
         
    print(FINAL)

    conn.executemany("insert into health values(?,?,?,?,?,?,?)", FINAL)

    cur = conn.cursor()
    cur.execute( "select * from health" )
    list = cur.fetchall()
    print( list )

    conn.commit()
conn.close()
