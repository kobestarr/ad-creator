# Freeagent Integration Status

## Connected Companies

### Stripped Media Ltd ✅
| Field | Value |
|-------|-------|
| Client ID | IAGBbfkZ3BUyCid8kcwhug |
| Access Token | 1ACMWEeoBkg8URh_j5ZqS9vJO-zjzuKKoC3ALyK5A |
| Status | Active |
| Last Check | 2026-02-01 |
| Balance | £2,457.06 |

### Kobestarr Engineering & Media Ltd ⏳
| Field | Value |
|-------|-------|
| Client ID | KJr1XQFAiaqXxYMZ0diILA |
| Access Token | 1ACMXEeoBMEvPUYqOet9dFZybwQsI-9DTVKjyOs_r |
| Status | Token obtained, but API only shows primary company (Stripped Media) |
| Notes | Freeagent returns primary company for both tokens |

---

## Automated Commands

### Get Stripped Media Balance
```bash
curl -H "Authorization: Bearer 1ACMWEeoBkg8URh_j5ZqS9vJO-zjzuKKoC3ALyK5A" \
  "https://api.freeagent.com/v2/bank_accounts"
```

### Get Recent Invoices
```bash
curl -H "Authorization: Bearer 1ACMWEeoBkg8URh_j5ZqS9vJO-zjzuKKoC3ALyK5A" \
  "https://api.freeagent.com/v2/invoices?per_page=5"
```

---

## Next Steps
1. Use Stripped Media token for automated tracking
2. Manual input for Kobestarr until we find a way to access it via API
3. Consider using Starling API for Kobestarr bank data

---

*Last Updated: 2026-02-01*
