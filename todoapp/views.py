from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms

class TodoTask():
    def __init__(self, task, idc):
        self.task = task
        self.complete = False
        self.id = idc

class TaskForm2(forms.Form):
    task = forms.CharField(max_length=200, widget = forms.TextInput(attrs={'placeholder': 'type smth..','class': 'form-control mt-2'}))

tasks = []
id_count = []
# Create your views here.
def index(request):
    form = TaskForm2() 
    post_dict = request.POST
    post_items = list(post_dict.items())
    print(post_items)

    if "tasks" not in request.session:
        request.session["tasks"] = []

    try:
        if post_items[1][0].isdigit():
            task_id = post_items[1][0]
            for task in tasks:
                if int(task_id) == task.id:
                    todo = task
    except:
        pass
    print(len(tasks))

    if len(tasks)==0:
        request.session["tasks"] = []
    
    if request.method == 'POST': 
        if "Create Task" in request.POST:
            form = TaskForm2(request.POST)
            if form.is_valid():
                task = post_items[1][1]
                id_count.append(1)
                taskobj = TodoTask(task, len(id_count))
                tasks.append(taskobj)
                session_task_id = request.session["tasks"]
                session_task_id.append(taskobj.id)
                request.session["tasks"] = session_task_id
                print(taskobj.id)
               
            return redirect('/')
        
        elif post_items[1][1] == 'Complete':
            
            if todo.complete == False:
                print(post_items[1][1])
                todo.complete = True     

            elif todo.complete == True:
                print(post_items[1][1])
                todo.complete = False
        
        elif post_items[1][1] == 'Delete':
            print(request.POST)
            print(post_items[1][1])
            tasks.remove(todo)
            request.session["tasks"].remove(todo.id)
        
    
    print(request.session.items())
   
    context = {'tasks': tasks,'form':form, 'session_task_id': request.session["tasks"]}
    return render(request, 'todoapp/list.html', context)
    