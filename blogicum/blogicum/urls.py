from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.iternal_server_error'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Если проект запущен в режиме разработки...
# if settings.DEBUG:
#     import debug_toolbar
#
#   # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
#     urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
