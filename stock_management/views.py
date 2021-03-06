from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import csv
from .models import Stock, StockHistory, StockRequestHistory
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, ReorderLevelForm, CategoryCreateForm, MakeRequestForm
from django.contrib.auth.decorators import login_required
from .decorators import teacher_only, manager_only, unauthenticated_user


# Create your views here.

def home(request):
    title = 'Welcome to Jaytwih Stock System'
    context = {
        "title": title,
    }
    return render(request, "home.html", context)


@login_required
def list_approval(request):
    title = 'My Requests'
    form = MakeRequestForm(request.POST or None)
    # edit
    user = request.user
    queryset = StockRequestHistory.objects.filter(request_by=user)

    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockRequestHistory.objects.filter(
            stock__item_name__icontains=form['item_name'].value()
        )
        if (category != ''):
            queryset = queryset.filter(stock__category_id=category)
    context = {
        "form": form,
        "title": title,
        "queryset": queryset,
    }
    return render(request, "my_list.html", context)


@login_required
@manager_only
def list_item(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "form": form,
        "title": title,
        "queryset": queryset,
    }
    # if request.method == 'POST':
    #     queryset = Stock.objects.filter(category__icontains=form['name'].value(),
    #                                     item_name__icontains=form['item_name'].value()
    #                                     )
    if request.method == 'POST':
        category = form['category'].value()
        queryset = Stock.objects.filter(
            item_name__icontains=form['item_name'].value()
        )
        if (category != ''):
            queryset = queryset.filter(category_id=category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of Stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

        context = {
            "form": form,
            "title": title,
            "queryset": queryset,
        }
    return render(request, "list_item.html", context)


# @login_required
# def select_item (request):
#     title = 'Make Request'
#     form = MakeRequestForm(request.POST or None)
#     queryset = Stock.objects.all()
#     if request.method == 'POST':
#         #category=form['field'].value() - it a function to get form field value
#         category = form['category'].value()
#         #joining two querysets togeher with filter - sql similtude of
#         #select itemname.value() where TABLE Stock category_id = formvalue
#         #so the category_id belongs is a foreignkey. know as ordinary id in category Table
#         #category here is a the form value. #form['field'].value() function, #in quotes because its string
#         #so once we use a foreignkey the items of the foreign key becomes part of the table (inheritance - inherits all).
#         #so filter this table where querysetfield = value passed in from the form
#         #QuerysetTotal = queryset1.filter(foreignkey[similarfield||not necessary fk]=formvalue)
#         #not necessary fk so far it has the tablename before i.e category_id = tablecategory with the field id
#         #icontans filters the text but because the new field is a pk. in the database table it is referenced with a key
#         #in the database table the new field is not text, so we cannot use icontains. its a number - id referenced to a text in the category table
#         #now we have two filters here because we are filtering based on two criteria from forms i.e (item_name and category)
#         queryset = Stock.objects.filter(
#             item_name__icontains=form['item_name'].value()
#         )
#         if (category != ''):
#             queryset = queryset.filter(category_id=category)
#     context = {
#         "form": form,
#         "title": title,
#         "queryset": queryset,
#     }
#     return render(request, "select_item.html", context)

@login_required
@manager_only
def add_items(request):
    # StockCreateForm
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('list_item')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)


@login_required
@manager_only
def add_category(request):
    form = CategoryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Created')
        return redirect('list_item')
    context = {
        "form": form,
        "title": "Add Category",
    }
    return render(request, "add_items.html", context)


@login_required
@manager_only
def update_items(request, pk):
    # query the dbtable model to get the specific id,pk, record or (queryset for a record)
    queryset = Stock.objects.get(id=pk)
    # the result/instance of the query should be displayed in this form
    form = StockUpdateForm(instance=queryset)
    # after getting the instance is the user decides to post/if the request is post .... line below
    if request.method == 'POST':
        # post into the instance of the form i.e request to post into the query set
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('list_item')

    context = {
        'form': form
    }
    # update and add items using the same form
    return render(request, 'add_items.html', context)


@login_required
@manager_only
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('list_item')
    return render(request, 'delete_items.html')


@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


@login_required
@teacher_only
def request_items(request, pk):
    # telling request here that our primary key is same as the id in our models,py file; id=pk
    queryset = Stock.objects.get(id=pk)
    # the below code is requesting the post on the instance. i.e updating the instance & instance is the M.O.G-ID
    # note in a database all the row, records go together. a call to the id calls the entire row/record
    # queryset.approval = False
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        # if the form is valid, then save into record the new issue quantity
        # then after saving the new issue quantity, subtract it from issue quantity by the code below
        # instance.quantity -= instance.issue_quantity
        # instance.request_by = str(request.user)
        messages.success(request, str(instance.item_name) + " " + "Requested SUCCESSFULLY and PENDING Approval. ")
        # instance.save()
        # here we are calling an entire model here StockHistory to write/record the following parameters into its own database
        request_history = StockRequestHistory(
            stock=instance,
            request_by=str(request.user),
            request_quantity=instance.request_quantity,
            approval1 = 'Pending',
        )
        request_history.save()
        # here the new model is saving everything written to its database
        return redirect('list_approval')
        # return redirect('/stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Requested By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


@login_required
@manager_only
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        # if form is valid, first save the instance temporarily (don't comit) then do calculation(substraction), then save the instance again
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        # instance.receive_by = str(request.user)
        instance.save()
        receive_history = StockHistory(
            # stock_id=instance.id,
            # last_updated=instance.last_updated,
            stock=instance,
            receive_quantity=instance.receive_quantity,
            receive_by=str(request.user)
        )
        receive_history.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.item_name) + "s now in Store")

        return redirect('list_item')
        # return redirect('/stock_detail/' + str(instance.id))
    # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Receive ' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Received By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


@login_required
@manager_only
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(
            instance.reorder_level))

        return redirect("list_item")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_items.html", context)


@login_required
def list_history(request):
    title = 'Purchases'
    # receive history
    queryset = StockHistory.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, "purchase_history.html", context)


@login_required
# @manager_only
def request_list_history(request):
    title = 'LIST OF ITEMS'
    # receive history
    queryset = StockRequestHistory.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, "list_history.html", context)


from itertools import chain


@login_required
@manager_only
def approve_items(request, pk):
    # this_stock = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset = StockRequestHistory.objects.get(id=pk)
        # ap =  Approval.object.get(stockrequest_id=queryset)
        this_stock = Stock.objects.get(id=queryset.stock_id)
        #just 1 made the diffrence in code below - Thank you JESUS
        if queryset.request_quantity <= this_stock.quantity:
            if queryset.approval1 == 'Pending':
                this_stock.quantity -= queryset.request_quantity
                this_stock.save()
                queryset.approval1 = 'Approved'
                queryset.approved_by = str(request.user)
                queryset.save()
                messages.success(request, "Approved and Issued SUCCESSFULLY. " + str(this_stock.quantity) + " " + str(
                    this_stock.item_name) + "s now left in Store")
                return redirect('request_list_history')
            elif queryset.approval1 == 'Rejected':
                messages.error(request, 'Approval previously Rejected')
                pass
            else:
                messages.error(request, 'Previously Approved')
                pass
                return redirect('request_list_history')
            queryset.save()
        else:
            messages.error(request, 'Quantity Requested more than Available Stock')
            return redirect('request_list_history')
            pass
    return render(request, 'approve_items.html')

# ajax
def load_item_name(request):
    category_id = request.GET.get('category_id')
    item_names = Stock.objects.filter(category_id=category_id).all()
    return render(request, 'item_name_dropdown_list_options.html', {'item_names': item_names})


######temp
# @login_required
# @manager_only
# def list_item(request):
#     form = StockSearchForm()
#     queryset = Stock.objects.all()
#     if request.method == 'POST':
#         # category = form.data.get('category')
#         category = form['category'].value()
#         print(category)
#         # if (category != ''):
#         #     form.fields['item_name'].queryset = Stock.objects.filter(category_id=2)
#         # form = StockSearchForm(request.POST)
#         # if form.is_valid():
#             # form.save()
#             # return redirect('list_item')
#     return render(request, "list_item.html", {'form': form})
#########

#duplicate - testing filter
@login_required
@teacher_only
def select_item(request):
    title = 'Make Request'
    form = MakeRequestForm(request.POST or None)
    queryset = Stock.objects.all()
    if request.method == 'POST':
        item = request.POST.get('item_name')
        cat = request.POST.get('category')
        print(item)
        print(cat)
        q1 = Stock.objects.filter(
            item_name__icontains=item)
        if (cat != ''):
            queryset = q1.filter(category=cat)
    context = {
        "form": form,
        "title": title,
        "queryset": queryset,
    }
    return render(request, "select_item.html", context)


# 2222222222
#search modified
from django.db.models import Q
@login_required
def search(request):
    title = 'Search'
    # form = SearchForm(request.POST or None)
    if request.method == 'POST':
        q = request.POST.get('search', '')
        if q:
            queryset = Stock.objects.filter(Q(item_name__icontains=q) | Q(category__name__icontains=q)).distinct()
            count = queryset.count()
            context = {
                # "form": form,
                "title": title,
                "query": q,
                "results": queryset,
                "count": count
            }
            return render(request, 'search.html', context)
        else:
            messages.error(request, 'No search Input')
            pass
    return redirect ('/')

# #search previous
# from django.db.models import Q
# @login_required
# def search(request):
#     title = 'Search'
#     form = SearchForm(request.POST or None)
#     if request.method == 'POST':
#         # q = form.data['search']
#         q = request.POST.get('search', '')
#         # cat = request.POST.get('category')
#         # print(item) #my_debug
#         # print(cat) #my_debug
#         if q:
#             # (q != ''):
#             queryset = Stock.objects.filter(Q(item_name__icontains=q) | Q(category__name__icontains=q)).distinct()
#             count = queryset.count()
#         else:
#             # redirect ('home')
#             #this is done to prevent errors if tthe error (queryset| count referenced before assignt if and empty form is posted)
#             queryset = []
#             count = []
#     context = {
#         "form": form,
#         "title": title,
#         "query": q,
#         "results": queryset,
#         "count": count
#     }
#     return render(request, 'search.html', context)
