from datetime import datetime
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


DEFAULT_TASK_TYPE = "12"
DEFAULT_STATUS = "2"
DEFAULT_START_TIME = "12:00:00"
DEFAULT_END_TIME = "21:00:00"
POST_SUBMIT_WAIT_SECONDS = 2

TIMESHEET_2026_ENTRIES = [
    {"date": "02/01/2026", "task": "MGHP-1814", "description": "All Hands on Deck: Comprehensive ClientCare Integration Testing"},
    {"date": "05/01/2026", "task": "MGHP-1814", "description": "All Hands on Deck: Comprehensive ClientCare Integration Testing"},
    {"date": "06/01/2026", "task": "MGHP-1835", "description": "Fix Nil [] Access Error in ProcessAthenaVisitsCron and Prevent Sentry errors"},
    {"date": "06/01/2026", "task": "MGHP-1836", "description": "Fix TypeError: no implicit conversion of String into Integer in ProcessAthenaVisitsCron"},
    {"date": "07/01/2026", "task": "MGHP-1839", "description": "Fix GitHub Security Alerts for SQL Queries Built from User-Controlled Inputs"},
    {"date": "08/01/2026", "task": "MGHP-1839", "description": "Fix GitHub Security Alerts for SQL Queries Built from User-Controlled Inputs"},
    {"date": "09/01/2026", "task": "MGHP-1839", "description": "Fix GitHub Security Alerts for SQL Queries Built from User-Controlled Inputs"},
    {"date": "12/01/2026", "task": "MGHP-1840", "description": "Fix Athena Orders Retrieval by Using Practice-Aware Integration Mapping Lookup"},
    {"date": "12/01/2026", "task": "MGHP-1841", "description": "Resend Breast Pump Order to Athena for Patient ID 1643"},
    {"date": "13/01/2026", "task": "MGHP-1845", "description": "Add Athena Sticky Note to Indicate Patient RPM Enrollment Status"},
    {"date": "14/01/2026", "task": "MGHP-1846", "description": "Handle Insurance Information with Schedule Data from Client Care"},
    {"date": "16/01/2026", "task": "MGHP-1846", "description": "Handle Insurance Information with Schedule Data from Client Care"},
    {"date": "19/01/2026", "task": "MGHP-1791", "description": "Change asset-generation paths from app/assets to tmp (Sidekiq write-access safe)"},
    {"date": "20/01/2026", "task": "MGHP-1853", "description": "Update Emergency Alert Message to Include Triggering BP Measurement"},
    {"date": "21/01/2026", "task": "MGHP-1857", "description": "Stop Measurement Ingestion and Remove Patient from RPM Maintenance Cohort When Marked Lost to Follow Up"},
    {"date": "23/01/2026", "task": "MGHP-1859", "description": "Update Billing CPT Codes"},
    {"date": "23/01/2026", "task": "MGHP-1861", "description": "Investigate Incorrect Cohort Assignment and Manually Add Patient to Nourish Cohort"},
    {"date": "27/01/2026", "task": "MGHP-1862", "description": "Investigate Breast Pump Order Failure for Patient Cortne Bonilla (#3876)"},
    {"date": "28/01/2026", "task": "MGHP-1862", "description": "Investigate Breast Pump Order Failure for Patient Cortne Bonilla (#3876)"},
    {"date": "29/01/2026", "task": "MGHP-1863", "description": "Prevent Duplicate RPM Maintenance Cohort Creation for Resolved Patients"},
    {"date": "29/01/2026", "task": "MGHP-1864", "description": "Fix Password Reset Failure Due to Case-Sensitive Email Lookup"},
    {"date": "30/01/2026", "task": "MGHP-1863", "description": "Prevent Duplicate RPM Maintenance Cohort Creation for Resolved Patients"},
    {"date": "02/02/2026", "task": "MGHP-1863", "description": "Prevent Duplicate RPM Maintenance Cohort Creation for Resolved Patients"},
    {"date": "03/02/2026", "task": "MGHP-1863", "description": "Prevent Duplicate RPM Maintenance Cohort Creation for Resolved Patients"},
    {"date": "04/02/2026", "task": "MGHP-1865", "description": "BFS Orders Clean UP"},
    {"date": "05/02/2026", "task": "MGHP-1845", "description": "Add Athena Sticky Note to Indicate Patient RPM Enrollment Status"},
    {"date": "06/02/2026", "task": "MGHP-1868", "description": "Update Reset Password Popup Message to Confirm Email Exists in System"},
    {"date": "06/02/2026", "task": "MGHP-1869", "description": "Migrate eClinicalWorks Integration from FHIR DSTU3 to FHIR R4 Before Jan 31, 2026"},
    {"date": "09/02/2026", "task": "MGHP-1819", "description": "Fix Pregnancy Data Issues: Document Transfer, Duplicate Pregnancies, and New Pregnancy Creation"},
    {"date": "10/02/2026", "task": "MGHP-1819", "description": "Fix Pregnancy Data Issues: Document Transfer, Duplicate Pregnancies, and New Pregnancy Creation"},
    {"date": "11/02/2026", "task": "MGHP-1819", "description": "Fix Pregnancy Data Issues: Document Transfer, Duplicate Pregnancies, and New Pregnancy Creation"},
    {"date": "12/02/2026", "task": "MGHP-1819", "description": "Fix Pregnancy Data Issues: Document Transfer, Duplicate Pregnancies, and New Pregnancy Creation"},
    {"date": "13/02/2026", "task": "MGHP-1819", "description": "Fix Pregnancy Data Issues: Document Transfer, Duplicate Pregnancies, and New Pregnancy Creation"},
    {"date": "16/02/2026", "task": "MGHP-1818", "description": "MGHP-1818:Enable Second Pregnancy Handling from ECW with Integration Mapping Support"},
    {"date": "17/02/2026", "task": "MGHP-1818", "description": "MGHP-1818:Enable Second Pregnancy Handling from ECW with Integration Mapping Support"},
    {"date": "18/02/2026", "task": "MGHP-1879", "description": "Fix Healthix File Upload Failure from Mother Goose App (S3 PutObjectAcl Blocked)"},
    {"date": "19/02/2026", "task": "MGHP-1880", "description": "Investigate Missing Sync for Approved Breast Pump Orders from Athena (User IDs: 4791, 4443, 4294)"},
    {"date": "20/02/2026", "task": "MGHP-1881", "description": "Exclude WHG-Chicago Patients from “Not Having Final Due Date” Weekly Report + Validate Report Logic"},
    {"date": "20/02/2026", "task": "MGHP-1882", "description": "Sentry: NoMethodError – undefined method name for MgCohort (Monthly RPM Maintenance)"},
    {"date": "23/02/2026", "task": "MGHP-1891", "description": "(DTC investigation)Validate Existing User by Email or Mobile in MGH DB and Return User + Practice Information"},
    {"date": "24/02/2026", "task": "MGHP-1891", "description": "(DTC Planning)Validate Existing User by Email or Mobile in MGH DB and Return User + Practice Information"},
    {"date": "25/02/2026", "task": "MGHP-1892", "description": "Implement Create User API (POST) with Uniqueness Validation"},
    {"date": "25/02/2026", "task": "MGHP-1893", "description": "Implement POST /user_id/register_existing_user API for EHR Validation, Integration Mapping Update, and Pregnancy Creation"},
    {"date": "26/02/2026", "task": "MGHP-1894", "description": "Fix NoMethodError: undefined method 'disabled' for nil:NilClass in SendMailOfUsersListNotHavingFinalDueDate"},
    {"date": "27/02/2026", "task": "MGHP-1893", "description": "Implement POST /user_id/register_existing_user API for EHR Validation, Integration Mapping Update, and Pregnancy Creation"},
    {"date": "02/03/2026", "task": "MGHP-1893", "description": "Implement POST /user_id/register_existing_user API for EHR Validation, Integration Mapping Update, and Pregnancy Creation"},
    {"date": "03/03/2026", "task": "MGHP-1896", "description": "Add Patients to Nourish Cohort for #1641 and #1345"},
    {"date": "03/03/2026", "task": "MGHP-1893", "description": "Implement POST /user_id/register_existing_user API for EHR Validation, Integration Mapping Update, and Pregnancy Creation"},
    {"date": "04/03/2026", "task": "MGHP-1175", "description": "EcwDirectController and GenerateOAuthUrl Route (POST)"},
    {"date": "05/03/2026", "task": "MGHP-1175", "description": "EcwDirectController and GenerateOAuthUrl Route (POST)"},
    {"date": "06/03/2026", "task": "MGHP-1175", "description": "EcwDirectController and GenerateOAuthUrl Route (POST)"},
    {"date": "09/03/2026", "task": "MGHP-1178", "description": "AccessTokens Table"},
    {"date": "09/03/2026", "task": "MGHP-1179", "description": "User can have many integration_mappings"},
    {"date": "10/03/2026", "task": "MGHP-1182", "description": "EcwDirect::PrepUpsertAccessToken.rb Interactor and Rspec"},
    {"date": "10/03/2026", "task": "MGHP-1181", "description": "ECW Redirect Route"},
    {"date": "11/03/2026", "task": "MGHP-1181", "description": "ECW Redirect Route"},
    {"date": "12/03/2026", "task": "MGHP-1183", "description": "EcwDirect::HandleRedirectAuthAndIngest.rb Interactor"},
    {"date": "13/03/2026", "task": "MGHP-1183", "description": "EcwDirect::HandleRedirectAuthAndIngest.rb Interactor"},
    {"date": "16/03/2026", "task": "MGHP-1904", "description": "Update TBFS API Endpoints and Credentials Based on BFS API Workflow Changes"},
    {"date": "16/03/2026", "task": "MGHP-1907", "description": "Create Interactor to Fetch Access Token Using Refresh Token for eCW Patient Portal APIs"},
    {"date": "17/03/2026", "task": "MGHP-1907", "description": "Create Interactor to Fetch Access Token Using Refresh Token for eCW Patient Portal APIs"},
    {"date": "18/03/2026", "task": "MGHP-1908", "description": "Fetch Encounters - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "19/03/2026", "task": "MGHP-1908", "description": "Normalize and Encounter details and upsert Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "20/03/2026", "task": "MGHP-1908", "description": "Normalize and upsert Condition (Encounter Diagnosis) details - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "23/03/2026", "task": "MGHP-1908", "description": "Normalize and upsert Observation (Vitals)details - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "24/03/2026", "task": "MGHP-1908", "description": "Normalize and upsert DocumentReference (Clinical Notes) - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "25/03/2026", "task": "MGHP-1908", "description": "Normalize and upsert Immunization - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "26/03/2026", "task": "MGHP-1908", "description": "Normalize and upsert Location and Organization- Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "27/03/2026", "task": "MGHP-1908", "description": "Normalize and upsert Medication details - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "30/03/2026", "task": "MGHP-1908", "description": "Normalize and upsert DiagnosticReport (Laboratory Results Reporting) - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "31/03/2026", "task": "MGHP-1908", "description": "Normalize and upsert Practitioner details - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "01/04/2026", "task": "MGHP-1908", "description": "Normalize and upsert Coverage - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "02/04/2026", "task": "MGHP-1908", "description": "Normalize and upsert Coverage - Fetch Past 1 Year User Resources via eCW patient portal After Initial Access Token Retrieval (Background Job)"},
    {"date": "03/04/2026", "task": "MGHP-1916", "description": "Investigate Missing Approved Breast Pump Order from Athena Not Reflected in MGH DB"},
    {"date": "07/04/2026", "task": "MGHP-1917", "description": "Implement DTC User Subscription Page with Authentication"},
    {"date": "08/04/2026", "task": "MGHP-1917", "description": "Implement DTC User Subscription Page with Authentication"},
    {"date": "09/04/2026", "task": "MGHP-1922", "description": "Fix Appointment Reminders Being Sent for Lenox Patients Despite Feature Being Disabled"},
    {"date": "09/04/2026", "task": "MGHP-1921", "description": "Add API to Capture DTC Patient Insurance Details and Prioritize Over EHR Data"},
    {"date": "10/04/2026", "task": "MGHP-1921", "description": "Add API to Capture DTC Patient Insurance Details and Prioritize Over EHR Data"},
    {"date": "14/04/2026", "task": "MGHP-1921", "description": "Add API to Capture DTC Patient Insurance Details and Prioritize Over EHR Data"},
    {"date": "16/04/2026", "task": "MGHP-1921", "description": "Add API to Capture DTC Patient Insurance Details and Prioritize Over EHR Data"},
    {"date": "17/04/2026", "task": "MGHP-1921", "description": "Add API to Capture DTC Patient Insurance Details and Prioritize Over EHR Data"},
    {"date": "20/04/2026", "task": "MGHP-1928", "description": "Test Athena Document Upload Using originalfilename for Custom Labeling with Clinical Document Subclass"},
    {"date": "21/04/2026", "task": "MGHP-1930", "description": "Implement Reusable Chart Alert Interactor for Referral Alerts in Athena"},
    {"date": "22/04/2026", "task": "MGHP-1931", "description": "Investigate Missing Patient Ingestion for Teresa Moquete Gonzales and Manually Create if Needed"},
    {"date": "24/04/2026", "task": "MGHP-1930", "description": "Implement Reusable Chart Alert Interactor for Referral Alerts in Athena"},
    {"date": "27/04/2026", "task": "MGHP-1932", "description": "Send Email Notifications to Care Team for Failed EHR Patient or Visit Ingestion with Error Details"},
    {"date": "28/04/2026", "task": "MGHP-1935", "description": "Investigate Appointment Time Discrepancies Between MGH and Athena Encounters"},
    {"date": "29/04/2026", "task": "MGHP-1936", "description": "Implement iHealth BP Cuff Order Tracking Number Sync via Order ID and Webhook"},
    {"date": "30/04/2026", "task": "MGHP-1936", "description": "Implement iHealth BP Cuff Order Tracking Number Sync via Order ID and Webhook"},
    {"date": "30/04/2026", "task": "MGHP-1937", "description": "Manually Insert Patient Evangelia Pantazis into MGH Backend Due to Appointment Type Mismatch"},
]


def trigger_change(driver, element):
    driver.execute_script(
        """
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """,
        element,
    )


def set_text_input(driver, element, value):
    driver.execute_script(
        """
        const input = arguments[0];
        const fieldValue = arguments[1];
        input.focus();
        input.value = '';
        input.value = fieldValue;
        if (window.jQuery) {
            window.jQuery(input).val(fieldValue).trigger('input').trigger('change').trigger('blur');
        }
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new Event('blur', { bubbles: true }));
        """,
        element,
        value,
    )


def set_date_input(driver, date_input, value):
    driver.execute_script(
        """
        const input = arguments[0];
        const dateValue = arguments[1];
        input.removeAttribute('readonly');
        input.value = dateValue;
        if (window.jQuery) {
            window.jQuery(input).val(dateValue).trigger('change').trigger('blur');
        }
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new Event('blur', { bubbles: true }));
        """,
        date_input,
        value,
    )


def set_description(driver, textarea, value):
    driver.execute_script(
        """
        const input = arguments[0];
        const content = arguments[1];
        input.value = content;
        if (window.CKEDITOR && CKEDITOR.instances && CKEDITOR.instances.pagecontent) {
            CKEDITOR.instances.pagecontent.setData(content);
            CKEDITOR.instances.pagecontent.updateElement();
        }
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        """,
        textarea,
        value,
    )


def select_value(driver, wait, element_id, value):
    dropdown = wait.until(EC.presence_of_element_located((By.ID, element_id)))
    driver.execute_script(
        """
        const select = arguments[0];
        const selectedValue = arguments[1];
        select.value = selectedValue;
        if (window.jQuery) {
            window.jQuery(select).val(selectedValue).trigger('change').trigger('blur');
        }
        select.dispatchEvent(new Event('change', { bubbles: true }));
        select.dispatchEvent(new Event('blur', { bubbles: true }));
        """,
        dropdown,
        value,
    )
    wait.until(lambda d: d.find_element(By.ID, element_id).get_attribute("value") == value)
    return dropdown


def normalize_date(date_value):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_value.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {date_value}")


def build_entries():
    if len(sys.argv) >= 2:
        entry_date = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y-%m-%d")
        return [{
            "date": normalize_date(entry_date),
            "task": sys.argv[1],
            "description": sys.argv[2] if len(sys.argv) > 2 else "",
        }]
    return [
        {
            **entry,
            "date": normalize_date(entry["date"]),
        }
        for entry in TIMESHEET_2026_ENTRIES
    ]


def login(driver, wait):
    driver.get("https://mycipl.in/")

    username = wait.until(EC.presence_of_element_located((By.ID, "login_user")))
    password = wait.until(EC.presence_of_element_located((By.ID, "login_pwd")))

    username.send_keys(os.getenv("MYCIPL_USERNAME", "hemachandran@colanonline.com"))
    password.send_keys(os.getenv("MYCIPL_PASSWORD", "Nxmoc9$"))

    wait.until(EC.element_to_be_clickable((By.ID, "login_submit"))).click()


def open_manual_timesheet_form(driver, wait):
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'module=ts')]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[2]/ul/li[3]/a"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//table//tr[6]/td[6]/a[1]"))).click()
    wait.until(EC.presence_of_element_located((By.ID, "add_tab")))
    return driver.current_url


def open_saved_form(driver, wait, form_url):
    driver.get(form_url)
    wait.until(EC.presence_of_element_located((By.ID, "add_tab")))


def fill_billable_timesheet(driver, wait, entry):
    select_value(driver, wait, "mile", "General_Bill")
    wait.until(lambda d: d.find_element(By.ID, "billable_form").is_displayed())
    wait.until(lambda d: d.find_element(By.ID, "billable_genform").is_displayed())

    task_input = wait.until(EC.presence_of_element_located((By.ID, "task1")))
    set_text_input(driver, task_input, entry["task"])
    wait.until(lambda d: d.find_element(By.ID, "task1").get_attribute("value").strip() == entry["task"])

    select_value(driver, wait, "type", DEFAULT_TASK_TYPE)

    date_input = wait.until(EC.presence_of_element_located((By.ID, "date1")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_input)
    set_date_input(driver, date_input, entry["date"])
    wait.until(lambda d: d.find_element(By.ID, "date1").get_attribute("value").strip() == entry["date"])

    if entry["description"]:
        description_input = wait.until(EC.presence_of_element_located((By.ID, "pagecontent")))
        set_description(driver, description_input, entry["description"])
        wait.until(lambda d: entry["description"] in d.find_element(By.ID, "pagecontent").get_attribute("value"))

    select_value(driver, wait, "status1", DEFAULT_STATUS)
    select_value(driver, wait, "tms_sttime", DEFAULT_START_TIME)
    select_value(driver, wait, "tms_endtime", DEFAULT_END_TIME)

    wait.until(lambda d: d.find_element(By.ID, "hr").get_attribute("value").strip() != "")
    wait.until(lambda d: d.find_element(By.ID, "mins").get_attribute("value").strip() != "")
    wait.until(lambda d: d.find_element(By.ID, "add_ts").get_attribute("disabled") is None)

    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "add_ts")))
    driver.execute_script("arguments[0].click();", submit_button)


def run():
    entries = build_entries()

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    wait = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        form_url = open_manual_timesheet_form(driver, wait)

        for index, entry in enumerate(entries, start=1):
            try:
                if index > 1:
                    open_saved_form(driver, wait, form_url)

                fill_billable_timesheet(driver, wait, entry)
                print(f"[{index}/{len(entries)}] Submitted {entry['date']} - {entry['task']}")
                time.sleep(POST_SUBMIT_WAIT_SECONDS)
            except Exception as exc:
                print(f"[{index}/{len(entries)}] Skipped {entry['date']} - {entry['task']}: {exc}")
                continue
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
