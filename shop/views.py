from django.shortcuts import render

def test_base(request):
    return render(request, 'shop/base.html')