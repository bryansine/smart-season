# SmartSeason: Agricultural Field Monitoring System

## Overview
SmartSeason is a streamlined AgTech solution designed to manage field observations between **Coordinators** and **Field Agents**. It moves away from generic marketplace structures to focus on data-driven agricultural monitoring.

## Core Features
- **Dual-Role RBAC:** Distinct dashboards and permissions for Coordinators (Admins) and Field Agents.
- **Dynamic Field Tracking:** Coordinators register fields (Location, Crop, Agent); Agents submit real-time status updates.
- **"At Risk" Logic:** Automated color-coded indicators for fields requiring immediate attention based on status updates. eg Fields are marked 'At Risk' when flagged   manually by an agent or if no updates are recorded within a 14-day window.
- **Mobile-Responsive UI:** Built with a custom forest-green AgTech palette and Bootstrap 5.

##  Tech Stack
- **Backend:** Django 5.x (Python 3.12)
- **Database:** SQLite (Development) / PostgreSQL compatible
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Environment:** Ubuntu Linux 

## Demo Credentials
To review the different role-based views, please use the following accounts:

| Role | Username | Password |
| :--- | :--- | :--- |
| **Coordinator (Admin)** | admin_user | password123 |
| **Field Agent** | agent_sine | password123 |

## Installation
1. Clone the repository.
2. Create a virtual environment: `python3 -m venv venv`.
3. Activate: `source venv/bin/activate`.
4. Install requirements: `pip install -r requirements.txt`.
5. Run migrations: `python manage.py migrate`.
6. Start server: `python manage.py runserver`.