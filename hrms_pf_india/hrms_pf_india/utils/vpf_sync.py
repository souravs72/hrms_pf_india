# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils import add_years, flt, getdate, today

from hrms_pf_india.hrms_pf_india.setup.salary_components import ADDITIONAL_PF_COMPONENT
from hrms_pf_india.hrms_pf_india.utils.pf_calculator import (
	MANDATORY_PF_CAP,
	calculate_pf_breakup,
	calculate_voluntary_pf,
	get_pf_wages,
)

MAX_VPF_PERCENT_OF_WAGES = 1.0  # EPF allows up to 100% of wages as employee contribution


def validate_employee_pf_settings(doc, method=None):
	breakup = calculate_pf_breakup(doc, pf_wages=get_pf_wages(doc))
	doc.estimated_mandatory_pf = breakup["mandatory_pf"]
	doc.estimated_voluntary_pf = breakup["voluntary_pf"]
	doc.estimated_total_employee_pf = breakup["total_employee_pf"]

	contribution_type = doc.get("pf_contribution_type") or "Statutory Minimum"
	if contribution_type == "Statutory Minimum":
		return

	if not doc.get("pf_consent_date"):
		frappe.throw(_("PF Voluntary Consent Date is required for voluntary PF contributions."))

	pf_wages = breakup["pf_wages"]
	if pf_wages and breakup["total_employee_pf"] > flt(pf_wages * MAX_VPF_PERCENT_OF_WAGES):
		frappe.throw(
			_("Total employee PF ({0}) cannot exceed 100% of PF wages ({1}).").format(
				breakup["total_employee_pf"], pf_wages
			)
		)

	if contribution_type == "Voluntary Fixed Amount" and flt(doc.get("voluntary_pf_amount")) <= 0:
		frappe.throw(_("Voluntary PF Amount must be greater than zero."))


def sync_vpf_additional_salary(doc, method=None):
	if frappe.flags.in_install or frappe.flags.in_migrate:
		return

	voluntary_amount = calculate_voluntary_pf(doc, get_pf_wages(doc))
	existing = _get_active_vpf_additional_salary(doc.name)

	if voluntary_amount <= 0:
		_disable_vpf_additional_salary(existing)
		return

	if existing:
		if flt(existing.amount) != flt(voluntary_amount):
			additional = frappe.get_doc("Additional Salary", existing.name)
			additional.amount = voluntary_amount
			additional.save(ignore_permissions=True)
		return

	_create_vpf_additional_salary(doc, voluntary_amount)


def _get_active_vpf_additional_salary(employee):
	return frappe.db.get_value(
		"Additional Salary",
		{
			"employee": employee,
			"salary_component": ADDITIONAL_PF_COMPONENT,
			"docstatus": 1,
			"is_recurring": 1,
			"disabled": 0,
		},
		["name", "amount"],
		as_dict=True,
		order_by="from_date desc",
	)


def _create_vpf_additional_salary(employee_doc, amount):
	company = employee_doc.company or frappe.defaults.get_user_default("Company")
	if not company:
		frappe.msgprint(
			_("Could not auto-create VPF Additional Salary: Company not set on Employee."),
			indicator="orange",
		)
		return

	from_date = employee_doc.get("pf_consent_date") or today()
	to_date = add_years(from_date, 10)

	doc = frappe.get_doc(
		{
			"doctype": "Additional Salary",
			"employee": employee_doc.name,
			"company": company,
			"salary_component": ADDITIONAL_PF_COMPONENT,
			"amount": amount,
			"is_recurring": 1,
			"from_date": from_date,
			"to_date": to_date,
			"overwrite_salary_structure_amount": 0,
		}
	)
	doc.insert(ignore_permissions=True)
	doc.submit()
	frappe.msgprint(
		_("Recurring Additional Salary created for Voluntary PF: {0}").format(
			frappe.format(amount, {"fieldtype": "Currency"})
		),
		indicator="green",
	)


def _disable_vpf_additional_salary(existing):
	if not existing:
		return

	frappe.db.set_value("Additional Salary", existing.name, "disabled", 1)
	frappe.msgprint(_("Voluntary PF Additional Salary disabled for this employee."), indicator="blue")


@frappe.whitelist()
def get_pf_preview(employee, pf_wages=None):
	employee_doc = frappe.get_doc("Employee", employee)
	pf_wages = flt(pf_wages) if pf_wages else get_pf_wages(employee_doc)
	breakup = calculate_pf_breakup(employee_doc, pf_wages=pf_wages)
	breakup["statutory_wage_ceiling"] = 15000
	breakup["mandatory_pf_cap"] = MANDATORY_PF_CAP
	return breakup
