from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Client, Carrier, Auction
from .forms import AuctionForm, CarrierFormForUser


def index(request):
    auction_list = Auction.objects.all()
    return render(request, 'transportation/index.html', locals())


def add_auction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            form.save()
            auction = Auction.objects.last()
            return reverse_lazy('auction_detail', auction.pk)
    form = AuctionForm()
    return render(request, 'transportation/add_auction.html', locals())


def start_timer(request, pk):
    Auction.objects.get(pk=pk).start_timer()
    return redirect('auction_detail', pk)


def stop_timer(request, pk):
    auction = Auction.objects.get(pk=pk)
    auction.stop()
    return redirect('auction_detail', pk)


def auction_detail(request, pk):
    auction = Auction.objects.get(pk=pk)
    form = CarrierFormForUser()
    return render(request, 'transportation/auction_detail.html', locals())


def take_step(request, pk):
    auction = Auction.objects.get(pk=pk)

    if request.method == 'POST':
        form = CarrierFormForUser(request.POST)
        if form.is_valid():
            auction.take_step(request.POST)
            return redirect('auction_detail', auction.pk)
