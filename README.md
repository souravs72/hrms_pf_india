# HRMS PF India

Per-employee EPF/VPF for Frappe HRMS.

## Install

```bash
bench get-app https://github.com/souravs72/hrms_pf_india
bench --site your-site install-app hrms_pf_india
bench --site your-site migrate
```

## Setup

Salary Structure deduction:

| Component | Formula |
|---|---|
| Provident Fund | `min(BS, 15000) * 0.12` |

Voluntary PF is synced via Additional Salary — do not add it to the structure.

## Employee PF types

| Type | Result |
|---|---|
| Statutory Minimum | Provident Fund only |
| Voluntary Fixed Amount | Provident Fund + fixed Additional PF |
| Voluntary on Full Basic | Provident Fund + Additional PF (12% of basic − mandatory) |

## License

MIT
