from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime
import os
import json
from web3 import Web3, HTTPProvider
from datetime import datetime

global uname, details, owner, car_no, amount

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CarRental.json' #CarRental Contract contract code
    deployed_contract_address = '0xd374Cb05bd6187D6cF905D7bBD85f2b704fBDD29' #hash address to access Banking Contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'adduser':
        details = contract.functions.getUsers().call()
    if contract_type == 'addcars':
        details = contract.functions.getCars().call()
    if contract_type == 'rentals':
        details = contract.functions.getRentals().call()    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CarRental.json' #CarRental Contract file
    deployed_contract_address = '0xd374Cb05bd6187D6cF905D7bBD85f2b704fBDD29' #Banking contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'adduser':
        details+=currentData
        msg = contract.functions.addUsers(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'addcars':
        details+=currentData
        msg = contract.functions.addCars(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'rentals':
        details+=currentData
        msg = contract.functions.setRentals(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def updateBlockChain(currentData):
    global details
    global contract
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CarRental.json' #CarRental Contract file
    deployed_contract_address = '0xd374Cb05bd6187D6cF905D7bBD85f2b704fBDD29' #Banking contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    msg = contract.functions.setRentals(currentData).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)      

def OwnerLogin(request):
    if request.method == 'GET':
       return render(request, 'OwnerLogin.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        usertype = request.POST.get('t6', False)
        record = 'none'
        readDetails("adduser")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == username:
                record = username+" already exists"
                break
        if record == 'none':
            data = username+"#"+password+"#"+contact+"#"+email+"#"+address+"#"+usertype+"\n"
            saveDataBlockChain(data,"adduser")
            context= {'data':'Signup process completed and record saved in Blockchain'}
            return render(request, 'Signup.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'Signup.html', context)           

def UserLoginAction(request):
    if request.method == 'POST':
        global uname, details
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        readDetails("adduser")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == username and arr[1] == password and arr[5] == 'Rented User':
                status = 'success'
                uname = username
                break
        if status == 'success':
            context= {'data':"Welcome "+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)

def OwnerLoginAction(request):
    if request.method == 'POST':
        global uname, details
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        readDetails("adduser")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == username and arr[1] == password and arr[5] == 'Owner':
                status = 'success'
                uname = username
                break
        if status == 'success':
            context= {'data':"Welcome "+username}
            return render(request, 'OwnerScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'OwnerLogin.html', context)         

def AddCars(request):
    if request.method == 'GET':
        return render(request, 'AddCars.html', {})

def AddCarsAction(request):
    if request.method == 'POST':
        global uname, details
        carname = request.POST.get('t1', False)
        carno = request.POST.get('t2', False)
        vehicle_details = request.POST.get('t3', False)
        rent = request.POST.get('t4', False)
        myfile = request.FILES['t5'].read()
        fname = request.FILES['t5'].name
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        with open("CarSharingApp/static/cars/"+fname, "wb") as file:
            file.write(myfile)
        file.close()
        data = uname+"#"+carname+"#"+carno+"#"+vehicle_details+"#"+rent+"#"+dt_string+"#"+fname+"\n"
        saveDataBlockChain(data,"addcars")
        context= {'data':'Rented car details added to Blockchain'}
        return render(request, 'AddCars.html', context)
        
def ViewBookedHistory(request):
    if request.method == 'GET':
        global uname, details
        output = '<table border=1 align=center width=100%>'
        font = '<font size="3" color="black">'
        arr = ['Rented ID', 'Username', 'Car Owner Name', 'Car No', 'Rent Date', 'Total Rented Days', 'Amount Paid', 'Card No', 'CVV No', 'Status']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails("rentals")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[2] == uname:
                output += "<tr><td>"+font+arr[0]+"</td>"
                output += "<td>"+font+arr[1]+"</td>"
                output += "<td>"+font+arr[2]+"</td>"
                output += "<td>"+font+arr[3]+"</td>"
                output += "<td>"+font+arr[4]+"</td>"
                output += "<td>"+font+arr[5]+"</td>"
                output += "<td>"+font+arr[6]+"</td>"
                output += "<td>"+font+arr[7]+"</td>"
                output += "<td>"+font+arr[8]+"</td>"
                output += "<td>"+font+arr[9]+"</td></tr>"
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request, 'OwnerScreen.html', context)    

def checkStatus(car_no, rows):
    status = "none"
    global details
    for i in range(len(rows)-1):
        arr = rows[i].split("#")
        if arr[3] == car_no and arr[9] == 'Booked':
            status = "not available"
            break
    return status

def getContact(owner, rows):
    contact = "none"
    for i in range(len(rows)-1):
        arr = rows[i].split("#")
        if arr[0] == owner:
            contact = arr[2]
            break
    return contact
            

def BookCarsAction(request):
    if request.method == 'GET':
        global uname, owner, car_no, amount
        owner = request.GET.get('t1', False)
        car_no = request.GET.get('t2', False)
        amount = request.GET.get('t3', False)
        return render(request, 'Payment.html', {})

def PaymentAction(request):
    if request.method == 'POST':
        global uname, owner, car_no, amount
        rented_days = request.POST.get('t1', False)
        cardno = request.POST.get('t2', False)
        cvvno = request.POST.get('t3', False)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        total_amount = float(rented_days) * float(amount)
        readDetails("rentals")
        rentals = details.split("\n")
        rented_id = len(rentals)
        data = str(rented_id)+"#"+uname+"#"+owner+"#"+car_no+"#"+dt_string+"#"+rented_days+"#"+str(total_amount)+"#"+cardno+"#"+cvvno+"#Booked\n"
        saveDataBlockChain(data,"rentals")
        context= {'data':'Car Booking Completed with Booking ID = '+str(rented_id)}
        return render(request, 'UserScreen.html', context)        
        

def BookCars(request):
    if request.method == 'GET':
        global uname, details
        output = '<table border=1 align=center width=100%>'
        font = '<font size="3" color="black">'
        arr = ['Owner Name', 'Contact No', 'Car Brand Name', 'Car No', 'Car Details', 'Rent Per Day', 'Car Added Date', 'Car Image', 'Book Car']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails("adduser")
        users = details.split("\n")
        readDetails("rentals")
        rentals = details.split("\n")
        readDetails("addcars")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            contact_no = getContact(arr[0], users)
            available = checkStatus(arr[2], rentals)
            if available == "none":
                output += "<tr><td>"+font+arr[0]+"</td>"
                output += "<td>"+font+contact_no+"</td>"
                output += "<td>"+font+arr[1]+"</td>"
                output += "<td>"+font+arr[2]+"</td>"
                output += "<td>"+font+arr[3]+"</td>"
                output += "<td>"+font+arr[4]+"</td>"
                output += "<td>"+font+arr[5]+"</td>"
                output+='<td><img src=static/cars/'+arr[6]+'  width=150 height=150></img></td>'
                output+='<td><a href=\'BookCarsAction?t1='+arr[0]+'&t2='+arr[2]+'&t3='+arr[4]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request, 'UserScreen.html', context)    
    
    
def ViewHistory(request):
    if request.method == 'GET':
        global uname, details
        output = '<table border=1 align=center width=100%>'
        font = '<font size="3" color="black">'
        arr = ['Rented ID', 'Username', 'Car Owner Name', 'Car No', 'Rent Date', 'Total Rented Days', 'Amount Paid', 'Card No', 'CVV No', 'Status']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails("rentals")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[1] == uname:
                output += "<tr><td>"+font+arr[0]+"</td>"
                output += "<td>"+font+arr[1]+"</td>"
                output += "<td>"+font+arr[2]+"</td>"
                output += "<td>"+font+arr[3]+"</td>"
                output += "<td>"+font+arr[4]+"</td>"
                output += "<td>"+font+arr[5]+"</td>"
                output += "<td>"+font+arr[6]+"</td>"
                output += "<td>"+font+arr[7]+"</td>"
                output += "<td>"+font+arr[8]+"</td>"
                output += "<td>"+font+arr[9]+"</td></tr>"
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request, 'UserScreen.html', context)       

def ReleasedBookCars(request):
    if request.method == 'GET':
        global uname, details
        output = '<tr><td><font size="" color="black">Choose&nbsp;Booking&nbsp;ID</b></td><td><select name="t1">'
        readDetails("rentals")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[1] == uname and arr[9] == 'Booked':
                output += '<option value="'+arr[0]+'">'+arr[0]+'</option>'
        output += '</select></td></tr>'
        context= {'data1':output}        
        return render(request, 'ReleasedBookCars.html', context)

def ReleasedBookCarsAction(request):
    if request.method == 'POST':
        global uname
        rented_id = request.POST.get('t1', False)
        readDetails("rentals")
        rows = details.split("\n")
        data = ""
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            exp = arr[0].strip() != rented_id.strip()
            print(str(arr)+" "+arr[0]+" ==== "+rented_id+" == "+str(exp))
            if arr[0].strip() != rented_id.strip():
                data += rows[i]+"\n"
            else:
                data += arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+arr[4]+"#"+arr[5]+"#"+arr[6]+"#"+arr[7]+"#"+arr[8]+"#Released\n"
                break
        updateBlockChain(data)
        context= {'data':'Car Releasing Completed with Booking ID = '+str(rented_id)}
        return render(request, 'UserScreen.html', context)         
                
        


        
    
