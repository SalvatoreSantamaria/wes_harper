from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket #make sure import the models
from ..users.models import User

# Create your views here.
def index(req):
  if 'user_id' not in req.session:
    return redirect('users:new')# redirect is changing from /users/mew for the reverse lookup

  context = {
    'user_tickets': Ticket.objects.filter(assignee=req.session['user_id']),
    'other_tickets': Ticket.objects.exclude(assignee=req.session['user_id']),
    'user_info': User.objects.get(id=req.session['user_id'])
  }
  return render(req, 'tickets/index.html', context)

def new(req):#check to see if the users is logged in, and then render the new form
  if 'user_id' not in req.session:
    return redirect('users:new')

  context = {
    "assignees": User.objects.all() #get all the different users. to check, go to the  new.html page, and add {{ assignees }} . see the new.html page for reference to see how to make all assignees options
  }
  return render(req, 'tickets/new.html', context) # ie '/' aka the homepage.

def create(req):
  #to see what happens, use print(req.POST)
  if 'user_id' not in req.session: 
    return redirect('users:new')

  if req.method != 'POST':
    return redirect('tickets:new')

  errors = Ticket.objects.validate(req.POST)
  if errors:
    for error in errors:
      messages.error(req, error)
    return redirect('tickets:new')

  Ticket.objects.create_ticket(req.POST) #w7v1 @ 40 minutes : http://learn.codingdojo.com/m/83/4686/30181. This takes in the form data.
  return redirect('tickets:index')

def show(req, ticket_id): #accept id from the route
  if 'user_id' not in req.session:
    return redirect('users:new')

  try:
    context = {
      'ticket': Ticket.objects.get(id=ticket_id)
    }
  except:
    return redirect('tickets:index')

  return render(req, 'tickets/show.html', context)

def edit(req, ticket_id):
  if 'user_id' not in req.session:
    return redirect('users:new')

  try:
    context = {
      'ticket': Ticket.objects.get(id=ticket_id),
      'priority_list': [1, 2, 3, 4, 5],
      'status_list': ["New", "In Progress", "Done"],
      'assignees': User.objects.all()
    }
  except:
    return redirect('tickets:index')

  return render(req, 'tickets/edit.html', context)

def update(req, ticket_id):
  if 'user_id' not in req.session:
    return redirect('users:new')
  if req.method != 'POST':
    return redirect('tickets:edit', ticket_id)

  errors = Ticket.objects.validate(req.POST)
  if errors:
    for error in errors:
      messages.error(req, error)
    return redirect('tickets:edit', ticket_id)
  
  Ticket.objects.update_ticket(req.POST, ticket_id)
  return redirect('tickets:index')

def delete(req, ticket_id):
  Ticket.objects.delete_ticket(ticket_id)
  return redirect('tickets:index')
