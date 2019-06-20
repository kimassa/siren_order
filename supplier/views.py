from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Supplier
from customer.utils import login_required
from customer.models import Customer
from django.core import serializers
from geopy.distance import distance
import json

class SupplierAllView(View):
    def get(self, request):

        data = Supplier.objects.all().values()
        data_json = [ {
            'name' : d['name'],
            'branch' : d['branch'],
            'address' : d['address'],
            'zipcode' : d['zipcode'],
            'phone' : d['phone'],
            'latitude': d['latitude'],
            'longitude' : d['longitude']
        } for d in data.iterator() ]
        
        return JsonResponse(data_json, safe=False)

class SupplierDetailView(View):
    def get(self, request, pk):

        supplier = Supplier.objects.filter(id=pk)
        supplier_list = list(supplier.values())
              
        data_json = [ {
                'name' : d['name'],
                'branch' : d['branch'],
                'address' : d['address'],
                'zipcode' : d['zipcode'],
                'phone' : d['phone'],
                'latitude': d['latitude'],
                'longitude' : d['longitude']
            } for d in supplier_list
        ]
        
        return JsonResponse(data_json, safe=False)            

class SupplierLocationView(View):
    def get(self, request):

        suppliers = Supplier.objects.all().values()
        # suppliers_list = list(suppliers)
        latitude = request.GET['lat']
        longitude = request.GET['lon']
        current_coord = (latitude, longitude)    

        data_json = [ {
            'distance' : distance(current_coord, (d['latitude'], d['longitude'])).m,
            'name' : d['name'],
            'branch' : d['branch'],
            'address' : d['address'],
            'zipcode' : d['zipcode'],
            'phone' : d['phone'],
            'latitude': d['latitude'],
            'longitude' : d['longitude'],
        } for d in suppliers.iterator() ]

        sorted_list = sorted(data_json, key = lambda i: i['distance'])

        return JsonResponse(sorted_list, safe=False)

class SupplierFavoriteView(View):

    @login_required
    def post(self, request, pk):

        supplier = get_object_or_404(Supplier, id=pk)
        customer = get_object_or_404(Customer, id=request.user.id)

        if supplier.favorite.filter(id = request.user.id).exists():
                supplier.favorite.remove(customer)
                return JsonResponse({'message':'favorited'}, status=200)
        else :
                supplier.favorite.add(customer)
                return JsonResponse({'message':'Unfavorited'}, status=200)