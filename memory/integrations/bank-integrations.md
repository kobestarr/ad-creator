# Bank Integrations Status

## Connected ✅

### Kobestarr Engineering - Starling Bank
| Field | Value |
|-------|-------|
| Status | Connected ✅ |
| Account | Main |
| Balance | £280.99 |
| Token | Saved securely |

## Not Connected ❌

### Stripped Media - Starling Bank
| Field | Value |
|-------|-------|
| Status | Invalid token ❌ |
| Action Needed | Create new token at developer.starlingbank.com/personal/token |
| Permissions required | `account:read` + `balance:read` |

### Stripped Media - Freeagent
| Field | Value |
|-------|-------|
| Status | Connected ✅ |
| Company | Stripped Media Ltd |
| Balance | £2,457.06 |
| Token | Saved securely |

---

## How to Fix Stripped Media Starling Token

1. Go to: https://developer.starlingbank.com/personal/token
2. Click "Create Token"
3. Name: `Robyn AI - Stripped Media`
4. Tick: `account:read` + `balance:read`
5. Click "Create"
6. **Copy ENTIRE token** (all characters)
7. Share with Robyn

---

## Automated Commands

### Get Kobestarr Balance
```bash
curl -H "Authorization: Bearer <KSD_TOKEN>" \
  "https://api.starlingbank.com/api/v2/accounts/<ACCOUNT_UID>/balance"
```

### Get Stripped Media Freeagent Data
```bash
curl -H "Authorization: Bearer <FA_TOKEN>" \
  "https://api.freeagent.com/v2/bank_accounts"
```

---

*Last Updated: 2026-02-01*
