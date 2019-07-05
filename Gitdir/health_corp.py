import numpy as np
import sqlite3
conn = sqlite3.connect("health.db")

cur1 = conn.cursor()
cur1.execute("select * from health" )
list1 = cur1.fetchall() #id,date

new = np.array(list1)
u, c = np.unique(new, return_counts=True)
result = dict(zip(u, c))
print("要素,頻度", result)


print(len(result))

for k, v in sorted(result.items(), key=lambda x: -x[1]):
    print(str(k) + ": " + str(v))

health_cop = [k for k, v in sorted(result.items(), key=lambda x: -x[1])]
print(health_cop)

position = dict(zip(health_cop,[i+1 for i in range(len(health_cop))]))
print(position)

def Dicthealth():
    return position

def size():
    return len(position)

def get_pos(x):
    result = position[x]
    return result

print(list1[0])

#NEW = [[t for t in i]for i in list1][3]
FINAL = [tuple([get_pos(t) for t in i]) for i in list1]

print(FINAL)
print(len(FINAL))

#conn.executemany("insert into position values(?,?,?,?,?,?,?)", FINAL)

#cur = conn.cursor()
#cur.execute( "select * from position" )
#list = cur.fetchall()
#print( list )

#conn.commit()
conn.close()
