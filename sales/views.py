from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib import messages
from sales.models import Materials, Coming, Expenses, StockMaterials, Stock
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from .forms import StockFilterForm
from django.core.paginator import Paginator
import telegram
import logging
from datetime import date
from django.db.models import Q


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'login.html', {"login_form": login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse("sales:main_menu"))
        else:
            messages.error(request, "Неверный логин или пароль.")
            return render(request, 'login.html', {"login_form": login_form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("sales:login")


class MainMenuView(LoginRequiredMixin, View):
    template_name = 'base.html'
    login_url = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        page_title = 'PIM - Меню'
        if hasattr(self, 'title'):
            page_title = self.title
        return render(request, self.template_name, {'page_title': page_title})


class AddComingView(LoginRequiredMixin, CreateView):
    model = Coming
    fields = ['material', 'quantity', 'price', 'arrival_date']
    template_name = 'add_coming.html'
    success_url = reverse_lazy('sales:main_menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_stocks'] = user.stock_set.all()
        context['page_title'] = 'PIM - Приход'

        return context

    def form_valid(self, form):
        user = self.request.user

        if user.stock_set.exists():
            form.instance.stock = user.stock_set.first()
        else:
            form.instance.stock = None

        return super().form_valid(form)


class AddExpensesView(LoginRequiredMixin, CreateView):
    model = Expenses
    fields = ['stock', 'material', 'quantity', 'price', 'on_credit', 'debtor_name', 'expenses_date']
    template_name = 'add_expenses.html'
    success_url = reverse_lazy('sales:main_menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'PIM - Расход'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_stocks = Stock.objects.filter(users=self.request.user)
        form.fields['stock'].queryset = user_stocks
        form.fields['material'].queryset = Materials.objects.filter(remainder__gt=0)
        return form

    def form_valid(self, form):
        selected_stock = form.cleaned_data['stock']
        selected_material = form.cleaned_data['material']
        entered_quantity = form.cleaned_data['quantity']

        if not StockMaterials.objects.filter(stock=selected_stock, material=selected_material).exists():
            form.add_error('material', 'Выбранный материал не найден на выбранном складе.')
            return self.form_invalid(form)

        material_instance = Materials.objects.get(stockmaterials__stock=selected_stock, id=selected_material.id)
        remaining_quantity = material_instance.remainder

        if entered_quantity > remaining_quantity:
            form.add_error('quantity',
                           f'Введенное количество превышает доступное количество ({remaining_quantity}) для выбранного материала на выбранном складе.')
            return self.form_invalid(form)

        return super().form_valid(form)


class LeftoversView(LoginRequiredMixin, ListView):
    model = StockMaterials
    template_name = 'leftovers.html'
    context_object_name = 'leftovers'

    def get_queryset(self):
        user = self.request.user
        accessible_stocks = Stock.objects.filter(users=user)
        queryset = super().get_queryset().filter(quantity__gt=0, stock__in=accessible_stocks)
        form = StockFilterForm(self.request.GET, user=user)

        if form.is_valid():
            stock_filter = form.cleaned_data['stock']
            if stock_filter:
                queryset = queryset.filter(stock=stock_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context['form'] = StockFilterForm(request.GET, user=request.user)
        context['page_title'] = 'PIM - Остаток'

        return context


class MaterialsListView(LoginRequiredMixin, View):
    template_name = 'materials_list.html'
    item_page = 4

    def get(self, request):
        page_title = 'PIM - Материалы'
        if hasattr(self, 'title'):
            page_title = self.title
        materials = Materials.objects.all()
        paginator = Paginator(materials, self.item_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_title': page_title, 'page': page})


class AddMaterialsView(LoginRequiredMixin, CreateView):
    model = Materials
    fields = ['name', 'unit']
    template_name = 'add_materials.html'
    success_url = reverse_lazy('sales:materials_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'PIM - Создание материала'
        return context


class SendTelegramMessageView(LoginRequiredMixin, View):
    async def post(self, request, *args, **kwargs):
        bot_token = '6960789766:AAFCOGJJQ4hP53IOfcuWaBF2jJFGGos84cI'
        chat_id = '-4059381918'
        total_earnings = request.POST.get('total_earnings')
        message = request.POST.get('message')

        try:
            bot = telegram.Bot(token=bot_token)
            await bot.send_message(chat_id=chat_id, text=message)
            await bot.send_message(chat_id=chat_id, text=total_earnings)
        except Exception as e:
            logging.error(f"Ошибка отправки в Telegram: {e}")

        return redirect(reverse('sales:main_menu'))


class ComingListView(LoginRequiredMixin, View):
    template_name = 'coming_list.html'

    def get(self, request, *args, **kwargs):
        page_title = 'PIM - Итог прихода'
        if hasattr(self, 'title'):
            page_title = self.title
        current_user = self.request.user
        start_date = request.GET.get('start_date', date.today())
        end_date = request.GET.get('end_date', date.today())
        print(f"Start Date: {start_date}, End Date: {end_date}")
        user_stocks = Stock.objects.filter(users=current_user)
        coming = Coming.objects.filter(Q(stock__in=user_stocks), Q(arrival_date__date__gte=start_date),
                                       Q(arrival_date__date__lte=end_date)).select_related('stock')
        return render(request, self.template_name, {'page_title': page_title, 'coming': coming})


class ExpensesListView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses_list.html'

    def get_queryset(self):
        current_user = self.request.user
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        user_stocks = Stock.objects.filter(users=current_user)
        stored_start_date = self.request.GET.get('stored_start_date')
        stored_end_date = self.request.GET.get('stored_end_date')

        if stored_start_date:
            start_date = stored_start_date

        if stored_end_date:
            end_date = stored_end_date

        return Expenses.objects.filter(
            stock__in=user_stocks,
            expenses_date__date__range=[start_date, end_date]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'PIM - Итог расхода'
        if hasattr(self, 'title'):
            context['page_title'] = self.title
        context['expenses'] = self.get_queryset()
        return context


class DutyListView(LoginRequiredMixin, View):
    template_name = 'duty.html'

    def get_queryset(self):
        current_user = self.request.user
        start_date = self.request.GET.get('start_date', date.today())
        end_date = self.request.GET.get('end_date', date.today())
        user_stocks = Stock.objects.filter(users=current_user)
        stored_start_date = self.request.GET.get('stored_start_date')
        stored_end_date = self.request.GET.get('stored_end_date')

        if stored_start_date:
            start_date = stored_start_date

        if stored_end_date:
            end_date = stored_end_date

        expenses = Expenses.objects.filter(
            stock__in=user_stocks,
            expenses_date__date__range=[start_date, end_date],
            on_credit=True
        )

        return expenses

    def get(self, request, *args, **kwargs):
        page_title = 'PIM - Итог долга'
        if hasattr(self, 'title'):
            page_title = self.title
        expenses = self.get_queryset()

        return render(request, self.template_name, {'page_title': page_title, 'expenses': expenses})
