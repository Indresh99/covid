from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.
import requests
import time
import json
import re

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Country
from .serializer import CountrySerializer


class Corona(APIView):
    flag = False

    def get(self, request, format=None):
        country = Country.objects.all()
        serializer = CountrySerializer(country, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response = requests.get('https://www.covidvisualizer.com/api/')
        self.data = json.loads(response.text)
        self.countries_key = list(self.data['countries'].keys())
        self.data_keys = list(self.data.keys())
        self.world_keys = list(self.data['worldwide'].keys())

        name=[]
        flag=[]
        reports=[]
        cases=[]
        deaths=[]
        recovered=[]
        lat=[]
        lng=[]
        deltaCases=[]
        deltaDeaths = []
        for i in range(len(self.countries_key)):
            name.append(self.data['countries'][self.countries_key[i]]['name'])
            flag.append(self.data['countries'][self.countries_key[i]]['flag'])
            reports.append(self.data['countries'][self.countries_key[i]]['reports'])
            cases.append(self.data['countries'][self.countries_key[i]]['cases'])
            deaths.append(self.data['countries'][self.countries_key[i]]['deaths'])
            recovered.append(self.data['countries'][self.countries_key[i]]['recovered'])
            lat.append(self.data['countries'][self.countries_key[i]]['lat'])
            lng.append(self.data['countries'][self.countries_key[i]]['lng'])
            deltaCases.append(self.data['countries'][self.countries_key[i]]['deltaCases'])
            deltaDeaths.append(self.data['countries'][self.countries_key[i]]['deltaDeaths'])
#         print(json.dumps({name, flag}))
        score_titles = [{
           "name": name,
           "flag": flag,
           "reports": reports,
           "cases": cases,
           "deaths": deaths,
           "recovered": recovered,
           "lat": lat,
           "lng": lng,
           "deltaCases": deltaCases,
           "deltaDeaths": deltaDeaths
        } for name, flag, reports, cases,deaths, recovered, lat,lng,deltaCases,deltaDeaths  in zip(  name, 
                                                                                                     flag, 
                                                                                                     reports, 
                                                                                                     cases, 
                                                                                                     deaths, 
                                                                                                     recovered, 
                                                                                                     lat,
                                                                                                     lng,
                                                                                                     deltaCases,
                                                                                                     deltaDeaths)]
            # print(score_titles)
            
        # Country.objects.bulk_create(score_titles)
        # print(len (score_titles))
        # print(list(Country.objects.all()))

        if(list(Country.objects.all()) == []):
            print("if")
            for data in score_titles:
                # print(i)
                serializer = CountrySerializer(data=data)
                # serializer = Country.create(data)
                if serializer.is_valid():
                    serializer.save()
                    flag = True
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if(flag):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("else")
            name = Country.objects.get(name="United States of America")
            id = name.id;
            print(id)
            i=id
            for data in score_titles:
                # print(i)
                t = Country.objects.get(id=i)
                t.name = data['name']
                t.flag = data['flag']
                t.reports = data['reports']
                t.cases = data['cases']
                t.deaths = data['deaths']
                t.recovered = data['recovered']
                t.lat = data['lat']
                t.lng = data['lng']
                t.deltaCases = data['deltaCases']
                t.deltaDeaths = data['deltaDeaths']
                t.save()  
                i = i +1
                # serializer = Country.create(data)
            return HttpResponse("Success")

    


# class Corona(APIView):
#     def __init__(self):
#         response = requests.get('https://www.covidvisualizer.com/api/')
#         self.data = json.loads(response.text)
#         self.countries_key = list(self.data['countries'].keys())
#         self.data_keys = list(self.data.keys())
#         self.world_keys = list(self.data['worldwide'].keys())
    
     
#     def fetch_countries(self, request = None,format=None):
#         name=[]
#         flag=[]
#         reports=[]
#         cases=[]
#         deaths=[]
#         recovered=[]
#         lat=[]
#         lng=[]
#         deltaCases=[]
#         deltaDeaths = []
#         for i in range(len(self.countries_key)):
#             name.append(self.data['countries'][self.countries_key[i]]['name'])
#             flag.append(self.data['countries'][self.countries_key[i]]['flag'])
#             reports.append(self.data['countries'][self.countries_key[i]]['reports'])
#             cases.append(self.data['countries'][self.countries_key[i]]['cases'])
#             deaths.append(self.data['countries'][self.countries_key[i]]['deaths'])
#             recovered.append(self.data['countries'][self.countries_key[i]]['recovered'])
#             lat.append(self.data['countries'][self.countries_key[i]]['lat'])
#             lng.append(self.data['countries'][self.countries_key[i]]['lng'])
#             deltaCases.append(self.data['countries'][self.countries_key[i]]['deltaCases'])
#             deltaDeaths.append(self.data['countries'][self.countries_key[i]]['deltaDeaths'])
# #         print(json.dumps({name, flag}))
#         score_titles = [{
#            "name": name,
#            "flag": flag,
#            "reports": reports,
#            "cases": cases,
#            "deaths": deaths,
#            "recovered": recovered,
#            "lat": lat,
#            "lng": lng,
#            "deltaCases": deltaCases,
#            "deltaDeaths": deltaDeaths
#         } for name, flag, reports, cases,deaths, recovered, lat,lng,deltaCases,deltaDeaths  in zip(  name, 
#                                                                                                      flag, 
#                                                                                                      reports, 
#                                                                                                      cases, 
#                                                                                                      deaths, 
#                                                                                                      recovered, 
#                                                                                                      lat,
#                                                                                                      lng,
#                                                                                                      deltaCases,
#                                                                                                      deltaDeaths)]
# #         print (score_titles)
# # Printing in JSON format
#         return HttpResponse(json.dumps(score_titles))
# #         print(len(name))
# #         print(len(flag))
# #         print(len(reports))
# #         print(len(cases))
# #         print(len(deaths))
# #         print(len(recovered))
# #         print(len(lat))
# #         print(len(lng))
# #         print(len(deltaCases))
# #         print(len(deltaDeaths))


# def main(re):
#     obj = Corona()
#     return(obj.fetch_countries())