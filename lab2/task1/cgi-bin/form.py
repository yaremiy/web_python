import cgi
from http import cookies
import http.cookies
import os


cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))

count = cookie.get("count")

if count is None:
    count = 1
    print(f"Set-cookie: count={count} httponly")
else:
    count = int(count.value) + 1
    print(f"Set-cookie: count={count} httponly")

form = cgi.FieldStorage()

text1 = form.getvalue('text1')
text2 = form.getvalue('text2')

variants = ["Maths", "Biology", "Chemistry", "History"]
checked_lessons = []
for lesson in variants:
    if form.getvalue(lesson):
        checked_lessons.append(lesson)
lessons = ", ". join(checked_lessons)

if form.getvalue('language'):
    language = form.getvalue('language')
else:
    language = "Not set"

HTML = f'''
<html>
<head>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <form class="form">
        <h2><b>Обробка даних форм!</b></h2>
        <br>
        First text: {text1}
        <br><br>
        Second text: {text2}
        <br><br>
        So, your choice....: {lessons}
        <br><br>
        You want to study: {language}
            <br><br>
        Count of submit the form: {count}

    </form>
</body>
</html'''
print("Content-type: text/html\r\n\r\n")
print()
print(HTML)
