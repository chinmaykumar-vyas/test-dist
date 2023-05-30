import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, send_file, redirect, flash


app = Flask(__name__)
app.secret_key = 'secret_key' 

employee_list = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')
        
    
@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        # Get the survey data from the form
        employee_code = int(request.form["employee_code"])
        age = int(request.form["age"])
        gender = request.form["gender"]
        marital_status = request.form["marital_status"]
        job_location = request.form["job_location"]
        domicile_state = request.form["domicile_state"]
        department = request.form["department"]
        grade = request.form["grade"]
        education = request.form["education"]
        compa_ratio = float(request.form["compa_ratio"])
        job_level = int(request.form["job_level"])
        pms_1 = request.form["pms_1"]
        pms_2 = request.form["pms_2"]
        pms_3 = request.form["pms_3"]
        adani_exp = int(request.form["adani_exp"])
        previous_exp = int(request.form["previous_exp"])
        total_exp = int(request.form["total_exp"])
        job_clarity = int(request.form["job_clarity"])
        rewards_recognition = int(request.form["rewards_recognition"])
        l_d = int(request.form["l_d"])
        job_satisfaction = int(request.form["job_satisfaction"])
        company_culture1 = int(request.form["company_culture1"])
        over18 = request.form["over18"]
        employee_empowerment = int(request.form["employee_empowerment"])
        empowerment = int(request.form["empowerment"])
        company_culture2 = int(request.form["company_culture2"])
        communication = int(request.form["communication"])
        transparency = int(request.form["transparency"])
        workplace_wellbeing = int(request.form["workplace_wellbeing"])
        employee_wellness = int(request.form["employee_wellness"])
        employee_integrity = int(request.form["employee_integrity"])
        wlb1 = int(request.form["wlb1"])
        wlb2 = int(request.form["wlb2"])
        wlb3 = int(request.form["wlb3"])
        pattern_of_communication = int(request.form["pattern_of_communication"])
        team = int(request.form["team"])
        compensation = int(request.form["compensation"])
        welfare_facilities = int(request.form["welfare_facilities"])

        gender = gender1(gender)
        marital_status = Mar(marital_status)
        job_location = Job_location1(job_location)
        domicile_state=location(domicile_state)
        grade=Grade1(grade)

        pms = {'TP':1 , 'GP': 2, 'SP':2 , 'IP':3}
        pms_1 = pms[pms_1]
        pms_2 = pms[pms_2]
        pms_3 = pms[pms_3]

        edu = {'Diploma' : 1 , 'Bachelors' : 2, 'Masters' : 3, 'PhD' : 4}
        education = edu[education]

        temp = department

        dept_list=['AEL Support Service', 'Administration', 'Analytics', 'Business Excellence', 'Business Head Office',
                    'CEO Office', 'Contract Administration','Corporate Social\xa0Responsibility', 'Engineering Resource Center',
                    'Engineering Services', 'Environment', 'Estimation', 'Finance & Accounts', 'HSE', 'Health Services',
                    'Human Resources', 'Information Technology', 'Land Acquisition & CSR', 'Land Acquisition and R&R',
                    'Legal', 'Logistics', 'Mine Operation', 'Mine Planning', 'Mineral Resources & Exploration', 'Operations',
                    'Operations & Maintenance - Railways', 'Operations & Technology', 'PRMC', 'Projects', 'Proposal & Estimation',
                    'Quality Assurance & Control', 'Railway Services', 'Safety', 'Security', 'Strategy &  business development',
                    'Sustainability & compliances', 'Techno Commercial', 'Technology']
        
        dept_list = [1 if dept==temp else 0 for dept in   dept_list]


        set_employees_data([
            1, 1, age, education, compa_ratio, job_level, 1, pms_1, pms_2, pms_3, adani_exp, previous_exp,
            total_exp, job_clarity, rewards_recognition, l_d, job_satisfaction, company_culture1,
            employee_empowerment, empowerment, company_culture2, communication, transparency,
            workplace_wellbeing, employee_wellness, employee_integrity, wlb1, wlb2, wlb3,
            pattern_of_communication, team, compensation, welfare_facilities, domicile_state, marital_status, job_location, gender, grade
        ])

        df = pd.DataFrame([employee_list[0]+dept_list], columns=['Unnamed: 0','employee_number','age','education','compa_ratio','job_level', 'employee_count','pms_1','pms_2','pms_3',
                   'adani_exp','previous_exp','total_exp','job_clarity', 'rewards_recognition',
                    'l&d', 'job_satisfaction', 'company_culture1', 'employee_empowerment', 'empowerment', 'company_culture2',
                    'communication', 'tranparency', 'workplace_well-being', 'employee_wellness', 'employee_integrity',
                    'wlb1', 'wlb2', 'wlb3', 'pattern of communication', 'team', 'Compensation', 'welfare_facilities',
                    'new_location', 'Mar1', 'New_JobL', 'New_gen', 'New_grade',
                    'AEL Support Service', 'Administration', 'Analytics', 'Business Excellence', 'Business Head Office',
                    'CEO Office', 'Contract Administration','Corporate Social\xa0Responsibility', 'Engineering Resource Center',
                    'Engineering Services', 'Environment', 'Estimation', 'Finance & Accounts', 'HSE', 'Health Services',
                    'Human Resources', 'Information Technology', 'Land Acquisition & CSR', 'Land Acquisition and R&R',
                    'Legal', 'Logistics', 'Mine Operation', 'Mine Planning', 'Mineral Resources & Exploration', 'Operations',
                    'Operations & Maintenance - Railways', 'Operations & Technology', 'PRMC', 'Projects', 'Proposal & Estimation',
                    'Quality Assurance & Control', 'Railway Services', 'Safety', 'Security', 'Strategy &  business development',
                    'Sustainability & compliances', 'Techno Commercial', 'Technology'])
        
        X_test = df
        l = predict(X_test)

        if l[0] == 'stay':
            result = f'Employee is more likely to STAY with Organization'
        else:
            result = f'Employee is more likely to LEAVE with Organization' 
        return render_template('output.html', result=result)

    return render_template("survey.html")

@app.route('/upload', methods=['POST'])
def upload():
    # Retrieve the uploaded survey file
    survey_file = request.files['survey_file']
    
    # Save the file locally
    file_path = 'survey.xlsx'
    survey_file.save(file_path)
    
    data = pd.read_excel(file_path)
    data_ds = data["domicile_state"].apply(location)
    data['new_location'] = data_ds

    data_ms = data["marital_status"].apply(Mar)
    data['Mar1'] = data_ms

    data_jl = data["job_location"].apply(Job_location1)
    data['New_JobL'] = data_jl

    data_g = data["gender"].apply(gender1)
    data['New_gen'] = data_g

    data['New_grade'] = data['grade'].apply(Grade1)

    dept = pd.get_dummies(data["department"])
    dept = dept.replace({False : 0 ,True : 1})
    data= pd.concat([data, dept], axis = 1)

    columns_to_drop = ['gender', 'marital_status', 'job_location', 'employee_code', 'employee_number', 'employee_count', 'domicile_state', 'department', 'stay/left', 'grade', 'over18']
    data1 = data.drop(columns=columns_to_drop,errors='ignore')
    data1['Unnamed: 0'] = np.nan
    data1['employee_number'] = np.nan
    data1['employee_count'] = np.nan
    data1.fillna(1, inplace=True)
    data1['compa_ratio'] = data1['compa_ratio'].replace({'No PMS' : 0})
    #data1['Corporate Social\xa0Responsibility'] = np.nan

    data1 = data1[['Unnamed: 0','employee_number','age','education','compa_ratio','job_level', 'employee_count','pms_1','pms_2','pms_3',
                   'adani_exp','previous_exp','total_exp','job_clarity', 'rewards_recognition',
                    'l&d', 'job_satisfaction', 'company_culture1', 'employee_empowerment', 'empowerment', 'company_culture2',
                    'communication', 'tranparency', 'workplace_well-being', 'employee_wellness', 'employee_integrity',
                    'wlb1', 'wlb2', 'wlb3', 'pattern of communication', 'team', 'Compensation', 'welfare_facilities',
                    'new_location', 'Mar1', 'New_JobL', 'New_gen', 'New_grade',
                    'AEL Support Service', 'Administration', 'Analytics', 'Business Excellence', 'Business Head Office',
                    'CEO Office', 'Contract Administration','Corporate Social\xa0Responsibility', 'Engineering Resource Center',
                    'Engineering Services', 'Environment', 'Estimation', 'Finance & Accounts', 'HSE', 'Health Services',
                    'Human Resources', 'Information Technology', 'Land Acquisition & CSR', 'Land Acquisition and R&R',
                    'Legal', 'Logistics', 'Mine Operation', 'Mine Planning', 'Mineral Resources & Exploration', 'Operations',
                    'Operations & Maintenance - Railways', 'Operations & Technology', 'PRMC', 'Projects', 'Proposal & Estimation',
                    'Quality Assurance & Control', 'Railway Services', 'Safety', 'Security', 'Strategy &  business development',
                    'Sustainability & compliances', 'Techno Commercial', 'Technology']]
    

    X_test = data1
    l = predict(X_test)
    df=pd.DataFrame(l, columns=['stay/left'])

    data1['employee_code'] = data['employee_code']
    data1['stay/left'] = df
    
    data1.drop(columns=['employee_number','employee_count','Unnamed: 0'])

    # Save the modified DataFrame to a new Excel file
    output_file = 'survey_result.xlsx'
    data1.to_excel(output_file, index=False)

    # Remove the uploaded file
    survey_file.close()
    os.remove(file_path)
    
    # Redirect to the download route with the filename
    return redirect('/download/{}'.format(output_file))

@app.route('/download/<filename>')
def download(filename):
    # Provide the modified Excel file for download
    return send_file(filename, as_attachment=True)

def location(x):
    location_dict_new = {
    'Gujarat'          :8,
    'Bihar'            :7,
    'Madhya Pradesh'   :6,
    'Uttar Pradesh'    :6,
    'Jharkhand'        :5,
    'Odisha'           :5,
    'Chattisgarh'      :5,
    'Rajasthan'        :5,
    'West Bengal'      :4,
    'Haryana'          :4,
    'Maharashtra'      :4,
    'Karnataka'        :4,
    'Himachal Pradesh' :3,
    'Tamil Nadu'       :3,
    'Kerela'           :3,
    'Telangana'        :3,
    'Andhra Pradesh'   :2,
    'New Delhi'        :2,
    'Goa'              :1
}
    if str(x) in location_dict_new.keys():
        return location_dict_new[str(x)]
    else:
        return 0
    
def Mar(x):
    if x == 'Married':
        return int(1)
    else:
        return int(0)    
    
def Job_location1(x):
    if x == 'Corporate':
        return int(1)
    else:
        return int(0)
    
def gender1(x):
    if x == 'Male':
        return int(1)
    else:
        return int(0)   

def Grade1(x):
    grade_dict_new = {
    'O1' : 1,
    'O2' : 2,
    'O3' : 3,
    'O4' : 4,
    'O5' : 5,
    'E1' : 6,
    'E2' : 7,
    'E3' : 8,
    'E4' : 9,
    'GM' :10,
    'AP' :11,
    'VP' :12,
    'SP' :13,
    'JP' :14,
    'PR' :15
}
    if str(x) in grade_dict_new.keys():
        return grade_dict_new[str(x)]
    else:
        return None     



def set_employees_data(employee):
    # Add employee data to the list
    employee_list.append(employee)

@app.route("/save_data", methods=["POST"])
def save_data():
    # Convert employee data to DataFrame
    df = pd.DataFrame(employee_list, columns=[
        "Employee Code", "Age", "Gender", "Marital Status", "Job Location", "Domicile State", "Department", "Grade",
        "Education", "Compensation Ratio", "Job Level", "PMS 1", "PMS 2", "PMS 3", "Adani Exp",
        "Previous Exp", "Total Exp", "Job Clarity", "Rewards Recognition", "L&D", "Job Satisfaction",
        "Company Culture 1", "Over 18", "Employee Empowerment", "Empowerment", "Company Culture 2", "Communication",
        "Transparency", "Workplace Wellbeing", "Employee Wellness", "Employee Integrity", "WLB 1", "WLB 2", "WLB 3",
        "Pattern of Communication", "Team", "Compensation", "Welfare Facilities"
    ])

    # Save the DataFrame to a CSV file
    df.to_csv("employee_data.csv", index=False)

    # Clear employee data list
    employee_list.clear() 

def predict(X_test):
    # opening the file- model_jlib
    m_jlib = joblib.load('model_lr')

    # check prediction
    return m_jlib.predict(X_test) # similar output

if __name__ == "__main__":
    app.run(debug=True)