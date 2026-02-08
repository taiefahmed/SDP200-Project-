from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# DB CONNECT
def connect_db():
    try:
        return mysql.connector.connect(host="localhost", user="root", password="", database="sdp_200")
    except:
        messagebox.showerror("DB Error", "Cannot connect to MySQL Database!")
        return None

#  APP
root = Tk()
root.title("Student Result Analysis")
root.geometry("1550x600")
root.configure(bg="#e0f7fa")

# Button hover effect
def on_enter(e):
    e.widget['background'] = '#4fc3f7'
def on_leave(e):
    e.widget['background'] = '#0288d1'

# ===================== LOGIN SCREEN =====================
def login_screen():
    login = Frame(root, bg="#b3e5fc")
    login.pack(fill="both", expand=True)

    Label(login, text="Admin Login", font=("Helvetica", 30, "bold"), bg="#b3e5fc", fg="#01579b").pack(pady=40)

    # Function to add placeholder
    def add_placeholder(entry, text):
        entry.insert(0, text)
        entry.config(fg="grey")

        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, text)
                entry.config(fg="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # Username Entry
    user_entry = Entry(login, font=("Helvetica", 14), bd=2, relief="solid", width=25, highlightthickness=1, highlightbackground="#ccc")
    user_entry.pack(pady=10)
    add_placeholder(user_entry, "username")

    # Password Entry
    pass_entry = Entry(login, font=("Helvetica", 14), bd=2, relief="solid", width=25, highlightthickness=1, highlightbackground="#ccc", show="*")
    pass_entry.pack(pady=10)
    add_placeholder(pass_entry, "Password")

    # Make password show dots when typing
    def on_pass_focus_in(event):
        if pass_entry.get() == "Password":
            pass_entry.delete(0, "end")
            pass_entry.config(fg="black", show="*")

    def on_pass_focus_out(event):
        if pass_entry.get() == "":
            pass_entry.insert(0, "Password")
            pass_entry.config(fg="grey", show="")

    pass_entry.bind("<FocusIn>", on_pass_focus_in)
    pass_entry.bind("<FocusOut>", on_pass_focus_out)

    # Login button
    def check_login():
        username = user_entry.get()
        password = pass_entry.get()
        if username == "taief" and password == "1234":
            login.pack_forget()
            main_screen()
        else:
            messagebox.showerror("Login Failed", "Incorrect Username or Password")
    login_btn = Button(login, text="Login", font=("Helvetica", 16, "bold"), bg="#0288d1", fg="white",
                       width=14, command=check_login)
    login_btn.pack(pady=30)
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

# ===================== MAIN SCREEN =====================
def main_screen():
    main_frame = Frame(root, bg="#e0f7fa")
    main_frame.pack(fill="both", expand=True)

    Label(main_frame, text="Welcome Admin", font=("Helvetica", 26, "bold"), bg="#e0f7fa", fg="#01579b").pack(pady=60)

    btn_admin = Button(main_frame, text="Admin Panel", font=("Helvetica", 18, "bold"),
                       bg="#0288d1", fg="white", width=18, command=lambda:[main_frame.pack_forget(), admin_panel()])
    btn_admin.pack(pady=20)
    btn_admin.bind("<Enter>", on_enter)
    btn_admin.bind("<Leave>", on_leave)

    btn_logout = Button(main_frame, text="Logout", font=("Helvetica", 18, "bold"),
                        bg="#d32f2f", fg="white", width=18, command=lambda:[main_frame.pack_forget(), login_screen()])
    btn_logout.pack(pady=20)
    btn_logout.bind("<Enter>", lambda e: e.widget.config(bg="#ef5350"))
    btn_logout.bind("<Leave>", lambda e: e.widget.config(bg="#d32f2f"))

# ===================== ADMIN PANEL =====================
def admin_panel():
    admin_frame = Frame(root, bg="#e1f5fe")
    admin_frame.pack(fill="both", expand=True)

    left = Frame(admin_frame, bg="#81d4fa", width=300)
    left.pack(side=LEFT, fill=Y, padx=5, pady=5)

    right = Frame(admin_frame, bg="#ffffff")
    right.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

    # TreeView
    tree = ttk.Treeview(right, columns=('ID','Name','Age','Gender','Midterm','Teacher Eval','Final','Total','Grade','Attendance'),
                        show='headings')
    for c in tree['columns']:
        tree.heading(c, text=c)
        tree.column(c, width=130, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # ---------- SHOW MARKSHEET ----------
    def show_marksheet():
        conn = connect_db()
        if not conn: return
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        conn.close()

        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", END, values=row)

    # ---------- STUDENT SEARCH ----------
    def student_search():
        win = Toplevel()
        win.title("Search Student")
        win.geometry("670x750")
        win.configure(bg="#e0f7fa")

        Label(win, text="Search Student", font=("Helvetica", 18, "bold"),
              bg="#0288d1", fg="white").pack(fill=X, ipady=7)

        Label(win, text="Enter Student ID:", font=("Helvetica", 14),
              bg="#e0f7fa").pack(pady=10)

        entry = Entry(win, font=("Helvetica", 14))
        entry.pack(pady=5)

        result_box = Frame(win, bg="white", bd=2, relief=RIDGE)
        result_box.pack(pady=10, fill=BOTH, expand=False, padx=20)

        chart_frame = Frame(win, bg="#e0f7fa")
        chart_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        def search():
            for w in result_box.winfo_children(): w.destroy()
            for w in chart_frame.winfo_children(): w.destroy()

            sid = entry.get()
            if sid == "":
                Label(result_box, text="Please enter a Student ID",
                      fg="red", bg="white").pack(pady=20)
                return

            conn = connect_db()
            if not conn: return
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE id=%s", (sid,))
            data = cur.fetchone()
            conn.close()

            if data:
                titles = ['ID', 'Name', 'Age', 'Gender', 'Midterm', 'Teacher Eval', 'Final', 'Total', 'Grade',
                          'Attendance']
                for i, val in enumerate(data):
                    Label(result_box, text=f"{titles[i]} : {val}",
                          bg="white", font=("Helvetica", 12)).pack(anchor="w", pady=3, padx=10)

                # Convert student data to DataFrame for plotting
                df_student = pd.DataFrame([data[4:7]], columns=["Midterm", "Teacher Eval", "Final"])

                # -------- PIE CHART 1: Marks Breakdown --------
                fig1, ax1 = plt.subplots(figsize=(3, 3))
                df_student.iloc[0].plot(kind="pie", autopct="%1.2f%%", ax=ax1)
                ax1.set_ylabel("")
                ax1.set_title("Marks Breakdown")

                canvas1 = FigureCanvasTkAgg(fig1, master=chart_frame)
                canvas1.draw()
                canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

                # -------- PIE CHART 2: Attendance --------
                attend = int(data[9])
                not_attend = 100 - attend
                pie_data = [attend, not_attend]
                pie_labels = ["Present", "Absent"]

                fig2, ax2 = plt.subplots(figsize=(3, 3))
                ax2.pie(pie_data, labels=pie_labels, autopct="%1.f%%", colors=["#4fc3f7", "#ffc107"])
                ax2.set_title("Attendance %")

                canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame)
                canvas2.draw()
                canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)

            else:
                Label(result_box, text="No student found",
                      fg="red", bg="white").pack(pady=20)

        Button(win, text="Search", font=("Helvetica", 14, "bold"),
               bg="#0288d1", fg="white", command=search).pack(pady=10)

    # ---------- RESULT ANALYSIS ----------
    def result_analysis():
        conn = connect_db()
        if not conn:
            return
        df = pd.read_sql_query("SELECT * FROM students", conn)
        conn.close()

        if df.empty:
            messagebox.showinfo("No Data", "No data available")
            return

        win = Toplevel()
        win.title("Result Analysis")
        win.geometry("1280x900")

        # ---------------- TOP BUTTON FRAME ----------------
        button_frame = Frame(win, bg="#f5f5f5")
        button_frame.pack(fill=X, padx=10, pady=10)

        # MAIN CANVAS (for all plots)
        canvas = Canvas(win)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        frame = Frame(canvas, bg="#ffffff")
        canvas.create_window((0, 0), window=frame, anchor=NW)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # --------- FUNCTION TO CLEAR OLD PLOTS ----------
        def clear_plots():
            for widget in frame.winfo_children():
                widget.destroy()

        # ---------------- MIDTERM ANALYSIS ----------------
        def show_midterm():
            clear_plots()

            # Plot 1 → KDE Curve of MID
            fig1, ax1 = plt.subplots(figsize=(6, 3.8))
            df["mid"].plot(kind="kde", title="Midterm KDE Distribution", ax=ax1)
            canvas1 = FigureCanvasTkAgg(fig1, master=frame)
            canvas1.draw()
            canvas1.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

            # Plot 2 → Scatter Plot (Mid vs Final)
            fig2, ax2 = plt.subplots(figsize=(6, 3.8))
            sns.scatterplot(
                x=df["mid"],
                y=df["final"],
                hue=df["grade"],
                style=df["gender"],
                ax=ax2
            )
            ax2.set_title("Mid vs Final (Grade + Gender)")
            canvas2 = FigureCanvasTkAgg(fig2, master=frame)
            canvas2.draw()
            canvas2.get_tk_widget().grid(row=0, column=1, padx=20, pady=20)

            # Plot 3 → KDE for Each Grade
            fig3, ax3 = plt.subplots(figsize=(6, 3.8))
            sns.kdeplot(df[df["grade"] == "A+"]["mid"], color="Red", label="A+", ax=ax3)
            sns.kdeplot(df[df["grade"] == "A"]["mid"], color="Blue", label="A", ax=ax3)
            sns.kdeplot(df[df["grade"] == "A-"]["mid"], color="Green", label="A-", ax=ax3)
            sns.kdeplot(df[df["grade"] == "B"]["mid"], color="Purple", label="B", ax=ax3)
            sns.kdeplot(df[df["grade"] == "C"]["mid"], color="Pink", label="C", ax=ax3)
            ax3.legend()
            ax3.set_title("Midterm KDE by Grade")

            canvas3 = FigureCanvasTkAgg(fig3, master=frame)
            canvas3.draw()
            canvas3.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        # OTHER BUTTONS (still empty)
        def show_teacher_evaluation():
            clear_plots()

            # Plot 1 → KDE Curve of Teacher Evaluation
            fig1, ax1 = plt.subplots(figsize=(6, 3.8))
            df["eval"].plot(kind="kde", title="Teacher Evaluation KDE Distribution", ax=ax1)
            canvas1 = FigureCanvasTkAgg(fig1, master=frame)
            canvas1.draw()
            canvas1.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

            # Plot 2 → Scatter Plot (Evaluation vs Final)
            fig2, ax2 = plt.subplots(figsize=(6, 3.8))
            sns.scatterplot(
                x=df["eval"],
                y=df["final"],
                hue=df["grade"],
                style=df["gender"],
                ax=ax2
            )
            ax2.set_title("Teacher Evaluation vs Final (Grade + Gender)")
            canvas2 = FigureCanvasTkAgg(fig2, master=frame)
            canvas2.draw()
            canvas2.get_tk_widget().grid(row=0, column=1, padx=20, pady=20)

            # Plot 3 → KDE for Each Grade (Teacher Evaluation)
            fig3, ax3 = plt.subplots(figsize=(6, 3.8))
            sns.kdeplot(df[df["grade"] == "A+"]["eval"], color="Red", label="A+", ax=ax3)
            sns.kdeplot(df[df["grade"] == "A"]["eval"], color="Blue", label="A", ax=ax3)
            sns.kdeplot(df[df["grade"] == "A-"]["eval"], color="Green", label="A-", ax=ax3)
            sns.kdeplot(df[df["grade"] == "B"]["eval"], color="Purple", label="B", ax=ax3)
            sns.kdeplot(df[df["grade"] == "C"]["eval"], color="Pink", label="C", ax=ax3)

            ax3.legend()
            ax3.set_title("Teacher Evaluation KDE by Grade")

            canvas3 = FigureCanvasTkAgg(fig3, master=frame)
            canvas3.draw()
            canvas3.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        def show_final():
            clear_plots()
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            df["final"].plot(kind="kde", title="Final Marks KDE Distribution", ax=ax1)

            canvas1 = FigureCanvasTkAgg(fig1, master=frame)
            canvas1.draw()
            canvas1.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

        def show_grade():
            clear_plots()

            # Use grid layout
            positions = [
                (0, 0), (0, 1),
                (1, 0), (1, 1),
                (2, 0), (2, 1)
            ]

            figs = []

            fig1, ax1 = plt.subplots(figsize=(6, 2.6))
            df["grade"].value_counts().plot(kind="pie", autopct="%1.2f%%", ax=ax1)
            ax1.set_ylabel("")
            ax1.set_title("Grade Distribution")
            figs.append(fig1)

            fig2, ax2 = plt.subplots(figsize=(6, 2.6))
            sns.kdeplot(df[df["grade"] == "A+"]["mid"], color="Red", label="A+", ax=ax2)
            sns.kdeplot(df[df["grade"] == "A"]["mid"], color="Blue", label="A", ax=ax2)
            sns.kdeplot(df[df["grade"] == "A-"]["mid"], color="Green", label="A-", ax=ax2)
            sns.kdeplot(df[df["grade"] == "B"]["mid"], color="Purple", label="B", ax=ax2)
            sns.kdeplot(df[df["grade"] == "C"]["mid"], color="Pink", label="C", ax=ax2)
            ax2.legend()
            ax2.set_title("Midterm KDE by Grade")
            figs.append(fig2)

            fig3, ax3 = plt.subplots(figsize=(6, 2.6))
            sns.kdeplot(df[df["grade"] == "A+"]["eval"], color="Red", label="A+", ax=ax3)
            sns.kdeplot(df[df["grade"] == "A"]["eval"], color="Blue", label="A", ax=ax3)
            sns.kdeplot(df[df["grade"] == "A-"]["eval"], color="Green", label="A-", ax=ax3)
            sns.kdeplot(df[df["grade"] == "B"]["eval"], color="Purple", label="B", ax=ax3)
            sns.kdeplot(df[df["grade"] == "C"]["eval"], color="Pink", label="C", ax=ax3)
            ax3.legend()
            ax3.set_title("Teacher Evaluation KDE by Grade")
            figs.append(fig3)


            fig4, ax4 = plt.subplots(figsize=(6, 2.6))
            sns.kdeplot(df[df["grade"] == "A+"]["final"], color="Red", label="A+", ax=ax4)
            sns.kdeplot(df[df["grade"] == "A"]["final"], color="Blue", label="A", ax=ax4)
            sns.kdeplot(df[df["grade"] == "A-"]["final"], color="Green", label="A-", ax=ax4)
            sns.kdeplot(df[df["grade"] == "B"]["final"], color="Purple", label="B", ax=ax4)
            sns.kdeplot(df[df["grade"] == "C"]["final"], color="Pink", label="C", ax=ax4)
            ax4.legend()
            ax4.set_title("Final KDE by Grade")
            figs.append(fig4)

            fig5, ax5 = plt.subplots(figsize=(6, 2.6))
            sns.kdeplot(df[df["grade"] == "A+"]["attendance_percent"], color="Red", label="A+", ax=ax5)
            sns.kdeplot(df[df["grade"] == "A"]["attendance_percent"], color="Blue", label="A", ax=ax5)
            sns.kdeplot(df[df["grade"] == "A-"]["attendance_percent"], color="Green", label="A-", ax=ax5)
            sns.kdeplot(df[df["grade"] == "B"]["attendance_percent"], color="Purple", label="B", ax=ax5)
            sns.kdeplot(df[df["grade"] == "C"]["attendance_percent"], color="Pink", label="C", ax=ax5)
            ax5.legend()
            ax5.set_title("Attendance KDE by Grade")
            figs.append(fig5)

            fig6, ax6 = plt.subplots(figsize=(6, 2.6))
            sns.heatmap(pd.crosstab(df["grade"], df["gender"]), annot=True, fmt="d", cmap="YlGnBu", ax=ax6)
            ax6.set_title("Grade vs Gender")
            ax6.xaxis.tick_top()
            figs.append(fig6)

            for fig, pos in zip(figs, positions):
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.draw()
                canvas.get_tk_widget().grid(row=pos[0], column=pos[1], padx=10, pady=10)

        def show_attendance():
            clear_plots()  # Clear old plots first

            row_idx = 0
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            df["attendance_percent"].plot(kind="kde", title="Attendance Percent KDE", ax=ax1)
            canvas1 = FigureCanvasTkAgg(fig1, master=frame)
            canvas1.draw()
            canvas1.get_tk_widget().grid(row=row_idx, column=0, padx=20, pady=20)

            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.scatterplot(
                x=df["attendance_percent"],
                y=df["final"],
                hue=df["grade"],
                style=df["gender"],
                ax=ax2)
            ax2.set_title("Attendance % vs Final (Grade + Gender)")
            canvas2 = FigureCanvasTkAgg(fig2, master=frame)
            canvas2.draw()
            canvas2.get_tk_widget().grid(row=row_idx, column=1, padx=20, pady=20)
            row_idx += 1

        # Buttons
        Button(button_frame, text="Midterm", width=15, command=show_midterm).pack(side=LEFT, padx=10)
        Button(button_frame, text="Teachers Evaluation", width=20, command=show_teacher_evaluation).pack(side=LEFT,padx=10)
        Button(button_frame, text="Final", width=15, command=show_final).pack(side=LEFT, padx=10)
        Button(button_frame, text="Grade", width=15, command=show_grade).pack(side=LEFT, padx=10)
        Button(button_frame, text="Attendance", width=15, command=show_attendance).pack(side=LEFT, padx=10)

    # ---------- ML PREDICTION ----------
    def ml_prediction():
        conn = connect_db()
        if not conn: return

        df = pd.read_sql_query(
            "SELECT gender, mid, eval, attendance_percent, final, grade FROM students",
            conn
        )
        conn.close()

        if df.empty:
            messagebox.showinfo("No Data", "No student records found.")
            return

        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import accuracy_score

        # Encode categorical variables
        encoder_gender = LabelEncoder()
        df["encoded_gender"] = encoder_gender.fit_transform(df["gender"])

        encoder_grade = LabelEncoder()
        df["encoded_grade"] = encoder_grade.fit_transform(df["grade"])

        # ---------- MODEL 01 : Predict Final Marks ----------
        X_final = df[["encoded_gender", "mid", "eval", "attendance_percent"]]
        y_final = df["final"]

        X_train, X_test, y_train, y_test = train_test_split(X_final, y_final, test_size=0.25, random_state=42)

        scaler_1 = StandardScaler()
        X_train_scaled = scaler_1.fit_transform(X_train)

        model_01 = LinearRegression()
        model_01.fit(X_train_scaled, y_train)

        # Predicted final marks
        scaled_x_final = scaler_1.transform(X_final)
        df["Predicted_final"] = model_01.predict(scaled_x_final)

        # ---------- MODEL 02 : Predict Grade based on Predicted Final ----------
        X_grade = df[["encoded_gender", "mid", "eval", "attendance_percent", "Predicted_final"]]
        y_grade = df[["encoded_grade"]]

        x_grade_train, x_grade_test, y_grade_train, y_grade_test = train_test_split(X_grade, y_grade, test_size=0.25,
                                                                                    random_state=42)

        scaler_2 = StandardScaler()
        scaled_x_grade_train = scaler_2.fit_transform(x_grade_train)
        scaled_x_grade_test = scaler_2.transform(x_grade_test)

        model_02 = DecisionTreeClassifier()
        model_02.fit(scaled_x_grade_train, y_grade_train)

        # Accuracy (optional, you can display in UI)
        score_2 = accuracy_score(y_grade_test, model_02.predict(scaled_x_grade_test))

        # ==========================
        # ADD STUDENT WINDOW
        # ==========================
        def add_student():
            win = Toplevel()
            win.title("Add New Student")
            win.geometry("420x650")
            win.configure(bg="#e0f7fa")

            Label(win, text="Add Student", font=("Helvetica", 18, "bold"),
                  bg="#0288d1", fg="white").pack(fill=X, ipady=8)

            fields = {}

            def add_field(label):
                Label(win, text=label, font=("Helvetica", 13),
                      bg="#e0f7fa").pack(pady=4)
                e = Entry(win, font=("Helvetica", 13))
                e.pack(pady=4)
                fields[label] = e

            add_field("ID")
            add_field("Name")
            add_field("Age")
            add_field("Gender (Male/Female)")
            add_field("Midterm")
            add_field("Teacher Eval")
            add_field("Final")
            add_field("Total")
            add_field("Grade")
            add_field("Attendance %")

            def save_student():
                try:
                    data = (
                        int(fields["ID"].get()),
                        fields["Name"].get(),
                        int(fields["Age"].get()),
                        fields["Gender (Male/Female)"].get(),
                        int(fields["Midterm"].get()),
                        int(fields["Teacher Eval"].get()),
                        int(fields["Final"].get()),
                        int(fields["Total"].get()),
                        fields["Grade"].get(),
                        int(fields["Attendance %"].get())
                    )

                    conn = connect_db()
                    if not conn:
                        return

                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO students
                        (id, name, age, gender, mid, eval, final, total, grade, attendance_percent)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, data)

                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "Student Added Successfully")
                    win.destroy()
                    show_marksheet()  # auto refresh table

                except Exception as e:
                    messagebox.showerror("Error", f"Invalid Data\n{e}")

            Button(win, text="Save Student",
                   font=("Helvetica", 14, "bold"),
                   bg="#0288d1", fg="white",
                   command=save_student).pack(pady=20)

        print(f"Model Accuracy : {round(score_2 * 100)}%")

        # ---------- TKINTER INPUT WINDOW ----------
        win = Toplevel()
        win.title("ML Final & Grade Prediction")
        win.geometry("400x500")
        win.configure(bg="#e0f7fa")

        def add_field(label):
            Label(win, text=label, font=("Helvetica", 13), bg="#e0f7fa").pack(pady=5)
            e = Entry(win, font=("Helvetica", 13))
            e.pack(pady=5)
            return e

        e_mid = add_field("Midterm (0–30)")
        e_eval = add_field("Teacher Eval (0–30)")
        e_att = add_field("Attendance % (0–100)")

        Label(win, text="Gender", font=("Helvetica", 13), bg="#e0f7fa").pack()
        gender_box = ttk.Combobox(win, values=list(encoder_gender.classes_), state="readonly")
        gender_box.current(0)
        gender_box.pack(pady=5)

        result_final = Label(win, text="", font=("Helvetica", 15, "bold"), bg="#e0f7fa")
        result_final.pack(pady=10)

        result_grade = Label(win, text="", font=("Helvetica", 15, "bold"), bg="#e0f7fa")
        result_grade.pack(pady=10)

        def predict():
            try:
                mid = float(e_mid.get())
                eva = float(e_eval.get())
                att = float(e_att.get())

                if not (0 <= mid <= 30): return messagebox.showerror("Error", "Midterm must be 0–30")
                if not (0 <= eva <= 30): return messagebox.showerror("Error", "Eval must be 0–30")
                if not (0 <= att <= 100): return messagebox.showerror("Error", "Attendance must be 0–100")

                g = encoder_gender.transform([gender_box.get()])[0]

                # Predict Final
                data_final = scaler_1.transform([[g, mid, eva, att]])
                final_pred = float(model_01.predict(data_final))
                final_pred = max(0, min(final_pred, 40))
                result_final.config(text=f"Predicted Final Marks: {final_pred:.2f}/40")

                # Predict Grade
                data_grade = scaler_2.transform([[g, mid, eva, att, final_pred]])
                grade_pred_encoded = int(model_02.predict(data_grade))
                grade_pred = encoder_grade.inverse_transform([grade_pred_encoded])[0]
                result_grade.config(text=f"Predicted Grade(not exact): {grade_pred}")

            except:
                messagebox.showerror("Error", "Please enter valid numeric values")

        Button(win, text="Predict", bg="#0288d1", fg="white",
               font=("Helvetica", 13, "bold"), command=predict).pack(pady=10)

    # ---------- LEFT PANEL BUTTONS ----------
    def create_button(text, command):
        b = Button(left, text=text, font=("Helvetica", 14, "bold"), bg="#0288d1", fg="white", width=16, command=command)
        b.pack(pady=20)
        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)
        return b
    create_button("Mark Sheet", lambda: show_marksheet())
    create_button("Student Search", student_search)
    create_button("Result Analysis", result_analysis)
    create_button("ML Prediction", ml_prediction)
    Button(left, text="Back", font=("Helvetica",12,"bold"), bg="#d32f2f", fg="white",
           command=lambda:[admin_frame.pack_forget(), main_screen()]).pack(pady=40)



login_screen()
root.mainloop()
