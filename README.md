# Final report

## Group members
Álvaro García 486051
Vesa Heiskanen 62661W
Jaakko Kaisanlahti 78622A

## Features implemented
### Game-service interaction, saving and loading (Jaakko)
As I have a background in JavaScript development, doing the frontend JavaScript (iframeMessageListener) wasn't that
difficult. The most difficult part was coding the Django backend, since I wasn't familiar with the API.

Scores don't update real-time. You have to reload the page to see the updated high scores list. Doing real-time
updating seemed difficult (this is no AngularJS), so I didn't bother.

Only one save per game per user is supported.

Game-service interaction: 200
Saving / loading: 100

### Styling (Jaakko)
The Bootstrap library was used, and the website was built on Bootstrap supplied starter template. Only
basic classes were used, e.g. form-group, btn, table, etc.


### Mobile friendly (Jaakko)
Making the site mobile friendly was as easy as adding a meta tag to head, including the bootstrap Javascript
and tweaking the game iframe presentation.

Mobile friendly: 50

### Login view (Álvaro)
Manages the login of already registered user. Redirects to the profile.

### Payment service (Álvaro)
All the management of the niksula payment service and related (Games purchases, sales registrations, play permission for each game-user, sales model, game model)

### Store view (Álvaro)
View all the games added to the store.

### Profile (player) (Álvaro)
View all the games that a user has bought.

Score: 300/300

### Tweet feature (Álvaro)
It would redirect to a Twitter page that would tweet the score of the game you've just played. You can
access the stub at /tweet.

Score: 25/50

### Registration (Vesa)

A form where registering information is entered. If submitting the form is unsuccesful a guiding message is displayed above the form. Once registered succesfully the user's information is entered to the database and he is able to use the service immediately.

Since I'm new to web software development and not that familiar with Python it took time to sort out how things work. Things got a bit easier when the project got further. The basic idea of working with forms and GET and POST requests was pretty easy since the coure exercises featured a form exercise. Adding messages was easy.

Email confirmation feature was left unimplemented because I ran out of time. An unconfirmed account would have had the is_active field of the user model set to False and login would require the field to be True. This field would be unlocked by a link sent in an email.

Authentication as a whole: 100

### Developer functionalities, game inventory and sales statistics (Vesa)

A developer can see an extra division in his profile page labeled inventory, where he can see all the games he has added to the service. Beside each game there are buttons for deleting and editing a game, or to show the sales statistics of the given game. Below all the added games there is a button for adding a new game.

Adding and editing a game both use a similar form where the information about the game is entered. Pushing the delete button opens a new view to confirm the action. Messages are displayed to inform the user about the success of the actions mentioned above.

Clicking the 'sales' button beside a game in the inventory opens a view which shows how many times the game has been bought and what is the total income from the sales as well as details from the purchase events. Unfortunately the users' access to the sales data is lost if a game is deleted. A more reasonable approach would be to add e.g. a 'is_active' field to the game model. Inactive games would not be shown for everyone in the service but to the developer himself to see the sales history.

It took some thought to respond to unsuccesful actions.

Developer functionalities: 200

## Non-functional issues
We made features issues in Gitlab. Each issue had a branch worked on by one developer. When he was done, he made
a merge request for review and testing by another developer. The practice worked well, although there were some
bugs and merge issues that slipped through the cracks.


## Instruction on how to use the application and Heroku link

Register and log in. The functionality of the service should be self-explanotory. [Here is the link.](https://powerful-tor-8939.herokuapp.com/)

# Project plan 

## Mandatory features and their implementation

### Authentication

With Django authentication we can require email validation at registering. Django will have its users database with username and password. First view will be a log in form and a register form. When registering, we will create a new user with that password, but they can't login until they have validated their account by email. Users will have to select their role. Once logged in, we will jump to the basic managing window view. 
Once authenticated and accessing to a game, the application will check if the user has bought that game. If not, it will display an error/send you to the game page. When displaying the user's games list it will only show the bought games, therefore we should access the games by this list . This test its to avoid any direct access to a game by typing its URL.

### Basic player functionalities

Different views are implemented for viewing the basic information of the player (bought games etc.), buying games, playing games and searching games.

Users can play games in the ‘play games’ view where information about the game is shown and the game can be played inside an iframe element.

All games view with a search box, can be filtered. Games not matching search criteria won’t be shown.

Payment is handled by a mockup payment service: http://payments.webcourse.niksula.hut.fi/ 

### Basic developer functionalities

A developer can see an extra tab labeled inventory. By clicking it he sees all the games he has added to the service. There will also be a “Add a game” button.

Add a game: Add a game view opens. Dev enters all the required data. After clicking add, the game can be seen in All games view and be bought.

View game data: from inventory the dev can click a game he has added to the service. Doing so opens a view that allows him to modify the game information and see the sales data. Sales data is implemented as a relationship between user and game models, which can be queried for the total sales amounts and purchase times.

### Game / service interaction

The service sends messages to a game containing either a LOAD or a MESSAGE messageType attribute. With LOAD the game can be continued from a saved point. A message with MESSAGE attribute contains information that the service wants to relay to the game (e.g. that there was no gamestate matching the LOAD_REQUEST).

JQuery is used to react to certain events such as when player pushes a ‘Save game’ button. JQuery calls a function that fetches the information needed for a message and sends the message with postMessage.

## Additional features

These following features will be implemented if we have time. They are listed in priority order.

### Save / load feature

A save model is implemented. A save is created when a SAVE message is received. When a LOAD message is received, the application will try to find the a save for that user for that game. If one is found, the data is sent to the game in a message.

### Mobile friendly

Attention is paid to usability on mobile devices (smart phones/tablets)
It works with devices with varying screen width and is usable with touch based devices (see e.g. http://en.wikipedia.org/wiki/Responsive_web_design ) We will make different CSS that will adapt to different screen resolutions and dpi.

### Social media sharing

A simple sharing button for each social media site that will include the game’s name and image. Maybe a brief custom message with a high score. 

### RESTful API

There's a Django framework for making RESTful services.

## Views

- login
- registration
- my (purchased) games
- all games
- play game
- Developer: add game, manage a game, my (developed) games

## Models

- user: all are players. A developer is also a player but with more rights
- game
- purchase (connects users with games)
- author (connects developers with their games)


## Teamwork

Tasks are divided between the group members so that each member is liable for a certain part in the project. The group will have weekly meetings to discuss what is achieved so far and to work together to advance the project. Meetings in person are preferred if possible. Group members collaborate also outside the meetings when necessary. A group work service such as Basecamp will be used as the main electronic communication channel between the group members to keep all communication in the same place.

Git branches are used to ensure group members don't interfere with each other's work. A member creates a branch for a small feature, implements and tests it. It's then code reviewed by at least one other member before being merged back to master. Implemented features should be small enough to be finished within one day.

