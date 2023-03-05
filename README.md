# BattleShip

#create venv and install dependecies:

    Django==4.1
    djangorestframework==3.12.0
    pytz==2022.7.1
    drf-yasg==1.21.5
    

    pytest==7.2.0
    pytest-cov==4.0.0

#Run migrations : </br>
    python manage.py makemigrations </br>
    python manage.py migrate </br>
#Run tests: </br>
    python manage.py test </br>
#Run server: </br>
    python manage.py runserver </br>

## Endpoints
**/api/status/** - Status endpoint </br>
**api/battle?ships=10,6,4,5** - Battle endpoint</br>
**/api/swagger/** - Swagger endpoint</br>
**/api/redoc/**  - Redoc endpoint </br>

