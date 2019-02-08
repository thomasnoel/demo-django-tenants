# -*- utf-8 *-*
#

# https://django-tenant-schemas.readthedocs.io/

# Le moteur de base de données : c'est postgreSQL, mais
# *via* tenant_schemas qui va ajouter sa magie !
DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': 'demotenant',
    }
}
DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

# quand une requête arrive, on la fait passer par tenant_schemas
MIDDLEWARE.insert(0, 'tenant_schemas.middleware.TenantMiddleware')

# le modèle Django qui défini ce qu'est un client (un "tenant", un "locataire")
TENANT_MODEL = "customers.Client" # app.Model

# les applications communes à tous les tenants
SHARED_APPS = [
    'tenant_schemas',  # mandatory, should always be before any django app
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'customers',       # my tenant model
]

# les applications pour les tenants, c'est-à-dire les clients
TENANT_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'polls',
]

# et pour que le reste de Django marche, on fait un INSTALLED_APPS
# qui est la somme de SHARED_APPS et TENANT_APPS (sans doublon)
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# les URLs pour le tenant 'public' sont un peu spécifiques (y'en a pas!)
PUBLIC_SCHEMA_URLCONF = 'customers.urls'

# stockages de media et autres (inutiles ici, mais pour éviter des warning sur le runserver)
DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'

# last but not least
ALLOWED_HOSTS = ['*']
