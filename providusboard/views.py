from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import AccountStatusForm, TransactionStatusForm
import json
# Create your views here.
from providusAPI.bremit import Remit
import locale


def ProvidusDashboard(request):

    return render(request, 'providusboard/index.html')


def AccountBalance(request):

    if request.method == 'POST':
        form = AccountStatusForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            accountNumber = form['account_number']
            remit = Remit()
            payload = {
                'accountNumber': accountNumber,
                'userName': 'test',
                'password': 'test',
            }
            response = remit.NipTransfer.getProvidusAccount(payload)
            if response['data']['responseCode'] == '00':
                accountName = response['data']['accountName']
                cbaId = response['data']['cbaCustomerID']
                emailAddress = response['data']['emailAddress']
                phoneNumber = response['data']['phoneNumber']
                availableBal = response['data']['availableBalance']
                # locale.setlocale(locale.LC_ALL, 'en_NG')
                availableBal = "#{:,.2f}".format(float(availableBal))
                return render(request, 'providusboard/balance_status.html', {'availableBal': availableBal, 'accountName': accountName, 'emailAddress': emailAddress, 'phoneNumber': phoneNumber, 'cbaId': cbaId})
    form = AccountStatusForm()
    return render(request, 'providusboard/balance.html', {'form': form})


def TransactionStatus(request):

    if request.method == 'POST':
        form = TransactionStatusForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            transactionRef = form['transaction_reference']
            remit = Remit()
            payload = {
                'transactionReference': transactionRef,
                'userName': 'test',
                'password': 'test',
            }
            response = remit.NipTransfer.getNIPTransactionStatus(payload)

            message = response['data']['responseMessage']
            recipientAccount = response['data']['recipientAccountNumber']
            date = response['data']['transactionDateTime']
            transactionRef = response['data']['transactionReference']
            amount = response['data']['amount']

            # for i in range(len(response['data'])):
            #     # for key, value in response['data']:
            #     #     details[key] = value
            #     print(response['data'][i])

            return render(request, 'providusboard/transaction_status.html', {'message': message, 'amount': amount, 'date': date, 'recipientAccount': recipientAccount, 'transactionRef': transactionRef})
    form = TransactionStatusForm()
    return render(request, 'providusboard/status.html', {'form': form})


def SearchTransaction(request):

    if request.method == 'POST':
        pass

    return render(request, 'providusboard/search.html')


def MailUser(request):

    if request.method == 'POST':
        pass

    return render(request, 'providusboard/mail.html')
