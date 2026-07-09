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
				"insert_after": _employee_pf_anchor_field(),
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
				"module": "HRMS PF India",
			},
			{
				"fieldname": "employer_matches_vpf",
				"label": "Employer Matches Voluntary PF",
				"fieldtype": "Check",
				"insert_after": "pf_consent_date",
				"depends_on": 'eval:doc.pf_contribution_type!="Statutory Minimum" && doc.pf_contribution_type',
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


def _employee_pf_anchor_field():
	for fieldname in ("provident_fund_account", "pan_number", "payroll_cost_center", "company"):
		if frappe.db.exists("Custom Field", {"dt": "Employee", "fieldname": fieldname}):
			return fieldname
		if fieldname in frappe.get_meta("Employee").get_valid_columns():
			return fieldname
	return "company"
