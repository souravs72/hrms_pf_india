# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe.tests.utils import FrappeTestCase

from hrms_pf_india.hrms_pf_india.utils.vpf_sync import _voluntary_amount


class TestVPFAmount(FrappeTestCase):
	def test_not_opted_returns_zero(self):
		doc = frappe._dict(opt_for_voluntary_pf=0, voluntary_pf_amount=2000)
		self.assertEqual(_voluntary_amount(doc), 0)

	def test_opted_returns_amount(self):
		doc = frappe._dict(opt_for_voluntary_pf=1, voluntary_pf_amount=2000)
		self.assertEqual(_voluntary_amount(doc), 2000)

	def test_opted_with_zero_amount(self):
		doc = frappe._dict(opt_for_voluntary_pf=1, voluntary_pf_amount=0)
		self.assertEqual(_voluntary_amount(doc), 0)
