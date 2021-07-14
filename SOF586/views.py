from django.shortcuts import render
from django.http import JsonResponse
import MySQLdb as sql
import datetime
import json




def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def menu(request):
    con = sql.connect(host = 'analytiq.co.kr', user = 'sof586', database = 'sof586', charset = 'utf8')
    cursor = con.cursor()
    #Get menu prices
    cursor.execute("select * from menu_items")
    prices = {c[1]:int(c[2]) for c in cursor.fetchall()}
    con.close()
    return render(request, 'menu.html', prices)

def place_order(request):
    cart = json.loads(request.GET.get('cart'))
    customer = json.loads(request.GET.get('customer'))
    con = sql.connect(host = 'analytiq.co.kr', user = 'sof586', database = 'sof586', charset = 'utf8')
    cursor = con.cursor()
    #Get menu item to id map
    cursor.execute("select menu_name, id from menu_items")
    idmap = {c[0]:c[1] for c in cursor.fetchall()}
    #Get Customer ID
    nres = cursor.execute("select id from customer where name = %s", [customer['name']])
    if nres == 0:
        #If customer is not found, add Customer Information
        cursor.execute("select max(id)+1 from customer")
        customer_id = cursor.fetchone()[0]
        cursor.execute("insert into customer values (%s,%s,%s,%s)",[customer_id, customer['name'], customer['address'], customer['phone']])
    else: #If customer is found, update address and phone
        #Update Address Information
        customer_id = cursor.fetchone()[0]
        cursor.execute("update customer set address = %s, phone_no = %s where id = %s", [customer['name'], customer['phone'], customer_id])
    #Insert orders into orders table
    cursor.execute("select max(id)+1 from orders")
    order_id = cursor.fetchone()[0]
    cursor.execute("insert into orders values (%s,%s,%s)",[order_id, customer_id, datetime.datetime.now()])
    for item in cart:
        cursor.execute("insert into order_items values (%s,%s,%s)",[order_id, idmap[item], cart[item]])
    con.commit()
    con.close()
    return JsonResponse({'msg':'Order submited successfully'})

def shopper_history_report(request):
    con = sql.connect(host = 'analytiq.co.kr', user = 'sof586', database = 'sof586', charset = 'utf8')
    cursor = con.cursor()
    cursor.execute("""select name, order_id, order_time, menu_name, quantity from orders 
    inner join customer on orders.customer_id = customer.id 
    inner join order_items on orders.id = order_items.order_id
    inner join menu_items on order_items.item_id = menu_items.id""")
    history = cursor.fetchall()
    con.close()
    history_dic = {}
    for name, order_id, order_time, menu_name, quantity in history:
        if name not in history_dic: history_dic[name] = {}
        if order_id not in history_dic[name]: history_dic[name][order_id]={'order_time':order_time.strftime("%Y-%m-%d %H:%M"), 'items':[]}
        history_dic[name][order_id]['items'].append(f'{menu_name} ({quantity})')
    print(history_dic)
    return render(request, 'shopper_history.html', {'history':history_dic})