from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from IamDB_A.models import movie
import re


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

            regex_object = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
            if len(regex_object.findall(email)) == 0:
                return "Invalid Email"
            try:
                User.objects.get(username=username)
                return "user already exists"
            except:
                new_user = User.objects.create_superuser(username, email, password)
                new_user.save()
                return True
        else:
            return False

    x = serialize(serialized_data)
    if x == True:
        pk = User.objects.get(username=serialized_data['username']).pk
        token = Token.objects.get(user=pk).key
        data = {"response": "Succesfully registered User",
                "token": token
                }
        status = 200

    elif x == "user already exists":
        data = {
            "response": "User Already Exists"
        }
        status = 409

    elif x == "Invalid Email":
        data = {
            "response": "Invalid Email"
        }
        status = 422

    else:
        data = {
            "response": "Something is missing from Username, Password, Email, Please provide that also!!"
        }
        status = 400

    return JsonResponse(data, status=status)


@api_view(['POST'])
def search(request):
    recv_data = request.data
    search_key = recv_data.get('search-key')
    auth_token = recv_data.get("token")

    x = Token.objects.filter(key=auth_token)
    if auth_token is None or len(x) != 1:
        data = {
            "response": "You're not authenticated to access this feature"
        }
        status = 401

    elif search_key is None:
        data = {
            "response": "Search Key not provided"
        }
        status = 400

    else:
        data = []
        try:
            data.extend(movie.objects.filter(_99popularity__icontains=search_key))
        except:
            pass
        try:
            data.extend(movie.objects.filter(genre__icontains=search_key))
        except:
            pass
        try:
            data.extend(movie.objects.filter(name__icontains=search_key))
        except:
            pass
        try:
            data.extend(movie.objects.filter(director__icontains=search_key))
        except:
            pass
        try:
            data.extend(movie.objects.filter(score__icontains=search_key))
        except:
            pass

        data = set(data)
        temp = []
        for i in data:
            a = {}
            a['movie-name'] = i.name
            a['99popularity'] = i._99popularity
            a['imdb-score'] = i.score
            a['director'] = i.director
            a['genre'] = i.genre
            temp.append(a)
        data = {
            'data': temp
        }
        status = 200

    return JsonResponse(data, status=status)


@api_view(['PATCH'])
def update(request):
    recv_data = request.data
    update_parameter = recv_data['parameter']
    update_key = recv_data['key']
    update_data = recv_data['data']
    auth_token = recv_data.get("token")

    x = Token.objects.filter(key=auth_token)
    if auth_token is None or len(x) != 1:
        data = {
            "response": "You're not authenticated to access this feature"
        }
        status=401

    else:
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
            status = 400
            return JsonResponse(data, status=status)

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
        status = 200

    return JsonResponse(data, status=status)


@api_view(['DELETE'])
def delete(request):
    recv_data = request.data
    parameter = recv_data['parameter']
    key = recv_data['key']
    auth_token = recv_data.get("token")

    x = Token.objects.filter(key=auth_token)
    if auth_token is None or len(x) != 1:
        data = {
            "response": "You're not authenticated to access this feature"
        }
        status = 401

    else:
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
            status = 400
            return JsonResponse(data, status=status)

        for i in record_instances:
            i.delete()
        data = {
            "response": "All matching records are deleted"
        }
        status = 200

    return JsonResponse(data,status=status)


@api_view(['POST'])
def fetch_all(request):
    recv_data = request.data
    auth_token = recv_data.get("token")

    x = Token.objects.filter(key=auth_token)
    if auth_token is None or len(x) != 1:
        data = {
            "response": "You're not authenticated to access this feature"
        }
        status = 401
    else:
        temp = []
        for i in movie.objects.all():
            a = {}
            a['movie-name'] = i.name
            a['99popularity'] = i._99popularity
            a['imdb-score'] = i.score
            a['director'] = i.director
            a['genre'] = i.genre
            temp.append(a)

        data = {
            "data": temp
        }
        status = 200
    return JsonResponse(data, status=status)


@api_view(['POST'])
def signout(request):
    recv_data = request.data
    auth_token = recv_data.get("token")

    x = Token.objects.filter(key=auth_token)
    if auth_token is None or len(x) != 1:
        data = {
            "response": "Invalid User"
        }
        status = 401

    else:
        x.delete()
        data = {
            "response": "Logged Out"
        }
        status = 200

    return JsonResponse(data, status=status)