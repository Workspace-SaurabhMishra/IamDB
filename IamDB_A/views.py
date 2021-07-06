from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from IamDB_A.models import movie


# Create your views here.
@api_view(['GET'])
def sample(request):
    return HttpResponse("API endpoint working fine!!")


@api_view(['POST'])
def signup(request):
    serialized_data = request.data
    data = {}

    def serialize(credentials: "dict"):
        if credentials.get("username") and credentials.get("password") and credentials.get("email"):
            username = credentials["username"]
            password = credentials["password"]
            email = credentials["email"]
            try:
                User.objects.get(username=username)
                return 'User already exists'
            except:
                new_user = User.objects.create_user(username, email, password)
                new_user.save()
                return True
        else:
            return False

    x = serialize(serialized_data)
    if x == True:
        data["response"] = "Succesfully registered User"
        pk = User.objects.get(username=serialized_data['username']).pk
        token = Token.objects.get(user=pk).key
        data["token"] = token

    elif x == "User already exists":
        data = {
            "response": "User Already exists"
        }

    else:
        data = {
            "response": "Something is missing from Username, Password, Email, Please provide that also!!"
        }

    return JsonResponse(data)


@api_view(['POST'])
def search(request):
    data = request.data
    search_key = data['search-key']
    search_result = []
    try:
        search_result.extend(movie.objects.filter(_99popularity__icontains=search_key))
    except:
        pass
    try:
        search_result.extend(movie.objects.filter(genre__icontains=search_key))
    except:
        pass
    try:
        search_result.extend(movie.objects.filter(name__icontains=search_key))
    except:
        pass
    try:
        search_result.extend(movie.objects.filter(director__icontains=search_key))
    except:
        pass
    try:
        search_result.extend(movie.objects.filter(score__icontains=search_key))
    except:
        pass

    search_result = set(search_result)
    temp = []
    for i in search_result:
        a = {}
        a['movie-name'] = i.name
        a['99popularity'] = i._99popularity
        a['imdb-score'] = i.score
        a['director'] = i.director
        a['genre'] = i.genre
        temp.append(a)
    search_result = {
        'data': temp
    }
    return JsonResponse(search_result)


@api_view(['POST'])
def update(request):
    data = request.data
    update_parameter = data['parameter']
    update_key = data['key']
    update_data = data['data']

    if update_parameter == '99popularity':
        record_instances = movie.objects.filter(_99popularity__icontains=update_key)

    elif update_parameter == 'movie-name':
        record_instances = movie.objects.filter(name__icontains=update_key)

    elif update_parameter == 'genre':
        record_instances = movie.objects.filter(genre__icontains=update_key)

    elif update_parameter == 'director':
        record_instances = movie.objects.filter(director__icontains=update_key)

    elif update_parameter == 'imdb-score':
        record_instances = movie.objects.filter(score__icontains=update_key)

    else:
        data = {
            "response": "Invalid updation parameter"
        }
        return JsonResponse(data)

    for record_instance in record_instances:
        try:
            record_instance._99popularity = update_data['99popularity']
        except:
            pass

        try:
            record_instance.name = update_data['movie-name']
        except:
            pass

        try:
            record_instance.director = update_data['director']
        except:
            pass

        try:
            record_instance.genre = update_data['genre']
        except:
            pass

        try:
            record_instance.score = update_data['imdb-score']
        except:
            pass

        record_instance.save()

    data = {
        "response": 'Updation Successful'
    }

    return JsonResponse(data)


@api_view(['POST'])
def delete(request):
    data = request.data
    parameter = data['parameter']
    key = data['key']

    if parameter == '99popularity':
        record_instances = movie.objects.filter(_99popularity__icontains=key)

    elif parameter == 'movie-name':
        record_instances = movie.objects.filter(name__icontains=key)

    elif parameter == 'genre':
        record_instances = movie.objects.filter(genre__icontains=key)

    elif parameter == 'director':
        record_instances = movie.objects.filter(director__icontains=key)

    elif parameter == 'imdb-score':
        record_instances = movie.objects.filter(score__icontains=key)

    else:
        data = {
            "response": "Invalid deletion parameter"
        }
        return JsonResponse(data)

    record_instances.delete()
    data = {
        "response": "All matching records are deleted"
    }
    return JsonResponse(data)


@api_view(['GET'])
def fetch_all(request):
    data = []
    for i in movie.objects.all():
        a = {}
        a['movie-name'] = i.name
        a['99popularity'] = i._99popularity
        a['imdb-score'] = i.score
        a['director'] = i.director
        a['genre'] = i.genre
        data.append(a)

    data = {
        "data": data
    }
    return JsonResponse(data)
