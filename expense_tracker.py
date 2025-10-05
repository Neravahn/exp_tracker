import pymysql 
 
conn= pymysql.connect (
host ="localhost",
user = "root",
password = "prashant1",
database = "tracker_db"
)

cursor  = conn.cursor()

cursor.execute ("""create table if not exists exp_table(
                id int auto_increment primary key,
                income int default 0,
                expenses int default 0,
                note varchar(100),
                date_time timestamp default current_timestamp
               
)"""
)

print ("operations-- \n" \
"enter (1) to show transactions \n" \
"enter (2) to record transaction \n" \
"enter (3) to calculate interst \n4" \
"enter (4) to clear transaction history" )


var_operations = int(input ("ENTER OPER.NO. :"))

if var_operations == 1:
    cursor.execute( " select * from exp_table;")
    rows = cursor.fetchall()
    if rows:
        print( "ID|INCOME|EXPENSE|NOTE|DATE & TIME"  )
        for row in rows:
            print (row)
    else:
        print ("not transaction to print")
        
elif var_operations == 2:
     var_income = int ( input ( "INCOME:" ))
     var_expense = int ( input ( "EXPENSE:" ))
     var_note = input ( "NOTE(optional):" )
     insert_query = """ insert into exp_table (income, expenses, note)
                   values ( %s, %s, %s)
                    """

     data = (var_income, var_expense, var_note )


     cursor.execute(insert_query,data)
     conn.commit()

     cursor.execute( """ select sum(income) -  sum(expenses) as current_balance from exp_table """)
     current_balance = cursor.fetchone()[0]  

     print ("transaction recorded")
     print ("current balance", current_balance)
    

elif var_operations == 3:
    emi_prin = int ( input ( "Enter the principle amount:"))
    emi_rate = int ( input ( "Enter emi rate : "))
    emi_time = int ( input ("Enter time period in months:"))
    emi_interest = ( emi_prin * emi_rate * emi_time ) / 100
    print ( "interest :", emi_interest)

elif var_operations ==4:
    cursor.execute("delete from exp_table")
    cursor.execute("alter table exp_table auto_increment = 1")
    print ( "--TRANSACTION HISTORY CLEARED--")

else:
    print (" wrong operation ")



cursor.close()
conn.close()

