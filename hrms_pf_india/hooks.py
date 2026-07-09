app_name = "hrms_pf_india"
app_title = "HRMS PF India"
app_publisher = "Ascra Technologies"
app_description = "India EPF/VPF per-employee payroll configuration for HRMS (EPF Scheme 2026)"
app_email = "admin@ascratech.com"
app_license = "mit"

required_apps = ["hrms"]

after_install = "hrms_pf_india.hrms_pf_india.install.after_install"
after_migrate = "hrms_pf_india.hrms_pf_india.install.after_migrate"

doctype_js = {
	"Employee": "public/js/employee_pf.js",
}

doc_events = {
	"Employee": {
		"validate": "hrms_pf_india.hrms_pf_india.utils.vpf_sync.validate_employee_pf_settings",
		"after_insert": "hrms_pf_india.hrms_pf_india.utils.vpf_sync.sync_vpf_additional_salary",
		"on_update": "hrms_pf_india.hrms_pf_india.utils.vpf_sync.sync_vpf_additional_salary",
	},
}

fixtures = [
	{
		"dt": "Custom Field",
		"filters": [["module", "=", "HRMS PF India"]],
	},
]
