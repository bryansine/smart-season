#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# 1. Collect static files
python manage.py collectstatic --no-input

# 2. Sync the database schema
python manage.py makemigrations users fields
python manage.py migrate

# 3. Handle the Superuser
python manage.py shell -c "
from django.contrib.auth import get_user_model; 
User = get_user_model(); 
if not User.objects.filter(username='admin_user').exists():
    User.objects.create_superuser('admin_user', 'admin@example.com', 'password123')
    print('Superuser created.')
else:
    u = User.objects.get(username='admin_user')
    u.set_password('password123')
    u.save()
    print('Superuser password updated.')
"