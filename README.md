
This is a simple webforum project. This is the master branch for the project -
another repository with the original code will be set up shortly.

Special features will be detailed upon completion.

Commit as of 4/9/15:

    - spiked directmessages app. Untested and incomplete.
    - modified the following in profiles/views:
        - removed old code for "register_or_login"
        - deleted EditProfileView
        - ProfileView is now a subclass of UpdateView
            - Profile form submissions are done via a jquery dialog.
        - added LoginView
        
    - modified the following in forums/models:
        - removed the forum_group field on Forum model that limited the number of possible forums.
        - added a new field called Category which is a foreignkey to the new Category model.
    
    - modified the following in forums/views:
        - ForumIndexView is now a ListView of the Category model.
            - the template cycles through different color labels derived from base.css
    
    - added paginator block to base.html
            
            