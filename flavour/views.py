from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <html>
    <head>
        <title>Django Restaurant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            .links { margin-top: 20px; }
            .links a { margin-right: 20px; text-decoration: none; color: #007bff; }
            .links a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Welcome to Django Restaurant!</h1>
        <p>Your Django application is running successfully.</p>
        <div class="links">
            <a href="/admin/">Admin Panel</a>
            <a href="/accounts/login/">Login</a>
            <a href="/accounts/signup/">Sign Up</a>
        </div>
    </body>
    </html>
    """)
