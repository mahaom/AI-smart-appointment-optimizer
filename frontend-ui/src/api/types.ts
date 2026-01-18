export type Appointment = {
  id: string;
  clinic_id: string;
  provider_id: string;
  appt_datetime: string;
  appt_type: string;
  lead_time_days: number;
  prior_no_shows: number;
  prior_shows: number;
  dow: number;
  hour_of_day: number;
  no_show_label: boolean | null;
  risk_score: number | null;
  risk_tier: string | null;
};

export type TrendPoint = {
  bucket: string;
  total: number;
  no_shows: number;
  no_show_rate: number;
};

export type DowPoint = {
  dow: number;
  total: number;
  no_shows: number;
  no_show_rate: number;
};

export type TierPoint = {
  risk_tier: string;
  count: number;
};
