from django.shortcuts import render, HttpResponse
from node.models import Node



# Create your views here.
def index(request):
    return render(request, 'node/index.html', context={})


def node_create(request):
    context = {
        "form_name": "Create",

    }
    return render(request, 'node/form.html', context=context)
    

def node_delete(request):
    pass

def node_detail(request):
    pass

def node_list(request):
    pass


def api_node_temperature_create(request):
    if request.GET:
        device_name = request.GET.get('device_name', None)
        temperature = request.GET.get('temperature', None)
        if device_name and temperature:
            device = Node.objects.filter(device_name=device_name)
            if device.count() > 0:
                t = device.first().temperature_set.create(temperature=temperature)
                return HttpResponse(f"Created temperature:{t.temperature} to {t.device}")

            

def api_node_create(request):
    if request.GET:
        device_name = request.GET.get("device_name")
        confirm = request.GET.get("confirm", None)
        if confirm:
            unique_contol = Node.objects.filter(device_name=device_name)
            if unique_contol.count() > 0:
                return HttpResponse(f"Already saved {device_name}")

            node = Node(device_name=device_name)
            node.save()
            return HttpResponse(f"Get Request api_node_create {device_name}, {confirm}, Saved PK: {node.pk}")
        else:    
            return HttpResponse(f"Device create fail!")
    

def api_node_delete(request):
    if request.GET:
        return HttpResponse("Get Request api_node_delete")
    pass

def api_node_detail(request):
    if request.GET:
        return HttpResponse("Get Request api_node_detail")
    pass

def api_node_list(request):
    if request.GET:
        return HttpResponse("Get Request api_node_list")
    pass
