from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.PropertyListView.as_view(), name='property_list'),
    path('property/<slug:slug>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('new-projects/', views.new_projects, name='new_projects'),
    path('top-agents/', views.top_agents, name='top_agents'),
    path('agent/<int:pk>/', views.agent_detail, name='agent_detail'),
    path('encyclopedia-properties/', views.encyclopedia_properties, name='encyclopedia_properties'),
    path('propworth/', views.propworth, name='propworth'),
    path('bank-offers/', views.bank_offers_detail, name='bank_offers_detail'),
    path('loan-application/', views.loan_application, name='loan_application'),
    path('loan-application/employment/', views.loan_application_employment, name='loan_application_employment'),
    path('loan-application/loan/', views.loan_application_loan, name='loan_application_loan'),
    path('loan-application/profile/', views.loan_application_profile, name='loan_application_profile'),
    path('rates-trends/', views.rates_trends, name='rates_trends'),
    path('buy-vs-rent/', views.buy_vs_rent, name='buy_vs_rent'),
    path('tips-guides/', views.tips_guides, name='tips_guides'),
    path('emi-calculator/', views.emi_calculator, name='emi_calculator'),
    path('stamp-duty/', views.stamp_duty, name='stamp_duty'),
    path('eligibility-calculator/', views.loan_eligibility, name='loan_eligibility'),
    path('interiors-estimator/', views.interiors_estimator, name='interiors_estimator'),
    path('home-interiors/', views.home_interiors, name='home_interiors'),
    path('sell/', views.sell_property, name='sell'),
    path('area-converter/', views.area_converter, name='area_converter'),
]
