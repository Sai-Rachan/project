from django.shortcuts import render
from datetime import datetime
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import json
from web3 import Web3, HTTPProvider
import base64

global username, policyList, purchaseList, usersList
global contract, web3

#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Insure.json' #Insurance contract file
    deployed_contract_address = '0x024a545767ccBD7E208E25eedd48b6b0a9cEf43e' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getUsersList():
    global usersList, contract
    usersList = []
    count = contract.functions.getUserCount().call()
    for i in range(0, count):
        user = contract.functions.getUsername(i).call()
        password = contract.functions.getPassword(i).call()
        phone = contract.functions.getPhone(i).call()
        email = contract.functions.getEmail(i).call()
        address = contract.functions.getAddress(i).call()
        usersList.append([user, password, phone, email, address])

def getPolicyList():
    global policyList, contract
    policyList = []
    count = contract.functions.getPolicyCount().call()
    for i in range(0, count):
        policy_id = contract.functions.getPolicyID(i).call()
        name = contract.functions.getPolicyName(i).call()
        insured_amount = contract.functions.getInsuredAmount(i).call()
        purchase_amount = contract.functions.getPurchaseAmount(i).call()
        duration = contract.functions.getDuration(i).call()
        desc = contract.functions.getDescription(i).call()
        provider = contract.functions.getProviderName(i).call()
        policyList.append([policy_id, name, insured_amount, purchase_amount, duration, desc, provider])

def getPurchaseList():
    global purchaseList, contract
    purchaseList = []
    count = contract.functions.getPurchaseCount().call()
    for i in range(0, count):
        purchaser_name = contract.functions.getPurchaserName(i).call()
        insurance_id = contract.functions.getInsuranceID(i).call()
        purchase_date = contract.functions.getPurchaseDate(i).call()
        claims = contract.functions.getClaimDetails(i).call()
        purchaseList.append([purchaser_name, insurance_id, purchase_date, claims])
getUsersList()
getPolicyList()    
getPurchaseList()

def ViewClaimStatus(request):
    if request.method == 'GET':
        global purchaseList, username
        users = request.POST.get('t1', False)
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Purchaser Name</font></th>'
        output+='<th><font size=3 color=black>Insurance ID</font></th>'
        output+='<th><font size=3 color=black>Claim Amount</font></th>'
        output+='<th><font size=3 color=black>Claim Description</font></th>'
        output+='<th><font size=3 color=black>Status</font></th>'
        output+='<th><font size=3 color=black>Claim Request Date</font></th></tr>'
        for i in range(len(purchaseList)):
            plist = purchaseList[i]
            if plist[0] == username:
                status = plist[3]
                if len(status) > 0:
                    status = status.split("\n")
                    for j in range(len(status)):
                        arr = status[j].split(",")
                        if len(arr) > 1:
                            output+='<tr><td><font size=3 color=black>'+plist[0]+'</font></td>'
                            output+='<td><font size=3 color=black>'+plist[1]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[0]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[3]+'</font></td></tr>'                        
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'UserScreen.html', context) 


def GenerateClaimAction(request):
    if request.method == 'POST':
        global username, purchaseList
        amount = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        current_date = str(datetime.now().date())
        for i in range(len(purchaseList)):
            plist = purchaseList[i]
            if plist[0] == username:
                details = plist[3]
                print(str(details)+" "+str(len(details)))
                if len(details) == 0:
                    plist[3] = amount+","+desc+","+"Pending,"+current_date+"\n"
                    contract.functions.updateClaim(i, amount+","+desc+","+"Pending,"+current_date+"\n").transact()
                else:
                    details += amount+","+desc+","+"Pending,"+current_date+"\n"
                    plist[3] = details
                    contract.functions.updateClaim(i, details).transact()
        context= {'data':'Your claim successfully updated in Blockchain'}
        return render(request, 'UserScreen.html', context)            

def GenerateClaim(request):
    if request.method == 'GET':
        return render(request,'GenerateClaim.html', {})

def ViewPolicyAction(request):
    if request.method == 'GET':
        global username, purchaseList
        policy_id = request.GET['policy_id']
        current_date = str(datetime.now().date())
        msg = contract.functions.savePurchase(username, policy_id, current_date, "").transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        purchaseList.append([username, policy_id, current_date, ""])
        context= {'data':'Your insurance purchased ssuccessfully update in Blockchain'}
        return render(request, 'UserScreen.html', context)        

def ViewPolicies(request):
    if request.method == 'GET':
        global policyList, username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Insurance ID</font></th>'
        output+='<th><font size=3 color=black>Policy Name</font></th>'
        output+='<th><font size=3 color=black>Insured Amount</font></th>'
        output+='<th><font size=3 color=black>Purchase Amount</font></th>'
        output+='<th><font size=3 color=black>Policy Duration</font></th>'
        output+='<th><font size=3 color=black>Policy Description</font></th>'
        output+='<th><font size=3 color=black>Insurance Provider</font></th>'
        output+='<th><font size=3 color=black>Purchase Insurance</font></th></tr>'
        for i in range(len(policyList)):
            plist = policyList[i]
            output+='<tr><td><font size=3 color=black>'+plist[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[2]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[3]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[4]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[5]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[6]+'</font></td>'
            output+='<td><a href=\'ViewPolicyAction?policy_id='+plist[0]+'\'><font size=3 color=red>Click Here to Purchase</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'UserScreen.html', context)

def ClaimRequestAction(request):
    if request.method == 'GET':
        global username
        cid = request.GET['cid']
        row = request.GET['row']
        status = request.GET['status']
        global purchaseList
        plist = purchaseList[int(cid)]
        details = plist[3].split("\n")
        output = ""
        for i in range(len(details)):
            if len(details[i].strip()) > 0:
                if i != int(row):
                    arr = details[i].split(",")
                    print(str(arr)+"============"+str(len(arr))+" "+str(i)+" "+str(row)+" "+status)
                    if len(arr) > 1:
                        output += arr[0]+","+arr[1]+","+arr[2]+","+arr[3]+"\n"
                else:
                    arr = details[i].split(",")
                    print(str(arr)+"*************"+str(len(arr))+" "+str(i)+" "+str(row)+" "+status)
                    if len(arr) > 1:
                        output += arr[0]+","+arr[1]+","+status+","+arr[3]+"\n"        
        if len(output) > 0:
            print(output)                        
            plist[3] = output
            contract.functions.updateClaim(int(cid), output).transact()
        context= {'data':'Claim status successfuly updated as '+status}        
        return render(request,'AdminScreen.html', context)        

def ViewClaimsRequest(request):
    if request.method == 'GET':
        global purchaseList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Purchaser Name</font></th>'
        output+='<th><font size=3 color=black>Insurance ID</font></th>'
        output+='<th><font size=3 color=black>Claim Amount</font></th>'
        output+='<th><font size=3 color=black>Claim Description</font></th>'
        output+='<th><font size=3 color=black>Status</font></th>'
        output+='<th><font size=3 color=black>Claim Request Date</font></th>'
        output+='<th><font size=3 color=black>Approved Claim</font></th>'
        output+='<th><font size=3 color=black>Reject Claim</font></th></tr>'
        for i in range(len(purchaseList)):
            plist = purchaseList[i]
            status = plist[3]
            if len(status) > 0:
                status = status.split("\n")
                for j in range(len(status)):
                    if len(status[j].strip()) > 0:
                        arr = status[j].split(",")
                        print(arr)
                        if arr[2] == 'Pending':
                            output+='<tr><td><font size=3 color=black>'+plist[0]+'</font></td>'
                            output+='<td><font size=3 color=black>'+plist[1]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[0]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[3]+'</font></td>'
                            output+='<td><a href=\'ClaimRequestAction?cid='+str(i)+'&row='+str(j)+'&status=Approved\'><font size=3 color=red>Click Here to Approved</font></a></td>'
                            output+='<td><a href=\'ClaimRequestAction?cid='+str(i)+'&row='+str(j)+'&status=Rejected\'><font size=3 color=red>Click Here to Reject</font></a></td></tr>'
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'AdminScreen.html', context) 

def ViewClaimsHistoryAction(request):
    if request.method == 'POST':
        global purchaseList
        username = request.POST.get('t1', False)
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Claim Amount</font></th>'
        output+='<th><font size=3 color=black>Claim Description</font></th>'
        output+='<th><font size=3 color=black>Status</font></th>'
        output+='<th><font size=3 color=black>Claim Date</font></th></tr>'
        for i in range(len(purchaseList)):
            plist = purchaseList[i]
            if plist[0] == username:
                status = plist[3]
                if len(status) > 0:
                    status = status.split("\n")
                    for j in range(len(status)):
                        if len(status[j].strip()) > 0:
                            arr = status[j].split(",")
                            print(arr)
                            output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[2]+'</font></td>'
                            output+='<td><font size=3 color=black>'+arr[3]+'</font></td></tr>'            
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'AdminScreen.html', context)         

def ViewClaimsHistory(request):
    if request.method == 'GET':
        global purchaseList
        output = '<tr><td><font size="3" color="black">Policy&nbsp;Holder</td><td><select name="t1">'
        for i in range(len(purchaseList)):
            plist = purchaseList[i]
            output += '<option value="'+plist[0]+'">'+plist[0]+'</option>'
        output += '</select></td></tr>'
        context= {'data1':output} 
        return render(request,'ViewClaimsHistory.html', context)

def getDescription(insurance_id):
    insured_amount = ""
    purchase_amount = ""
    desc = ""
    provider = ""
    global policyList
    for i in range(len(policyList)):
        plist = policyList[i]
        if plist[0] == insurance_id:
            insured_amount = plist[2]
            purchase_amount = plist[3]
            desc = plist[5]
            provider = plist[6]
            break
    return insured_amount, purchase_amount, desc, provider    

def ViewPurchaseList(request):
    if request.method == 'GET':
        global purchaseList, username
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Purchaser Name</font></th>'
        output+='<th><font size=3 color=black>Policy ID</font></th>'
        output+='<th><font size=3 color=black>Purchase Date</font></th>'
        output+='<th><font size=3 color=black>Insured Amount</font></th>'
        output+='<th><font size=3 color=black>Purchase Amount</font></th>'
        output+='<th><font size=3 color=black>Insurance Description</font></th>'
        output+='<th><font size=3 color=black>Insurance Provider</font></th></tr>'
        for i in range(len(purchaseList)):
            plist = purchaseList[i]
            insured_amount, purchase_amount, desc, provider = getDescription(plist[1])
            output+='<tr><td><font size=3 color=black>'+plist[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+plist[2]+'</font></td>'
            output+='<td><font size=3 color=black>'+insured_amount+'</font></td>'
            output+='<td><font size=3 color=black>'+purchase_amount+'</font></td>'
            output+='<td><font size=3 color=black>'+desc+'</font></td>'
            output+='<td><font size=3 color=black>'+provider+'</font></td></tr>'            
        output += "</table><br/><br/><br/><br/>"
        context= {'data':output}        
        return render(request,'AdminScreen.html', context) 

def AddPolicyAction(request):
    if request.method == 'POST':
        global policyList
        policy_name = request.POST.get('t1', False)
        insured_amount = request.POST.get('t2', False)
        purchase_amount = request.POST.get('t3', False)
        duration = request.POST.get('t4', False)
        description = request.POST.get('t5', False)
        provider = request.POST.get('t6', False)
        policy_id = len(policyList) + 1
        msg = contract.functions.savePolicy(str(policy_id), policy_name, insured_amount, purchase_amount, duration, description, provider).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        policyList.append([str(policy_id), policy_name, insured_amount, purchase_amount, duration, description, provider])
        context= {'data':'New Policy Created with Insurance ID = '+str(policy_id)+'<br/>'+str(tx_receipt)}
        return render(request, 'AdminScreen.html', context)
        
def AddPolicy(request):
    if request.method == 'GET':
        return render(request,'AddPolicy.html', {})

def index(request):
    if request.method == 'GET':
        return render(request,'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})
    
def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def RegisterAction(request):
    if request.method == 'POST':
        global usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        status = "none"
        for i in range(len(usersList)):
            users = usersList[i]
            if username == users[0]:
                status = "exists"
                break
        if status == "none":
            msg = contract.functions.saveUser(username, password, contact, email, address).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            usersList.append([username, password, contact, email, address])
            context= {'data':'Signup Process Completed<br/>'+str(tx_receipt)}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'Register.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        for i in range(len(usersList)):
            ulist = usersList[i]
            user1 = ulist[0]
            pass1 = ulist[1]
            if user1 == username and pass1 == password:
                status = "success"
                break
        if status == 'success':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "UserScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)
        
def AdminLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        if username == 'admin' and password == 'admin':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "AdminScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'AdminLogin.html', context)










        


        
