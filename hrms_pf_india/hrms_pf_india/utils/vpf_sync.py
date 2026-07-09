# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe import _
from frappe.utils import add_years, flt, getdate, today

from hrms_pf_india.hrms_pf_india.constants import (
	MAX_VPF_PERCENT_OF_WAGES,
	PF_CONTRIBUTION_STATUTORY,
	PF_CONTRIBUTION_VOLUNTARY_FIXED,
	STATUTORY_WAGE_CEILING,
	VPF_ADDITIONAL_SALARY_YEARS,
)
from hrms_pf_india.hrms_pf_india.setup.salary_components import ADDITIONAL_PF_COMPONENT
from hrms_pf_india.hrms_pf_india.utils.pf_calculator import (
	MANDATORY_PF_CAP,
	calculate_pf_breakup,
	calculate_voluntary_pf,
	get_pf_wages,
)


def validate_employee_pf_settings(doc, method=None):
	breakup = calculate_pf_breakup(doc, pf_wages=get_pf_wages(doc.name))
	doc.estimated_mandatory_pf = breakup["mandatory_pf"]
	doc.estimated_voluntary_pf = breakup["voluntary_pf"]
	doc.estimated_total_employee_pf = breakup["total_employee_pf"]

	contribution_type = doc.get("pf_contribution_type") or PF_CONTRIBUTION_STATUTORY
	if contribution_type == PF_CONTRIBUTION_STATUTORY:
		return

	if not doc.get("pf_consent_date"):
		frappe.throw(_("PF Voluntary Consent Date is required for voluntary PF contributions."))

	if not frappe.db.exists("Salary Component", ADDITIONAL_PF_COMPONENT):
		frappe.throw(
			_("Salary Component {0} is not set up. Run migrate or reinstall HRMS PF India.").format(
				ADDITIONAL_PF_COMPONENT
			)
		)

	if not _has_salary_structure_assignment(doc.name, doc.get("pf_consent_date")):
		frappe.throw(
			_(
				"A submitted Salary Structure Assignment is required before enabling voluntary PF for {0}."
			).format(doc.name)
		)

	pf_wages = breakup["pf_wages"]
	if not pf_wages:
		frappe.throw(
			_(
				"Salary Structure Assignment base pay is required to configure voluntary PF. Assign a salary structure first."
			)
		)

	if breakup["total_employee_pf"] > flt(pf_wages * MAX_VPF_PERCENT_OF_WAGES):
		frappe.throw(
			_("Total employee PF ({0}) cannot exceed 100% of PF wages ({1}).").format(
				breakup["total_employee_pf"], pf_wages
			)
		)

	if contribution_type == PF_CONTRIBUTION_VOLUNTARY_FIXED and flt(doc.get("voluntary_pf_amount")) <= 0:
		frappe.throw(_("Voluntary PF Amount must be greater than zero."))


def sync_vpf_additional_salary(doc, method=None):
	if frappe.flags.in_install or frappe.flags.in_migrate or frappe.flags.in_import:
		return

	if doc.status != "Active":
		return

	voluntary_amount = calculate_voluntary_pf(doc, get_pf_wages(doc.name))
	active = _get_active_vpf_additional_salary(doc.name)

	if voluntary_amount <= 0:
		_disable_vpf_additional_salary(active)
		return

	if active and flt(active.amount) == flt(voluntary_amount):
		return

	if active:
		_replace_vpf_additional_salary(doc, voluntary_amount, active.name)
		return

	_create_vpf_additional_salary(doc, voluntary_amount)


def _has_salary_structure_assignment(employee, from_date):
	from_date = getdate(from_date or today())
	return frappe.db.exists(
		"Salary Structure Assignment",
		{
			"employee": employee,
			"docstatus": 1,
			"from_date": ["<=", from_date],
		},
	)


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


def _replace_vpf_additional_salary(employee_doc, amount, existing_name):
	"""Submitted Additional Salary rows cannot update amount; cancel and recreate."""
	additional = frappe.get_doc("Additional Salary", existing_name)
	if additional.docstatus != 1:
		_create_vpf_additional_salary(employee_doc, amount)
		return

	try:
		additional.flags.ignore_permissions = True
		additional.cancel()
		_create_vpf_additional_salary(employee_doc, amount)
	except Exception:
		frappe.log_error(
			title="HRMS PF India: VPF Additional Salary update failed",
			message=frappe.get_traceback(),
		)
		frappe.throw(
			_(
				"Failed to update Voluntary PF Additional Salary for {0}. "
				"The previous record may have been cancelled — please verify Additional Salary manually."
			).format(employee_doc.name)
		)


def _create_vpf_additional_salary(employee_doc, amount):
	company = employee_doc.company
	if not company:
		frappe.throw(_("Company is required on Employee before enabling voluntary PF."))

	if not _has_salary_structure_assignment(employee_doc.name, employee_doc.get("pf_consent_date")):
		frappe.throw(
			_("Cannot create VPF Additional Salary without a submitted Salary Structure Assignment.")
		)

	from_date = getdate(employee_doc.get("pf_consent_date") or today())
	to_date = add_years(from_date, VPF_ADDITIONAL_SALARY_YEARS)
	currency = frappe.db.get_value("Company", company, "default_currency")

	doc = frappe.get_doc(
		{
			"doctype": "Additional Salary",
			"naming_series": "HR-ADS-.YY.-.MM.-",
			"employee": employee_doc.name,
			"company": company,
			"salary_component": ADDITIONAL_PF_COMPONENT,
			"amount": amount,
			"currency": currency,
			"is_recurring": 1,
			"from_date": from_date,
			"to_date": to_date,
			"overwrite_salary_structure_amount": 0,
		}
	)
	doc.flags.ignore_permissions = True
	try:
		doc.insert()
		doc.submit()
	except Exception:
		frappe.log_error(
			title="HRMS PF India: VPF Additional Salary creation failed",
			message=frappe.get_traceback(),
		)
		raise

	frappe.msgprint(
		_("Recurring Additional Salary created for Voluntary PF: {0}").format(
			frappe.format(amount, {"fieldtype": "Currency"})
		),
		indicator="green",
	)


def _disable_vpf_additional_salary(existing):
	if not existing:
		return

	frappe.db.set_value(
		"Additional Salary",
		existing.name,
		"disabled",
		1,
		update_modified=True,
	)
	frappe.msgprint(_("Voluntary PF Additional Salary disabled for this employee."), indicator="blue")


@frappe.whitelist()
def get_pf_preview(employee, pf_wages=None):
	frappe.has_permission("Employee", "read", employee, throw=True)

	employee_doc = frappe.get_doc("Employee", employee)
	pf_wages = flt(pf_wages) if pf_wages else get_pf_wages(employee)
	breakup = calculate_pf_breakup(employee_doc, pf_wages=pf_wages)
	breakup["statutory_wage_ceiling"] = STATUTORY_WAGE_CEILING
	breakup["mandatory_pf_cap"] = MANDATORY_PF_CAP
	return breakup
