
This is a webforum project!

You can see an example site at djangoforums.herokuapp.com.

The apps are split into a few different functionalities.

Profiles, naturally, deals with user profiles. At this point a user has only a small degree
of customization available, but I'm toying with ways to change that.

The centerpiece of the site is an old-school internet forums.

Lastly, the directmessages app allows users to send private messages to one another.

Commits as of 4/20/15:

    - directmessages app is now complete. Users can view conversations with other users in a threaded
        format.
    - the search functionality is complete. Upon entering a search term in the navbar, the search
        function will query the database for users, thread titles, and post content that
        contains the search terms.
    - tests for the forums app have been rewritten to account for changes in functionality.
        the "testutils" file under the main project directory is for commonly used functions.
        Future changes include more additional moderation tools, and additional profile
        features.



    
Commits as of 4/14/15:

    - added querysets to display most popular thread in a given forum on the index page.
    - added pagination to thread and forum views.
    - upon replying to a thread, a decorator verifies that the user is logged in and active.
    - inactive (banned) users will be redirected to a "You've been banned" page.
    - after login, a user will be redirected to the thread they were attempting to post in,
        assuming they weren't logging in from the main page.
    - from the single post view, users now have the option to look at the page their post inhabits.

Commit of 4/10/15, #4:

    - added profile index page with thumbnails and links to profiles.


Commit of 4/10/15, #3:

    - added custom css functionality for forums and threads.
    - The an admin user will need to make the upload. Please see the file titled "sample.css"
        for an example of which elements the file needs to touch in order to display properly.


Commit of 4/10/15, #2:

    - "profile" page now includes a user's favorite thread and forum.

Commit as of 4/10/15:

    - continued directmessage app spike
    - directmessages app now includes inbox, outbox, and conversation viewing.
    - inbox and outbox include buttons that display dialogs with message content.
    - directmessages app now includes composition of new messages. Replies are not yet available.
    - spiked directmessages app is almost complete - only feature to add is the reply, and tests.