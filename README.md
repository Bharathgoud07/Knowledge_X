# 🚀 KnowledgeX – AI-Powered Educational Resource Sharing Platform

KnowledgeX is a full-stack Django web application that enables students and educators to upload, organize, discover, and collaborate on academic resources. The platform combines intelligent AI-powered document analysis with community-driven resource sharing, moderation, analytics, and an interactive learning experience.

---

## 🌟 Key Features

### 🔐 Authentication & User Management

- Secure user registration and login
- Email verification
- Password reset via email
- User profile management
- Avatar upload
- College, branch & location details
- GitHub & LinkedIn profile links
- Login streak tracking
- Longest streak statistics

---

## 📚 Resource Management

Users can upload and manage various educational resources including:

- 📄 PDF Notes
- 📝 Handwritten Notes
- 📑 DOCX Files
- 📊 PPT / PPTX
- 🖼️ Images & Diagrams
- 📦 ZIP Resources
- 📖 Reference Materials
- ❓ Important Questions

### Resource Features

- Subject categorization
- Semester categorization
- Resource type filtering
- Edit/Delete uploaded resources
- Download tracking
- Resource verification workflow
- Online document viewer

---

## 🤖 AI-Powered Learning Assistant

KnowledgeX integrates **Google Gemini AI** to enhance the learning experience.

### AI Features

- 📄 Automatic document summarization
- ❓ AI-generated important questions
- 💬 Chat with uploaded PDF documents
- 🧠 Intelligent document text extraction
- Semantic document understanding

---

## 💬 Community Features

- ⭐ Resource rating system (1–5 stars)
- 💬 Threaded comments
- ↳ Nested replies
- ❤️ Favorite/Bookmark resources
- 🔍 Search resources
- 📂 Advanced filtering
- 📈 Most downloaded resources

---

## 🔔 Notification System

Real-time notifications for:

- Comments
- Replies
- Ratings
- Verification updates
- Report status
- Administrative actions

---

## 🛡️ Moderation System

### Resource Verification

- Pending
- Approved
- Rejected

### Reporting System

Users can report resources for:

- Duplicate content
- Incorrect information
- Irrelevant uploads
- Copyright concerns
- Illegal content

Administrators can review and resolve reports.

---

## 👨‍💼 Admin Dashboard

The platform includes a comprehensive administration panel.

### Admin Features

- Dashboard analytics
- User management
- Resource management
- Subject management
- Report management
- Resource verification
- Broadcast notifications
- Platform statistics

---

## 📊 Analytics & Gamification

### User Analytics

- Total uploads
- Downloads
- Resource views
- Favorites
- Ratings received

### Platform Analytics

- Active users
- Upload statistics
- Download statistics
- Resource distribution
- Popular subjects

### Leaderboards

- Top contributors
- Most active users

---

## 📈 Visit Tracking

Custom middleware tracks:

- Page visits
- Request methods
- User engagement
- Platform activity

---

# 🛠️ Tech Stack

## Backend

- Django 5.x
- Django REST Framework
- Python

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Database

- SQLite (Development)

## AI

- Google Gemini API

## File Processing

- pypdf
- python-docx
- python-pptx
- Pillow

## Rich Text Editor

- CKEditor 5

## Charts

- Chart.js

---

# 📁 Project Structure

```
KnowledgeX
│
├── accounts/          # Authentication & user profiles
├── resources/         # Resources, AI, comments, ratings
├── core/              # Homepage & dashboards
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

---

# 🚀 Installation

```bash
git clone https://github.com/Bharathgoud07/Knowledge_X.git

cd Knowledge_X

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

---

# 📸 Features Overview

✅ Secure Authentication

✅ AI Document Summarization

✅ AI Question Generation

✅ Chat with PDF

✅ Resource Upload & Management

✅ Online Resource Viewer

✅ Ratings & Reviews

✅ Comments & Replies

✅ Favorites

✅ Notifications

✅ Resource Verification

✅ Report Management

✅ Admin Dashboard

✅ User Analytics

✅ Leaderboards

✅ Visit Tracking

---

# 🔮 Future Enhancements

- PostgreSQL support
- Docker deployment
- Elasticsearch-based semantic search
- AI resource recommendations
- Email notifications
- Mobile application
- Multi-college support
- Cloud storage integration
- Dark mode
- REST API documentation

---

# 👨‍💻 Author

**Bharath Goud Andhyala**

- GitHub: https://github.com/Bharathgoud07
- LinkedIn: https://www.linkedin.com/in/bharath-goud-andhyala

---

## ⭐ If you found this project useful, consider giving it a star!
