##### Configuration tutorial:
1) Register on Vkontakte *www.vk.com* and create a group if you haven't already
2) Create your web-app:

    a) Go to *www.vk.com/dev* and click on "My Apps"

    b) Click "Create app"
    
    c) Choose "Website", enter a title, Website address, Base domain. You can change them later
    
    d) And click "Connect website"
    
    ![Creation](https://sun9-21.userapi.com/c858028/v858028031/1e311c/I0BVEQFMy68.jpg)
3) Go to "Settings". You will need the info here to set up the program
4) Open "config.py";

    a) Copy "App ID" and paste it into CLIENT_ID in the config file
    
    b) Copy "Secure key" and paste it into SECRET_KEY
    
    c) Copy "Service token" and paste it into ACCESS_TOKEN
    
    ![Configuration](https://sun9-3.userapi.com/c858028/v858028031/1e312c/ZIs6PEz-DVQ.jpg)
5) Then you need to find the page's ID, copy it and paste into VK_GROUP_ID **(include the minus before the digits)**

    Everything else will be set up automatically 

6) Host the app to get the URL address;
7) Copy the URL // ex: https://yoursite.com. Paste it into Website address in App/Settings (VKontakte app). Paste it into Base domain omitting 'https://' or 'http://'. Save the changes
    
    ![Getting the URL](https://sun9-21.userapi.com/c858028/v858028031/1e316f/j7iv11eRx8Y.jpg)
8) Go to your group's settings / manage

    a) Open "API usage"
    
    b) Go to "Callback API", paste the URL of your site + '/callback' // ex: https://yoursite.com/callback
    
    ![Configuring Callback API](https://sun9-60.userapi.com/c858028/v858028031/1e3180/oozs3kRJa6M.jpg)
    
    c) Open app/data/posts_callback. Then, before the function docstring paste 'return' + string to be returned (you can find the string on the page with the Callback API settings)
    
    d) Confirm the Callback API for your group and delete the line you pasted previously

And that's all. I hope your app is working.