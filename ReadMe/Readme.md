# IamDB API Based Documentation

### 1. Recommended System Configurations

> - BEFORE USING ACTIVATE VENV
> - UBUNTU PREFERRED
>> - Because submitted project uses Ubuntu based Virtual Environment.
> - CONFIGURATION FOR DIFFERENT OS
>> - Create a Virtual Environment
>> - Install Requirements.txt
>> - You're good to go.

### 2. IamDB app URL Structure

| Service Name | API | Methods Allowed | Return |
| ------- | ------- | ----- | --- |
| Sample API | http://127.0.0.1:8000/app/sample | GET | HTTPResponse |
| New User/Sign UP | http://127.0.0.1:8000/app/signup | POST | JSON |
| Sign IN | http://127.0.0.1:8000/app/signin | POST | JSON |
| Fetch All | http://127.0.0.1:8000/app/fetch_all | GET | JSON |
| Search | http://127.0.0.1:8000/app/Search | POST | JSON |
| Update | http://127.0.0.1:8000/app/update | POST | JSON |
| Delete | http://127.0.0.1:8000/app/delete | POST | JSON |

### 3. Utility URL Structure

| Service Name | API | Methods Allowed | Return |
| ------- | ------- | ----- | --- |
| Admin | http://127.0.0.1:8000/superuser | GET | Webpage |
| Default JSON Loader | http://127.0.0.1:8000/load_db/default | GET | mssg "Sample Database Creation Successful" |

### 6. DATABASE Model Structure
![Alt text](./database.png)
> - Special case is in GENRE because it contains list field So to handle that JsonField is used.
>
> - 99popularity is named as _99popularity because of variable naming convention.


### 5. API usage

> ####Sample API
> ```
> Hit 
>   http://127.0.0.1:8000/app/sample
> with GET method
> ```
> - SAMPLE OUTPUT

![Alt text](./sample_response.png)


> ####Sign UP or New User
> ```
> Hit 
>   http://127.0.0.1:8000/app/signup
> with POST method
> {
>   "username": "<sample_username>",
>   "password": "<sample_password>",
>   "email": "<sample@email.com>"
> }
> ```
> - SAMPLE OUTPUT

![Alt text](./signup_response.png)


> ####Sign IN
> ```
> Hit 
>   http://127.0.0.1:8000/app/signin
> with POST method
> {
>   "username": "<sample_username>",
>   "password": "<sample_password>"
> }
> ```
> - SAMPLE OUTPUT
> 
![Alt text](./signin_response.png)

#### _NOTE : Session Management through token authentication implemented._

> ####Search
> ```
> Hit 
>   http://127.0.0.1:8000/app/search
> with POST method
> {
>   "search-key": "<any keyword like 'charlies'>"
> }
> ```
> - SAMPLE OUTPUT
> 
![Alt text](./search_response.png)

#### _NOTE : Case sensitiveness (Uppercase and Lowercase) of search parameter handled, keyword will be searched in every attribute of 'DATABASE'._

> ####Update
> ```
> Hit 
>   http://127.0.0.1:8000/app/update
> with POST method
> {
>    "parameter":"director",
>    "key": "<director's name>",
>    "data": {
>        "movie-name":"<new movie-name>"
>    }
> }
> ```
> - SAMPLE OUTPUT
>
![Alt text](./update_response.png)

#### _NOTE : Handled invalid parameter passing, Also only provided details will be updated._

> ####Update
> ```
> Hit 
>   http://127.0.0.1:8000/app/delete
> with POST method
> {
>    "parameter":"director",
>    "key": "<director's name>"
> }
> ```
> - SAMPLE OUTPUT
>
![Alt text](./delete_response.png)

#### _NOTE : All records that contain similar string in it according to parameter passed will be deleted._


> ####Fetch All
> ```
> Hit 
>   http://127.0.0.1:8000/app/fetch_all
> with GET method
> ```
> - SAMPLE OUTPUT
>
![Alt text](./fetch_all_response.png)

> ###NOTE
>> - #### Superuser or Admins has been kept inaccessable from API access because of the security reasons and only accessed from browser.
>> - #### Only Normal users can login using API.




