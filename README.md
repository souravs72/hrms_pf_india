# HRMS PF India

India EPF/VPF per-employee payroll extension for [Frappe HRMS](https://github.com/frappe/hrms), aligned with **EPF Scheme 2026**.

## What it does

- Adds **Employee PF settings** (statutory minimum vs voluntary PF)
- Auto-syncs **Additional Salary** for voluntary PF (VPF)
- Creates **Provident Fund** and **Additional Provident Fund** salary components
- Validates consent date and wage limits
- Shows live PF preview on the Employee form

## Requirements

- Frappe v15 + ERPNext + HRMS
- Company country: **India** (for full HRMS India payroll fields)

## Installation

```bash
bench get-app https://github.com/souravs72/hrms_pf_india
bench --site your-site install-app hrms_pf_india
bench --site your-site migrate
```

## Salary Structure setup (required)

Add to **Deductions** on your shared salary structure:

| Component | Formula |
|---|---|
| Provident Fund | `min(BS, 15000) * 0.12` |

Do **not** add voluntary PF to the structure — this app syncs it via Additional Salary.

## Employee PF types

| Type | Salary slip |
|---|---|
| Statutory Minimum | Provident Fund only (e.g. ₹1,800 when basic > ₹15,000) |
| Voluntary Fixed Amount | Provident Fund + Additional Provident Fund (fixed amount) |
| Voluntary on Full Basic | Provident Fund + Additional PF = 12% of basic − mandatory |

## Production checklist

- [ ] Company country = India
- [ ] Salary Structure has mandatory PF formula with ₹15,000 ceiling
- [ ] Salary Structure Assignment exists for each employee **before** enabling VPF
- [ ] Employee **Provident Fund Account (UAN)** filled
- [ ] VPF employees have **Consent Date** recorded
- [ ] Run **Provident Fund Deductions** report monthly for remittance tracking

## Tests

```bash
bench --site your-site set-config allow_tests true
bench --site your-site run-tests --app hrms_pf_india
```

## Customization vs this app

| Need | HRMS setup only | This app |
|---|---|---|
| Mandatory PF formula | Yes | Documents standard |
| Per-employee VPF | Manual Additional Salary | Auto-sync from Employee |
| Consent tracking | Manual | Built-in validation |
| PF preview | No | Yes |

## License

MIT
