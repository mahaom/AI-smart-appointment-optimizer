Model name
No show risk baseline model

Intended use
Predicts likelihood of a missed appointment to support reminder prioritization and scheduling interventions.

Training data
Synthetic and or de identified appointment history with labels indicating no show outcomes.

Features
lead_time_days
prior_no_shows
prior_shows
dow
hour_of_day

Output
risk_score between 0 and 1
risk_tier low medium high

Evaluation
Metrics are stored in backend app ml artifacts metrics.json.

Limitations
This baseline model is for demonstration and requires validation with real clinical data before any real world use.

Responsible use notes
The model should support staff decisions and should not be used to deny care. Monitoring for drift and bias should be implemented for production use.
