import json
import os
from IamDB_A.models import movie
from django.http import HttpResponse

def def_loader(request):
    with open(os.getcwd()+"/DB_Loader/sample_data.json","r") as json_file:
        jsn = json.load(json_file)
        for i in jsn:
            _99popularity = i["99popularity"]
            director = i["director"]
            score = i["imdb_score"]
            name = i["name"]
            genre = list()
            for i in i['genre']:
                genre.append(i)

            data_obj = movie()
            data_obj.name = name
            data_obj._99popularity = _99popularity
            data_obj.score = score
            data_obj.director = director
            data_obj.genre = genre
            data_obj.save()

    return HttpResponse("Sample Database Creation Successful")