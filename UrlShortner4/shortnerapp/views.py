from django.shortcuts import render
from forms import UrlForm
from django.views.generic import FormView
from .models import WordList, WordRecord
import re
import random
import datetime


class IndexView(FormView):
    template_name = "search.html"
    form_class = UrlForm

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form, **kwargs):
        """
            If the form is valid
        """
        context = self.get_context_data(**kwargs)
        # clean the url
        original_url = form.cleaned_data['url']
        # split the url in a list
        url = IndexView.splitted_url(original_url)
        # search for url shortened and will return name of word
        get_word_name = IndexView.element_searching(url, original_url)
        # get the object by the name of word
        word = WordList.objects.filter(get_word_name)
        # display the shortened Url
        context['word'] = word.values_list('last_url')
        return render(self.request, "display-search.html", context)

    def form_invalid(self, form, **kwargs):
        """
            If the form is invalid
        """
        context = self.get_context_data(**kwargs)
        context['form'] = UrlForm.clean_url(form)
        return render(self.request, "display-search.html", context)

    def splitted_url(self):
        """

        :return: split the url in a list
        """
        url = self
        if not url.endswith('/'):
            # if end Url do not have '/' then insert it
            url = url + '/'
        # extract the domain name of Url e.g .com, .se , .org etc
        s = re.sub('\.[a-zA-Z]*/', ' ', url).lower()
        # extract the special character and strip to 5 elements for 'http'/'https'
        s = re.sub(r'\W+', ' ', s).strip()
        # reverse the list order so that we can use search from first index
        list_url = list(s.split(' '))[::-1]
        # if list contains list1. Remove it and return the list
        list1 = ['www', 'http', 'https']
        for l in list1:
            if list_url.__contains__(l):
                list_url.remove(l)
        return list_url

    def element_searching(self, original_url):
        """

        :param original_url: the original url
        :return: shortened url
        """
        # splitted url
        url = self
        # WordRecord will keep [used] word records
        used_words = WordRecord.objects.values_list('used_word',
                                                    flat=True
                                                    )
        # all words which are not used yet in db_list
        db_list = WordList.objects.filter(last_url__isnull=True)

        element_found = []
        element_name = ""
        # if there are unused word in database
        if db_list:
            # iterate over splitted url
            for w in url:
                # if a word already used for shortened the other url
                if str(w) in WordRecord.objects.values_list('used_word', flat=True):
                    continue
                # otherwise search in database for a word
                else:
                    element_name = w
                    element_found = WordList.objects.filter(word=w)[:1]
                    # if found in database then break
                    break
            if element_found:
                # delete the object and recreate it with data
                WordList.objects.filter(word=element_name).delete()
                # current datetime
                date = str(datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
                # create the object with same word
                WordList.objects.create(word=element_name,
                                        last_url=original_url,
                                        last_used=date
                                        )
                WordRecord.objects.create(used_words=element_name)
                # return the name of word
                return element_name
            else:
                # if element not found in database
                # pick a random word
                random_word = random.choice(db_list)
                # search for the random word
                element = WordList.objects.filter(word=random_word)\
                    .values_list('word',
                                 flat=True
                                 )
                # get the name of random word
                element_name = str(list(element)[0])
                # delete it from database
                WordList.objects.filter(word=element_name).delete()
                date = str(datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
                # recreate the object with same random word
                WordList.objects.create(word=element_name,
                                        last_url=original_url,
                                        last_used=date
                                        )
                WordRecord.objects.create(used_words=element_name)
                # return the random word name
                return element_name
        # if all words are used then we will reuse them
        else:
            flag = False
            for w in url:
                w = str(w)
                # if the word already shortened and in WordRecords
                if w in used_words:
                    # delete it from database
                    WordList.objects.filter(word=w).delete()
                    date = str(datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
                    # recreate the object with same word
                    WordList.objects.create(word=w,
                                            last_url=original_url,
                                            last_used=date
                                            )
                    WordRecord.objects.create(used_words=w)
                    flag = True
                    element_name = w
                    # return the word name
                    return element_name
            # if word is do not match in database
            if flag is False:
                # pick the first one in descending order by datetime
                element = WordList.objects.values_list('word',
                                                       flat=True
                                                       )[0]
                # get the name of word
                element_name = str(list(element)[0])
                # delete it from database
                WordList.objects.filter(word=element_name).delete()
                date = str(datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
                # recreate the object with same word
                WordList.objects.create(word=element_name,
                                        last_url=original_url,
                                        last_used=date
                                        )
                WordRecord.objects.create(used_words=element_name)
                # return the word name
                return element_name

        return None
