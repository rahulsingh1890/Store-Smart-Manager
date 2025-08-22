import mysql.connector
def conctn():
    global mydb
    try:
        userName = input(" ENTER MYSQL SERVER'S USERNAME : ")
        paSSword = input(" ENTER MYSQL SERVER'S PASSWORD : ")
        mydb=mysql.connector.connect(host="localhost",user=userName,passwd=paSSword)
    except:
        print("INCORRECT USERNAME OR PASSWORD, TRY AGAIN")
        conctn()
conctn()
dbcursor=mydb.cursor()
dbcursor.execute("create database if not exists mydb")
dbcursor.execute("use mydb")
dbcursor.execute("show tables")
a=0
for i in dbcursor:
    if i==('item',):
        a=1
if a==0:
    dbcursor.execute("CREATE TABLE item (ID int not NULL primary key ,Product_Name varchar(50) not NULL , stock int not NULL,cp float not NULL,sp float not NULL, vendor varchar(50) ,expiry_date int , position varchar(50)) ")
    mydb.commit()


def add():
    try:
        n=input("ENTER PRODUCT NAME:")
        st=int(input("ENTER NUMBER OF PRODUCTS TO BE ADDED:"))
        c=round(float(input("ENTER COST PER PRODUCT:")),2)
        s=round(float(input("ENTER SALE PRICE PER PRODUCT:")),2)
        v=input("ENTER VENDOR:")
        while True:
            exp=input("ENTER EXPIRY DATE YYYYMMDD n IF NO EXPIRY DATE:")
            a1=0
            if exp in "nN":
                a1=1
                break
            else:
                a=checkdate(exp)
                if a=="invalid":
                    print("PLEASE WRITE A VALID DATE")
                elif a=="valid":
                    break
        p=input("ENTER POSITION OF THESE ITEMS:")
        while True:
            id1=int(input("ENTER UNIQUE CODE/ID FOR THESE ITEMS:"))
            a=checkunqid(id1)
            if a=="valid":
                break
        if a1==0:
            t=(id1,n,st,c,s,v,exp,p)
            dbcursor.execute("insert into item values(%s,%s,%s,%s,%s,%s,%s,%s)",t)
        elif a1==1:
            t=(id1,n,st,c,s,v,p)
            dbcursor.execute("insert into item values(%s,%s,%s,%s,%s,%s,null,%s)",t)
        mydb.commit()
        print("SUCCESSFULLY ADDED")
    except:
        print("ERROR GENERATED ,TRY AGAIN")
        add()


def checkdate(d):
	year=d[0:4]
	month=d[4:6]
	date=d[6:8]
	a=0
	if date=="00":
		a=1
	if int(month)>12:
		a=1
	if int(date)>31:
		a=1
	if month in ["04","06","09","11"]:
		if int(date)>30:
			a=1
	elif month =="02":
		if int(year)%4==0:
			if int(date)>29:
				a=1
		else:
			if int(date)>28:
				a=1
	if a==0:
		return "valid"
	elif a==1:
		return "invalid"


def search():
    l=[]
    d1=D
    while True:
        if d1[-2:0]=="32":
            d1=str(int(d1)+68)
        d1=str(int(d1)+1)
        a=checkdate(d1)
        if a=="valid":
            l.append(int(d1))
        if len(l)==7:
            break
    print(" ID , PRODUCT NAME , STOCK , COST PRICE , SELLING PRICE , VENDOR , EXPIRY DATE , POSITION ")
    a=0
    for i in l:
        dbcursor.execute("select * from item where expiry_date=%s",(i,))
        for j in dbcursor:
            print(j)
            a+=1
    if a==0:
        print("NONE OF THE PRODUCTS EXPIRING IN NEXT 7 DAYS")


def checkunqid(q):
    dbcursor.execute("select * from item where ID=%s",(q,))
    a=0
    for i in dbcursor:
        print(i)
        a+=1
    if a==0:
        return "valid"
    else:
        print("UNIQUE ID ALREADY USED")
        return "invalid"


def bill():
    try:
        global p
        cn=input("ENTER CUSTOMER NAME:")
        a=int(input("ENTER THE NUMBER OF DISTINCT ITEMS:"))
        l=[["CUSTOMER NAME:",cn],["S.No.","Product name"+" "*18,"units","price"]]
        bil=0
        for i in range(a):
            b=int(input("ENTER THE UNIQUE CODE OF THE ITEM:"))
            c=int(input("ENTER THE NUMBER OF SUCH ITEMS BOUGHT:"))
            dbcursor.execute("select * from item where ID=%s",(b,))
            for j in dbcursor:
                st=j[2]
                p+=(j[4]-j[3])*c
                bil+=j[4]*c
                if st-c==0:
                    dbcursor.execute("delete from item where ID=%s",(b,))
                elif st>c:
                    dbcursor.execute("update item set stock=%s where ID=%s",(st-c,b))
                else:
                    print("OUT OF STOCK, ",st,"IN STOCK")
                    bill()
                    break
                l.append([forma(i+1,5,"right"),forma(j[1],30,"right"),forma(c,3,"left"),"₹",forma(j[4]*c,5,"left")])
        mydb.commit()
        l.append([forma("net:",38,"right"),"₹",bil])
        dis=input("enter n if no discount ,pd for percentage discount in total ,d for rupees discount in total:")
        disc=0
        if dis in"dD":
        	disc=int(input("enter the discount amount:"))
        elif dis =="pd" or dis=="PD":
        	pd=int(input("enter the percentage discount:"))
        	disc=((pd*bil)/100)
        l.append([forma("discount:",38,"right"),"₹",disc])
        bil=bil-disc
        l.append([forma("net payable amount:",38,"right"),bil])
        for i in l:
            	for j in i:
            		print(j,end="  ")
            	print("\n")
            	
    except:
        print("ERROR GENERATED , TRY AGAIN")
        bill()


def forma(a,l,t):
	a=str(a)
	b=l-len(a)
	if t=="left":
		return b*" "+a
	elif t=="right":
		if l>len(a):
			return a+" "*b
		else:
			return a[0:l]


D=""
p=0
while True:
    a=input("ENTER u TO UPDATE,b TO GENERATE BILL,p TO SEE TODAYS PROFIT,s TO SEE THE ITEMS EXPIRING IN NEXT 7 DAYS, st TO STOP THE PROGRAM:")
    from datetime import date
    d=date.today()
    d=str(d)
    d=d[0:4]+d[5:7]+d[8:10]
    #d=todays date
    if d!=D:
	    p=0
	    D=d
	    #D=Previously saved date
    if a.isalpha():
	    a=a.lower()
    if a=="u":
	    add()
    elif a=="b":
	    bill()
	    print("bill")
    elif a=="p":
	    print(p)
    elif a=="s":
	    search()
    elif a=="st":
	    break
