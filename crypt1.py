import random
import time
import mysql.connector
from collections import defaultdict


def grouping(args, X):
    args = str(args)
    a = args.count("1")
    #print(a)
    T = random.randint(5 ,2**31-1)
    #T = 6
    x = len(str(args))-a
    if x >= T:
        grouping(args[:x], X)
    else:
        X.append(x)
    if a>=T:
        grouping(args[x:], X)
    else:
        X.append(a)
def rearrange(args, X, Y):
    a = 0
    arg = str(args)
    for i in X:
        Y.append(arg[a:a+i+1])
        a = a+i+1
    for i in Y:
        p = i.count("1")
        x = i[p:]+i[:p]
        i = x

    
def conversion(args1,args2):
    args1 = bin(args1)[2:]
    args2 = bin(args2)[2:]
    LA = []
    LB = []
    AA = []
    BB = []
    Q = []
    grouping(args1,LA)
    grouping(args2,LB)
    rearrange(args1, LB, AA)
    rearrange(args2, LA, BB)
    A1 = "".join(AA)
    B1 = "".join(BB)
    A1 = "0b" + A1
    A1 = int(A1, base= 2)
    #print (A1)
    B1 =  "0b" + B1
    B1 = int(B1, base= 2)
    #print (B1)
    QA = int(A1) ^ int(B1)
    #print('qa: ',QA)
    return QA

def rotate(x,y):
    z=bin(y).count('1')
    v = str(bin(x))[2:]
    vu = v[z:]+v[:z]
    vu =  "0b" + vu
    return int(vu, base= 2)





db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="qwerty1234",
  database="mydatabase"
 
)
mycursor=db.cursor()
# def fun(a):
#     a=5
# b=0
# fun(b)
# print(b)
class Reader:
    def register():
        
        ids=random.randint(0,2**31-1)
        k1=random.randint(0,2**31-1)
        k2=random.randint(0,2**31-1)
        #insert ids,k1,k2 into db
        mycursor.execute('insert into mydatabase.server(ids,k1,k2) values("%d","%d","%d")'%(ids,k1,k2))
        db.commit()
        return ids,k1,k2
    def authenticate(arg):
        mycursor.execute('select k1 from mydatabase.server where ids="%d"'%(arg))
        k1=0
        for x in mycursor.fetchone():
            k1=x
        mycursor.execute('select k2 from mydatabase.server where ids="%d"'%(arg))
        k2=0    
        for x in mycursor.fetchone():
            k2=x
        
        if k1==0:
            print('terminated')
            return 0
        n=random.randint(0,2**31-1)
        a = conversion(k1, k2)^n
        b = conversion(rotate(k1,n), k1^k2)^rotate(conversion(k2,k2^n),k1)
        bbin = str(bin(b))[2:]
        wtb0 = bbin.count("0")
        wtb1 = bbin.count("1")
        hb = int((wtb0+wtb1)/2)
        if wtb1%2==0:
            bu = bbin[hb:]
        else:
            bu = bbin[:hb]
        return a,bu
    def authenticate2(cu,arg,n,bo,b, id):
        mycursor.execute('select k1 from mydatabase.server where ids="%d"'%(arg))
        k1=0
        #print("fetch",mycursor.fetchone())
        for x in mycursor.fetchone():
            k1=x
        mycursor.execute('select k2 from mydatabase.server where ids="%d"'%(arg))  
        k2=0
        #print("fetch",mycursor.fetchone())  
        for x in mycursor.fetchone():
            k2=x
        if k1==0:
            print('Terminated')
            return 0
        print("k1: ", k1)
        print("k2: ", k2)
        print("ids: ", arg)
        k1 = conversion(k1,n)^k2
        k2 = conversion(k2,b)^k1
        print("Updated k1: ", k1)
        print("Updated k2: ", k2)
        c = conversion(conversion(b,k1), conversion(k1,k2^n))^id
        cbin = str(bin(c))[2:]
        wtc0 = cbin.count("0")
        wtc1 = cbin.count("1")
        hc = int((wtc0+wtc1)/2)
        if wtc1%2==0:
                cur = cbin[hc:]
                cor=cbin[:hc]
        else:
                cur = cbin[:hc]
                cor=cbin[hc:]
        ids = conversion(arg, int(n)^int("0b"+bo+cor, base=2))
        print("Updated ids: ", ids)
        if cu==cur:
            print('Tag is legitimate!')
            mycursor.execute('update mydatabase.server set k1="%d", k2="%d",ids="%d" where ids="%d"'%(k1,k2,ids,arg))
            return 0
        else:
            print('tag is illegitmitate')
            return 0
class Tag:
    def __init__(self,arg):
        self.id=0
        self.id=arg
        self.ids=0
        self.k1=0
        self.k2=0
        self.ids,self.k1,self.k2=Reader.register()

        #print(self.ids)
    def authenticate(self):
        start_time=time.time()
        at,but=Reader.authenticate(self.ids)
        #print("at:" , at)
        #print(conversion(self.k1,self.k2))
        #print("but:" , but)
        n = at^conversion(self.k1,self.k2)
        print("n:", n)
        b = conversion(rotate(self.k1,n), self.k1^self.k2)^(rotate(conversion(self.k2,self.k2^n),self.k1))
        bbin = str(bin(b))[2:]
        wtb0 = bbin.count("0")
        wtb1 = bbin.count("1")
        hb = int((wtb0+wtb1)/2)
        if wtb1%2==0:
            bu = bbin[hb:]
            bo=bbin[:hb]
        else:
            bu = bbin[:hb]
            bo=bbin[hb:]
        
        if bu == but:
            print("Reader is authenticated!")
            self.k1 = conversion(self.k1,n)^self.k2
            self.k2 = conversion(self.k2,b)^self.k1
            c = conversion(conversion(b,self.k1), conversion(self.k1,self.k2^n))^self.id
            cbin = str(bin(c))[2:]
            wtc0 = cbin.count("0")
            wtc1 = cbin.count("1")
            hc = int((wtc0+wtc1)/2)
            if wtc1%2==0:
                cu = cbin[hc:]
                co=cbin[:hc]
            else:
                cu = cbin[:hc]
                co=cbin[hc:]
            ids1=self.ids
            self.ids = conversion(self.ids, int(n)^int("0b"+bo+co, base=2))
            Reader.authenticate2(cu,ids1,n,bo,b, self.id)
            print('time taken for authentication protocol: ',time.time()-start_time)
        else:
            print("Reader authentication is terminated...")
user1=Tag(7)
# user2= Tag(9)
# user3 = Tag(10)
# user4 = Tag(11)
# user5 = Tag(2)
user1.authenticate()
# user2.authenticate()
# user3.authenticate()
# user4.authenticate()
# user5.authenticate()