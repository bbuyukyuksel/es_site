from django.urls import path
import node.views

app_name = 'node'

urlpatterns = [
    path('', node.views.index, name='index'),
        
    path('node/create', node.views.node_create, name='node_create'),
    path('node/update/<int:pk>', node.views.node_update, name='node_update'),
    path('node/list',   node.views.node_list,   name='node_list'),
    

    path('api/node/create', node.views.api_node_create, name='api_node_create'),
    path('api/node/update/<int:pk>', node.views.api_node_update, name='api_node_update'),
    path('api/node/delete/<int:pk>', node.views.api_node_delete, name='api_node_delete'),
    path('api/node/detail/<int:pk>', node.views.api_node_detail, name='api_node_detail'),
    path('api/node/list', node.views.api_node_list, name='api_node_list'),
    path('api/node/parameter', node.views.api_node_parameter, name='api_node_parameter'),
    path('api/node/is_active', node.views.api_node_is_active, name='api_node_is_active'),

    path('api/temperature/create', node.views.api_node_temperature_create, name='api_temperature_create'),
    path('api/temperature/delete_all', node.views.api_node_temperature_delete_all, name='api_temperature_delete_all'),
    path('api/temperature/delete/<int:pk>', node.views.api_node_temperature_delete, name='api_temperature_delete'),

]

