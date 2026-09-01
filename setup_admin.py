import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

# Verifica se já existe um admin, se não, cria.
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@oficina.com', 'admin123')
    print("========================================")
    print("✅ USUÁRIO CRIADO COM SUCESSO!")
    print("👤 Usuário: admin")
    print("🔑 Senha:   admin123")
    print("========================================")
else:
    # Se já existir, reseta a senha para garantir
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("========================================")
    print("✅ SENHA DO ADMIN RESETADA COM SUCESSO!")
    print("👤 Usuário: admin")
    print("🔑 Senha:   admin123")
    print("========================================")
