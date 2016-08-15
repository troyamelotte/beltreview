from django.shortcuts import render, redirect
from .models import User, Book, Author, Review
import bcrypt
from django.contrib import messages
def index(request):
    if 'user' in request.session:
        return redirect('/books')
    return render(request, 'beltreview/index.html')

def register(request):
    check = User.userManager.checkreg(first=request.POST['first'], last=request.POST['last'], alias=request.POST['alias'], email=request.POST['email'], password=request.POST['pass'], confirm_password=request.POST['conf_pass'])
    if check == True:
        passinput = request.POST['pass'].encode()
        hashed = bcrypt.hashpw(passinput, bcrypt.gensalt())
        User.objects.create(first=request.POST['first'], last=request.POST['last'],alias=request.POST['alias'], email=request.POST['email'], password=hashed)
        return redirect('/')
    else:
        for error in check:
            messages.error(request, error)
        return redirect('/books')

def login(request):
    check = User.userManager.checklog(request.POST['loginemail'], request.POST['loginpass'])

    if check[0] == True:
        request.session['user']=check[1].id
        return redirect('/books')
    else:
        for error in check:
            messages.error(request, error)
        return redirect ('/')


    return redirect('/')

def books(request):
    if not 'user' in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user'])
        recentreview = Review.objects.all().order_by('-id')[:3]
        books = Book.objects.all()
        context ={
            'user':user,
            'recentreview':recentreview,
            'books':books
        }
        return render(request, 'beltreview/books.html', context)

def logout(request):
    del request.session['user']
    return redirect('/')

def booksadd(request):
    if not 'user' in request.session:
        return redirect('/')
    authors = Author.objects.all()
    context = {
        'authors':authors
    }
    return render(request, 'beltreview/add.html',context)

def newbook(request):
    if len(request.POST['newauthor'])<1:
        author = Author.objects.get(id=request.POST['authorlist']).name
        check = Book.bookManager.bookchecker(title=request.POST['title'], review=request.POST['review'])
    else:
        author = request.POST['newauthor']
        check = Book.bookManager.bookchecker(title=request.POST['title'], author=author, review=request.POST['review'])
    print('*'*100)
    print(author)
    if check == True and author==request.POST['newauthor']:
        Author.objects.create(name=author)
    if check==True:
        Book.objects.create(title=request.POST['title'], author=Author.objects.get(name=author))
        Review.objects.create(review=request.POST['review'],rating=request.POST['rating'], user =User.objects.get(id=request.session['user']), Book=Book.objects.get(title=request.POST['title']))
        return redirect('/')
    else:
        for error in check:
            messages.error(request, error)
        return redirect('/books/add')

def viewbook(request,id):
    if not 'user' in request.session:
        return redirect('/')
    book = Book.objects.get(id=id)
    reviews = Review.objects.filter(Book=book)
    context={
        'book':book,
        'reviews':reviews
    }
    return render(request, 'beltreview/view.html', context)

def newreview(request,id):
    book = Book.objects.get(id=id)
    check = Review.reviewManager.reviewchecker(review=request.POST['review'])
    if check == True:
        Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], user=User.objects.get(id=request.session['user']), Book=book)
        return redirect('/books/'+str(book.id))
    else:
        for error in check:
            messages.error(request, error)
        return redirect ('/books/'+str(book.id))

def removereview(request, id):
    review = Review.objects.get(id=id)
    book = review.Book.id
    review.delete()
    return redirect('/books/'+str(book))
def account(request, id):
    user = User.objects.get(id=id)
    totreviews = Review.objects.filter(user=user).count()
    booksreviewed = Review.objects.filter(user=user)
    context ={
        'user':user,
        'totreviews':totreviews,
        'booksreviewed':booksreviewed
    }
    return render(request, 'beltreview/user.html', context)
