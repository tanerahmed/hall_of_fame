from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall


def home(request):
    return render(request, 'halls/home.html')


def dashboard(request):
    return render(request, 'halls/dashboard.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    # Customize signup form, when user is created logged into the site
    def form_valid(self, form):
        # before return view ('home/') just do logged in the user and than return view ('home')
        view = super(SignUp, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateHall(generic.CreateView):
    model = Hall
    fields = ['title']
    template_name = 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    # Customize create hall form
    # When create hall we assigned to the user which created the hall
    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect('home')


class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'halls/detail_hall.html'


class UpdateHall(generic.UpdateView):
    model = Hall
    template_name = 'halls/update_hall.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')


class DeleteHall(generic.DeleteView):
    model = Hall
    template_name = 'halls/delete_hall.html'
    success_url = reverse_lazy('dashboard')