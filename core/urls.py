"""v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls import url
# from django.contrib.auth.views import login
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path('login/', login),
    path('login/', auth_views.LoginView.as_view()),
    path('', views.index, name='index'),
    # path('accounts/login/', auth_views.LoginView.as_view()),
    # Organizations
    path('organizations/', views.organizations, name='organizations'),
    path('organizations/set/<int:id>', views.set_organization, name='set_organization'),
    # Threats
    path('threats/', views.threats, name='threats'),
    path('threat_list/', views.threat_list, name='threat_list'),
    path('threats/createupdate/', views.createupdate_threat, name='createupdate_threat'),
    path('threats/delete/<int:id>', views.delete_threat, name='delete_threat'),
    path('risk_matrix/', views.risk_matrix, name='risk_matrix'),
    path('threat_chart/', views.threat_chart, name='threat_chart'),
    path('pop_threats/<int:impact>/<int:likelihood>/', views.pop_threats, name='pop_threats'),
    # Vulnerabilities
    path('activities/', views.activities, name='activities'),
    path('activities_list/', views.activities_list, name='activities_list'),
    path('activities/createupdate/', views.createupdate_activity, name='createupdate_activity'),
    path('activities/delete/<int:id>', views.delete_activity, name='delete_vulnerability'),

    path('vulnerabilities/', views.vulnerabilities, name='vulnerabilities'),
    path('vulnerability_list/', views.vulnerability_list, name='vulnerability_list'),
    path('vulnerability/createupdate/', views.createupdate_vulnerability, name='createupdate_vulnerability'),
    path('vulnerability/delete/<int:id>', views.delete_vulnerability, name='delete_vulnerability'),
    # Recommendations
    path('recommendations/', views.recommendations, name='recommendations'),
    path('recommendation_list/', views.recommendation_list, name='recommendation_list'),
    path('recommendation/createupdate/', views.createupdate_recommendation, name='createupdate_recommendation'),
    path('recommendation/delete/<int:id>', views.delete_recommendation, name='delete_recommendation'),
    # Reports
    path('reports/', views.reports, name='reports'),
    path('report_list/', views.report_list, name='report_list'),
    path('report/createupdate/', views.createupdate_report, name='createupdate_report'),
    path('report/delete/<int:id>', views.delete_report, name='delete_report'),
    path('report/view_html/<int:id>', views.view_report, name='view_report'),
]
