Appointments table
clinic_id string
provider_id string
appt_datetime datetime
appt_type string
lead_time_days integer
prior_no_shows integer
prior_shows integer
dow integer 0 Monday to 6 Sunday
hour_of_day integer 0 to 23
no_show_label boolean historical outcome
risk_score float prediction output
risk_tier string low medium high

Reminders table
appointment_id uuid reference
channel string
status string
template_name string
sent_at datetime

Users table
email string
role string
password_hash string

Audit logs table
action string
entity_type string
entity_id string
timestamp datetime
details_json text
