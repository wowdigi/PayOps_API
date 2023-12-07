from django import forms


class TransactionStatusForm(forms.Form):
    transaction_reference = forms.CharField(max_length=30)


class AccountStatusForm(forms.Form):
    account_number = forms.CharField(max_length=10)
