import os
import django
from django.core.management import call_command
from django.db import IntegrityError

def setup():
    """Set up the initial database and create a superuser."""
    try:
        # Make migrations
        print("Making migrations...")
        call_command('makemigrations')
        
        # Apply migrations
        print("Applying migrations...")
        call_command('migrate')
        
        # Create superuser
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            if not User.objects.filter(email='admin@medcare.com').exists():
                print("Creating superuser...")
                User.objects.create_superuser(
                    username='admin',
                    email='admin@medcare.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User',
                    phone_number='+1234567890',
                    address='123 Admin Street'
                )
                print("Superuser created successfully!")
            else:
                print("Superuser already exists.")
                
            # Verify the superuser exists
            admin_user = User.objects.get(email='admin@medcare.com')
            if not admin_user.is_superuser:
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save()
                print("Superuser permissions verified and updated if needed.")
                
        except IntegrityError:
            print("Error: Could not create superuser. The email or username might already be in use.")
        except Exception as e:
            print(f"Error creating superuser: {str(e)}")
            
    except Exception as e:
        print(f"Error during setup: {str(e)}")
        raise

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medcare.settings')
    django.setup()
    setup() 