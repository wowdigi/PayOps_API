from django import forms


class AgentRefForm(forms.Form):
    agentReference = forms.CharField(max_length=40)
