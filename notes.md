# Get Django
pip install pipenv
pipenv shell # to activate a virtualenv in the given folder
pipenv install django

# Make an 'app' called pollster
django-admin startproject pollster

# Start server
cd pollster
python manage.py runserver 8000

# Apply migrations (database)
Need to apply the migrations to create database table such as the admin table, auth, content-type, sessions
python manage.py migrate

# Create an app called polls
python manage.py startapp polls

# Files
## Models.py
    - Make classes that refer to tables in the database (Question and Choices in poll app)
## Views.py
    - Can render templates. Can render json.

# First Steps
## Make Models
```{python}
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = model.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

## Add App to installed app
vim settings.py
INSTALLED_APPS
Add 'polls.apps.PollsConfig'

## Run the migrations for the model
$ python manage.py makemigrations polls
Will make a file in polls/migrations/0001_inital.py with a Migration class
Then run
$ python manage.py migrate

## Manipulate the data from within a shell
python manage.py shell
from polls.models import Question, Choice
Question.objects.all() # Query all questions
from django.utils import timezone
q = Question(question_text='What is your favorite Python framework?',
             pub_date=timezone.now())
q.save()
print(q.id) # 1
q.question_text # 'What is your favorite python framework'

## Getting the question
```{python}
q = Question.objects.get(pk=1)
#somehow even though choice_set is not defined anywhere, knows
# how to create choice_set and choices.
# some magic
q.choice_set.all()
q.choice_set.create(choice_text="Django", votes=0)
q.choice_set.create(choice_text="Flask", votes=0)
q.choice_set.create(choice_text="Web2Py", votes=0)
q.choice_set.all()
```

## Setup admin area
python manage.py createsuperuser
python manage.py runserver 8000
/admin

Then open polls/admin.py
Add admin.site.register(Question)
Add admin.site.register(Choice)

Refresh

## Better connect Question with choices
comment out admin.site.rigsetr, both lines
```{python}

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields':['question_text']}),
            ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),]

    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
```


## Go back to polls/views.py
```{python}
from .models import Question, Choice

def index(request):
    return render(request, 'polls/index.html')
```

## Open polls/urls.py
```{python}
from django.urls import path
from . import views
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index')
]
```

## Open pollster/urls.py
```{python}
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

## Create a top level templates folder, and index.html
pollster/templates/polls/index.html
Change pollster/pollster/settings.py/TEMPLATES/DIRS = [os.path.join(BASE_DIR, 'templates')]

## Modify templates/base.html
<title>Pollster {% block title %}{% endblock %}</title>
<body>
        <div>
            {% block content %}{% endblock %}
        </div>
</body>

## Extend it from templates.index.html
{% extends 'base.html' %}

{% block content %}
    POLLSIT
{% endblock %}

## Go back to views.py, modify index function
```{python}
# get latest questions
latest_question_list = Question.objects.order_by('-pub_date')[:5]
content = dict(latest_question_list=latest_question_list)
return render(request, 'polls/index.html', context)
```

## Go back to index.html

Add a Card for each Poll

{% extends 'base.html' %}

{% block content %}
<h1 class="tc ma3">Poll Question</h1>
{% if latest_question_list %}
    {% for question in latest_question_list %}
        <article class="center mw5 ba">
            <h1 class="f4 bg-near-black white mv0 pv2 ph3">Title</h1>
            <div class="pa3 bt">
                <p>{{ question.question_text }}</p>
                <!-- Button -->
                <a href="{% url 'polls:detail' question.id %}"
                   class="f5 no-underline black bg-animate hover-bg-black
                        hover-white inline-flex items-center pa3 ba border-box">
                   Vote Now
                </a>
            </div>
        </article>
    {% endfor %}

{% else %}
    <p>Latest question list not set</p>
{% endif %}

{% endblock %}



## Go back to views.py and add in detail view
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/results.html', {'question' : question})

## Add a route for the detail (go to polls/urls.py)
path('<int:question_id>', views.detail, name='detail')

## Add in results in views.py
def results(request, question_id):
   question = get_object_or_404(Question, pk=question_id)
   return render(request, 'polls/results.html', {'question': question})

## Add in results in urls.py
path('<int:question_id>/results/', views.results, name='results')

## Side stuff
{% for choice in question.choice_set.all %}
<div class="form-check">
    <input id="choice{{ forloop.counter }}" class="form-check-input" type="radio" name="choice" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">
        {{ choice.choice_text }}
    </label>
</div.

# then

selected_choice = request.POST['choice']
selected_choices.votes += 1
selecetd_choice.save()
# redirect to results
return HttpResponseRedirect(reverse('polls:results', args=(question.id,))


# Partials
templates/partials/_navbar.html
<nav class="flex justify-between bb b--white-10">
    <div class="container">
        <a class="navbar-brand" href="/">Pollster</a>
    </div>
</nav>

Add to it to base.html

{% include 'partials/_navbar.html' %}

# Add landing page
Make a view in pollster for index and reference it in pollster/urls.py
