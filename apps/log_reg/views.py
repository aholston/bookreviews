from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.

def index(request):
    if 'userid' in request.session:
        return redirect("/home")
    return render(request, 'log_reg/index.html')

def addreview(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'log_reg/addbook.html', context)

def logout(request):
    del request.session['userid']
    return redirect('/')

def user(request, id):
    user = User.objects.get(id=id)
    reviews = Review.objects.filter(user=id).order_by('-created_at')
    total_reviews = reviews.count()
    recent_reviews = []

    x = 0
    while x < int(total_reviews) and x < 3:
        print reviews[x].book.title
        recent_reviews.append(reviews[x])
        x = x + 1

    context = {
        'user': user,
        'recent_reviews': recent_reviews,
        'total_reviews': total_reviews
    }
    return render(request, 'log_reg/user.html', context)

def viewbook(request, id):
    book = Book.objects.get(id=id)
    users = User.objects.all()
    reviews = Review.objects.filter(book=book.id)

    context = {
        'book': book,
        'reviews': reviews
        }


    if 'latest_review' in request.session:
        my_review = Review.objects.get(id=request.session['latest_review'])

        if my_review.book.id == book.id:
            context['my_review'] = my_review

    return render(request, 'log_reg/book.html', context)


def register(request):
    errors = User.objects.validate(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        pwHash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        newUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwHash)
        request.session['userid'] = newUser.id

    return redirect('/home')

def home(request):
    if not Review.objects.all():
        context = {
            'user': User.objects.get(id=request.session['userid'])
        }
        return render(request, 'log_reg/home.html', context)
    reviews = Review.objects.order_by('-created_at')
    recent_reviews = []
    x = 0
    while x < 3:
        recent_reviews.append(reviews[x])
        x = x + 1

    book_scroll = Book.objects.all()


    context = {
        'user': User.objects.get(id=request.session['userid']),
        'recent_reviews': recent_reviews,
        'book_scroll': book_scroll
    }
    return render(request, 'log_reg/home.html', context)

def login(request):

    try:
        user = User.objects.get(email=request.POST['email'])

        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['userid'] = user.id
            return redirect('/home')
        else:
            message.error(request, 'Password invalid')
            return redirect('/')
    except Exception:
        messages.error(request, 'Email not found, please register or use a different email')
        return redirect('/')

def addbook(request):
    user = User.objects.get(id=request.session['userid'])

    if 'hidden' in request.POST:
        book = Book.objects.get(id=request.POST['hidden'])
        review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], user=user, book=book)
        request.session['latest_review'] = review.id
        return redirect('/viewbook/'+str(book.id))



    if Book.objects.filter(title=request.POST['title']):
        books = Book.objects.filter(title=request.POST['title'])
        test = Book.objects.get(id=21)

        for x in books:
            y = 'X'
            print y

            if x.author.name == request.POST['new_author']:
                print 'here'
                author = Author.objects.get(books=x.id)
                print author.id
            if x.author.name == request.POST['new_author'] or x.author.name == request.POST['listed']:
                book = x
                print 'here2'
                review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], user=user, book=x)
                request.session['latest_review'] = review.id
                return redirect('/viewbook/'+str(x.id))




    if 'listed' in request.POST and request.POST['listed'] != 'none':
        print request.POST
        author = Author.objects.get(id=request.POST['listed'])
        book = Book.objects.create(title=request.POST['title'], author=author)
        review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], user=user, book=book)
        return redirect('/viewbook/'+str(book.id))

    if 'new_author' in request.POST:
        author = Author.objects.create(name=request.POST['new_author'])
        book = Book.objects.create(title=request.POST['title'], author=author)
        review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], user=user, book=book)
        request.session['latest_review'] = review.id
        return redirect('/viewbook/'+str(book.id))
