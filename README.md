# ManageIT

The online version of our platform can be accessed via the following link:

    https://manage--it.herokuapp.com/

Use the folowing default credentials to access a demo account with sample data:

    Username: TEST

    Password: APS12_ZZS8

## Local Environment, how to get started:
1. Clone the github repository of the project, or download the source code. Using your terminal navigate in the root folder “ManageIT”.

2. Confirm that you have python 3 installed. If not, download python from its official website:

    https://www.python.org/downloads/

3. Install Django using the following command in your terminal. “pip” is required for this. If you don’t have “pip” installed, please proceed to install it

    `pip install django`
    
5. Download and setup Postgresql and PgAdmin.

    https://www.postgresql.org/download/
    https://www.pgadmin.org/download/ 
    
5. Create a new database using pgadmin. The credentials used in the source code are

    Database Name: manageitdb
    Database password: password
    
6. Using your terminal use the following commands to download the postgresql adapters for python.

    `pip install psycopg2`
    
    `pip install psycopg2-binary`
    
7. Navigate to the “manageit” folder and open the settings.py in your preferred text editor. Scroll down at the "DATABASE" section and change the name and password according to the credentials you used at step 2.

9. Using your terminal, cd into ManageIT\manageit. Use the following commands to install the required dependencies to run the project.

    `pip install gunicorn`
    
    `pip install django-heroku`
    
    `pip install whitenoise`
    
    `pip install pillow`
    
    `pip install pandas`
    
    `pip install django-session-timeout`
    
    `pip install -U selenium`
    
9. Run the following commands to apply the migrations in your postgresql database

    `python manage.py makemigrations`
    
    `python manage.py migrate `
    
10. (Optional) Go back to your pgadmin database. You should see under the "tables" section that now the database is populated with our django models.

11. Create a superuser account by using the following command and typing your credentials. This will give you access to the admin page of the platform.

     `python manage.put createsuperuser`
     
12. cd .. back to the root folder, ManageIT. Use the following command to run the code:

    `python manage.py runserver`
    
13. Use the link displayed at the terminal, http://127.0.0.1:8000/, to access the platform

# Admin Page:

In order to access the admin page, type "/admin" after the home page url of your working environment:

    Local:  http://127.0.0.1:8000/admin
    Hosted: https://manage--it.herokuapp.com/admin

Use the superuser cretentials to login to the admin page:

    Username: Foxtrot
    Password: qbV5Zj@5M

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
