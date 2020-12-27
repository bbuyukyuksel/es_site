from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from node.models import Node, Temperature
import json


# Create your views here.
def index(request):
    Chart_Values = []
    nodes = Node.objects.all()
    for node in nodes:
        temp = {
            "values": node.temperature_this_mount_list(),
            "line-color": "#0884D9",
            #/* "dotted" | "dashed" */
            "line-width": 5, #/* in pixels */ ,
            "marker": { #/* Marker object */
                "background-color": "#067dce",
                #/* hexadecimal or RGB value */
                "size": 5,
                #/* in pixels */
                "border-color": "#067dce",
                #/* hexadecimal or RBG value */
            }
        }
        Chart_Values.append(temp)
    return render(request, 'node/index.html', context={"chart_values":Chart_Values})


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
    nodes = Node.objects.all()
    t = nodes.first().temperature_last_update_date()
    print("Last:", t)
    return render(request, 'node/list.html', context={'nodes':nodes})



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
            return redirect('node:node_list')
            #return HttpResponse(f"Get Request api_node_create {device_name}, {confirm}, Saved PK: {node.pk}")
        else:    
            return redirect('node:node_list')
            #return HttpResponse(f"Device create fail!")
    

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

def api_node_temperature_create(request):
    if request.GET:
        device_name = request.GET.get('device_name', None)
        temperature = request.GET.get('temperature', None)
        if device_name and temperature:
            device = Node.objects.filter(device_name=device_name)
            if device.count() > 0:
                t = device.first().temperature_set.create(temperature=temperature)
                return HttpResponse(f"Created temperature:{t.temperature} to {t.device}")


def api_node_temperature_delete_all(request):
    if request.GET:
        if request.GET.get("confirm").lower() == 'true':
            Temperature.objects.all().delete
            return redirect('node:node_list')
            #return HttpResponse("All temperatures all deleted!")

def api_node_temperature_delete(request, pk):
    node = get_object_or_404(Node, pk=pk)
    node.temperature_set.all().delete()

    return redirect('node:node_list')