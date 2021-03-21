from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls 

from search import views as search_views
from home import views as home_views
from account import views as account_views

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    path('account/', include('django.contrib.auth.urls')),
    url(r'account/register/$', account_views.register_user, name='register'),
    
    # Charge Codes
    url('create-chargecode', home_views.create_chargecode, name="create-chargecode"),
    url('get-chargecode', home_views.get_chargecode, name="get-chargecode"),
    url('delete-chargecode', home_views.delete_chargecode, name="delete-chargecode"),
    # url('edit-chargecode', home_views.edit_chargecode, name="edit-chargecode"),

    # Task Authorizations
    url('create-taskAuth', home_views.create_taskauth, name="create-taskAuth"),
    url('get-taskAuth', home_views.get_taskauth, name="get-taskAuth"),
    url('delete-taskAuth', home_views.delete_taskauth, name="delete-taskAuth"),

    # Events
    url('add-event', home_views.add_event, name="add_event"),
    url('remove-event', home_views.remove_event, name="remove_event"),
    url('update-event', home_views.update_event, name="update_event"),
    url('get-events', home_views.get_events, name="get_events"),
    url('get-ccs', home_views.get_chargecodes, name="get_ccs"),
    #url('get-tables',home_views.get_tables, name='tables'),
    # url('^update_event$', home_views.update_event, name='update'),
    # url('^remove_event', home_views.remove_event, name='remove'),

    # url('/', account_views.redirect_unauth, name ='redirect-unauth'),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
