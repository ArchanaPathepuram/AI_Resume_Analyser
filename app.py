from flask import Flask, render_template, request, redirect, session
from db import Base, engine, SessionLocal
import models
import PyPDF2
import docx
import json
from ai import analyze_resume

from flask_mail import Mail, Message
import random
import os
from dotenv import load_dotenv


app = Flask(__name__, template_folder="template")

app.secret_key = "secret123"


load_dotenv()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

# Create database tables
Base.metadata.create_all(bind=engine)


# =========================
# HOME
# =========================

@app.route("/")
def home():

    if "user" in session:
        return redirect("/dashboard")

    return redirect("/login")


# =========================
# SIGN UP
# =========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    db = SessionLocal()

    try:

        if request.method == "POST":

            email = request.form.get("email")
            password = request.form.get("password")

            existing_user = (
                db.query(models.User)
                .filter_by(email=email)
                .first()
            )

            if existing_user:
                return "User already exists"

            user = models.User(
                email=email,
                password=password
            )

            db.add(user)
            db.commit()

            return redirect("/login")

        return render_template("signup.html")

    finally:
        db.close()


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    db = SessionLocal()

    try:

        if request.method == "POST":

            email = request.form.get("email")
            password = request.form.get("password")

            user = (
                db.query(models.User)
                .filter_by(
                    email=email,
                    password=password
                )
                .first()
            )

            if user:

                session["user"] = user.email

                return redirect("/dashboard")

            else:

                return "Invalid credentials"

        return render_template("login.html")

    finally:
        db.close()


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect("/login")

    result = None

    if request.method == "POST":

        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")

        file = request.files.get("file")

        # =========================
        # FILE HANDLING
        # =========================

        if file and file.filename != "":

            # ---------- PDF ----------
            if file.filename.lower().endswith(".pdf"):

                try:

                    pdf_reader = PyPDF2.PdfReader(file)

                    text = ""

                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""

                    resume_text = text

                except Exception as e:

                    result = {
                        "error": f"Error reading PDF: {str(e)}"
                    }


            # ---------- DOCX ----------
            elif file.filename.lower().endswith(".docx"):

                try:

                    doc = docx.Document(file)

                    text = ""

                    for para in doc.paragraphs:
                        text += para.text + "\n"

                    resume_text = text

                except Exception as e:

                    result = {
                        "error": f"Error reading DOCX: {str(e)}"
                    }


        # =========================
        # ANALYZE RESUME
        # =========================

        if resume_text and user_goal:

            try:

                # Import AI function
                from ai import analyze_resume

                result = analyze_resume(
                    resume_text,
                    user_goal
                )

                # =========================
                # SAVE REPORT
                # =========================

                db = SessionLocal()

                try:

                    user = (
                        db.query(models.User)
                        .filter_by(
                            email=session["user"]
                        )
                        .first()
                    )

                    if user:

                        report = models.Report(
                            user_id=user.id,
                            resume_text=resume_text,
                            result=json.dumps(result)
                        )

                        db.add(report)
                        db.commit()

                finally:

                    db.close()

            except Exception as e:

                result = {
                    "error": f"AI error: {str(e)}"
                }


    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result
    )


# =========================
# HISTORY
# =========================

@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/login")

    db = SessionLocal()

    try:

        user = (
            db.query(models.User)
            .filter_by(
                email=session["user"]
            )
            .first()
        )

        if not user:
            return redirect("/login")

        reports = (
            db.query(models.Report)
            .filter_by(
                user_id=user.id
            )
            .all()
        )

        parsed_reports = []

        for r in reports:

            try:

                parsed_result = json.loads(r.result)

            except Exception:

                parsed_result = {}

            parsed_reports.append({
                "result": parsed_result,
                "resume": r.resume_text
            })

        return render_template(
            "history.html",
            reports=parsed_reports
        )

    finally:

        db.close()

# =========================
# FORGOT PASSWORD
# =========================

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email", "").strip()

        db = SessionLocal()

        try:

            user = (
                db.query(models.User)
                .filter_by(email=email)
                .first()
            )

            if not user:
                return "No account found with this email."

        finally:
            db.close()

        # Generate 6 digit OTP
        otp = str(random.randint(100000, 999999))

        # Store email and OTP in session
        session["reset_email"] = email
        session["reset_otp"] = otp

        # Send OTP to Gmail
        try:

            msg = Message(
                subject="AI Resume Analyzer - Password Reset OTP",
                sender=os.getenv("MAIL_USERNAME"),
                recipients=[email]
            )

            msg.body = f"""
Hello,

Your password reset OTP for AI Resume Analyzer is:

{otp}

This OTP is required to reset your password.

Please do not share this OTP with anyone.

Thank you,
AI Resume Analyzer
"""

            mail.send(msg)

            return redirect("/verify-otp")

        except Exception as e:

            return f"Error sending email: {str(e)}"

    return render_template("forgot_password.html")


# =========================
# VERIFY OTP
# =========================

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if "reset_email" not in session:
        return redirect("/forgot-password")

    if request.method == "POST":

        entered_otp = request.form.get("otp", "").strip()

        saved_otp = session.get("reset_otp")

        if entered_otp == saved_otp:

            session["otp_verified"] = True

            return redirect("/reset-password")

        else:

            return "Invalid OTP. Please try again."

    return render_template("verify_otp.html")


# =========================
# RESET PASSWORD
# =========================

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if "reset_email" not in session:
        return redirect("/forgot-password")

    # User must verify OTP first
    if not session.get("otp_verified"):
        return redirect("/verify-otp")

    if request.method == "POST":

        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            return "Passwords do not match."

        if len(password) < 6:
            return "Password must be at least 6 characters."

        db = SessionLocal()

        try:

            user = (
                db.query(models.User)
                .filter_by(
                    email=session["reset_email"]
                )
                .first()
            )

            if not user:
                return "User not found."

            # Change password
            user.password = password

            db.commit()

            # Clear reset information
            session.pop("reset_email", None)
            session.pop("reset_otp", None)
            session.pop("otp_verified", None)

            return redirect("/login")

        finally:
            db.close()

    return render_template("reset_password.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop(
        "user",
        None
    )

    return redirect("/login")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )