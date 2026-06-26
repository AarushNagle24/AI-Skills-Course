# AI Skills Course Studio

A Streamlit prototype for a company that creates custom AI skills courses for other businesses. The public website explains the service and collects company inquiries. The course platform is separate and opens from the public `Courses` link with `?page=courses`.

## Features

- Public pages for Home, Sample Courses, and Contact
- Course platform login and account creation with hashed passwords
- SQLite storage for users, courses, enrollments, progress, creation keys, and contact requests
- Company course creation with one-time 15-character course creation keys
- Random 6-character uppercase employee join codes
- Employee course enrollment and progress tracking
- Admin course management with employee progress, quiz completion, join code regeneration, and course editing
- Sample course content with reading lessons and quizzes, including a full marketing and advertising sample course

No pricing is shown in the app. Companies submit a request so course scope and pricing can be discussed by email.

## Install

```bash
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

The app creates `ai_skills_courses.db` automatically on first run.

## Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. In Streamlit Community Cloud, create a new app from the repository.
3. Set the main file path to `app.py`.
4. Deploy. Streamlit will install `requirements.txt` automatically.

Do not use Docker for this project.

## Seeded test course creation keys

These keys are seeded automatically if they are not already present:

```text
A7xQ9L2#mP4zR8$
B4nT6K1@vS8pL3!
C9rM2V5&hQ7wN6?
```

These 10 additional generic course creation keys are also seeded for testing:

```text
D5pR8#vL2qM9sT!
E2mN7@kQ4zP8rW$
F9tL3&xA6cR2vH?
G4wC8!nP5yK1qZ#
H6zV2$eT9mB4xL@
J8qP3#rN6vC1sY!
K2mW9@tH5xD7pR$
L7cA4&zQ8nF2vT?
N3yR6!pK9mE5xB#
P5vT1$sL8qG4nW@
```

These two keys create courses with the same readings and quiz questions as the marketing and advertising sample course:

```text
M4rK9A2!dQ7xP5$
Ad8V2#kL9pQ4zR!
```

Each key can be used once by a logged-in user to create a company course. After a course is created, the app generates a 6-character join code for employees.

## Demo flow

1. Open the public site and review Home, Sample Courses, and Contact.
2. Submit a contact request.
3. Click `Courses` to open the platform route in a new browser tab.
4. Create an admin account and log in.
5. Use one seeded creation key to create a company course.
6. Copy the generated join code from the managed course card or admin panel.
7. Create another account and log in as an employee.
8. Join the course with the 6-character join code.
9. Open the course, view the reading lesson, complete the quiz, and confirm progress reaches 100%.
10. Log back in as the admin and view employee progress in the admin panel.

## Prototype note

SQLite is used for local prototype and demo storage. For production, use a managed database, stronger account controls, email delivery, audit logging, and a more complete course authoring workflow.

## Portfolio

View the portfolio here:

https://github.com/varshajagadeesh/Aardvarks_portfolio/tree/main
