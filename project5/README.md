
# Distinctiveness and Complexity: 
I have created a personal calendar for this capstone project. I believe that it is sufficiently distinct from other projects as it does not resemble any of CS50W projects. I have implemented the datetime field from Django which was hardly used at all in this course. Learning to use django datetime field was a challenge to me as I had to figure out python datetime package as well as making queries with django datetime field. To further challenge myself, I have decided to improve the UI of the application such as researching on ways to generate random colours so that Weekview would be more interactive.  

# What’s contained in each file you created:

### In models.py:
I have created 2 classes:

- **User** inherits from AbstractUser

- **Event** inherits from models.Model. The class **Event** requires 5 field, **user** which is a ForeignKey to the class User, **eventname** would be a character field, **description** would be a text field, **when** would be a datetime field and lastly, **till** would also be a datetime field. It also contains 3 function addtional function. **serailize** returns the serailized format for JSONresponse. The next two function **whenhourandmin** and **tillhourandmin** returns the time in HHMM format which helps for easier computation.


### In views.py:
I have created 3 'helper' functions namely 'weeks', 'weekchecker' and 'leapyear'. 

- **weeks**: takes in two arguments year and month and returns a list of 6 weeks starting from the first of the month. In each of the week, it also displays the date and month.

- **weekchecker**: takes in an arguement of a week and returns a 'proper' formatted week. In short, it determines if the week spills into the next or previous month and        whether the previous,current and next month has 28,29,30 or 31 days.

- **leapyear**: takes in an argument of year and returns true if the current year is a leap year.

I have also created 9 functions namely 'index', 'othermonth', 'weekview', 'eventapi', 'weekeventapi', 'editevent', 'login_view', 'logout_view' and 'register'.
 
- **index**: Shows the current month of the year and filters events that are currently in this month as well as created by the user. It also checks if the user is authenticated. If the user is authenticated, it displays the index page. Else, it prompts the user to login. If user submits a PUT request, it takes in the request and creates a new event.

- **othermonth**: Takes in two arguments year and month and shows that particular month and filters events that are in the month as well as created by the user. It also allows user to create new event in that particular month.

- **weekview**: Displays the current week in 30min fragments and filters events that are currently in that week.

- **editevent**: Allows user select an event to update/delete.

- **eventapi**: Filters the events based on the user as well as the current month and year and returns a JSONresponse.

- **weekeventapi**: Filters the events based on the user and the current week and returns a JSONresponse.

- **login_view**: Authenticates logins and redirecting to index page if login is successful.

- **logout_view**: Logs the user out.

- **register**: Registers the user.

### In urls.py:

It contains all of the url of this applications

### In templates folder:
- **layout.html**: Consist of the navbar styled using bootstrap. All of the templates uses the layout page.

- **index.html**: Displays the current month with the dates. Additionally, displays the upcomming events in the current month as well as a form for creating new event. There is also an up and down button to toggle between months.

- **othermonth.html**: Displays the current toggled month with the dates. Additionally, displays the upcomming events in the current toggled month as well as a form for creating new event.

- **weekview.html**: Displays the current week in 30min fragments.

- **editevent.html**: Displays a select menu where user can select the event they want to edit/delete. Additonally, it displays the specific form for which event is selected

- **register.html**: Displays a form where user can register.

- **login.html**: Displays the login page.

### In static folder:
- **index.js**: index.html and othermonth.html uses this script. Once DOM is loaded, it changes the display style of the form for creating a new event to be none. Once the user clicks on a specific date, it changes the display style of the form to block, allowing user to type into the form to create a new event on the day they have clicked on. Once the user submits the form it sends a PUT request to the index function in views.py. Additionally, it fetchs data from eventapi in views.py to set a different background color for dates that have events.

- **editevent.js**: editevent.html uses this script. Once DOM is loaded, it changes the display style of all forms for editing to be none. Once a user selects an event to be edited, the respective form would have its display style changed to block. The form will be pre-populated with its existing details but user can edit and update its details.

- **weekview.js**: weekview.html uses this script. Once DOM is loaded, it fetches data from weekeventapi in views.py. If there are events during this week, the timeframe background color would be changed. The colors are random and different for different events.

# How to run the application

Run "python manage.py runserver" to run the project.

After logging in, it displays the current month. User can click on a specific date on the month and a form would appear on the right. This form is for user to create an event on the date that is clicked. After creating an event, it would appear in the Upcomming section of the page.  
User can also toggle through the months with an up and down button on the top left of the page. Clicking on dates of other months would also show the form for creating events.  
User can view the current week in 30min fragments when they click on Weekview in the navbar.  
User can edit or delete events when they enter edit event page on the nav bar.
