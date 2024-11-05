# Cyber security base - Project 1
This project was made for the [Cybersecurity Project I](https://cybersecuritybase.mooc.fi/module-3.1) mooc.fi course. 

It's a basic web application containing 5 security flaws from the [OWASP Top10 2017 list](https://owasp.org/www-project-top-ten/2017/Top_10) and comments about how to fix these flaws. 

Do not reuse code from this project, as it has multiple extremely dangerous security vulnerabilities.

___

### LINK: [link to the repository](https://github.com/utrox/cybersecuritybase-project-1)
### INSTALLATION:
1. Pull the repo to local
2. Make a virtual environment using `python -m venv .venv`
3. Activate the virtual environment `.\.venv\Scripts\activate`
4. Install packages from requirements.txt: `pip install -r .\requirements.txt`
5. Run `python manage.py makemigrations` and `python manage.py migrate`
6. Create user(s) with `python manage.py createsuperuser` and follow instructions
7. Run `python manage.py runserver` to run the server
8. Log in with your user on `loalhost:8000/admin/`
9. Now you're ready to follow the instructions below to test each vulnerability if you choose to do so.

___

### FLAW 1: A1:2017 - SQL Injection 
[See code](https://github.com/utrox/cybersecuritybase-project-1/blob/15d7755d8154319ec339c09d9aaa35aebd712207/src/friends/views.py#L27)

This attack is one of the most common security risks against databases. The attacker adds malicious SQL code into the SQL query that runs on the database, thus either doing damage (like dropping the database), or accessing information we don't want them to access.

In my example, you can recreate this attack by going to the /add/ endpoint. On this page, you can add another user to your friendlist by entering their username into the searchbox. If you input malicious SQL code as the username, like  `' OR address LIKE '%Helsinki%' --`, the query that's going to run on the database is `SELECT * FROM friends_user WHERE username = '' OR address LIKE '%Helsinki%' --`. When submitting this, a user (if such exist) will be added to our friendlist. Thus we will know that that user lives in Helsinki.

Never trust the user to the point that you put their input into the raw SQL query without prepared statements, stored procedures, or escaping user input. You can simply use Django's ORM to make queries.

```
# Easiest is to just use the ORM way to get the user object
try:
    friend = User.objects.get(id=request.POST['username'])
except User.DoesNotExist:
    return HttpResponse('User not found', status=404)
```

___

### FLAW 2: A2:2017 - Broken Authentication
[See code](https://github.com/utrox/cybersecuritybase-project-1/blob/15d7755d8154319ec339c09d9aaa35aebd712207/src/core/session_manager.py#L3)

Poor session management leads to session highjacking. In this example, we generate the `sessionId` in order. (session-1, session-2, session-3, ... etc)

This makes the application vulnerable, because just as we could in the one of the exercises in the `Securing Software` course, the attacker can hijack other users' sessions by just bruteforcing the sessionIds one-by-one, if they figure out that the generation of these sessionIds are logical, and easy to break.

To test this, you can go to any endpoint (after logging in), opening the developer console, and checking the cookies. You can do it for example by entering `document.cookies` into the console.

It will include a the sessionId, because it is stored in a cookie. It's usually stored in a HttpOnly cookie to protect users from XSS attacks, because that way JavaScript code cannot access, read or use it. I've made it so that you'll be able to view it. The cookie will include something like this: 
`[...] sessionId=session-1 [...]`

You can just skip on using your own session manager, if you are using Django. The default `SessionStore` class takes care of it, and is quite secure. If you are dead set on using your own sessionstore, make sure that the ids that are being generated are not guessable; they don't follow any logic, and are randomly generated. You may use random bits, uuids, or something similar.

___

### FLAW 3: A3:2017 - Sensitive Data Exposure
[See code](https://github.com/utrox/cybersecuritybase-project-1/blob/15d7755d8154319ec339c09d9aaa35aebd712207/src/friends/serializers.py#L17)

Leaking sensitive data about the user is never good. It's usually not this blatant though, it might just be something like sending sensitive data as plaintext instead of using proper methods.

What I did, was just simply include the user's birth date, address, and phone number in the `api/users/` API endpoint itself. This is obviously a really big issue, I think there's nothing else to explain about it.

The fix in this case is simple: just remove it from the `UserSerializer`'s `fields` list. This will make it so that on the endpoint that uses this serializer, those fields will not be accessible. Thus we stop exposing sensitive information.

___

### FLAW 4: A5:2017 - Broken Access Control
[See code](https://github.com/utrox/cybersecuritybase-project-1/blob/15d7755d8154319ec339c09d9aaa35aebd712207/src/friends/views.py#L48)

Not restricting access to some resources is bad practice. Let's say that facebook allowed anyone without restriction to delete posts. Like they didnt check if the user who is requesting the deletion of this particular post is the original poster, or just a random user.

It's important for the web application to have correct access control implemented. For resources, that should only be viewed/modified by certain user(s), it's important to make that check, and dont just allow anyone to do as they please.

In my application, you can test this by creating two users (see above on how). Log in with one user in your browser, then with the other in an incognito window. Add a secret through the `/admin/` page to one of the users. Now go to the `/api/secrets/<id>` endpoint to that particular endpoint with both users, and you'll see that you can see the secret with both of them. You don't even need to be logged in.


To prevent this, we can use some way to make sure the user is logged in, and has access to that particular resource. I've opted to use a decorator function, which checks if the logged in user is the owner of the secret, or not. (See in the code, using the above link.) 

___

### FLAW 5: A7:2017 - Cross-Site Scripting (XSS) Attacks
[See code](https://github.com/utrox/cybersecuritybase-project-1/blob/15d7755d8154319ec339c09d9aaa35aebd712207/src/friends/templates/friends/secret.html#L10)

XSS attacks are when malicious JavaScript code runs on the machine of the user. This can allow attackers to steal cookies, make requests disguised as the user, or redirect users to malicious sites. XSS happens when user inputs aren’t properly sanitized and are displayed as executable code on a web page.

In my application, logged in users have the ability to add secrets on the page `api/secrets/`. On this page, you can see a form. If you enter JavaScript code between `<script></script>` tags, (for example `<script>alert('Get PWNED')</script>`) that code will run every time someone opens that secret (by going to the `api/secrets/<id>/` endpoint, that's using the `secret.html` template), because in the `secret.html` template, the secret is marked with the `safe` template tag.

Django has a built-in way to escape the data before putting it in the HTML. So just dont use the safe tag on unsafe data, and you are good to go. Never trust data entered by users as safe, just like in the case of SQL injection attacks.

