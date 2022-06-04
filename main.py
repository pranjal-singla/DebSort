import mysql.connector as mysql
from flask import Flask, render_template, request, redirect

db = mysql.connect(host="localhost", user="root", password="Nokia@221415", database='debating')
command_handler = db.cursor(buffered=True)
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template("index.html")

# ---- Defining Authorization Functions ----
def auth_admin(un, pwd):
    command_handler.execute("SELECT * FROM users WHERE user_id=%s AND password=%s AND privilege=%s", (un, pwd, 'admin'))
    if command_handler.rowcount <= 0:
        return render_template("index.html")
    return render_template("admin.html")

def auth_participant(un, pwd):
    command_handler.execute("SELECT * FROM users WHERE user_id=%s AND password=%s AND privilege=%s", (un, pwd, 'participant'))
    if command_handler.rowcount <= 0:
        return render_template("index.html")
    return render_template("participants.html")
# --------------------------------------------------------------------------------------------------

# ---- Log In ----
@app.route('/', methods=['POST'])
def login_submit():
    if request.method != 'POST':
        pass
    else:
        try:
            ltype = request.form['type']
            un = request.form['username']
            pwd = request.form['password']
        except Exception:
            return render_template("index.html")
        if ltype == 'admin':
            return auth_admin(un, pwd)
        elif ltype == 'participant':
            return auth_participant(un, pwd)
        else:
            return render_template("index.html")
# ---------------------------------------------------------------------------------------------------


# ----------- Participant Dashboard --------------
@app.route('/participants', methods=['POST'])
def student_action():
    if request.method != 'POST':
        pass
    else:
        choice = request.form['choice']
        if choice == 'Change Password':
            return render_template('change_password.html', src = '/participants')
        elif choice=='Log Out':
            return render_template('index.html', message="Logged Out Successfully.")
        elif choice=='Institutions':
            command_handler.execute("select code, insti_name from institutions order by insti_name asc;")
            records = command_handler.fetchall()
            cols = ['Code', 'Institution Name']
            return render_template("view.html", message=records, src="/participants", cols=cols)
        elif choice=='Adjudicators':
            command_handler.execute("SELECT name, core from adjudicator_view_participant order by core desc;")
            records = command_handler.fetchall()
            cols = ['Name', 'Core']
            return render_template("view.html", message=records, src="/participants", cols=cols)

        elif choice=='Teams':
            command_handler.execute("select* from team_view_participant;")
            records = command_handler.fetchall()
            cols = ['Name', 'Speaker 1', 'Speaker 2', 'Speaker 3']
            return render_template("view.html", message=records, src="/participants", cols=cols)
        elif choice=='Speakers':
            command_handler.execute("SELECT* from speaker_view_participant;")
            records = command_handler.fetchall()
            cols = ['Name', 'Team Name', 'Speaker Category']
            return render_template("view.html", message=records, src="/participants", cols=cols)
        elif choice=='Back':
            return render_template("participants.html")
# -----------------------------------------------------------------------------------

# ----------- Admin Dashboard --------------
@app.route('/admin', methods=['POST'])
def admin_action():
    if request.method != 'POST':
        pass
    else:
        choice = request.form['choice']
        if choice == 'Add Institutions':
            return render_template("add_institution.html")
        elif choice == 'Add Adjudicators':
            return render_template("add_adjudicator.html")
        elif choice == 'Add Teams':
            return render_template("add_team.html")
        elif choice == 'Add Speakers':
            return render_template("add_speaker.html")
        elif choice == 'Add Users':
            return render_template("add_user.html")
        elif choice == 'View Adjudicators':
            command_handler.execute("select name, base_score, institution, email, gender, core, adj_id, code,region from adjudicators left outer join institutions  on institutions.code = adjudicators.institution;")
            records = command_handler.fetchall()
            cols = ['Name', 'Base Score', 'Institution', 'Email ID', 'Gender', 'Core',  'Adjudicator Number',  'Institution Code', 'Region']
            return render_template("view.html", message=records, src="/participants", cols=cols)
        elif choice == 'Remove Adjudicators':
            return render_template("remove_adjudicator.html")
        elif choice == 'Edit Adjudicators':
            return render_template("edit_adjudicator.html")
# -----------------------------------------------------------------------------------

#EDIT ADJUDICATOR
@app.route('/edit_adjudicator', methods = ['POST'])
def edit_adj():
    if request.method != 'POST':
        pass
    else:
        try:
            ltype = request.form['type']
            un = request.form['username']
            change = request.form['password']
        except Exception:
            return render_template("edit_adjudicator.html", message = 'Please enter correct credentials.')
        if ltype == 'name':
            command_handler.execute("UPDATE adjudicators SET name = %s where adj_id = %s",
                                    (change, un))
            return render_template("edit_adjudicator.html", message = 'Upadted Adjudicator.')
        elif ltype == 'base_score':
            command_handler.execute("UPDATE adjudicators SET base_score = %s where adj_id = %s",
                                    (change, un))
            return render_template("edit_adjudicator.html", message='Upadted Adjudicator.')
        elif ltype == 'institution':
            command_handler.execute("UPDATE adjudicators SET institution = %s where adj_id = %s",
                                    (change, un))
            return render_template("edit_adjudicator.html", message='Upadted Adjudicator.')
        elif ltype == 'email':
            command_handler.execute("UPDATE adjudicators SET email = %s where adj_id = %s",
                                    (change, un))
            return render_template("edit_adjudicator.html", message='Upadted Adjudicator.')
        elif ltype == 'gender':
            command_handler.execute("UPDATE adjudicators SET gender = %s where adj_id = %s",
                                    (change, un))
            return render_template("edit_adjudicator.html", message='Upadted Adjudicator.')
        elif ltype == 'core':
            command_handler.execute("UPDATE adjudicators SET core = %s where adj_id = %s",
                                    (change, un))
            return render_template("edit_adjudicator.html", message='Upadted Adjudicator.')

        else:
            return render_template("admin.html", message = 'Unexpected.')
# -----------------------------------------------------------------------------------



# ADDING AN INSTITUTION
@app.route('/add_institution', methods=['POST', 'GET'])
def add_institution():
    if request.method != 'POST':
        pass
    else:
            code = request.form['code']
            name = request.form['institution-name']
            region = request.form['region']

            queries = [code, name, region]
            print(queries)

            for q in queries:
                if len(q) < 3:
                    render_template('admin.html', message='Please fill all the correct credentials')
            command_handler.execute("INSERT INTO institutions (code, name, region) VALUES (%s, %s, %s)",(code, name, region))
            db.commit()
            return render_template('admin.html', message='Added successfully.')
# -----------------------------------------------------------------------------------

#ADD TEAMS
@app.route('/add_teams', methods=['POST', 'GET'])
def add_team():
    if request.method != 'POST':
        pass
    else:
            team = request.form['team']
            insti_name= request.form['institution-name']
            break_category = request.form['break-category']
            spk1 = request.form['speaker_1']
            spk2 = request.form['speaker_2']
            spk3 = request.form['speaker_3']

            queries = [team, insti_name, break_category, spk1,spk2,spk3]
            print(queries)

            for q in queries:
                if len(q) < 3:
                    render_template('add_teams.html', message='Please fill all the correct credentials')
            command_handler.execute("INSERT INTO institutions VALUES (%s, %s, %s, %s, %s, %s)",(team, insti_name, break_category, spk1,spk2,spk3))
            db.commit()
            return render_template('admin.html', message='Added successfully.')

#ADDING AN ADJUDCIATOR
@app.route('/add_adjudicator', methods=['POST'])
def add_adjudicator():
    if request.method != 'POST':
        pass
    else:
            name = request.form['name']
            base_score = request.form['base_score']
            insti = request.form['institution']
            email = request.form['email']
            gender = request.form['gender']
            core = request.form['core']

            queries = [name, base_score, insti, email, gender, core]
            print(queries)

            for q in queries:
                if len(q) < 6:
                    render_template('add_adjudicator.html', message='Please fill all the correct credentials')
            command_handler.execute("INSERT INTO adjudicators (name, base_score, institution, email, gender, core) VALUES (%s, %s, %s, %s, %s, %s)",(name, base_score, insti, email, gender, core))
            db.commit()
            return render_template('add_adjudicator.html', message='Added successfully.')
#-----------------------------------------------------------------------------------------------------------

#REMOVING ADJUDICATOR
@app.route('/remove', methods = ['POST'])
def remove_adjudicator():
    if request.method != 'POST':
        pass
    else:
        choice = request.form['choice']
        if choice == 'BACK':
            return render_template('admin.html')
        elif choice == 'REMOVE':

            try:
                uid = request.form['name']
                username = request.form['institution']

            except Exception:
                return render_template('admin.html', message="Please enter the correct credentials.")
            command_handler.execute("DELETE from adjudicators where name = %s AND institution = %s",
                                    (uid, username))
            db.commit()
    return render_template('remove_adjudicator.html', message='Adjudicator Deleted!')
#--------------------------------------------------------------------------------------------

#CHANGE PASSWORD ----------------------------------------------------------------------------
@app.route('/change_password', methods=['POST'])
def change_password():
    if request.method != 'POST':
        pass
    else:
        choice = request.form['choice']
        if choice == 'BACK':
            return render_template("participants.html")
        elif choice == 'SUBMIT':
            try:
                username = request.form['username']
                old_password = request.form['old password']
                new_password = request.form['new password']

            except Exception:
                return render_template("participants.html", message="Please enter the correct credentials...")
            command_handler.execute("UPDATE users SET password=%s WHERE user_id=%s AND password=%s",
                                    (new_password, username, old_password))
            db.commit()
    return render_template("participants.html", message='Password Updated!')
# -----------------------------------------------------------------------------------


app.run(debug=True)

