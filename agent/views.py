from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView
from baxi_api.geekOps import geekOps
from django.http import HttpResponse
# Create your views here.


from django.template.defaulttags import register
from .forms import AgentRefForm
from django.contrib.auth.decorators import login_required


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class HomeView(TemplateView):
    template_name = 'index.html'


@login_required
def RequeryView(request):
    if request.method == 'POST':
        form = AgentRefForm(request.POST)
        if form.is_valid():
            agentref = form.cleaned_data['agentReference']
            geekOps = geekOps("myApiKey")
            payload = {'agentReference': agentref}
            response = geekOps.AgentTransaction.transaction(payload)
            try:
                return HttpResponse(response['data']['data']['transactionStatus'])
            except:
                return HttpResponse('Request Failed')

    form = AgentRefForm()
    return render(request, 'requery.html', {'form': form})


@login_required
def RetryView(request):
    if request.method == 'POST':
        form = AgentRefForm(request.POST)
        if form.is_valid():
            agentref = form.cleaned_data['agentReference']
            geekOps = geekOps("myApiKey")
            payload = {'agentReference': agentref}
            response = geekOps.AgentTransaction.retry_transaction(payload)
            try:
                return HttpResponse(response['data'])
            except:
                return HttpResponse('Request Failed')
    form = AgentRefForm()
    return render(request, 'retry.html', {'form': form})


@login_required
def BalanceView(request):
    if request.method == 'GET':
        geekOps = geekOps("myApiKey")

        # payload = {'agentReference':agentref}
        response = geekOps.AgentTransaction.agent_balance()
        agentbal = response['data']['data']['balance']
        lastdeposit = response['data']['data']['lastDeposit']

        return render(request, 'balance.html', {'agentbal': agentbal, 'lastdeposit': lastdeposit})


@login_required
def RefreshView(request):
    if request.method == 'GET':
        geekOps = geekOps("myApiKey")

        # payload = {'agentReference':agentref}
        response = geekOps.AgentTransaction.refresh()
        account_refresh = response['data']['data']
        return render(request, 'refresh.html', {'refresh': account_refresh})
