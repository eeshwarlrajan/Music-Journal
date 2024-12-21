# Music Journal

#### Video Demo:  [https://youtu.be/KCFsOoftRbQ?si=qzC-IREZw0ghzZ2t](https://youtu.be/KCFsOoftRbQ?si=qzC-IREZw0ghzZ2t)

#### Description: A flask web-application that allows users to log reviews and ratings for their favourite albums which can be looked up using the last fm api and view them as their virtual music collection.

# app.py

## /Login

### This route carries out the process of logging in the user by ensuring they provide inputs on the input fields on the server-side and by looking up the database to check whether their inputted username exists in the database’s users table and wheter it matches with the chosen password. If it doesnt, it renders an error page, “input\_error.html” otherwise it renders “library.html”.

# /

### This route fetches all the album information from the library table in the database to display on “library.html”

## /register

### This route ensures the user provides input for the username, password, and confirm password fields. It then looks up to check wheter the given username is already taken, and if the confirmed password matches the password, and adds the details to the users table in the database. It then redirects to the login page when successful.

## /search

### This gets a query from the search page and passes it to the last.fm API which returns the JSON information front the API and stores it in the albums variable, which is passed to search\_results.html.

## /add

### Adds selected albums from the search results to the albums database table.

## /review/\<album\_id\>

### Takes the user to a specific album’s review page when clicked on from the library.

## /submit\_review/\<album\_id\>

### This ensures an input is received from the user for the album review and rating, and then adds that information to the albums database where the user\_id is that of the user logged in.

## /remove/\<album\_id\>

### This removes a the selected album from the user’s library from the library table in the database.

## /logout

### Logs out the currently logged in user.

# helpers.py

## Login\_required

### Used in app.py to define routes where login is required.

# musicjournal.db

## Users Table

### Contains information about user accounts (id, username and password hash)

## Library Table

### Contains every album that has been added to the database from the search results, with a foreign key of user\_id that references the user id in the users table.

# Templates

## Added.html

### Confirmation when an album is added to the library database table from the search results.

## Confirmation\_error.html

### Displays an error message when the confirmed password doesn’t match with the given password when user creates an account.

## Input\_error.html

### Displays an error message when an invalid username or password is provided when attempting to login with an invalid username or password.

## Layout.html

### Displays a navigation bar when the user is logged in. imports bootstrap, fonts, and styles.css for css stylings.

## Library.html

### Displays all the albums the users have added to the library in a grid. Gets flash messages from app.py for when an album is added or removed successfully.

## Login.html

### Displays a login field with text inputs for username and password, and a button to submit the form.

## Register.html

### Displays 3 input fields for username, password, and password confirmation, as well as a button for submitting the form.

## Review.html

### Displays a review page for the selected album from the library, as well as a text form for leaving a review, an existing review if one had been left previously, and drop-down menu for selecting a rating.

## Search\_results.html

### Displays the search results from the search query pulled from the last fm api in a card-grid style. Includes an add to library button on each one.

## Search.html

### Displays a search bar for users to type in search queries for albums.

# styles.css

### Various stylings, including a universal site-wide font, hover effects, rounded corners and padding.

# Other notes.

### As an avid music lover, I’ve always valued having a physical music collection in the form of cds. That also stemmed from my love for album covers and how they relate and add to the meaning and sonics of an album. I wanted to put album covers as the forefront, which is why my library only displays them, as it would be in a CD or Vinyl record collection. To maintain a streamlined design (and because of me being a newbie with this stuff) I chose a simple webpage design, inspired by a tutorial from the Youtube Channel “Ludiflex”. Adding a rating system without numerical values was my way of keeping track of wheter you enjoyed an album, without having to apply a concrete number on it, as its not realistic to grade such a subjective matter that way. 

## Credits: 

### Search Icon in search page from: icons8

### Login and Sign up page, overall webpage theming inspired by YouTube Channel “Ludiflex”. General guidance and debugging from ChatGPT 4o/4o-mini.

### I am Eeshwar Leninrajan, this was my CS50 Final project

## 

