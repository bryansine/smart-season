# SmartSeason: Agricultural Field Monitoring System

## Overview
SmartSeason is a streamlined AgTech solution designed to manage field observations between **Coordinators** and **Field Agents**. It moves away from generic marketplace structures to focus on data-driven agricultural monitoring.

## Core Features
- **Dual-Role RBAC:** Distinct dashboards and permissions for Coordinators (Admins) and Field Agents.
- **Dynamic Field Tracking:** Coordinators register fields (Location, Crop, Agent); Agents submit real-time status updates.
- **"At Risk" Logic:** Automated color-coded indicators for fields requiring immediate attention based on status updates. eg Fields are marked 'At Risk' when flagged   manually by an agent or if no updates are recorded within a 14-day window.
- **Mobile-Responsive UI:** Built with a custom forest-green AgTech palette and Bootstrap 5.


## Field Status Logic
The system utilizes a dynamic status calculation engine within the `Field` model to categorize agricultural plots. Instead of hard-coding a static status, the system computes the state in real-time using the following logic:

* **Completed:** Any field where the `is_harvested` flag is set to `True`. This overrides all other statuses as it signifies the end of the production cycle.
* **At Risk:** Triggered by two conditions:
    1.  **Manual Flag:** If a Field Agent explicitly marks the status as "At Risk" during a field visit.
    2.  **Stale Data:** If the `last_observation_date` is more than 14 days old, indicating a lack of monitoring.
* **Active:** The default state for any field that is currently being monitored, has been updated within the last 14 days, and has not been harvested.

**Approach:** This logic is implemented using a Python property method in the backend. This ensures data integrity by preventing "status mismatch" where a field could be harvested but still marked as active.

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