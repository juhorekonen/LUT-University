# urls.py
from django.urls import path
	 
	from .views import homePageView, taskView, addView
	 
	urlpatterns = [
	    path('', homePageView, name='home'),
	    path('tasks', taskView, name='tasks'),
	    path('add', addView, name='add'),
	]
	 


# views.py
from django.shortcuts import render
	from django.http import JsonResponse
	from django.views.decorators.csrf import csrf_exempt
	import json
	 
	# Create your views here.
	 
	tasks = ['Wash the car', 'Finish the project', 'Build a time machine']
	 
	def taskView(request):
		return JsonResponse({'tasks' : [{'name': t} for t in tasks]})
	 
	 
	@csrf_exempt # this exempt would not be ok in production without replacement csrf protection
	def addView(request):
		name = 'untitled'
		if request.method == 'POST':
			body = json.loads(request.body)
			name = body.get('name', 'untitled').strip()
	 
		tasks.append(name)
		return JsonResponse({'name' : name})
	 
	 
	def homePageView(request):
		# shorter way of writing instead of loader
		return render(request, 'pages/tasks.html')



# tasks.html
<!DOCTYPE html>
	<html xmlns="http://www.w3.org/1999/xhtml" xmlns:th="http://www.thymeleaf.org">
	    <head lang="en">
	        <meta charset="UTF-8" />
	        <title>Tasks</title>
	    </head>
	    <body>
	 
	        <h2>Tasks</h2>
	 
	        <!-- TODO: add the ability to list tasks -->
	        <ul id="tasks">
	        </ul>
	 
	 
	        <form>
	            <input type="text" name="name" id="name"/>
	            <input type="button" onclick="addTask();" value="Add!"/>
	        </form>
	 
	        <!-- the javascript has been embedded to the same site -->
	        <script inline="javascript">
	            // The URL to the application server that holds the tasks.
	            var url = null;
	 
	            function loadTasks() {
	                // Write loading code here
	                var http = new XMLHttpRequest();
	                http.open("GET", 'tasks', true);
	 
	                http.onreadystatechange = function () {
	                    if (http.readyState === 4) {
	                        if (http.status === 200) {
	                            var tasks = JSON.parse(http.responseText);
	                            for (var i = 0; i < (tasks.tasks).length; i++) {
	                                console.log((tasks.tasks)[i])
	                                addTaskToList((tasks.tasks)[i]);
	                            }
	                        }
	                    }
	                }
	                http.send(null);
	            }
	 
			</script>
	 
	        <script inline="javascript">
	            function addTask() {
	                var name = document.querySelector("#name").value;
	                if (!name) {
	                    return;
	                }
	 
	                console.log(name);
	 
	                var http = new XMLHttpRequest();
	 
					// We are not using any CSRF protection(!) this should not be done in production
	                http.open("POST", 'add', true);
	                http.setRequestHeader("Content-type", "application/json");
	                var data = new Object();
	                data.name = name;
	 
	                http.onreadystatechange = function () {
	                    if (http.readyState === 4) {
	                        if (http.status === 200) {
	                            addTaskToList(JSON.parse(http.responseText));
	                        }
	                    }
	                }
	 
	                http.send(JSON.stringify(data));
	            }
	 
	 
	            function addTaskToList(task) {
	                var liElement = document.createElement("li");
	                liElement.appendChild(document.createTextNode(task.name));
	                document.querySelector("#tasks").appendChild(liElement);
	            }
	 
	 
	            window.onload = function () {
	                loadTasks();
	            };
	        </script>
	    </body>
	</html>