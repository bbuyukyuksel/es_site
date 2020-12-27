from django.urls import path
import node.views

app_name = 'node'

urlpatterns = [
    path('', node.views.index),
    
    path('node/create', node.views.node_create, name='node_create'),
    path('node/delete', node.views.node_delete, name='node_delete'),
    path('node/detail', node.views.node_detail, name='node_detail'),
    path('node/list',   node.views.node_list,   name='node_list'),

    path('api/node/create', node.views.api_node_create, name='api_node_create'),
    path('api/node/delete/<int:pk>', node.views.api_node_delete, name='api_node_delete'),
    path('api/node/detail/<int:pk>', node.views.api_node_detail, name='api_node_detail'),
    path('api/node/list', node.views.api_node_list, name='api_node_list'),

    path('api/temperature/create', node.views.api_node_temperature_create, name='api_temperature_create'),
    path('api/temperature/delete_all', node.views.api_node_temperature_delete_all, name='api_temperature_delete_all'),
    path('api/temperature/delete/<int:pk>', node.views.api_node_temperature_delete, name='api_temperature_delete'),

]

