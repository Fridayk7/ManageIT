# ManageIT

How to get started:

1. Download and setup Postgresql and PgAdmin
    https://www.youtube.com/watch?v=d--mEqEUybA&ab_channel=Telusko
    1b. Create a new database using pgadmin ( I named mine "manageitdb" with password: "password" )
    1c. Using your terminal use the commands (make sure you are inside your django application environment ):
        
        1. pip install psycopg2
        
        2. pip install psycopg2-binary
    1c. Go to your settings.py file and scroll down at the "DATABASE" section
    If you named your database something else, or if you are using another password please change the settings accordingly
    
    Remember that we are talking about "local development" here. So, we are not sharing the same database, just the models. Any data you put in the database will only appear at your local machine.
    When pulling files at github pay attention to the settings.py file. Someone might have changed the password or the name of the database so you will have to put the correct ones that apply for you
    
2. (If you haven't done already) Using your terminal, cd into ManageIT\manageit>
3. use the commands:
   
    `1. pip install gunicorn`
    
   ` 2. pip install django-heroku`
    
    `3. pip install whitenoise`
    
    `4. pip install Pillow`

    `5. python manage.py makemigrations`
    
    `6. python manage.py migrate`

3.5 if you go back to your pgadmin database, you should see under the "tables" section that now the database is populated with our django models

4. Create a superuser account
5. Run the server and log into your account. You should see all the tables and be able to create new entries through the admin page

## Gmail
- `Email:` manageit.easyy@gmail.com
- `PS:` ManageIT321


## PayPal Sandbox

###### (Personal)
- `Email:` Per_SonaL_Sandbox@gmail.com
- `PS:` ManageIT321

###### (Business)
- `Email:` BizNess_Sandbox@gmail.com
- `PS:` ManageIT321
