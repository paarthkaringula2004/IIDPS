
# IIDPS - Internal Intrusion Detection and Protection System

> **A Hybrid Approach for Insider Threats Detection Using System Call Analysis and Malware API Monitoring**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.1.3-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Product%20License-red.svg)](https://github.com/paarthkaringula2004/IIDPS/blob/main/PRODUCT%20LICENCE.md)


## Introduction

In modern digital infrastructures, **insider threats** pose severe risks, as attackers can exploit valid credentials to bypass perimeter defenses. Traditional security systems often lack behavioral analysis to detect such malicious internal activity.

**IIDPS** (Internal Intrusion Detection and Protection System) is a hybrid intelligent system that combines:

- **System Call Mining & Behavioral Profiling**
- **Machine Learning-based Malware Detection**

This approach aims to detect both insider threats and malware uploads in real-time, enhancing the security posture of organizational environments.

---

## Features

### System Call Analysis & Profiling

- Captures sequences of system calls per user session.
- Builds user-specific behavioral fingerprints.
- Detects deviations indicating insider attacks.

### Machine Learning Malware Detection

- Analyses API call sequences in uploaded files.
- Employs TF-IDF vectorization for feature extraction.
- Classifies files using Random Forest, SVM, and Naïve Bayes models.

### Real-Time Alerts & Dashboard

- Issues instant alerts for anomalous behavior or malicious file uploads.
- Provides an admin dashboard for monitoring threats and reviewing logs.

### Secure Web Application

- Built with Django for scalability and security.
- User-friendly interface with authentication and file upload monitoring.

---

## Architecture

The system consists of two primary modules:

1. **Insider Threat Detection Module**
    - Captures system call sequences during user sessions.
    - Uses a Naïve Bayes classifier to detect anomalies.
    - Alerts admins upon suspicious deviations.

2. **Malware Detection Module**
    - Processes API call datasets from uploaded files.
    - Transforms data using TF-IDF vectorization.
    - Classifies files with machine learning models to block malicious uploads.

### System Architecture Diagram

![IIDPS System Architecture](https://github.com/paarthkaringula2004/Project-Images-Video/blob/main/Images-Videos/IIDPS/IIDPS%20System%20Architecture.png?raw=true)

---

## System Requirements

### Software Requirements

- Python >= 3.8
- Django == 3.1.3
- MySQL 8.x
- Required Python libraries:

```text
matplotlib==3.3.2
mysql-connector==2.2.9
mysqlclient==2.0.3
PyMySQL==1.0.2
scikit-learn==0.23.2
pandas==1.1.4
nltk
````

### Hardware Requirements

* OS: Windows 10 or above
* Processor: Intel i5 or higher
* RAM: Minimum 8 GB
* Storage: Minimum 25 GB free space

## Installation

---

## Required Installers

Before setting up the project, download the following software installers from the link below:

- Python (python-3.6.7-amd64)
- SQL Log (SQLyog607)
- MySQL Installer (mysql-installer-community-8.0.28.0)

👉 [Download Installers from Google Drive](https://drive.google.com/drive/folders/12hGIU70vnj4FqCHIb3L6_XEoQdHoLjNL?usp=sharing)

Ensure you install these tools before proceeding with the project setup.
---

## Setup Process for Required Installers

Follow these steps to install and configure the necessary software for running IIDPS:

---

### Python (python-3.6.7-amd64)

- Run the Python installer as an **administrator**.
- During installation, ensure you select:
  - **Add Python to PATH** → ✓ Checked

This allows Python commands to be recognized globally in your system.

---

### SQL Log (SQLyog607)

- Launch the **SQLyog607** installer and complete the installation.
- During setup, use the following credentials:
  - **Password:** `root`

![SQLyog Setup Screenshot](https://github.com/user-attachments/assets/0823535a-944a-40cc-becf-617083f38675)

**Important:**  
- Ensure SQLyog is running whenever you start the IIDPS project.
- This maintains the database connection required by the system.

---

### MySQL Installer (mysql-installer-community-8.0.28.0)

- Run the MySQL installer.
- Select:
  - **Developer Default** setup mode.
- Click **Next** to accept the default options during installation.
- When prompted for database credentials, use:
  - **Username:** `root`
  - **Password:** `root`

**As we have in code -->** ![image](https://github.com/user-attachments/assets/d9097f3c-0533-4913-beda-3431207976ee)

This will set up the MySQL server with the required user configuration for IIDPS.

---



Clone this repository:

```bash
git clone https://github.com/paarthkaringula2004/IIDPS.git
cd Django
cd IIDPS
````

Install all required Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Project Path Configuration

Before running the project, update the file paths as follows:

1. Open this project in Visual Studio Code.
2. Go to: 
- **Project Folder**
  ```
  C:\user\Django\IIDPS\webapp\views.py
  ```

3. Update these lines under views.py:
- **Line 397** → set your path to:
  ```
  Your_Project_Path\Django\IIDPS\MalwareAnalyisis\malware_analysis_data.csv
  ```
- **Line 485** → set your path to:
  ```
  Your_Project_Path\Django\IIDPS\Data\
  ```

4. Save the file.

Your project paths are now configured!

---

Run database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

By default, the application will be available at:

```
http://127.0.0.1:8000
```

## Demo Video

👉 [Watch this video for Further Installation and Running of Project](https://drive.google.com/file/d/1CcW7d9q6JlRE8pj2cj7OT7mPZW2Oj1lA/view?usp=drivesdk)

---


## Usage

The IIDPS system provides a secure web platform for user authentication and advanced behavior monitoring. Here’s how it works:

### User Authentication

- Users can **sign up** and **log in** securely through the web interface.
- Both regular users and administrators have access to the system, with role-based permissions.

### Behavioral Pattern Matching

- The system tracks each user’s unique operational patterns using system call sequences.
- **Example scenario:**
  - User A typically performs operations 1, 2, and 3.
  - User B typically performs operations 4, 5, and 6.
- If User B suddenly performs operations 1, 2, or 3, the system detects this deviation.
  - Such a mismatch may indicate that User B is using credentials stolen from User A.
  - The system flags this suspicious activity and generates an alert for administrators to review.

This intelligent pattern-matching mechanism ensures **behavioral consistency checks** and helps detect insider threats even when valid credentials are misused.

### File Upload Malware Detection

- The system includes a **malware detection module** for file uploads.
- When a user uploads a file:
  - The file is analyzed using trained machine learning models (Random Forest, SVM, Naïve Bayes).
  - API call sequences are examined for malicious patterns.
- If the system identifies the file as malware:
  - The upload is blocked.
  - An alert is generated and logged for further review.

These combined features provide robust protection against **insider threats** and external malware, safeguarding sensitive data and maintaining system integrity.

---


## Model Performance

The system includes three machine learning models for malware detection:

| Model         | Accuracy       |
| ------------- | -------------- |
| Random Forest | 98.1%          |
| SVM           | 62.5%          |
| Naïve Bayes   | Lower but fast |

**Random Forest** was selected for deployment due to its high accuracy and robustness.

## License

This project is licensed under the Product License. See the [PRODUCT LICENCE](https://github.com/paarthkaringula2004/IIDPS/blob/main/PRODUCT%20LICENCE.md) file for details.

---

## Acknowledgments

This project references several works in the field of intrusion detection, system call mining, and malware detection, including:

* Wu and Banzhaf, 2024
* Ramamoorthy & Karuppasamy, 2024
* Roberts and Singh, 2022
* Kale et al., 2022
* Leu et al., 2021

