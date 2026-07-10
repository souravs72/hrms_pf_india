# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.utils import flt


def make_custom_fields():
	create_custom_fields(get_custom_fields(), update=True)


def rebuild_employee_fields():
	"""Drop and recreate app fields so labels/order stay clean across upgrades."""
	legacy = _read_legacy_vpf_employees()
	_delete_app_employee_fields()
	create_custom_fields(get_custom_fields(), update=True)
	_apply_legacy_vpf_employees(legacy)


def get_custom_fields():
	return {
		"Employee": [
			{
				"fieldname": "pf_contribution_section",
				"label": "Voluntary Provident Fund",
				"fieldtype": "Section Break",
				"insert_after": _employee_pf_anchor_field(),
				"collapsible": 1,
				"module": "HRMS PF India",
			},
			{
				"fieldname": "opt_for_voluntary_pf",
				"label": "Opt for Voluntary PF",
				"fieldtype": "Check",
				"insert_after": "pf_contribution_section",
				"default": "0",
				"module": "HRMS PF India",
			},
			{
				"fieldname": "voluntary_pf_amount",
				"label": "Voluntary PF Amount",
				"fieldtype": "Currency",
				"insert_after": "opt_for_voluntary_pf",
				"depends_on": "eval:doc.opt_for_voluntary_pf",
				"mandatory_depends_on": "eval:doc.opt_for_voluntary_pf",
				"module": "HRMS PF India",
			},
			{
				"fieldname": "pf_consent_date",
				"label": "Consent Date",
				"fieldtype": "Date",
				"insert_after": "voluntary_pf_amount",
				"depends_on": "eval:doc.opt_for_voluntary_pf",
				"mandatory_depends_on": "eval:doc.opt_for_voluntary_pf",
				"module": "HRMS PF India",
			},
		],
	}


def _read_legacy_vpf_employees():
	"""Capture VPF opt-in data before custom fields are rebuilt."""
	columns = {row[0] for row in frappe.db.sql("SHOW COLUMNS FROM `tabEmployee`")}
	rows = []

	if "pf_contribution_type" in columns:
		for employee, amount, consent in frappe.db.sql(
			"""
			SELECT name, IFNULL(voluntary_pf_amount, 0), pf_consent_date
			FROM `tabEmployee`
			WHERE IFNULL(pf_contribution_type, '') IN (
				'Voluntary Fixed Amount',
				'Voluntary on Full Basic'
			)
			"""
		):
			rows.append((employee, flt(amount), consent))
		return rows

	if "opt_for_voluntary_pf" in columns:
		for employee, amount, consent in frappe.db.sql(
			"""
			SELECT name, IFNULL(voluntary_pf_amount, 0), pf_consent_date
			FROM `tabEmployee`
			WHERE IFNULL(opt_for_voluntary_pf, 0) = 1
			"""
		):
			rows.append((employee, flt(amount), consent))

	return rows


def _apply_legacy_vpf_employees(rows):
	for employee, amount, consent in rows:
		frappe.db.set_value(
			"Employee",
			employee,
			{
				"opt_for_voluntary_pf": 1,
				"voluntary_pf_amount": amount,
				"pf_consent_date": consent,
			},
			update_modified=False,
		)


def _delete_app_employee_fields():
	names = frappe.get_all(
		"Custom Field",
		filters={"dt": "Employee", "module": "HRMS PF India"},
		pluck="name",
	)
	for name in names:
		frappe.delete_doc("Custom Field", name, force=True, ignore_permissions=True)


def _employee_pf_anchor_field():
	for fieldname in ("provident_fund_account", "pan_number", "payroll_cost_center", "company"):
		if frappe.db.exists("Custom Field", {"dt": "Employee", "fieldname": fieldname}):
			return fieldname
		if fieldname in frappe.get_meta("Employee").get_valid_columns():
			return fieldname
	return "company"
