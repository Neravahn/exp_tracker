import pymysql 
import matplotlib.pyplot as plt
import pandas as pd
 
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


while True:

    try:
        class exit(Exception):
            pass
    
        print ("operations-- \n" \
        "enter (show) to show transactions\n"\
        "enter (record) to record transaction \n" \
        "enter (interest) to calcualte interest\n"\
        "enter (clear) to clear transaction history\n"\
        "enter (graph) to see the savings graph\n" \
        "enter (exit) to exit")


        var_operations = input ("ENTER OPER.NO. :")
        while True:
            if var_operations.lower() == "show":
                
                cursor.execute("""update exp_table set savings = income - expenses""")
                conn.commit()
                cursor.execute("""select id, income, expenses, note, savings, date_time from exp_table""")
                data_trn = cursor.fetchall()
                df = pd.DataFrame(data_trn, columns = ["ID", "INCOME", "EXEPENSE", "NOTE", "SAVINGS", "DATE & TIME"])
                print(df)
                var = input("Enter 'Back' for main menu:")
                if var.lower() == "back":
                    break

            elif var_operations.lower() == "record":
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
                var = input("Enter 'Back' for main menu:")
                if var.lower() == "back":
                    break
                

            elif var_operations.lower() == "interest":
                emi_prin = int ( input ( "Enter the principle amount:"))
                emi_rate = int ( input ( "Enter emi rate : "))
                emi_time = int ( input ("Enter time period in months:"))
                emi_interest = ( emi_prin * emi_rate * emi_time ) / 100
                print ( "interest :", emi_interest)
                var = input("Enter 'Back' for main menu:")
                if var.lower() == "back":
                    break

            elif var_operations.lower() == "clear":
                cursor.execute("delete from exp_table")
                cursor.execute("alter table exp_table auto_increment = 1")
                print ( "--TRANSACTION HISTORY CLEARED--")
                var = input("Enter 'Back' for main menu:")
                if var.lower() == "back":
                    break

            elif var_operations.lower() == "graph":
                cursor.execute("""select savings from exp_table """)
                y = [row[0] for row in cursor.fetchall()]
                cursor.execute("""select id from exp_table""")
                x = [row[0] for row in cursor.fetchall()]
                plt.plot(x, y)
                plt.show()
                var = input("Enter 'Back' for main menu:")
                if var.lower() == "back":
                    break
            elif var_operations:
                raise exit("success")


            
            else:
                print (" wrong operation ")
    
    except ValueError:
        print ("You have a value error")
    except IndexError:
        print ("You have a index error")
    


cursor.close()
conn.close()

