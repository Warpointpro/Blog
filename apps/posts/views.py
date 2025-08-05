from django.shortcuts import render

def home(request):
    return render(request, 'posts/home.html')
def about(request):
    return render(request, 'posts/acerca_de.html') 