from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST.get('listing')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        if listing_id is not None and listing.strip() and phone.strip() and email.strip():
            contact = Contact(listing=listing, listing_id=listing_id, name=name,
                              email=email, phone=phone, message=message, user_id=user_id)
            contact.save()
            send_mail(
                'Property lisiting enquery',
                'There has been an enqery for '+listing + '.',
                'varunkapoor031@gmail.com',
                ['vkvarunkapoor1994@gmail.com'],
                fail_silently=False
                )
            messages.success(
                request, 'Your request has been succesfully submitted.')
        else:
            messages.success(
                request, 'Please enter valid Data.')
        return redirect('/listings/'+listing_id)
