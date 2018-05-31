from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import OLBooksAPIForm
import requests


def get_call_list(form, field_name):
    
    field_content = form.cleaned_data.get(field_name)
    if field_content is '':
        return []

    field_list = map(str.strip, field_content.split(','))
    seperator = f',{field_name}:'
    field_call =  f'{field_name}:' + seperator.join(field_list)
    field_list = field_call.split(',')

    return field_list



# Create your views here.
def redirect_home(request):
    return redirect('home')

@login_required
def home(request):

    form = OLBooksAPIForm(request.POST)
    context = {'form':form}
    
    if form.is_valid():

        call_list = []
        
        # ISBN:0201558025
        call_list += get_call_list(form, 'ISBN')
        
        # OCLC:297222669
        call_list += get_call_list(form, 'OCLC')

        # LCCN:93005405
        call_list += get_call_list(form, 'LCCN')

        # OLID:OL123M
        call_list += get_call_list(form, 'OLID')

        #Set up call to the API
        final_call = ','.join(call_list)
        call_url = 'http://openlibrary.org/api/books?bibkeys='
        call_url += final_call + '&format=json&jscmd=data'

        demo = requests.get(call_url)
        json_reponse = demo.json()

        all_results = []

        #Check for format requested:
        is_raw = form.cleaned_data.get('show_raw')
        
        #Show 'raw' response returned by API
        
        #Need to do:
        #   Some keys are only shown if there is a value.
        #   So need to determine all keys in all JSON responses, then run
        #   values = [json_entry] + [(json_info[key] if key in json_info else '') for key in keys]

        if is_raw:
            first_entry = list(demo.json().keys())[0]
            keys = demo.json()[first_entry].keys()
            keys = list(keys)

            for json_entry in demo.json():
                
                json_info = demo.json()[json_entry]

                values = [json_entry] + list(json_info.values())
                all_results.append(values)                 

        
        #show customized response
        else:
            keys = ['title', 'authors', 'publishers', 'publish_date', 'number_of_pages','url']

            #Need to validate this        
            for identifier in call_list:
                if identifier not in demo.json():
                    continue

                json_info = demo.json()[identifier]

                #Get names of all Authors
                authors = ','.join(author['name'] for author in json_info['authors'])
                
                #Get names of all Publishers
                publishers = ','.join(publisher['name'] for publisher in json_info['publishers'])
                
                values = [json_info['title'], authors, publishers]
                values += [json_info[key] for key in keys[3:]]
                
                values = [identifier] + values
                all_results.append(values) 

        keys = ['bibkey'] + keys
        context['keys'] = keys
        context['all_results'] = all_results
        #context['books'] = json_info
        
        return render(request, 'queries/index.html', context)

    return render(request, 'queries/index.html', context)



def login_view(request):
    
    form = OLBooksAPIForm(request.POST)
    context = {'form':form}
    
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect('/home') # Set to whatever home page will be
    
    return render(request, 'users/form.html', context)
