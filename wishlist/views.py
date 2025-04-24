from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import get_user_model
import datetime

from .models import WishlistElement, WishList, UserProfile
User = get_user_model()

# Create your views here.
def index(request):
    """View function for home page"""

    return render(
        request,
        'index.html',
        context={
            'users': UserProfile.objects.all()
        }
    )



def homeRedirect(request):
    print('starting')
    if request.user.is_authenticated:
        print(request.user)
        return HttpResponseRedirect(reverse('user-lists', args=[request.user]))
    
    else:
        return HttpResponseRedirect('/')


def userLists(request, username):
    lists = WishList.objects.all().filter(author=User.objects.get(username=username))
    return render(
        request,
        'wishlist/lists.html',
        context={
            'username': username,
            'user_lists': lists,
        }
    )





def wishListView(request, username, title):
    user = User.objects.get(username=username)
    # list = WishList.objects.get(author=user, title=title)
    list = WishList.objects.get(id=title)
    elements = WishlistElement.objects.filter(list=list)

    context = {
            'object_list': elements,
            'list': list
        }

    
        


    return render(
        request,
        'wishlist/wishes.html',
        context=context,
    )



from django.views.generic.edit import UpdateView, CreateView
from .forms import WishUpdate, DeleteForm, ListUpdate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

        

@login_required
def wishUpdateView(request, username, title, pk):
    element = WishlistElement.objects.get(id=pk)


    if request.user.username != username:
        return render(request, 'wishlist/forbidden.html')

    ##### POST_SECTION #####
    if request.method == 'POST':
        form = WishUpdate(request.POST)
        print(request.POST)
        
        if form.is_valid():
            data  = form.cleaned_data

            element.name = data['name']
            element.notes = data['notes']
            element.link = data['link']
            element.status = data['status']
            element.date = element.date
            element.save()            

            return HttpResponseRedirect(reverse('wish-list', args=[username, title]))
        

    #### GET_SECTION ####
    else:
        data = {'name':element.name, 'notes':element.notes, 'link':element.link, 'status': element.status}
        form = WishUpdate(data)

        context = {
            'form': form,
            'object': element
        }

        return render(request, 'wishlist/wishlistelement_form.html', context)



@login_required
def wishDeleteView(request, username, title, pk):
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            element = WishlistElement.objects.get(id=pk)
            element.delete()
    
    return HttpResponseRedirect(reverse('wish-list', args=[username, title]))


from django.utils.text import capfirst

@login_required
def wishAddView(request, username, title):
    if request.user.username != username:
        return render(request, 'wishlist/forbidden.html')



    if request.method == 'POST':
        form = WishUpdate(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            el = WishlistElement()
            el.name = data['name']
            if el.name == '':
                el.name = f'Wish #{len(WishlistElement.objects.all())}'
            el.link = data['link']
            el.status = data['status']
            el.notes = data['notes']
            date = datetime.date.today().strftime('%Y-%m-%d')
            el.date = date
            el.list = WishList.objects.get(id=(title))

            el.save()

            return HttpResponseRedirect(reverse('wish-list', args=[username, title]))


    else:
        # form = WishUpdate({'name':f'Wish #{len(WishlistElement.objects.all())}'})
        form = WishUpdate()
        context = {
            'form': form
        }

        return render(request, 'wishlist/wishadd.html', context)
    





@login_required
def listEdit(request, username, title):
    mylist = WishList.objects.get(id=title)

    if request.user.username != username:
        return render(request, 'wishlist/forbidden.html')


    if request.method == 'POST':
        form = ListUpdate(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            mylist.title = capfirst(data['title'])
            mylist.description = data['description']

         
            mylist.save()
                
        
        return HttpResponseRedirect(reverse('wish-list', args=[username, title]))
    

    else:
        form = ListUpdate({'title': mylist.title, 'description':mylist.description})
        context = {
            'form': form,
            'list': mylist,
            'username': username,
            }
        return render(request, 'wishlist/listedit.html', context)



@login_required
def listDelete(request, username, title):
    mylist = WishList.objects.get(id=title)

    if request.user.username != username:
        return render(request, 'wishlist/forbidden.html')


    if request.method == 'POST':
        form = DeleteForm(request.POST)

        if form.is_valid():
            # data = form.cleaned_data['deletion']
            

            # if data == True:
            #     print('daje')
            mylist.delete()
                
        
        return HttpResponseRedirect(reverse('user-lists', args=[username]))
    

    else:
        form = DeleteForm()
        context = {
            'form': form,
            'list': mylist,
            }
        return render(request, 'wishlist/deleter.html', context)
    

@login_required
def listCreate(request, username):
    
    if request.user.username != username:
        return render(request, 'wishlist/forbidden.html')


    if request.method == 'POST':
        form = ListUpdate(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            el = WishList()
            el.title = capfirst(data['title'])
            if el.title == '':
                el.title = f'My List'
            el.description = data['description']
            date = datetime.date.today().strftime('%Y-%m-%d')
            el.date = date
            el.author = User.objects.get(username=username)

            el.save()

            return HttpResponseRedirect(reverse('wish-list', args=[username, el.title]))


    else:
        form = ListUpdate()
        context = {
            'form': form
        }

        return render(request, 'wishlist/listadd.html', context)
    