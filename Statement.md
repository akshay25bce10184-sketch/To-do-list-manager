Project Statement: Secure CLI Task Manager

1. Problem Statement

In an increasingly digital world, individuals often struggle with personal organization and time management. While many task management applications exist, they often suffer from one of two extremes: they are either bloated with unnecessary features and subscription models, or they are simple scripts that lack security, storing sensitive user data and passwords in plain text. There is a critical need for a lightweight, offline, and secure solution that allows users to manage their daily priorities without compromising their data privacy.

2. Scope of the Project

The scope of this project is to develop a standalone, multi-user command-line interface (CLI) application designed to manage personal tasks securely on a local machine.

In-Scope:

User Authentication: A secure login and registration system that utilizes SHA-256 hashing to protect user credentials.

Task Lifecycle Management: Facilities to Create, Read, Update (mark complete), and Delete tasks.

Smart Prioritization: Logic to organize tasks not just by date, but by urgency levels (High, Medium, Low).

Data Persistence: Secure local storage of all user profiles and tasks using a relational database (SQLite).

User Isolation: Ensuring that tasks are linked strictly to specific User IDs, so users cannot access each other's private data.

Out-of-Scope:

Graphical User Interface (GUI) implementation (currently CLI only).

Cloud synchronization or remote server access.

Password recovery mechanisms (e.g., "Forgot Password" via email).

Collaboration features (sharing tasks between users).

3. Target Users

The primary target users for this application are:

Privacy-Conscious Individuals: Users who prefer keeping their data on their local machine rather than on cloud servers.

Developers & Students: Users comfortable with terminal environments who need a quick, distraction-free tool for tracking project milestones.

Minimalists: People looking for a tool that does one thing well without the overhead of complex project management software.

4. High-Level Features

Secure Password Hashing: Implementation of the hashlib library to ensure passwords are never stored in plain text, adhering to modern security standards.

Relational Database Design: Use of Foreign Keys in SQLite to maintain data integrity between Users and their specific Tasks.

Custom Sorting Logic: An intelligent ORDER BY query that ranks tasks effectively by mapping text priorities (High/Medium/Low) to numerical values.

Persistent Local Storage: Utilization of a serverless SQLite database ensures data is saved instantly and remains available across application restarts.

Input Validation: Robust han
