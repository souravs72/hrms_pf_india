# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def make_custom_fields():
	create_custom_fields(get_custom_fields(), update=True)


def get_custom_fields():
	return {
		"Employee": [
			{
				"fieldname": "pf_contribution_section",
				"label": "PF Contribution (India)",
				"fieldtype": "Section Break",
				"insert_after": "provident_fund_account",
				"collapsible": 1,
				"module": "HRMS PF India",
			},
			{
				"fieldname": "pf_contribution_type",
				"label": "PF Contribution Type",
				"fieldtype": "Select",
				"insert_after": "pf_contribution_section",
				"options": "\nStatutory Minimum\nVoluntary Fixed Amount\nVoluntary on Full Basic",
				"default": "Statutory Minimum",
				"description": "Statutory Minimum = 12% on wage ceiling (₹15,000). Voluntary options add Additional PF via Additional Salary.",
				"module": "HRMS PF India",
			},
			{
				"fieldname": "voluntary_pf_amount",
				"label": "Voluntary PF Amount (Monthly)",
				"fieldtype": "Currency",
				"insert_after": "pf_contribution_type",
				"depends_on": 'eval:doc.pf_contribution_type=="Voluntary Fixed Amount"',
				"mandatory_depends_on": 'eval:doc.pf_contribution_type=="Voluntary Fixed Amount"',
				"module": "HRMS PF India",
			},
			{
				"fieldname": "pf_consent_date",
				"label": "PF Voluntary Consent Date",
				"fieldtype": "Date",
				"insert_after": "voluntary_pf_amount",
				"depends_on": 'eval:doc.pf_contribution_type!="Statutory Minimum" && doc.pf_contribution_type',
				"mandatory_depends_on": 'eval:doc.pf_contribution_type!="Statutory Minimum" && doc.pf_contribution_type',
				"description": "Required for voluntary PF under EPF Scheme 2026.",
				"module": "HRMS PF India",
			},
			{
				"fieldname": "employer_matches_vpf",
				"label": "Employer Matches Voluntary PF",
				"fieldtype": "Check",
				"insert_after": "pf_consent_date",
				"depends_on": 'eval:doc.pf_contribution_type!="Statutory Minimum" && doc.pf_contribution_type',
				"description": "Employer matching is optional under EPF Scheme 2026. Track consent here; employer share is not deducted from employee salary.",
				"module": "HRMS PF India",
			},
			{
				"fieldname": "pf_preview_column",
				"fieldtype": "Column Break",
				"insert_after": "employer_matches_vpf",
				"module": "HRMS PF India",
			},
			{
				"fieldname": "estimated_mandatory_pf",
				"label": "Estimated Mandatory PF",
				"fieldtype": "Currency",
				"insert_after": "pf_preview_column",
				"read_only": 1,
				"description": "12% of PF wages up to statutory ceiling (₹15,000).",
				"module": "HRMS PF India",
			},
			{
				"fieldname": "estimated_voluntary_pf",
				"label": "Estimated Voluntary PF",
				"fieldtype": "Currency",
				"insert_after": "estimated_mandatory_pf",
				"read_only": 1,
				"module": "HRMS PF India",
			},
			{
				"fieldname": "estimated_total_employee_pf",
				"label": "Estimated Total Employee PF",
				"fieldtype": "Currency",
				"insert_after": "estimated_voluntary_pf",
				"read_only": 1,
				"module": "HRMS PF India",
			},
		],
	}
