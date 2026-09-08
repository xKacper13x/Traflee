# Traflee 🚗 - Fleet Telemetry MVP

Traflee is a specialized telemetry SaaS Proof of Concept (PoC) designed for small to medium-sized car rental businesses. Unlike traditional GPS fleet management systems, Traflee focuses strictly on **asset protection**—monitoring engine health, detecting mechanical abuse, and automating deposit validation through real-time OBD-II data analysis.

## 🎯 Project Overview

Local car rental companies often suffer financial losses due to customers aggressively driving vehicles on cold engines or ignoring "Check Engine" lights. Traflee solves this by acting as a "Deposit Guardian." It reads live engine data, evaluates driver behavior against predefined business rules, and logs violations directly into a relational database.

## ✨ Key Features

* **Real-time OBD-II Ingestion:** Continuously extracts core engine metrics (RPM, engine load, coolant temperature, and ECU voltage) using Bluetooth ELM327 adapters.
* **Smart Diagnostics (DTC):** Parses standard OBD-II Diagnostic Trouble Codes to monitor vehicle health and translate mechanical faults.
* **Deposit Guardian Logic:** A decoupled validation engine that detects vehicle thrashing (e.g., high RPM and heavy load on a cold engine) using custom exception handling for hardware sensor dropouts.
* **Relational Database Storage:** Maps fleet assets to rental accounts and persists validated rule violations using SQLite and SQLAlchemy ORM.

## 🛠️ Technology Stack

* **Language:** Python 3.10+
* **Hardware Interface:** `python-obd` (communicating via `/dev/rfcomm0`)
* **Database & ORM:** SQLite, SQLAlchemy
* **Architecture:** Object-Oriented Programming (OOP), Data-Driven Design, Decoupled Modules

## 🏗️ System Architecture

The MVP is built with a strong focus on modularity and separation of concerns, laying the groundwork for a future cloud-based architecture:

1. **`CarDataReader` (The Senses):** Safely interfaces with the vehicle's ECU. It handles connection stability and returns sanitized data dictionaries.
2. **`DepositValidator` (The Brain):** Evaluates the sanitized metrics against business rules. It operates completely independently of the hardware layer.
3. **`SQLAlchemy Models` (The Memory):** Stores structured data regarding the vehicles, current rentals, and recorded telemetry alerts.

## 🚀 Getting Started

### Prerequisites

You need a Linux-based environment (or Windows with appropriate COM port mapping) and a paired Bluetooth OBD-II adapter (e.g., Vgate iCar Pro).

### Installation

1. Clone the repository:
   `git clone https://github.com/xKacper13x/traflee.git`
2. Create and activate a virtual environment:
   `python -m venv venv`
   `source venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Bind your Bluetooth adapter to the RFCOMM port:
   `sudo rfcomm bind 0 <MAC_ADDRESS>`
5. Initialize the database and run the main script:
   `python main.py`

## 🗺️ Roadmap

* **Phase 1 (Current):** Local MVP using `python-obd`, SQLite, and Bluetooth ELM327.
* **Phase 2 (Upcoming):** Cloud ingestion architecture using FastAPI, PostgreSQL, and professional GSM/GPRS trackers (e.g., Teltonika).
* **Phase 3:** Streamlit-based web dashboard for fleet owners.
