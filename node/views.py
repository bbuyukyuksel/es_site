from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from node.models import Node, Temperature
from django.contrib import messages
from django.utils import timezone
import datetime
import json
import random

'''
messages.debug(request, '%s SQL statements were executed.' % count)
messages.info(request, 'Three credits remain in your account.')
messages.success(request, 'Profile details updated.')
messages.warning(request, 'Your account expires in three days.')
messages.error(request, 'Document deleted.')

alert-success
alert-info
alert-warning
alert-danger

'''

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
    return render(request, 'node/form_node_create.html', context=context)

def node_update(request, pk):
    node = get_object_or_404(Node, pk=pk)
    print(node.threshold)        
    context = {
        'form_name': 'Update',
        'node': node,
    }
    return render(request, 'node/form_node_update.html', context=context)

def node_list(request):
    nodes = Node.objects.all()
    if nodes.count() > 0:
        t = nodes.first().temperature_last_update_date()
    return render(request, 'node/list.html', context={'nodes':nodes})

def api_node_create(request):
    if request.method == "POST":
        device_name = request.POST.get("device_name")
        ip_address = request.POST.get('ip_address', None)
        threshold = request.POST.get('threshold', None)
        m_d_time = request.POST.get('m_d_time', None)

        confirm = request.POST.get("confirm", None)
        if confirm and device_name and ip_address and threshold and m_d_time:
            ip_address = ip_address.strip()
            
            unique_contol_device_name = Node.objects.filter(device_name=device_name)
            unique_contol_ip_address = Node.objects.filter(ip_address=ip_address)
            
            if unique_contol_device_name.count() > 0:
                messages.error(request, f"Already saved {device_name}", extra_tags='alert-danger')
                return redirect('node:node_create')

            if unique_contol_ip_address.count() > 0:
                messages.error(request, f"Already saved {ip_address}", extra_tags='alert-danger')
                return redirect('node:node_create')

            node = Node(device_name=device_name, ip_address=ip_address, threshold=threshold, measurement_delay_time=m_d_time)
            node.save()
            messages.success(request, f"Node is saved", extra_tags='alert-success')
            return redirect('node:node_list')

        else:    
            messages.error(request, f"Node is not saved", extra_tags='alert-danger')
            return redirect('node:node_list')
            

def api_node_update(request, pk):
    if request.method == 'POST':
        if request.POST.get('confirm', None):
            node = get_object_or_404(Node, pk=pk)
            device_name = request.POST.get('device_name', None)
            ip_address = request.POST.get('ip_address', None)
            threshold = request.POST.get('threshold', None)
            m_d_time = request.POST.get('m_d_time', None)

            if device_name: node.device_name = device_name
            if ip_address: node.ip_address = ip_address
            if threshold: node.threshold = threshold
            if m_d_time: node.measurement_delay_time = m_d_time 
            node.save()
            messages.success(request, 'Node is updated', extra_tags='alert-success')
        else:
            #Kaydedilemedi.
            messages.error(request, 'Node is not updated', extra_tags='alert-danger')
        return redirect(reverse('node:node_update', args=(pk,)))

        
def api_node_delete(request, pk):
    node = get_object_or_404(Node, pk=pk)
    node.delete()
    messages.success(request, 'Node is deleted', extra_tags='alert-success')
    return redirect(reverse('node:node_list'))

def api_node_detail(request):
    if request.GET:
        return HttpResponse("Get Request api_node_detail")
    pass

def api_node_list(request):
    if request.GET:
        return HttpResponse("Get Request api_node_list")
    pass

def api_node_parameter(request):
    if request.GET:
        device_name = request.GET.get('device_name', None)
        if device_name:
            nodes = Node.objects.filter(device_name=device_name)
            if nodes.count() > 0:
                node = nodes.first()
                parameter = {
                    str(node.device_name): {
                        "threshold":node.threshold,
                        "m_d_time": node.measurement_delay_time,    
                    } ,
                }
                return HttpResponse(json.dumps(parameter))

            else:
                return HttpResponse("-1")


def api_node_temperature_list(request, offsetdate):
    def fake_color():
        color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))
        return color    

    nodes = Node.objects.all()
    response = {}
    for index, node in enumerate(nodes):
        date_from = timezone.now().date() - datetime.timedelta(days=abs(offsetdate))
        temperature_objs = None
        
        if offsetdate == 0:
            temperature_objs= node.temperature_set.filter(created_date__date=date_from)
        else:
            temperature_objs= node.temperature_set.filter(created_date__gt=date_from)
        
        temperature_list = [x.temperature for x in temperature_objs]

        response[node.device_name] = {}
        response[node.device_name]["temperature_list"] = temperature_list
        response[node.device_name]["index"] = index
        response[node.device_name]["color"] = fake_color()


    return HttpResponse(json.dumps(response))


def api_node_is_active(request):
    nodes = Node.objects.all()
    r = {}

    for node in nodes:
        r[node.device_name] = node.is_active()

    return HttpResponse(json.dumps(r))

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
            Temperature.objects.all().delete()
            return redirect('node:node_list')
            #return HttpResponse("All temperatures all deleted!")

def api_node_temperature_delete(request, pk):
    node = get_object_or_404(Node, pk=pk)
    node.temperature_set.all().delete()

    return redirect('node:node_list')
