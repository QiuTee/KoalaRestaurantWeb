import psycopg2
from django.dispatch import receiver
from django.db.models.signals import pre_migrate
from django.conf import settings
from django.core.management.base import BaseCommand
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Command(BaseCommand): 
    help = "Check and create database if not exist ="
    def handle(self, *args, **options ):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings.get('PORT','5432')
        
        try: 
            conn = psycopg2.connect(
                database= 'postgres', 
                user = db_user,
                password = db_password, 
                host= db_host, 
                port = db_port
            )
            
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor() 
            
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
            exist = cursor.fetchone()
            
            if exist: 
                print(f"Database already exist")
            else: 
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database {db_name} create successfully")
            
            cursor.close() 
            conn.close()
        except Exception as e : 
            conn.rollback()
            print(f"error : {str(e)}")
        