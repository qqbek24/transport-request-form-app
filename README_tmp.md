# bot-template

A template project for every BCOE bot. Works in tandem with rpa-bot library.


Jenkins triggers main.py

Your Task(Process) class inherits from Bot class of the rpa-bot library. Utilize either a built in context manager or a @process decorator.


# Example project domumentation. Please keep all the necessary information.

# my-robot-name

| Data                     | Values
|--------------------------|--------------------------------------------------------------|
| **Developer:**           | Skrypciech Developerski                                         |
| **Business Analyst:**    | Rozkminiusz Dokumentowski                                        |
| **Business Owners:**     | Ksiegucja Klikowska                                        |
| **Redmine:**             | _ci_rpa_AMS - Some Project                       |
|                          | http://vdi-rpaacp-16.europe.mittalco.com/redmine/issues/XXXX|
| **Jenkins:**             | PL/AP/mybot                                              |
| **VM:**                  | acprpa-X-unobtanium-desktop                                        |
| **Initialization Type:** | Scheduled                                                    |
| **Run Periods:**         | - Wednesday (runs for Wednesday(previous)-Thusday(yesterday))                           |
| **Teams folder**         | https://arcelormittal.sharepoint.com/:f:/r/sites/mybot/Shared%20Documents/General?XXXX  |


## Description

Robot extracts data from SAP then performs data manipulation to produce 2 tabs - 'Invoices', 'F4' and a pivot table based on the 'Invoices' tab.

Report run on Wednesday for period between last Wednesday to Thusday (yesterday)

## Input

- SAP extract/File etc. [name/path here]

## Output

- Excel file [name/path here]


# Process

## 1. Robot Start
Scheduled on [ days ] / Triggered via e-mail to run.mybot@arcelormittal.com

Parameters passed:
- bot_mode
- add_my_custom_parameter

## 2. SAP


| Parameter Name       | Value              |
| :---                  |    :----   |
| **SAP System Name:**  | WCE      |
| **Client:**           | "100"                    |
| **Language:**         | 'EN'             |
| **Transaction:**      | YFBL3N           |
| **GL account:**       | 401100 to 401101 |
| **Company Code**      | 086              |
| **Layout**            | //YPAYABLESR     |
| **Variant**           | bot_variant       |

Handled by methods from mysapscript.py

## 3. Excel/Sharepoint or anything else

## X. etc.



# Env setup

Run this commands in Visual Studio Code's terminal in this order:
```
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
```

