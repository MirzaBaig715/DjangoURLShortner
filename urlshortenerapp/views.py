from django.shortcuts import render
from urlshortenerapp.models import Line
import re
import random
from collections import deque
# Create your views here.

dictionary = {}  # for storing the url_name and url e.g 'lawsuit': 'http://youtube.com/'
queue = deque([])  # for storing the url key name for reuse of keys later


class Count(object):
    count = 0


def search_url(request):
    """

    :param request:
    :return: display the form for input Url
    """
    return render(request,'get_link_form.html')


def display_url(request):
    """

    :param request:
    :return: display the shortened Url with complete link
    """
    # check if the input is not None
    check = request.GET['url_input']
    if check is None or check == "":
        # if None then display input Url page
        return render(request, 'get_link_form.html')
    # if there is input
    if check:
        url = request.GET['url_input']
        key = ""
        # list_url will have the splitted url in list
        list_url = url_func(url)
        # if user has shortened more than 10000 Url's then reuse the previous one's
        if Count.count >= 10000:
            key = reuse_func(list_url,url)
        else:

            key = use_wordlist(list_url,url)
        # count++ each time user enters the Url
        Count.count += 1
        return render(request, 'result_form.html', {'url_key': key, 'url': dictionary[key], 'q':queue})


def url_func(url):
    """

    :param url: Url to be split
    :return: splitted url in a list
    """
    if not url.endswith('/'):
        # if end Url do not have '/' then insert it
        url = url + '/'
    # extract the domain name of Url e.g .com, .se , .org etc
    s = re.sub('\.[a-z]*/', ' ', url)
    # extract the special character and strip to 5 elements for 'http'/'https'
    s = re.sub(r'\W+', ' ', s)[5:].strip()
    # reverse the list order so that we can use search from first index
    list_url = list(s.split(' '))[::-1]
    # if list contains 'www'. Remove it and return the list
    if list_url.__contains__('www'):
        list_url.remove('www')
    return list_url


def use_wordlist(list_url,url):
    """

    :param list_url: splitted url in list form
    :param url: actual Url
    :return: name of the key to which this url associates to
    """
    l = []
    object_name = ""
    # loop through the splitted Url list
    for element in list_url:
        # if element found in wordlist of database
        l = Line.objects.filter(text=element)[:1]
        # if element already exists in dictionary of already shortened Url's
        if element in dictionary.keys():
            # continue with the other element of Url
            l = []
            continue
        if l:
            # if element  found . Store it in string 'object_name'
            object_name = str(l[0])
            # store this element as a key to required Url
            dictionary[object_name] = url
            # also append this name in 'queue' list so that we reuse it later
            queue.append(object_name)
            break
    # if element could not found in database wordlist
    if not l:
        # store all objects in list
        list_objects = Line.objects.all()
        # pick a random word
        randm = random.choice(list_objects)
        while randm in dictionary.keys():
            # loop if the random word is in dictionary keys
            randm = random.choice(list_objects)
        # if a unique word found. Store it in dictionary with a key of Unique random word
        dictionary[randm] = url
        # also append in list queue and return it
        queue.append(str(randm))
        return randm
    return object_name


def reuse_func(list_url,url):
    """
    This function is called when the user has shortened already 10000 Url's

   :param list_url: splitted url in list form
    :param url: actual Url
    :return: name of the key to which this url associates to
    """
    object_name = ""
    # loop through the splitted Url list
    for element in list_url:
        # if element match with the key of dictionary. store it in variable
        if element in dictionary.keys():
            object_name = element
            break
    if object_name:
        # if element found. Pop this element and again append it so that it would be new object
        queue.pop(object_name)
        queue.append(object_name)
        dictionary[object_name] = url
    else:
        # if any word of the provided Url does not match with existing keys
        # pop from left and store the key name
        name = queue.popleft()
        # append the new object with the poped name and also store in dictionary
        queue.append(name)
        dictionary[name] = url
    # return the key name of newly created object
    return  object_name