from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import LoginView, LogoutView, MainMenuView, AddComingView, AddExpensesView, LeftoversView, \
    MaterialsListView, AddMaterialsView, SendTelegramMessageView, ComingListView, ExpensesListView, DutyListView

app_name = 'sales'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('main-menu/', login_required(MainMenuView.as_view()), name='main_menu'),
    path('add-coming/', AddComingView.as_view(), name='add_coming'),
    path('add-expenses/', AddExpensesView.as_view(), name='add_expenses'),
    path('leftovers/', LeftoversView.as_view(), name='leftovers'),
    path('materials-list/', MaterialsListView.as_view(), name='materials_list'),
    path('add-materials/', AddMaterialsView.as_view(), name='add_materials'),
    path('send_telegram_message/', SendTelegramMessageView.as_view(), name='send_telegram_message'),
    path('coming/', ComingListView.as_view(), name='coming_list'),
    path('expenses/', ExpensesListView.as_view(), name='expenses_list'),
    path('duty/', DutyListView.as_view(), name='duty_list'),
]
