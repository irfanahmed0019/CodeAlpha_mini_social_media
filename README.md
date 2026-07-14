# 🚀 VIBE – Social Media Platform

**VIBE** is a full-stack social media web application built with **Python and Django** as part of my **Full Stack Development Internship at CodeAlpha**.

The project focuses on understanding how real social media features work behind the interface.

Features such as likes, comments, profiles, and follows may look simple to users, but behind them are **database relationships, backend logic, authentication, and CRUD operations**.

This project helped me move beyond simply building pages and understand how users and content are connected inside a Django application.

---

## ✨ Features

- 🔐 User Authentication
- 👤 User Profiles
- 🖼️ Profile Pictures
- 📝 Create Posts
- ✏️ Update Posts
- 🗑️ Delete Posts
- 💬 Comment on Posts
- ❤️ Like and Unlike Posts
- 👥 Follow and Unfollow Users
- 📊 Followers and Following Relationships
- ⚡ Automatic Profile Creation using Django Signals
- 🗄️ Database Management using Django ORM
- 📱 Responsive Desktop and Mobile Interface

---

## 🧠 How the Application Works

A social media application is built around relationships between data.

```text
User ─────────► Profile
  │
  ├───────────► Posts
  │
  ├───────────► Comments
  │
  ├───────────► Likes
  │
  └───────────► Follow Relationships
```

The frontend provides the interactions.

The backend defines the rules.

The database remembers the relationships.

---

## 👤 User and Profile

Each Django `User` is connected to one `Profile`.

```text
User ─── One-to-One ─── Profile
```

The built-in Django `User` model handles authentication information such as:

- Username
- Password
- Email

The custom `Profile` model stores additional user information such as:

- Profile Picture
- Bio
- Website
- Location

A Django `post_save` signal automatically creates a profile whenever a new user is created.

This means every user can automatically have a corresponding profile without repeating profile-creation logic throughout the application.

---

## 📝 Posts

One user can create multiple posts.

```text
User ─── One-to-Many ─── Posts
```

Each post belongs to one user, while one user can create many posts.

The application supports CRUD operations:

- **Create** a new post
- **Read** existing posts
- **Update** a post
- **Delete** a post

---

## 💬 Comments

One post can have multiple comments.

```text
Post ─── One-to-Many ─── Comments
```

Each comment is connected to:

- The user who created the comment
- The post the comment belongs to

This allows the application to know exactly **who commented on which post**.

---

## ❤️ Like System

A Like is not simply a number.

Instead of only storing:

```text
likes = likes + 1
```

the application stores the actual relationship between the user and the post.

```text
User ─── Likes ─── Post
```

This allows the application to:

- Know who liked a post
- Count the total number of likes
- Prevent duplicate likes
- Allow users to unlike posts

The like count is calculated from the relationships stored in the database.

---

## 👥 Follow System

The Follow system represents a relationship between users.

```text
User A ─── Follows ───► User B
```

Instead of storing only a follower count, the application stores **who follows whom**.

When a user clicks the Follow button, the backend can:

1. Check whether the relationship already exists
2. Create the relationship if it does not exist
3. Remove the relationship when the user unfollows
4. Calculate followers and following counts from the stored relationships

This allows the application to:

- Display followers
- Display following users
- Calculate follower counts
- Prevent duplicate follows
- Support Follow and Unfollow actions

A counter tells us **how many**.

A relationship tells us **who**.

---

## ⚡ Django Signals

The project uses Django Signals to automatically create a `Profile` whenever a new `User` is created.

The `post_save` signal listens for the moment a `User` object is saved.

If the user has just been created, Django automatically creates the corresponding profile.

```text
New User Created
       ↓
post_save Signal Triggered
       ↓
Profile Automatically Created
```

This keeps the profile-creation logic separate from the registration flow and avoids repeating the same logic in multiple places.

---

## 🛠️ Tech Stack

### Backend

- Python
- Django
- Django ORM
- SQLite

### Frontend

- HTML5
- CSS3
- JavaScript

### Development Tools

- Git
- GitHub
- Visual Studio Code

---

## 📚 Concepts Used

This project helped me work with and understand:

- Django Models
- Django Views
- Django Templates
- Django Authentication
- Django ORM
- Django Signals
- One-to-One Relationships
- One-to-Many Relationships
- User-to-User Relationships
- ForeignKey Relationships
- Related Objects
- Database Constraints
- CRUD Operations
- Backend Business Logic
- Responsive Web Design

---

# ⚙️ Installation and Setup

Follow the steps below to run the project locally.

---

## 1️⃣ Clone the Repository

Open your terminal and clone the repository:

```bash
git clone https://github.com/irfanahmed0019/CodeAlpha_mini_social_media.git
```

Move into the project directory:

```bash
cd CodeAlpha_mini_social_media
```

---

## 2️⃣ Create a Virtual Environment

A virtual environment keeps the project's Python packages isolated from the system Python installation.

### Linux / macOS

```bash
python3 -m venv venv
```

### Windows

```bash
python -m venv venv
```

---

## 3️⃣ Activate the Virtual Environment

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows Command Prompt

```cmd
venv\Scripts\activate
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, you should see something similar to:

```text
(venv)
```

at the beginning of your terminal prompt.

---

## 4️⃣ Install the Dependencies

If the repository contains a `requirements.txt` file, run:

### Linux / macOS

```bash
pip install -r requirements.txt
```

### Windows

```bash
pip install -r requirements.txt
```

The main project dependencies include:

- Django
- Pillow

`Pillow` is required for working with Django's `ImageField`, including profile picture and image uploads.

---

## 5️⃣ Apply Database Migrations

Run the database migrations before starting the application.

### Linux / macOS

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Windows

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the required database tables based on the Django models.

---

## 6️⃣ Create a Superuser

To access the Django Admin Panel, create a superuser.

### Linux / macOS

```bash
python3 manage.py createsuperuser
```

### Windows

```bash
python manage.py createsuperuser
```

Enter your:

```text
Username
Email
Password
```

when prompted.

---

## 7️⃣ Run the Development Server

### Linux / macOS

```bash
python3 manage.py runserver
```

### Windows

```bash
python manage.py runserver
```

The application should now be available at:

```text
http://127.0.0.1:8000/
```

The Django Admin Panel can be accessed at:

```text
http://127.0.0.1:8000/admin/
```

---

## 📦 Requirements

The main dependencies required for this project are:

```text
Django
Pillow
```

To generate a `requirements.txt` file from your current environment:

```bash
pip freeze > requirements.txt
```

Another developer can then install the required dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

A simplified overview of the project structure:

```text
CodeAlpha_mini_social_media/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   └── views.py
│
├── social/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── views.py
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
├── staticfiles/
├── templates/
├── manage.py
├── requirements.txt
└── README.md
```

---

## 💡 Key Learning

The biggest lesson from this project was understanding that frontend interactions are often representations of backend relationships.

```text
The frontend provides the interaction.
The backend defines the rules.
The database remembers the relationships.
```

Before building a feature, one important question is:

> **What data needs to be connected?**

A Like is not just a counter.

A Follow is not just a button.

A Profile is not just a page.

Behind every simple interaction is:

- Data
- Relationships
- Validation
- Database queries
- Backend business logic

Building VIBE helped me understand how these pieces work together inside a full-stack Django application.

---

## 🎯 CodeAlpha Internship Task

This project was developed as **Task 2** of my **Full Stack Development Internship at CodeAlpha**.

Through this project, I gained practical experience with:

- Django Backend Development
- Authentication
- Database Relationships
- Django ORM
- CRUD Operations
- Django Signals
- Backend Business Logic
- Full-Stack Application Architecture

---

## 👨‍💻 Author

**Irfan Ahammad J**

- GitHub: [@irfanahmed0019](https://github.com/irfanahmed0019)
- LinkedIn: [Irfan Ahammad J](https://www.linkedin.com/in/irfan-ahammad-j/)

---

## ⭐ Support

If you found this project useful or interesting, consider giving the repository a ⭐.

It supports my learning journey and future projects.

---

## 🚀 Final Thought

> **The frontend provides the interactions.  
> The backend defines the rules.  
> The database remembers the relationships.**

**Built with Python and Django as part of my Full Stack Development journey. 🚀**
