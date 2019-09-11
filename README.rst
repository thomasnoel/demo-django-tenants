Une petite démo de django-tenant-schemas
========================================

On va prendre une petite application Django très simple (celle du tutoriel) et la rendre multi-tenant, c'est-à-dire que de cette application, avec le code qui tourne une seule fois, on pourra créer plusieurs sites distincts.

L'outil pour cela est django-tenant-schemas http://github.com/bernardopires/django-tenant-schemas (mais aller voir aussi https://github.com/tomturner/django-tenants)

Avant de se lancer
==================

Il faut, en plus d'un ordinateur avec un clavier et un écran :

* un accès à un PostgreSQL récent (> 9.1)

* la possibilité de modifier ``/etc/hosts`` ou équivalent (DNS) pour créer des noms tels que ``client1.maboite.com``

* ``git``, ``python``, ``virtualenv``... rien d'inhabituel

* aucun courage c'est tout facile et sans risque

Au niveau du ``/etc/hosts``, ajouter quelques noms qui seront ceux de vos clients::

    # ligne à ajouter dans /etc/hosts
    127.0.0.1    client1.maboite.com client2.maboite.com

Créer un virtualenv avec votre technique de favorite, par exemple::

    virtualenv -p python3 venv
    . venv/bin/activate

Installer Django et le module psycopg (pilote PostgreSQL) dans ce virtualenv::

    pip install Django psycopg2-binary

Enfin, faire un clone du présent projet::

    git clone https://github.com/thomasnoel/demo-django-tenants`

L'appli "votes" du tutoriel Django
==================================

Aller dans le répertoire du clone construit juste au dessus. Il contient un
répertoire ̀ django-tutorial` qui est le code du tutorial Django https://docs.djangoproject.com/fr/2.1/intro/

Lancer cette application tout simple::

    cd django-tutorial
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver

Se rendre sur le site http://127.0.0.1:8000, constater que c'est vide, aller
dans l'admin http://127.0.0.1:8000/admin/, ajouter un vote, revenir sur le
site... Voilà une application qui marche.

Si on va sur http://client1.maboite.com:8000 ou https://client2.maboite.com:8000 c'est toujours le même site avec le même contenu. On veut séparer tout ça ! On veut des «tenants» !

On coupe le runserver, on va la rendre l'application multi-tenant.

Installation de django-tenant-schemas
=====================================

On installe le paquet (dans le virtualenv, toujours)::

    pip install django-tenant-schemas

On adapte l'application tutorial pour l'utiliser. Cela se passe **uniquement par settings**. Vous pouvez lire le ``local_settings.py`` et apporter les modification au tutoriel, mais vous pouvez aussi tout simplement inclure ces settings locaux à la fin des settings, en ajoutant un simple ``exec`` à la toute fin de ``mysite/settings.py``::

    # une seule ligne à ajouter à la fin de django-tutorial/mysite/settings.py:
    exec(open('../local_settings.py').read())

Si on lance de nouveau le manager on voit apparaitre de nouvelles commandes::

    cd django-tutorial
    ./manage.py
    (...)
    [tenant_schemas]
        collectstatic_schemas
        createsuperuser
        list_tenants
        migrate
        migrate_schemas
        tenant_command

C'est signe que tout fonctionne. Allons-y pour utiliser la mécanique mise en place.

Création et initialisation de la base
=====================================

On créer la base PostgreSQL attendue (cf ``local_settings.py``)::

    createdb demotenant

Et on l'initialise en y créeant le premier schéma "public"::

    ./manage.py migrate_schemas --shared

On relance l'application::

    ./manage.py runserver

Si on va sur http://client1.maboite.com:8000 ou https://client2.maboite.com:8000, on a le message **No tenant for 'clientX.maboite.com:8000'**. L'application cherche le contenu du tenant associé au nom du site demandé.

Création d'un premier tenant
============================

Laisser le runserver tourner. Dans un autre terminal, appeler le shell Django pour créer un objet "Client" et l'enregistrer::

    ./manage.py shell
    >>> from customers.models import Client
    >>> client = Client(domain_url='client1.maboite.com', schema_name='client1', name='Mon premier client', paid_until='2050-12-31', on_trial=False)
    >>> client.save()

Cela créé aussitôt le schéma dans la base de données. On retourne sur http://client1.maboite.com:8000/ : c'est bon !

Pour ajouter du contenu, on doit aller dans l'admin, pour cela on créé d'abord un superuser. La commande createsuperuser est «tenantisée», elle va demander sur quel site on veut agir::

    ./manage.py createsuperuser
    Enter Tenant Schema ('?' to list schemas): ?
    client1 - client1.maboite.com
    Enter Tenant Schema ('?' to list schemas): client1
    Nom d'utilisateur: client1
    Adresse électronique:
    Password:
    Password (again):
    Superuser created successfully.

Aller sur http://client1.maboite.com:8000/, créer un vote... ça marche comme tout à l'heure.

Création d'un second tenant
===========================

Même principe::

    ./manage.py shell
    >>> from customers.models import Client
    >>> client = Client(domain_url='client2.maboite.com', schema_name='client2', name='Un second succes', paid_until='2050-12-31', on_trial=False)
    >>> client.save()

Puis son admin::

    ./manage.py createsuperuser
    Enter Tenant Schema ('?' to list schemas): ?
    client1 - client1.maboite.com
    client2 - client2.maboite.com
    Enter Tenant Schema ('?' to list schemas): client2
    ...

On a maintenant deux tenants, http://client1.maboite.com:8000/ et http://client2.maboite.com:8000/ dont les contenus sont complétement dissociés.

Et pourtant on n'a rien fait !
==============================

Un ``git diff`` montrera que le seul fichier a avoir bougé, c'est ``setting.py``


Fin de la démo, applaudissement, succès, gloire, richesse.
