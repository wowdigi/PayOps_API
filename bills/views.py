import json
from django.shortcuts import render
from django.conf import settings
import requests
from urllib.parse import urlencode
import urllib.parse as urlparse
import json
import datetime
import requests
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from baxi_api.geekops import geekops
from baxi_api.geekops_misc import GenerateReference
from .forms import *
from Betremit_API.providusAPI.geekops import Remit
from accounts.models import Transaction
from django.contrib.auth.models import User
from preauth.balance_auth import authenticate_balance
from preauth.get_balance import balance
from django.http import Http404
from preauth.verifypin import pin_auth
from accounts.models import CustomUser as User
import json
import logging
import os
from rave_python import Rave
# Create your views here.

with open('/home/nate/env_var.json','r') as json_file:
    env_var = json.load(json_file)



def PayHomeView(request):

    try:
        user_url = request.session['user_url']
       
        if user_url:
            userBalance = balance(
                user_url)
            username = request.session['username']
            print(username)
            return render(request, 'bills/cashout.html', {'account_balance': userBalance, 'email': username})

        
    except:
        # print(request.session['first_name'])
        # raise Http404("The requested Page doesnt Exist")
        
        return HttpResponse("<h1>You Dont Have Permissions to View this Page</h1>")


class SuccessPageView(TemplateView):
    template_name = 'bills/trans_success.html'


class ErrorPageView(TemplateView):
    template_name = 'trans_failure.html'


def CreatePINView(request):
    return render(request, 'accounts/create_pin.html', {})

# class OtpView(TemplateView):
#     template_name = 'verify_otp.html'


# def BankTransferView(request):
#     try:
#         user_url = request.session['user_url']
#     except:
#         return HttpResponse("Your Session has expired")

#     if request.method == "POST":
        
#         form = NIPTransferForm(request.POST)
#         ref = GenerateReference()
#         ##logging.info("Reference Generated: {},\n Confirming Valid form data was supplied".format(ref))
#         if form.is_valid():
#             ##logging.info("Bank Transactions Details Valid")
#             form = form.cleaned_data
#             transactionAmount = form['Transfer_Amount']
#             narration = form['narration']
#             account_number = form['Account_Number']
#             beneficiary_bank = form['beneficiary_Bank']
#             transaction_pin = form['transaction_Pin']
#             remit = Remit()
#             user_account = {"accountNumber": str(account_number),
#                             "beneficiaryBank": str(beneficiary_bank),
#                             "userName": env_var["PROVIDUS_USERNAME"] ,
#                             "password": env_var["PROVIDUS_PASSWORD"]}
#             ##logging.info("Validating User Account Details: {} ".format(user_account))
#             response = remit.NipTransfer.getNipAccount(user_account)

#             try:
#                 response_name = response['data']['accountName']
#                 #logging.info("User Account Details Valid")
#             except:
#                 #logging.warning("User Account Details Invalid")
#                 return HttpResponse('Couldnt Get Account Name')

#             beneficiary_Name = str(response_name)
#             transactionRef = str(ref)
#             currencyCode = 'NGN'
#             sourceAccountName = env_var["PROVIDUS_ACCOUNT_SOURCE_NAME"]
#             userName = env_var["PROVIDUS_USERNAME"]
#             password = env_var["PROVIDUS_PASSWORD"]
#             payload = {
#                 'beneficiaryAccountName': beneficiary_Name,
#                 'transactionAmount': transactionAmount,
#                 'currencyCode': currencyCode,
#                 'narration': narration,
#                 'sourceAccountName': sourceAccountName,
#                 'beneficiaryAccountNumber': account_number,
#                 'beneficiaryBank': beneficiary_bank,
#                 'transactionReference': transactionRef,
#                 'userName': userName,
#                 'password': password,

#             }
#             user_pin = request.session['transaction_Pin']
#             if pin_auth(user_pin, transaction_pin):
#                 user_url = request.session['user_url']
#                 has_EnoughBalance = authenticate_balance(
#                     user_url, transaction_amount=float(transactionAmount))
#                 #logging.info("User Pin Authenticated")

#                 if has_EnoughBalance:
#                     #logging.info("User has enough Balance, Proceeding to make Transaction")
#                     response = remit.NipTransfer.nipFundTransfer(payload)

#                     if response['data']['responseCode'] == '00':
#                         #logging.info("Transaction Successful")
#                         customer = User.objects.get(
#                             email=request.session['email'])
#                         transaction = Transaction(beneficiary_AccountName=beneficiary_Name,
#                                                   transaction_Amount=transactionAmount,
#                                                   transaction_Status=True,
#                                                   narration=narration,
#                                                   beneficiary_Bank=beneficiary_bank,
#                                                   customer=customer,
#                                                   transaction_Ref=transactionRef)
#                         transaction.save()
#                         redirect_url = request.session['profile_url']
#                         return render(request, 'bills/trans_success.html', {'beneficiaryAccountName': beneficiary_Name,
#                                                                             'transactionAmount': transactionAmount, 'redirect_url': redirect_url})

#                     else:
#                         redirect_url = request.session['profile_url']
#                         return redirect('failure', {'beneficiaryAccountName': beneficiary_Name,
#                                         'transactionAmount': transactionAmount, 'redirect_url': redirect_url})
#                 #logging.info("Insufficient Balance")
#                 return HttpResponse('Insufficient Balance')
#             #logging.info("Invalid Transaction Pin")    
#             return HttpResponse('Incorrect Transaction Pin')

#     form = NIPTransferForm()
#     user_url = request.session['user_url']
#     userBalance = balance(
#         user_url)
#     username = request.session['username']
#     return render(request, 'bills/niptransfer.html', {'form': form, 'account_balance': userBalance, 'email': username})


def BankTransferView(request):
    try:
         user_url = request.session['user_url']
    except:
         return HttpResponse("Your Session has expired")

    if request.method == "POST":

        form = NIPTransferForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            ref = GenerateReference()
            rave = Rave("FLWPUBK-a2b68185cfc78a9cc75bad82996ebcc1-X", "FLWSECK-65d0803f4ff317c972e41817209ca4fe-X",usingEnv = False)
            transactionAmount = form['Transfer_Amount']
            narration = form['narration']
            account_number = form['Account_Number']
            beneficiary_bank = form['beneficiary_Bank']
            transaction_pin = form['transaction_Pin']

            details = {
                        "account_number": account_number,
                        "account_bank": beneficiary_bank,
                        }
            url = "https://api.flutterwave.com/v3/accounts/resolve"
            headers = {"Content-Type": "application/json","Authorization": "Bearer FLWSECK-65d0803f4ff317c972e41817209ca4fe-X"}
            response = requests.post(url,json=details,headers=headers)
            beneficiary_name = response.json()['data']['account_name']

            details = {
                "account_bank": beneficiary_bank,
                "account_number": account_number,
                "amount": int(transactionAmount),
                "narration": narration,
                "currency": "NGN",
                "reference": ref,
                "beneficiary_name": beneficiary_name
            }
            user_pin = request.session['transaction_Pin']
            if pin_auth(user_pin, transaction_pin):
                    user_url = request.session['user_url']
                    has_EnoughBalance = authenticate_balance(
                        user_url, transaction_amount=float(transactionAmount))

                    if has_EnoughBalance:
                        url = 'https://api.flutterwave.com/v3/transfers'
                        headers = {"Content-Type": "application/json","Authorization": "Bearer FLWSECK-65d0803f4ff317c972e41817209ca4fe-X"}
                        response = requests.post(url,json=details,headers=headers)
                        res = response.json()
                        if res['status'] == 'success':
                            customer = User.objects.get(
                                            email=request.session['email'])
                            beneficiary_Name = res['data']['full_name']
                            transaction = Transaction(beneficiary_AccountName=beneficiary_Name,
                                                    transaction_Amount=transactionAmount,
                                                    transaction_Status=True,
                                                    narration=narration,
                                                    beneficiary_Bank=beneficiary_bank,
                                                    customer=customer,
                                                    transaction_Ref=ref)
                            transaction.save()
                            redirect_url = request.session['profile_url']
                            return render(request, 'bills/trans_success.html', {'beneficiaryAccountName': beneficiary_Name,
                                                                                'transactionAmount': transactionAmount, 'redirect_url': redirect_url})

                        else:
                            redirect_url = request.session['profile_url']
                            return redirect('failure', {'beneficiaryAccountName': beneficiary_Name,
                                            'transactionAmount': transactionAmount, 'redirect_url': redirect_url})
    
    form = NIPTransferForm()
    user_url = request.session['user_url']
    userBalance = balance(
        user_url)
    username = request.session['username']
    return render(request, 'bills/niptransfer.html', {'form': form, 'account_balance': userBalance, 'email': username})


def AirtimeView(request):
    try:
        user_url = request.session['user_url']
    except:
        return HttpResponse("Your Session has expired")

    user_url = request.session['user_url']

    #logging.info("Airtime Transaction Initiated.......")

    geekops = geekops(env_var["BAXI_DEV_API_KEY"])
#     agentId = env_var["BAXI_DEV_AGENT_ID"]
    agentId = 205
    agentReference = str(GenerateReference())
    user_url = request.session['user_url']
    userBalance = balance(
        user_url)

    username = request.session['username']
    if request.method == 'POST':
        #logging.info("Form Submission Validation......")
        # print(request.session['user_id'])
        form = AirtimePurchaseForm(request.POST)
        if form.is_valid():
           
            service_type = form.cleaned_data['service_type']
            amount = form.cleaned_data['amount']
            phone = form.cleaned_data['phone']
            transaction_pin = form.cleaned_data['transaction_Pin']
            payload = {
                'agentReference': agentReference,
                'agentId': 205,
                'plan': 'prepaid',
                "amount": int(amount),
                "phone": phone,
                "service_type": service_type,
            }
            user_pin = request.session['transaction_Pin']
            if pin_auth(user_pin, transaction_pin):
                #logging.info("User Pin Authenticated")
                user_url = request.session['user_url']
                #logging.info("Checking User Balance")
                has_EnoughBalance = authenticate_balance(
                    user_url, transaction_amount=float(amount))
                

                if has_EnoughBalance:
                    #logging.info("User has enough Balance, Proceeding to make Transaction")
                    response = geekops.Airtime.request_airtime(payload)
                    print(response)
                    if response['data']['status'] == 'success':
                        #logging.info("Transaction Successful")
                        user_id = request.session['user_id']
                        user_urll = request.session['redirect_url']

                        # t_status = {'status': 'successful',
                        #             'id': user_id,
                        #             'transaction_id': agentReference, 'amount': amount}
                        #print(user_urll)
                        #logging.info("Sending Transaction State To Partner")
                        endpoint = user_urll + "?id=" + str(user_id) + "&status=successful&amount=" + str(
                            amount) + "&transaction_id=" + str(agentReference)
                        requests.get(endpoint)
                        #logging.info("Transaction State Sent To Partner")
                        #print(re.text)
                        customer = User.objects.get(
                            email=request.session['email'])
                        transaction = Transaction(beneficiary_AccountName=phone,
                                                  transaction_Amount=amount,
                                                  transaction_Status=True,
                                                  narration='Airtime Transaction',
                                                  customer=customer,
                                                  transaction_Ref=agentReference)
                        transaction.save()
                        print(response['data'])
                        res = response['data']['data']['transactionMessage']
                        redirect_url = request.session['profile_url']
                        return render(request, 'bills/trans_success.html', {'transactionAmount': amount, 'beneficiaryAccountName': phone, 'agentref': agentReference, 'res': res, 'redirect_url': redirect_url})

                    else:
                        res = response['data']['message']
                        redirect_url = request.session['profile_url']
                        return render(request, 'bills/trans_failure.html', {'res': res, 'redirect_url': redirect_url})
                return HttpResponse('Insufficient balance')

            return HttpResponse('Incorrect Transaction Pin')

        else:
            return HttpResponse('Form is not valid')

    form = AirtimePurchaseForm()
    return render(request, 'bills/airtime.html', {'form': form, 'account_balance': userBalance, 'email': username})


def DataBundlesView(request):
    try:
        user_url = request.session['user_url']
    except:
        return HttpResponse("Your Session has expired")

    #logging.info("Data Bundles Transaction Initiated.......")
    userBalance = balance(
        user_url)

    username = request.session['username']
    geekops = geekops(env_var["BAXI_PROD_API_KEY"])
    agentId = 109
    agentReference = str(GenerateReference())
    if request.method == 'POST':
        #logging.info("Form Submission Validation......")
        # plan = form.cleaned_data['plan']
        service_type = request.POST.get('service_type')
        amount = request.POST.get('amount')
        phone = request.POST.get('phone')
        datacode = request.POST.get('datacode')
        transaction_pin = request.POST.get('transaction_Pin')
        #logging.info("Form Validation Successful....")
        payload = {
            'agentReference': agentReference,
            'agentId': env_var["BAXI_PROD_AGENT_ID"],
            'datacode': datacode,
            "amount": int(amount),
            "phone": phone,
            "service_type": service_type,
        }
        user_pin = request.session['transaction_Pin']
        if pin_auth(user_pin, transaction_pin):
            user_url = request.session['user_url']
            has_EnoughBalance = authenticate_balance(
                user_url, transaction_amount=float(amount))
            #logging.info("Pin Authentication Successful")
            #logging.info("Checking User Balance")
            if has_EnoughBalance:
                #logging.info("User has enough Balance, Proceeding to make Transaction")
                response = geekops.DataBundles.request_data_bundles(
                    payload)
                print(response)
                if response['data']['status'] == 'success':
                    #logging.info("Transaction Successful")
                    user_url = request.session['redirect_url']
                    user_id = request.session['user_id']
                    t_status = {'status': 'successful',
                                'id': user_id,
                                'transaction_id': agentReference, 'amount': amount}

                    endpoint = user_url + "?id=" + str(user_id) + "&status=successful&amount=" + str(
                        amount) + "&transaction_id=" + str(agentReference)
                    #logging.info("Sending Transaction State To Partner") 
                    requests.get(endpoint)
                    #logging.info("Transaction State Sent To Partner")
                    customer = User.objects.get(
                        email=request.session['email'])
                    transaction = Transaction(beneficiary_AccountName=phone,
                                              transaction_Amount=amount,
                                              transaction_Status=True,
                                              narration='Data Subscription',
                                              customer=customer,
                                              transaction_Ref=agentReference)
                    transaction.save()
                    res = response['data']['data']['transactionMessage']
                    redirect_url = request.session['profile_url']
                    return render(request, 'bills/trans_success.html', {'account_balance': userBalance, 'redirect_url': redirect_url, 'transactionAmount': amount, 'beneficiaryAccountName': phone, 'agentref': agentReference, 'res': res})

                else:
                    res = response['data']['message']
                    redirect_url = request.session['profile_url']
                    return render(request, 'bills/trans_failure.html', {'account_balance': userBalance, 'res': res, 'redirect_url': redirect_url})
            return HttpResponse('Insufficient Balance')
        return HttpResponse('Incorrect Transaction Pin')

    form = DataBundlesPurchaseForm()
    return render(request, 'bills/data_bundles.html', {'account_balance': userBalance, 'email': username})


def payDSTVView(request):
    try:
        user_url = request.session['user_url']
    except:
        return HttpResponse("Your Session has expired")
    #logging.info("DSTV Transaction Initiated.......")
    userBalance = balance(
        user_url)

    username = request.session['username']
    agentRef = str(GenerateReference())
    bremit = geekops(env_var["BAXI_PROD_API_KEY"])
    if request.method == 'POST':
        #logging.info("Form Submission Validation......")
        # view to process dstv subscription requests
        smartcard_number = request.POST.get('smartcard_number')
        total_amount = request.POST.get('total_amount')
        product_code = request.POST.get('code')
        months = request.POST.get('months')
        service_type = 'dstv'
        transaction_pin = request.POST.get('transaction_Pin')
        #logging.info("Form Validation Successful....")
        agentId = env_var["BAXI_PROD_AGENT_ID"]
        payload = {
            'smartcard_number': smartcard_number,
            'total_amount': total_amount,
            'product_code': product_code,
            'product_monthsPaidFor': months,
            'agentId': agentId,
            'agentReference': agentRef,
            'service_type': 'dstv',
        }

        user_pin = request.session['transaction_Pin']
        if pin_auth(user_pin, transaction_pin):
            user_url = request.session['user_url']
            #logging.info("Pin Authentication Successful")
            has_EnoughBalance = authenticate_balance(
                user_url, transaction_amount=float(total_amount))
            #logging.info("Checking User Balance")
            if has_EnoughBalance:
                #logging.info("User has enough Balance, Proceeding to make Transaction")
                response = bremit.CableTv.request_cable_tv(payload)

                if response['data']['status'] == 'success':
                    #logging.info("Transaction Successful")
                    user_id = request.session['user_id']
                    user_url = request.session['redirect_url']
                    # t_status = {'status': 'successful',
                    #             'id': user_id,
                    #             'transaction_id': agentRef, 'amount': total_amount}
                    endpoint = user_url + "?id=" + str(user_id) + "&status=successful&amount=" + str(
                        total_amount) + "&transaction_id=" + str(agentRef)
                    #logging.info("Sending Transaction State To Partner")
                    requests.get(endpoint)
                    #logging.info("Transaction State Sent To Partner")
                    customer = User.objects.get(
                        email=request.session['email'])
                    transaction = Transaction(beneficiary_AccountName=smartcard_number,
                                              transaction_Amount=total_amount,
                                              transaction_Status=True,
                                              narration='Dstv Subscription',
                                              customer=customer,
                                              transaction_Ref=agentRef)
                    transaction.save()
                    res = response['data']['data']['transactionMessage']
                    redirect_url = request.session['profile_url']
                    return render(request, 'bills/trans_success.html', {'account_balance': userBalance, 'redirect_url': redirect_url, 'transactionAmount': total_amount, 'beneficiaryAccountName': smartcard_number, 'agentref': agentRef, 'res': res})

                else:
                    res = res = response['data']['message']
                    redirect_url = request.session['profile_url']
                    return render(request, 'bills/trans_failure.html', {'account_balance': userBalance, 'res': res, 'redirect_url': redirect_url})
            return HttpResponse('Insufficient Balance')
        return HttpResponse('Incorrect Transaction Pin')

    return render(request, 'bills/pay_dstv.html', {'account_balance': userBalance, 'email': username})


def payGoTVView(request):
    try:
        user_url = request.session['user_url']
    except:
        return HttpResponse("Your Session has expired")
    #logging.info("GoTV Transaction Initiated.......")
    userBalance = balance(
        user_url)
    

    username = request.session['username']
    agentRef = str(GenerateReference())
    bremit = geekops(env_var["BAXI_PROD_API_KEY"])
    if request.method == 'POST':
        #logging.info("Form Submission Validation......")
        # view to process dstv subscription requests
        smartcard_number = request.POST.get('smartcard_number')
        total_amount = request.POST.get('total_amount')
        product_code = request.POST.get('code')
        months = request.POST.get('months')
        transaction_pin = request.POST.get('transaction_Pin')
        #logging.info("Form Validation Successful....")
        service_type = 'gotv'
        agentId = env_var["BAXI_PROD_AGENT_ID"]
        payload = {
            'smartcard_number': smartcard_number,
            'total_amount': total_amount,
            'product_code': product_code,
            'product_monthsPaidFor': months,
            'agentId': agentId,
            'agentReference': agentRef,
            'service_type': service_type,
        }

        user_pin = request.session['transaction_Pin']
        if pin_auth(user_pin, transaction_pin):
            user_url = request.session['user_url']
            #logging.info("Pin Authentication Successful")
            has_EnoughBalance = authenticate_balance(
                user_url, transaction_amount=float(total_amount))
            #logging.info("Checking User Balance")
            if has_EnoughBalance:
                #logging.info("User has enough Balance, Proceeding to make Transaction")
                response = bremit.CableTv.request_cable_tv(payload)

                if response['data']['status'] == 'success':
                    #logging.info("Transaction Successful")
                    user_url = request.session['redirect_url']
                    user_id = request.session['user_id']
                    t_status = {'status': 'successful',
                                'id': user_id,
                                'transaction_id': agentRef, 'amount': total_amount}
                    endpoint = user_url + "?id=" + str(user_id) + "&status=successful&amount=" + str(
                        total_amount) + "&transaction_id=" + str(agentRef)
                    #logging.info("Sending Transaction State To Partner")
                    requests.get(endpoint)
                    #logging.info("Transaction State Sent To Partner")
                    customer = User.objects.get(
                        email=request.session['email'])
                    transaction = Transaction(beneficiary_AccountName=smartcard_number,
                                              transaction_Amount=total_amount,
                                              transaction_Status=True,
                                              narration='GoTv Subscription',
                                              customer=customer,
                                              transaction_Ref=agentRef)
                    transaction.save()
                    res = response['data']['data']['transactionMessage']
                    redirect_url = request.session['profile_url']
                    return render(request, 'bills/trans_success.html', {'account_balance': userBalance, 'redirect_url': redirect_url, 'transactionAmount': total_amount, 'beneficiaryAccountName': smartcard_number, 'agentref': agentRef, 'res': res})

                else:
                    res = res = response['data']['message']
                    redirect_url = request.session['profile_url']
                    return render(request, 'bills/trans_failure.html', {'account_balance': userBalance, 'res': res, 'redirect_url': redirect_url})
            return HttpResponse('Insufficient balance')
        return HttpResponse('Incorrect Transaction Pin')

    return render(request, 'bills/pay_gotv.html', {'account_balance': userBalance, 'email': username})


def payStarTimesView(request):
    try:
        user_url = request.session['user_url']
    except:
        return HttpResponse("Your Session has expired")
    #logging.info("StarTimes Transaction Initiated.......")
    userBalance = balance(
        user_url)

    username = request.session['username']
    agentRef = str(GenerateReference())
    bremit = geekops(env_var["BAXI_PROD_API_KEY"])
    if request.method == 'POST':
        #logging.info("Form Submission Validation......")
        # view to process dstv subscription requests
        smartcard_number = request.POST.get('smartcard_number')
        total_amount = request.POST.get('total_amount')
        product_code = request.POST.get('code')
        months = request.POST.get('months')
        transaction_pin = request.POST.get('transaction_Pin')
        #logging.info("Form Validation Successful....")
        service_type = 'startimes'
        agentId = env_var["BAXI_PROD_AGENT_ID"]
        payload = {
            'smartcard_number': smartcard_number,
            'total_amount': total_amount,
            'product_code': product_code,
            'product_monthsPaidFor': months,
            'agentId': agentId,
            'agentReference': agentRef,
            'service_type': service_type,
        }

        user_pin = request.session['transaction_Pin']
        if pin_auth(user_pin, transaction_pin):
            user_url = request.session['user_url']
            #logging.info("Pin Authentication Successful")
            has_EnoughBalance = authenticate_balance(
                user_url, transaction_amount=float(total_amount))
            #logging.info("Checking User Balance")

            if has_EnoughBalance:
                #logging.info("User has enough Balance, Proceeding to make Transaction")
                response = bremit.CableTv.request_cable_tv(payload)

                if response['data']['status'] == 'success':
                    #logging.info("Transaction Successful")
                    user_url = request.session['redirect_url']
                    user_id = request.session['user_id']
                    t_status = {'status': 'successful',
                                'id': user_id,
                                'transaction_id': agentRef, 'amount': total_amount}

                    endpoint = user_url + "?id=" + str(user_id) + "&status=successful&amount=" + str(
                        total_amount) + "&transaction_id=" + str(agentRef)
                    #logging.info("Sending Transaction State To Partner")
                    requests.get(endpoint)
                    #logging.info("Transaction State Sent To Partner")
                    customer = User.objects.get(
                        email=request.session['email'])
                    transaction = Transaction(beneficiary_AccountName=smartcard_number,
                                              transaction_Amount=total_amount,
                                              transaction_Status=True,
                                              narration='StarTimes Subscription',
                                              customer=customer,
                                              transaction_Ref=agentRef)
                    transaction.save()
                    res = response['data']['data']['transactionMessage']
                    redirect_url = request.session['profile_url']
                    return render(request, 'bills/trans_success.html', {'account_balance': userBalance, 'redirect_url': redirect_url, 'transactionAmount': total_amount, 'beneficiaryAccountName': smartcard_number, 'agentref': agentRef, 'res': res})

                else:
                    res = res = response['data']['message']
                    redirect_url = request.session['profile_url']
                    return render(request, 'bills/trans_failure.html', {'account_balance': userBalance, 'res': res, 'redirect_url': redirect_url})

            return HttpResponse('Insufficient balance')

        return HttpResponse('Incorrect Transaction Pin')
    return render(request, 'bills/pay_startimes.html', {'account_balance': userBalance, 'email': username})


def ElectricityView(request):
    try:
        user_url = request.session['user_url']
    except:
        return HttpResponse("Your Session has expired")
    #logging.info("Electricity Transaction Initiated.......")
    userBalance = balance(
        user_url)

    username = request.session['email']
    geekops = geekops(env_var["BAXI_PROD_API_KEY"])
    agentReference = str(GenerateReference())
    agentId = env_var.BAXI_PROD_AGENT_ID
    if request.method == 'POST':
        #logging.info("Form Submission Validation......")
        form = ElectricityPurchaseForm(request.POST)
        if form.is_valid():
            #logging.info("Form Validation Successful....")
            # plan = form.cleaned_data['plan']
            service_type = form.cleaned_data['service_type']
            amount = form.cleaned_data['amount']
            phone = form.cleaned_data['phone']
            account = form.cleaned_data['account']
            transaction_pin = form.cleaned_data['transaction_Pin']
            payload = {
                'agentReference': agentReference,
                'agentId': agentId,
                "amount": int(amount),
                "phone": str(phone),
                "service_type": str(service_type),
                'account_number': str(account),
            }
            user_pin = request.session['transaction_Pin']
            if pin_auth(user_pin, transaction_pin):
                user_url = request.session['user_url']
                #logging.info("Pin Authentication Successful")
                has_EnoughBalance = authenticate_balance(
                    user_url, transaction_amount=float(amount))
                #logging.info("Checking User Balance")
                if has_EnoughBalance:
                    #logging.info("User has enough Balance, Proceeding to make Transaction")
                    response = geekops.Electricity.request_electricity(
                        payload)
                    if response['data']['status'] == 'success':
                        #logging.info("Transaction Successful")
                        user_id = request.session['user_id']
                        user_url = request.session['redirect_url']
                        t_status = {'status': 'successful',
                                    'id': user_id,
                                    'transaction_id': agentReference, 'amount': amount}
                        endpoint = user_url + "?id=" + str(user_id) + "&status=successful&amount=" + str(
                            amount) + "&transaction_id=" + str(agentReference)
                        #logging.info("Sending Transaction State To Partner")
                        requests.get(endpoint)
                        #logging.info("Transaction State Sent To Partner")
                        customer = User.objects.get(
                            email=request.session['email'])
                        transaction = Transaction(beneficiary_AccountName=account,
                                                  transaction_Amount=amount,
                                                  transaction_Status=True,
                                                  narration='ElectricityTransaction',
                                                  customer=customer,
                                                  transaction_Ref=agentReference)
                        transaction.save()
                        res = response['data']['data']['transactionMessage']
                        redirect_url = request.session['profile_url']
                        return render(request, 'bills/trans_success.html', {'account_balance': userBalance, 'redirect_url': redirect_url, 'transactionAmount': amount, 'beneficiaryAccountName': account, 'agentref': agentReference, 'res': res})

                    else:
                        res = response['data']['message']
                        redirect_url = request.session['profile_url']
                        return render(request, 'bills/trans_failure.html', {'account_balance': userBalance, 'res': res, 'redirect_url': redirect_url})
                else:
                    return HttpResponse('Incorrect Transaction Pin')

        else:
            return HttpResponse('Form is not valid')

    form = ElectricityPurchaseForm()
    return render(request, 'bills/buy_electricity.html', {'form': form, 'account_balance': userBalance, 'email': username})


from django.shortcuts import render

def error_404(request, exception):
        data = {}
        return render(request,'geekops/404.html', data)

def error_500(request,  exception):
        data = {}
        return render(request,'geekops/500.html', data)
