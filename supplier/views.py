from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Supplier
from user.utils import login_required
from user.models import User
from django.core import serializers
from geopy.distance import distance
import json, boto3
import my_settings


class SupplierAllView(View):
    def get(self, request):

        import pdb; pdb.set_trace()


        data = Supplier.objects.all().values()
        data_json = [ {
            'name' : d['name'],
            'supplier_id' : d['id'],
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
                'supplier_id' : d['id'],
                'branch' : d['branch'],
                'address' : d['address'],
                'zipcode' : d['zipcode'],
                'phone' : d['phone'],
                'latitude': d['latitude'],
                'longitude' : d['longitude'],
                'img_src' : "https://s3-siren.s3.ap-northeast-2.amazonaws.com/samsung_starbucks.jpeg"
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
            'supplier_id' : d['id'],
            'branch' : d['branch'],
            'address' : d['address'],
            'zipcode' : d['zipcode'],
            'phone' : d['phone'],
            'latitude': d['latitude'],
            'longitude' : d['longitude'],
        } for d in suppliers.iterator() ]

        sorted_list = sorted(data_json, key = lambda i: i['distance'])
        first_ten_list = sorted_list[:10]
        
        return JsonResponse(first_ten_list, safe=False)

class SupplierFavoriteView(View):

    @login_required
    def post(self, request, pk):

        supplier = get_object_or_404(Supplier, id=pk)
        user = get_object_or_404(User, id=request.user.id)

        if supplier.favorite.filter(id = request.user.id).exists():
                supplier.favorite.remove(user)
                return JsonResponse({'message':'favorited'}, status=200)
        else :
                supplier.favorite.add(user)
                return JsonResponse({'message':'Unfavorited'}, status=200)


class FileView(View):

    s3_client = boto3.client(
        's3',
        aws_access_key_id= my_settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key= my_settings.AWS_SECRET_ACCESS_KEY
    )

    def post(self, request):
        file = request.FILES['filename']

        self.s3_client.upload_fileobj(
            file, 
            "s3-test-wecode",
            file.name,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        return HttpResponse(status= 200)