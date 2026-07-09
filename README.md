# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

## Customization vs code — decision summary

| Need | Site customization only? | This app adds |
|---|---|---|
| Mandatory PF formula (12% on ₹15,000 ceiling) | Yes — Salary Structure | Documents standard formula |
| Per-employee VPF amount | Yes — manual Additional Salary per employee | **Auto-sync** from Employee master |
| VPF opt-in / consent tracking | Partial — custom fields via UI | **Custom fields + validation** |
| PF preview on Employee form | No | **Client script + API** |
| Additional Provident Fund component | Manual create + component type | **Auto-created on install** |
| Provident Fund Deductions report | Built into HRMS India setup | No change needed |
| Employer VPF matching on salary slip | No — employer cost, not employee deduction | Consent flag only (future: employer accrual) |
| EPFO ECR / challan file | No | Out of scope |

**Verdict:** Basic compliance works with HRMS site setup alone. This app removes manual HR work and enforces EPF Scheme 2026 consent/validation — that is what justifies a small extension app rather than only customizations.

---

## Installation

App is installed on site `hrms-pf.localhost` together with ERPNext and HRMS.

```bash
cd /path/to/bench
bench --site hrms-pf.localhost install-app hrms_pf_india
bench --site hrms-pf.localhost migrate
```

## Salary Structure setup (one-time per company)

Add to **Deductions**:

| Component | Formula |
|---|---|
| Provident Fund | `min(BS, 15000) * 0.12` |

Do **not** put voluntary PF in the structure — the app syncs it via Additional Salary.

## Employee PF types

| Type | Salary slip result |
|---|---|
| **Statutory Minimum** | Provident Fund = ₹1,800 (when basic > ₹15,000) |
| **Voluntary Fixed Amount** | Provident Fund + Additional Provident Fund (fixed) |
| **Voluntary on Full Basic** | Provident Fund + Additional PF = 12% of basic − mandatory |

## EPF Scheme 2026 notes

- Mandatory employee PF capped at **12% × ₹15,000 = ₹1,800/month**
- Amounts above ceiling are **voluntary** (VPF)
- Employer is **not required** to match VPF
- Consent date is required for voluntary options
