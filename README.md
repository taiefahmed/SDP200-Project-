# SDP200-Project-
Purpose:
Admin-এর মাধ্যমে student marks, grades, attendance manage করা, analysis করা এবং future prediction করা।

Features:
Login Screen: Admin authentication।

Admin Panel:
Marksheet view (TreeView)
Student search & detail + Pie charts (Marks & Attendance)
Result analysis: Midterm, Teacher Eval, Final, Grade, Attendance → KDE, Scatter, Heatmap
ML Prediction: Final marks & Grade prediction using Linear Regression + Decision Tree
Add new student → DB insert

DB:
MySQL (sdp_200)
Table students → ID, Name, Age, Gender, Mid, Eval, Final, Total, Grade, Attendance%
Tkinter ↔ MySQL → fetch, insert, update
Visualization: Matplotlib + Seaborn → Pie charts, KDE, Scatter, Heatmap

ML Models: Linear Regression → Final marks
Decision Tree → Grade prediction

Flow: 
Tkinter GUI → MySQL DB → Fetch/Update → Analysis/Visualization → ML Prediction
