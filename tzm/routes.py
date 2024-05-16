# coding=utf-8
# refer to https://www.python.org/dev/peps/pep-0263/ about encoding detail
# Author: CHIH JEN LEE
# hosais@gmail.com
from flask import Flask, session, render_template, request, redirect, url_for, abort
from flask import render_template
from flask.helpers import flash

from tzm import tzservices
from tzm.forms import RegisterForm, LoginForm


from tzm.model import User
from flask_login import login_user, logout_user, login_required


# linebot part to initial receive requests
from tzm.tzbot import YOUR_CHANNEL_SECRET
from linebot import WebhookHandler

handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@tzservices.route("/")
def home_page():
    return render_template("home.html")


@tzservices.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # in form validation, user_name and email address will be checked
        user_to_create = User(
            {
                "username": form.username.data,
                "email_address": form.email_address.data,
                "cart_total": 1000,  # <- need to change in the future
            }
        )
        # password will be hashed and save to dict sturcture
        user_to_create.password = form.password1.data
        print("insert a user")
        user_to_create.insert_doc()
        login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.getField('username')}",
            category="success",
        )

        return redirect(url_for("menu_page"))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a user: {err_msg}", category="danger"
            )

    return render_template("register.html", form=form)


@tzservices.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.find_by_username(form.username.data)
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            # login_user need self.id as unique key to put in session data.
            flash(
                f'Success! You are logged in as: {attempted_user.getField("username")}   ',
                category="success",
            )
            return redirect(url_for("home_page"))
        else:
            flash(
                "Username and password are not match! Please try again",
                category="danger",
            )

    return render_template("login.html", form=form)


@tzservices.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("home_page"))


@tzservices.route("/cart")
def cart_page():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user = users[username]
        return render_template("cart.html", user=user)
    else:
        print("No username found in session")


@tzservices.route("/menu")
@login_required
def menu_page():
    return render_template("menu.html")


@tzservices.route("/order")
def order_page():
    return render_template("order.html")


@tzservices.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    tzservices.logger.info("Request body: " + body)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"
