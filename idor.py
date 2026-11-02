
from flask import Flask, session, request, redirect, abort

app = Flask(__name__)
app.secret_key = "secret123"

users = {
    1: {"username": "alice", "password": "alice123",
        "name": "Alice", "email": "alice@gmail.com"},
    2: {"username": "bob", "password": "bob123",
        "name": "Bob", "email": "bob@gmail.com"}
}

@app.route("/")
def home():
    return """
    <h2>IDOR Practical</h2>
    <a href="/login">Login Here</a>
    """

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        for uid, user in users.items():
            if user["username"] == username and user["password"] == password:
                session["user_id"] = uid
                return redirect(f"/user/{uid}")

        return "Invalid username or password!"

    return """
    <h2>Login Page</h2>
    <form method="POST">
        Username: <input type="text" name="username" required><br><br>
        Password: <input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
    """

@app.route("/user/<int:user_id>")
def user_details(user_id):

    # IDOR Prevention
    if session.get("user_id") != user_id:
        abort(403)

    if user_id not in users:
        return "User not found"

    user = users[user_id]

    return f"""
    <h2>Welcome, {user['name']}!</h2>
    <p>Email: {user['email']}</p>
    <a href="/logout">Logout</a>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(port=5000)
