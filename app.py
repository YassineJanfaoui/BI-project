from flask import Flask, request, redirect, url_for, flash, session, render_template_string

app = Flask(__name__)
app.secret_key = "worldcup2022key"

# ==============================
# USERS
# ==============================
users = {
    "mohamedyassine.janfaoui@esprit.tn": {"password": "admin2022", "role": "Directeur Sportif"},
    "farah.boubaker@esprit.tn": {"password": "coach2022", "role": "Entraîneur France"},
    "rayen.aloui@esprit.tn": {"password": "recruit2022", "role": "Recruteur France"},
}

# multiple Power BI dashboard (RLS controls what each user sees)
# Map roles to dashboard URLs
DASHBOARD_URLS = {
    "Directeur Sportif": "https://app.powerbi.com/reportEmbed?reportId=7a2266a9-4920-4683-a606-86089ba6dbc7&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730&filterPaneEnabled=false&navContentPaneEnabled=false",
    "Entraîneur France": "https://app.powerbi.com/reportEmbed?reportId=bfc752d9-fab3-4e4f-88c3-15c3cd28de0c&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730&filterPaneEnabled=false&navContentPaneEnabled=false",
    "Recruteur France": "https://app.powerbi.com/reportEmbed?reportId=4796c976-389c-48be-b868-887d4db694c0&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730&filterPaneEnabled=false&navContentPaneEnabled=false",
}

# ==============================
# LOGIN
# ==============================
@app.route("/", methods=["GET", "POST"])
def login():
    login_html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" type="image/png" href="{{ url_for('static', filename='2022_FIFA_World_Cup.svg.png') }}">
        <title>Coupe du Monde 2022 | Connexion</title>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Montserrat', sans-serif;
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #8A1538, #c0c0c0);
                color: #FFF8E1;
            }
            .card {
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                text-align: center;
                width: 360px;
                backdrop-filter: blur(6px);
            }
            h1 { font-size: 1.8em; margin-bottom: 10px; color: #FFF8E1; }
            input {
                width: 80%; padding: 12px; margin: 8px 0;
                border: none; border-radius: 8px;
                font-size: 14px;
            }
            button {
                width: 80%;
                padding: 12px;
                background-color: #9f2344;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: 0.3s;
            }
            button:hover { background-color: #FFF8E1;color: #8A1538; }
            .error {
                background-color: rgba(255,0,0,0.7);
                padding: 10px;
                border-radius: 8px;
                
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="card">
    <img src="{{ url_for('static', filename='2022_FIFA_World_Cup.svg.png') }}" alt="World Cup 2022" style="width:100px;margin-bottom:15px;">
    <h1>World Cup 2022</h1>
    <h3>Portail des utilisateurs</h3>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="error">{{ messages[0] }}</div>
        {% endif %}
    {% endwith %}
    <form method="POST">
        <input type="text" name="username" placeholder="Email" required>
        <input type="password" name="password" placeholder="Mot de passe" required>
        <button type="submit">Se connecter</button>
    </form>
</div>
    </body>
    </html>
    """

    if request.method == "POST":
        username = request.form.get("username").strip().lower()
        password = request.form.get("password").strip()
        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        flash("Identifiants incorrects.")

    return render_template_string(login_html)

# ==============================
# DASHBOARD
# ==============================
@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))

    role = users[user]["role"]
    dashboard_url = DASHBOARD_URLS.get(role, DASHBOARD_URLS["Directeur Sportif"])  # fallback

    dashboard_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" type="image/png" href="{{ url_for('static', filename='2022_FIFA_World_Cup.svg.png') }}">
        <title>{role} | Tableau de bord</title>
        <style>
            body {{
                margin: 0;
                background-color: #F7E7CE;
                color: #8A1538;
                font-family: 'Montserrat', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
            }}
            header {{
    background-color: #8A1538;
    color: #F7E7CE;
    width: 90%;
    padding: 5px 40px;
    margin: 0px auto 0 auto;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}}

.header-buttons {{
    display: flex;
    gap: 15px;
}}

.logout, .chatbot {{
    background-color: #D4AF37;
    color: #8A1538;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    text-decoration: none;
    font-weight: 600;
    transition: background-color 0.2s ease;
}}

.logout:hover, .chatbot:hover {{
    background-color: #e6c85b;
}}
            iframe {{
                width: 77%;
                height: 650px;
                border: none;
                border-radius: 15px;
                margin-top: 30px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }}
            .logout {{
                background-color: #D4AF37;
                color: #8A1538;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                text-decoration: none;
                font-weight: 600;
            }}
            footer {{
                margin-top: auto;
                padding: 15px;
                color: #8A1538;
            }}
        </style>
    </head>
    <body>
        <header>
    <h2>{role}</h2>
    <div class="header-buttons">
        <a href="{{{{ url_for('logout') }}}}" class="logout">Déconnexion</a>
        <a href="/chatbot" class="chatbot">Chatbot</a>
    </div>
</header>
        <iframe src="{dashboard_url}" allowFullScreen="true"></iframe>
        <footer>© 2025 FIFA Analytics | Coupe du Monde 2022</footer>
    </body>
    </html>
    """
    return render_template_string(dashboard_html)

# ==============================
# LOGOUT
# ==============================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
