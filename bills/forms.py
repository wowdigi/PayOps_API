from django import forms
from django.forms.widgets import HiddenInput
from baxi_api.geekops_misc import GenerateReference
from providusAPI import bremit
plan_options = (
    ('prepaid', 'prepaid'),
    ('postpaid', 'postpaid'),
)

service_type = (
    ('9mobile', '9mobile'),
    ('airtel', 'Airtel'),
    ('glo', 'Glo'),
    ('mtn', 'Mtn'),
    ('smile', 'Smile'),
)

electricity = (('jos_electric_postpaid', 'Jos Postpaid'),
               ('jos_electric_prepaid', 'Jos Prepaid'),
               ('kaduna_electric_prepaid', 'Kaduna Prepaid'),
               ('eko_electric_prepaid', 'Eko Prepaid'),
               ('ibadan_electric_prepaid', 'Ibadan Disco Prepaid (Fets Wallet)'),
               ('portharcourt_electric_postpaid',
                'Port Harcourt Postpaid (Xpresspayments)'),
               ('portharcourt_electric_prepaid',
                'Port Harcourt Prepaid (Xpresspayments)'),
               ('enugu_electric_postpaid', 'Enugu Postpaid'),
               ('enugu_electric_prepaid', 'Enugu Prepaid'),
               ('abuja_electric_postpaid', 'Abuja Postpaid'),
               ('abuja_electric_prepaid', 'Abuja Prepaid'),
               ('kedco_electric_postpaid', 'Kano Postpaid'),
               ('kedco_electric_prepaid', 'Kano Prepaid'),
               ('ikeja_electric_prepaid', 'Ikeja Disco Token Vending (Prepaid)'),
               ('ikeja_electric_postpaid', 'Ikeja Disco Bill Payment (Postpaid)'),
               ('eko_electric_postpaid', 'Eko Postpaid'), ('ibadan_electric_postpaid', 'Ibadan Disco Postpaid (Fets Wallet)'))


bank_choices = (('None', 'Select Bank'), ('000014', 'ACCESS BANK'), ('100013', 'ACCESS MOBILE'),
                ('090133', 'AL-BARAKAH MICROFINANCE BANK'), ('090116',
                                                             'AMML MICROFINANCE BANK'),
                ('090001', 'ASO SAVINGS'), ('090127', 'BC KASH MICROFINANCE BANK'),
                ('090117', 'BOCTRUST MICROFINANCE BANK LIMITED'), ('100005', 'CELLULANT'),
                ('100015', 'CHAMS MOBILE'), ('000009',
                                             'CITI BANK'), ('060001', 'CORONATION BANK'),
                ('070006', 'COVENANT MFB'), ('000005',
                                             'DIAMOND BANK'), ('100021', 'EARTHOLEUM'),
                ('000010', 'ECOBANK'), ('100008', 'ECOBANK XPRESS ACCOUNT'),
                ('090114', 'EMPIRE TRUST MICROFINANCE BANK'), ('000019', 'ENTERPRISE BANK'),
                ('100006', 'eTRANZACT'), ('060002',
                                          'FBN MERCHANT BANK'), ('100014', 'FBN MOBILE'),
                ('090107', 'FBN MORTGAGES LIMITED'), ('090107',
                                                      'FBN MORTGAGES LIMITED'), ('100001', 'FET'),
                ('000007', 'FIDELITY BANK'), ('100019',
                                              'FIDELITY MOBILE'), ('090111', 'FINATRUST MICROFINANCE BANK'),
                ('000016', 'FIRST BANK OF NIGERIA'), ('000003',
                                                      'FIRST CITY MONUMENT BANK'),
                ('070002', 'FORTIS MICROFINANCE BANK'), ('100016',
                                                         'FORTIS MOBILE'), ('400001', 'FSDH'),
                ('090122', 'GOWANS MICROFINANCE BANK'), ('100009',
                                                         'GT MOBILE'), ('000013', 'GTBANK PLC'),
                ('090121', 'HASAL MICROFINANCE BANK'), ('100017',
                                                        'HEDONMARK'), ('000020', 'HERITAGE BANK'),
                ('090118', 'IBILE MICROFINANCE BANK'), ('100024',
                                                        'IMPERIAL HOMES MORTGAGE BANK'), ('100027', 'INTELLFIN'),
                ('000006', 'JAIZ BANK'), ('090003', 'JUBILEE LIFE'), ('000002',
                                                                      'KEYSTONE BANK'), ('100025', 'KONGAPAY'),
                ('100011', 'M KUDI'), ('090136',
                                       'MICROCRED MICROFINANCE BANK'), ('090113', 'MICROVIS MICROFINANCE BANK'),
                ('100020', 'MONEY BOX'), ('090128',
                                          'NDIORAH MICROFINANCE BANK'), ('090108', 'NEW PRUDENTIAL BANK'),
                ('999999', 'NIP VIRTUAL BANK'), ('070001',
                                                 'NPF MICROFINANCE BANK'), ('070007', 'OMOLUABI'),
                ('100026', 'ONE FINANCE'), ('100002',
                                            'PAGA'), ('070008', 'PAGE MFBank'),
                ('090004', 'PARALLEX'), ('100003', 'PARKWAY-READYCASH'),
                ('110001', 'PAYATTITUDE ONLINE'), ('100004',
                                                   'PAYCOM'), ('090135', 'PERSONAL TRUST MICROFINANCE BANK'),
                ('000023', 'PROVIDUS BANK'), ('000024',
                                              'RAND MERCHANT BANK'), ('090125', 'REGENT MICROFINANCE BANK'),
                ('090132', 'RICHWAY MICROFINANCE BANK'), ('090006', 'SAFETRUST'),
                ('090112', 'SEED CAPITAL MICROFINANCE BANK'), ('000008',
                                                               'SKYE BANK'), ('000012', 'STANBIC IBTC BANK'),
                ('100007', 'STANBIC MOBILE MONEY'), ('000021',
                                                     'STANDARD CHARTERED BANK'), ('000001', 'STERLING BANK'),
                ('100022', 'STERLING MOBILE'), ('000022', 'SUNTRUST BANK'), ('100023',
                                                                             'TAGPAY'), ('090115', 'TCF MICROFINANCE BANK'),
                ('100010', 'TEASY MOBILE'), ('090005', 'TRUSTBOND'), ('000018',
                                                                      'UNION BANK'), ('000004', 'UNITED BANK FOR AFRICA'),
                ('000011', 'UNITY BANK'), ('090123', 'VERITE MICROFINANCE BANK'), ('100012',
                                                                                   'VT NETWORKS'), ('000017', 'WEMA BANK'),
                ('090120', 'WETLAND  MICROFINANCE BANK'), ('000015', 'ZENITH BANK'), ('100018', 'ZENITH MOBILE'))


dstvproduct = (('PRWFRNSE36', 'DStv Premium French'), ('NLTESE36', 'Padi'), ('COMPE36', 'DStv Compact'), ('COMPLE36', 'DStv Compact Plus'), ('PRWE36', 'DStv Premium'),
               ('PRWASIE36', 'DStv Premium Asia'), ('ASIAE36', 'Asian Bouqet'), ('NNJ1E36', 'DStv Yanga Bouquet E36'), ('NNJ2E36', 'DStv Confam Bouquet E36'))


class AirtimePurchaseForm(forms.Form):
    service_type = forms.ChoiceField(label='Network', choices=service_type)
    amount = forms.IntegerField(label='Amount')
    phone = forms.CharField(max_length=11, label="Recipient's Phone Number")
    transaction_Pin = forms.CharField(max_length=4, widget=forms.PasswordInput(
        render_value=False, attrs={'class': 'form-control', 'placeholder': 'Your Pin'}))


class DataBundlesPurchaseForm(forms.Form):
    service_type = forms.ChoiceField(label='Network', choices=service_type)
    amount = forms.IntegerField(label='Amount')
    phone = forms.CharField(max_length=11, label='Phone Number')
    transaction_Pin = forms.CharField(max_length=4, widget=forms.PasswordInput(
        render_value=False, attrs={'class': 'form-control', 'placeholder': 'Your Pin'}))


class DstvCableTvPurchaseForm(forms.Form):
    amount = forms.IntegerField(label='Enter Amount')
    smartcard_number = forms.IntegerField(label='Enter SmartCard Number')
    product_monthPaidFor = forms.IntegerField(label='Enter Number of Months')
    product_code = forms.ChoiceField(label='Product Type', choices=dstvproduct)
    transaction_Pin = forms.CharField(max_length=4, widget=forms.PasswordInput(
        render_value=False, attrs={'class': 'form-control', 'placeholder': 'Your Pin'}))


class CableTvPurchaseForm(forms.Form):
    amount = forms.IntegerField(label='Enter Amount')
    smartcard_number = forms.IntegerField(label='Enter SmartCard Number')
    product_monthPaidFor = forms.IntegerField(label='Enter Number of Months')
    product_code = forms.ChoiceField(label='Product Type', choices=dstvproduct)
    transaction_Pin = forms.CharField(max_length=4, widget=forms.PasswordInput(
        render_value=False, attrs={'class': 'form-control', 'placeholder': 'Your Pin'}))


class ElectricityPurchaseForm(forms.Form):
    service_type = forms.ChoiceField(
        label='Service Provider', choices=electricity)
    amount = forms.IntegerField(label='Enter Amount')
    phone = forms.CharField(max_length=11, label='Enter Phone Number')
    account = forms.CharField(max_length=20)
    transaction_Pin = forms.CharField(max_length=4, widget=forms.PasswordInput(
        render_value=False, attrs={'class': 'form-control', 'placeholder': 'Your Pin'}))


class NIPTransferForm(forms.Form):
    Transfer_Amount = forms.CharField(max_length=6)
    narration = forms.CharField(widget=forms.Textarea(attrs={
        'style': 'height: 50px;width:100%'}))
    Account_Number = forms.CharField(max_length=10)
    beneficiary_Bank = forms.ChoiceField(choices=bank_choices)
    transaction_Pin = forms.CharField(max_length=4, widget=forms.PasswordInput(
        render_value=False, attrs={'class': 'form-control', 'placeholder': 'Your Pin'}))
