# Voluntary Provident Fund — User Guide

Guidance for explaining and demonstrating per-employee voluntary PF with HRMS PF India.

---

## What to communicate

| Topic | Behaviour |
|---|---|
| Mandatory PF | Configured once in the **Salary Structure** for all employees |
| Voluntary PF (VPF) | Opt-in on the **Employee** form: checkbox, amount, consent date |
| Salary slip | Mandatory PF always appears; VPF adds **Additional Provident Fund** only when opted in |
| HR effort | No manual Additional Salary per VPF employee — the app syncs it |

---

## How it works

```
Salary Structure
  └── Provident Fund (mandatory formula)
        ↓
Employee
  └── Opt for Voluntary PF + Amount + Consent Date
        ↓
App syncs recurring Additional Salary
  └── Additional Provident Fund
        ↓
Salary Slip
  ├── Provident Fund              ← from structure
  └── Additional Provident Fund   ← only if opted in
```

### Employee fields

| Field | Purpose |
|---|---|
| Opt for Voluntary PF | Enable or disable VPF |
| Voluntary PF Amount | Monthly voluntary contribution |
| Consent Date | Required when VPF is enabled |

### Owned by HRMS

- Mandatory PF formula and salary structure
- Payroll entry and salary slip generation
- Provident Fund Deductions report
- Accounting entries

### Added by this app

- Opt-in fields on Employee
- Auto create / update / disable Additional Salary for VPF
- Validation for amount, consent date, and assignment

---

## Suggested demo walkthrough

Use two employees on the same salary structure.

### A — Shared structure (mandatory PF)

1. Open the company **Salary Structure**.
2. Show earnings and the **Provident Fund** deduction formula.
3. Confirm **Additional Provident Fund** is not in the structure.

Talking point: one structure for the company; mandatory PF is not per employee.

### B — Employee without VPF

1. Open an employee with **Opt for Voluntary PF** unchecked.
2. Open their salary slip for a period.
3. Show **Provident Fund** only — no Additional Provident Fund row.

Talking point: default employees need no VPF setup.

### C — Employee with VPF

1. Open an employee with:
   - Opt for Voluntary PF checked
   - A voluntary amount
   - Consent date set
2. Show the related **Additional Salary** (created on save).
3. Open their salary slip.
4. Show both **Provident Fund** and **Additional Provident Fund**.

Talking point: opt-in on Employee → Additional Salary → extra slip row. Reporting stays separate.

### D — Live toggle (optional)

1. Enable VPF on a non-VPF employee, save, refresh or recreate the slip.
2. Disable VPF, save, and confirm future slips no longer include Additional Provident Fund.

### E — Print

Print a slip and show earnings, deductions, and net pay.

---

## Example numbers (illustrative)

Assume base pay ₹60,000, Basic = 50% of base, PF ceiling ₹15,000, VPF ₹2,000, professional tax ₹200.

| Line | Amount |
|---|---|
| Gross | ₹60,000 |
| Provident Fund (mandatory) | ₹1,800 |
| Additional Provident Fund (VPF) | ₹2,000 |
| Professional Tax | ₹200 |
| Net (approx.) | ₹56,000 |

Same structure, no VPF: deductions exclude the ₹2,000 VPF row.

---

## FAQ

**Can each employee choose a different VPF amount?**  
Yes. Amount is set per employee.

**Must the employer match VPF?**  
No. Matching is optional under EPF rules. This app only handles the employee voluntary deduction.

**Does VPF merge into mandatory PF on the slip?**  
No. Separate rows and separate columns in the PF report.

**How do we stop VPF?**  
Uncheck **Opt for Voluntary PF** and save. The recurring Additional Salary is disabled.

**Do we need a separate salary structure per VPF employee?**  
No. One shared structure plus per-employee opt-in is enough.
