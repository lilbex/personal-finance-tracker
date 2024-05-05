# Introduction
The Personal Finance Tracker is a web application designed to help users manage their finances effectively by tracking income, expenses, budgets, and financial goals.

# Main tools
- __Backend__: Python (Django and Django restframework)
- __Frontend__: Typescript (React)
- __Style__: Tailwind CSS
- __Email__: Amazon SES
- __Media Storage__: Amazon S3
- __Cache and Message Broker__: Redis
- __Task Scheduler__: Celery

Feel free to clone and personalize


# Features
- User Authentication: Secure user authentication system allowing users to register, login, and manage their accounts.
- Dashboard: Interactive dashboard displaying an overview of the user's financial status, including income, expenses, and budget progress.
- Expense Tracking: Ability to record and categorize expenses, with options for adding notes and attaching receipts.
- Income Tracking: Log and categorize income sources to track overall earnings.
- Budget Management: Set budgets for different expense categories and monitor spending against budgeted amounts.
- Goal Setting: Set financial goals such as savings targets or debt repayment goals, with progress tracking.
- Reports and Analytics: Generate reports and visualizations to analyze spending patterns, track progress towards goals, and gain insights into financial habits.
- Reminders and Notifications: Receive reminders for bill payments, upcoming expenses, or reaching budget thresholds.
- Multi-Currency Support: Support for multiple currencies to accommodate users from different regions.
- Data Export: Export financial data in various formats (e.g., CSV, PDF) for further analysis or record-keeping.

# Installation
1. `git clone https://github.com/lilbex/personal-finance-tracker.git`
2. `cd personal-finance-tracker`
3. cd into __backend__ folder and create a .env file to set Environment variable following the example in env_example. Do the same for __frontend__ folder
4. Ensure your docker daemon is running. you can download docker [here](https://www.docker.com/get-started/) 
5. On your root directory type `docker-compose up --build`
6. Visit http://localhost:5173/ on your browser to view the app

# License
This project is licensed under the MIT License. You are free to use, modify, and distribute the code for any purpose, with attribution.

# Acknowledgements
Special thanks to the creators of the following framework and libraries, which helped make this project possible.