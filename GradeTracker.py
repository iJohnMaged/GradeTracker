import configparser
import requests
import json
import os
from plyer import notification as notf

def read_config_file(config_file):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_file)
    data = dict()

    for section in config:
        data[section] = dict(config[section])

    return data


def write_grades(grades_dict, filename):
    output = ""

    for course, grade in grades_dict.items():
        output += course + ":" + grade + "\n"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(output)


def compare_write_grades(json_obj, filename):
    grades_dict = clean_dict_from_json(json_obj)
    saved_grades_dict = clean_dict_from_file(filename)

    if len(saved_grades_dict) == 0:
        write_grades(grades_dict, filename)
        notf.notify(title="Grades loaded!", message="Grades has been loaded to grades.txt!")
        return

    changed = False
    for course, grade in grades_dict.items():
        if (course in saved_grades_dict and grade != saved_grades_dict[course].rstrip('\n')) or course not in saved_grades_dict:
            changed = True

    if changed:
        notf.notify(title="NEW GRADES!", message="New grades is available, loaded  to grades.txt!")
        write_grades(grades_dict, filename)

    return grades_dict


def clean_dict_from_file(filename):
    if not os.path.isfile(filename):
        open(filename, 'w').close()
        return {}

    result = dict()

    with open(filename, 'r') as f:
        for line in f.readlines():
            data = line.split(':')
            result[data[0]] = data[1]

    return result


def clean_dict_from_json(json_obj):
    result = dict()

    for row in json_obj:
        grade_list = row['FinalGradeName'].split('|')
        result[row['CrName']] = str(grade_list[1]) if len(grade_list) == 2 else ''

    return result

def output_grades(grades):

    for course, grade in grades.items():
        letter = grade if grade else 'Not available'
        print(course + ": " + letter + "\n")

def check_grades():
    config = "config.ini"
    grades = "grades.txt"

    data = read_config_file(config)
    login_ = data['site']['login_url']
    JCI = data['site']['jci_url']

    requests.packages.urllib3.disable_warnings()

    print("Connecting to the server and grabbing information...\n\n")
    with requests.Session() as session:

        response = session.post(login_, data=data['formdata'], headers=data['headers'], verify=False)
        data['headers2']['Cookie'] = 'userID=' + response.cookies.get('userID')
        jci_form_data = data['jci_form_data']

        r = session.post(JCI, data=jci_form_data, headers=data['headers2'], verify=False)

        try:
            grades_dict = compare_write_grades(r.json()['Data'], grades)
            output_grades(grades_dict)
            input('Press any key to exit..')
        except json.decoder.JSONDecodeError:
            print(":(")

def main():
    check_grades()

if __name__ == "__main__":
    check_grades()
