from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user, logout_user
from .models import User
from . import db
import json
import datetime
import os
import pandas as pd
import numpy as np

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    students_list = pd.read_csv("./website/student_list.csv",encoding="utf_8_sig")
    StudentID = current_user.StudentID
    idx = current_user.idx_csv
    # group = current_user.group # don't want to use the group from sql. because group changes
    group = int(students_list.loc[students_list["ID"]==StudentID]["Group"])
    idx_group =np.where(students_list["Group"] == group)[0]
    user_name = students_list.iloc[idx,0]
    teammate_idxs = [idxs for idxs in idx_group if idxs != idx]
    teammate_names = []
    for i in range(len(teammate_idxs)): # maybe can remove some staff, but just keep it for now
        teammate_names.append(students_list.iloc[teammate_idxs[i], 0]) # 0 for name in sheet
    team_all_member = teammate_names.copy()
    team_all_member.insert(0,user_name)
    # test_teammate = ['Austin', "Jacob"]
    # flash([StudentID, idx, group, teammate_idxs, type(teammate_names)], category='error')
    # flash(int(idx), category='success')

    if request.method == 'POST':
        students_con = pd.read_csv("student_con.csv",encoding="utf_8_sig")
        score_dict = {"No contribution":0, "Minor contribution":1, "Contributed actively":2, "Major contribution":3, "Did all the work":4, "Drop":None}
        score = []
        _, week, day = datetime.date.today().isocalendar() # count week, devide by every Thursday
        if day in [1,2,3]:
            week -= 1
        if "s{week}".format(week=week) not in students_con.columns and "m{week}".format(week=week) not in students_con.columns :
            students_con["s{week}".format(week=week)]=0
            students_con["m{week}".format(week=week)]=0

        for i in range(len(team_all_member)): # get all data from HTML
            score.append(request.form.get(team_all_member[i]))


        if "Select contribution" in score:
            flash("Please select contribution", category='error')
            return render_template("home.html", user=current_user, team_all_member=team_all_member)
        else:
            flash("Thanks for survey. Your selection: {name}:{score}".format(name=team_all_member, score=score), category='success')
            students_con.loc[int(idx),"s{week}".format(week=week)] = score_dict[score[0]] # add self score, s for self


        score_to_save = [score_dict[score[j]] for j in range(1, len(score))] # check is m{week}.npy exist, and store score inside
        if os.path.isfile("./statistics_files/m{week}.npy".format(week=week)):# the data structure, [[],[],...] idx 0 means group 0
            score_file = np.load("./statistics_files/m{week}.npy".format(week=week), allow_pickle=True)
            score_file[idx] = score_to_save
            np.save("./statistics_files/m{week}.npy".format(week=week), score_file)
        else:
            score_file = [[] for k in range(len(students_list.iloc[:, 0]))]
            score_file[idx] = score_to_save
            np.save("./statistics_files/m{week}.npy".format(week=week), score_file)
       
        students_con.to_csv("student_con.csv",index=False, encoding="utf_8_sig")
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template("home.html", user=current_user, team_all_member=team_all_member)



@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        if request.form['submit_button'] == 'calculate_contribution_score':
            students_con = pd.read_csv("student_con.csv",encoding="utf_8_sig") # generate week
            _, week, day = datetime.date.today().isocalendar()
            if day in [1,2,3]:
                week -= 1
            score_file = np.load("./statistics_files/m{week}.npy".format(week=week), allow_pickle=True)
            survey_number_count = np.zeros(len(score_file))
            for i in range(len(survey_number_count)): # initial the score
                students_con.loc[i,"m{week}".format(week=week)] = 0
            
            for score_idx in range(len(score_file)):
                group = students_con.iloc[score_idx, 2]
                if len(score_file[score_idx])>0:
                    idx_group =np.where(students_con["Group"] == group)[0] # find group
                    teammate_idxs = [idxs for idxs in idx_group if idxs != score_idx]
                    for i in range(len(teammate_idxs)):
                        # print(score_file[score_idx],teammate_idxs )
                        if score_file[score_idx][i] != None: # add score in csv, count how many score for each student. devide them after
                            students_con.loc[teammate_idxs[i],"m{week}".format(week=week)] += score_file[score_idx][i] #m for member
                            survey_number_count[teammate_idxs[i]] += 1 
            
            for count_idx in range(len(survey_number_count)):
                if survey_number_count[count_idx] != 0: # calculate average
                    students_con.loc[count_idx,"m{week}".format(week=week)] = students_con.loc[count_idx,"m{week}".format(week=week)]/survey_number_count[count_idx]
                # pass
            students_con.to_csv("student_con.csv",index=False, encoding="utf_8_sig")
            flash("calulation done", category='success')
        elif request.form["submit_button"] == "delet_user": # remove user account from aql database
            ResetID=request.form.get('ResetID').upper()
            user = User.query.filter_by(StudentID=ResetID).first()
            if user:
                obj = User.query.filter_by(StudentID=ResetID).one()
                db.session.delete(obj)
                db.session.commit()
                flash("Reset {ID}".format(ID=ResetID), category='success')
            else:
                flash("No user: {ID}".format(ID=ResetID), category='error')
        else:
            pass

    return render_template("admin.html", user=current_user)
