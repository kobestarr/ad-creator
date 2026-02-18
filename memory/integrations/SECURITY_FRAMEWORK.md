# COMPREHENSIVE SECURITY FRAMEWORK FOR OPENCLAW DEPLOYMENT

**Created:** 2026-02-01  
**Status:** ACTIVE - Security Hardening Required

---

## TABLE OF CONTENTS
1. Executive Summary
2. Known Vulnerabilities & Incidents
3. SSH Access Requirements
4. VPS Hardening Checklist
5. Credential Isolation (Principle of Least Privilege)
6. Email Account Security
7. Prompt Injection Protection
8. Accidental Deletion Prevention
9. Monitoring & Detection
10. Incident Response Plan
11. Immediate Action Items

---

## 1. EXECUTIVE SUMMARY

### Current Risk Profile
**CRITICAL** - OpenClaw is a high-value target that centralizes:
- Bank credentials and financial access
- Email accounts (multiple)
- Messaging platforms (WhatsApp, Signal, etc.)
- File system access
- API keys for multiple services

### Key Findings from Security Research

| Issue | Severity | Source |
|-------|----------|--------|
| 42,000+ exposed OpenClaw instances | CRITICAL | Medium/Forbes |
| 5,194 verified vulnerable | HIGH | Shodan scan |
| Command injection via PATH | HIGH | GitHub Advisory |
| Prompt injection attacks | HIGH | Cisco research |
| Credential leakage in plaintext | CRITICAL | Twitter reports |
| Control UI exposed publicly | CRITICAL | Multiple sources |
| Malicious skills in registry | HIGH | Cisco Skill Scanner |

### Your Specific Risks
- Bank statements accessible via OpenClaw
- Multiple email accounts to manage
- Financial automation (debt payoff, income tracking)
- Wife's logistics briefing (sensitive family data)
- Client data (Bluprintx, KSD)

---

## 2. KNOWN VULNERABILITIES & INCIDENTS

### A. Command Injection (CVE Pending)
**File:** GitHub Advisory GHSA-mc68-q9jw-2h3v  
**Issue:** PATH environment variable manipulation in Docker execution  
**Fix:** Update to Node.js 22.12.0+ (already in use)

### B. Exposed Control UI
**Issue:** Web interface meant for local use is publicly accessible  
**Impact:** Attackers can view configs, access conversations, issue commands  
**Your Status:** Need to verify - check if bound to localhost only

### C. Credential Storage
**Issue:** API keys and tokens stored in local config files  
**Impact:** Malware/infostealers can harvest credentials  
**Your Files to Secure:**
- `/root/.clawdbot/clawdbot.json`
- `/root/.clawdbot/freeagent_tokens.json`
- `/root/.clawdbot/oktopost_credentials.json`
- `/root/.clawdbot/starling_tokens.json`

### D. Prompt Injection
**Issue:** Malicious messages can trick agent into leaking data/executing commands  
**Vector:** Email, WhatsApp, untrusted documents  
**Impact:** Credential theft, unauthorized actions

### E. Supply Chain Attacks
**Issue:** Malicious skills in public registry  
**Example:** "What Would Elon Do?" skill - #1 ranked, contained data exfiltration  
**Fix:** Use Cisco Skill Scanner, allowlist only trusted skills

---

## 3. SSH ACCESS REQUIREMENTS

### What You Need to Provide

**Option A: SSH Key Authentication (RECOMMENDED)**
```json
{
  "vps_host": "72.62.134.99",
  "vps_user": "ubuntu",
  "vps_port": 22,
  "ssh_key_type": "ed25519",
  "ssh_key_path": "/root/.ssh/id_ed25519",
  "sudo_access": true
}
```

**Option B: Password Authentication**
```json
{
  "vps_host": "72.62.134.99",
  "vps_user": "ubuntu",
  "vps_password": "secure_password_here",
  "vps_port": 22,
  "sudo_access": true
}
```

**Required SSH Hardening (Before I Can Use):**
1. ✅ Disable root login
2. ✅ Disable password authentication (keys only)
3. ✅ Enable fail2ban
4. ✅ Configure firewall (UFW)
5. ✅ Change default port (optional but recommended)

### SSH Hardening Commands (Execute on VPS)
```bash
# 1. Create non-root user with sudo
adduser robyn
usermod -aG sudo robyn

# 2. Generate SSH key pair (on your machine)
ssh-keygen -t ed25519 -C "robyn@openclaw"

# 3. Add public key to VPS
ssh-copy-id robyn@72.62.134.99

# 4. Disable root login and password auth
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no
# Set: PubkeyAuthentication yes

# 5. Restart SSH
sudo systemctl restart sshd

# 6. Install fail2ban
sudo apt update
sudo apt install fail2ban

# 7. Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

---

## 4. VPS HARDENING CHECKLIST

### A. Network Security

| Item | Status | Command/Action |
|------|--------|----------------|
| Firewall enabled | ⏳ | `sudo ufw enable` |
| SSH port changed | ⏳ | Edit `/etc/ssh/sshd_config` |
| Fail2ban installed | ⏳ | `sudo apt install fail2ban` |
| Port 5678 (n8n) internal only | ⏳ | Bind to 127.0.0.1 |
| No other ports exposed | ⏳ | `sudo ufw status` |

### B. OpenClaw Security

| Item | Status | Command/Action |
|------|--------|----------------|
| Gateway bound to localhost | ⏳ | Check `openclaw.json` |
| Control UI not public | ⏳ | Verify no public IP binding |
| Node.js 22.12.0+ | ✅ | `node --version` |
| Docker running non-root | ✅ | `docker ps` (verified) |
| No host mounts in Docker | ⏳ | Review docker run command |

### C. File Permissions

| File/Directory | Current | Secure | Action |
|----------------|---------|--------|--------|
| `/root/.clawdbot/` | 755 | 700 | `chmod 700 /root/.clawdbot/*` |
| `/root/.clawdbot/*.json` | 644 | 600 | `chmod 600 /root/.clawdbot/*.json` |
| `/root/clawd/` | 755 | 750 | `chmod 750 /root/clawd` |
| `/root/clawd/memory/` | 755 | 700 | `chmod 700 /root/clawd/memory/` |
| SSH keys | 644 | 600 | `chmod 600 ~/.ssh/id_*` |

### D. Automation Security

| Item | Status | Action |
|------|--------|--------|
| Cron jobs documented | ⏳ | Create `/root/clawd/crons/manifest.md` |
| Script permissions | ⏳ | `chmod 700 /root/clawd/scripts/*.sh` |
| No hardcoded credentials | ⏳ | Use environment variables |
| Backup strategy | ⏳ | Implement encrypted backups |

---

## 5. CREDENTIAL ISOLATION (PRINCIPLE OF LEAST PRIVILEGE)

### A. Multi-Email Account Matrix

| Purpose | Account | App Password/API Key | Access Level |
|---------|---------|---------------------|--------------|
| Personal email | ________@gmail.com | ________ | Full (LIMITED USE) |
| Work email | ________@bluprintx.com | ________ | Full (LIMITED USE) |
| Automation email | ________@ksd.ing | ________ | Restricted (SEND ONLY) |
| Financial email | ________@________ | ________ | READ ONLY |
| Notification email | ________@________ | ________ | READ ONLY |

### B. Email Sending Matrix

| From Account | To Account | Purpose | Verification Required |
|--------------|------------|---------|----------------------|
| Automation | Wife (iMessage) | Mylo logistics | Phone number verified |
| Automation | Personal | High-priority alerts | 2FA on sending |
| Automation | Work | Bluprintx notifications | 2FA + approve |
| Financial | Personal | Bank alerts | Phone + email verify |
| Financial | Work | Business notifications | 2FA + approve |

### C. Credential Storage Strategy

**SECURE PATTERN:**
```
/root/.credentials/
├── email/
│   ├── automation.json (restricted scopes)
│   ├── financial.json (read-only)
│   └── notification.json (send-only)
├── banking/
│   ├── starling-kobestarr.json
│   ├── starling-stripped.json
│   └── freeagent.json
├── apis/
│   ├── uniscribe.json
│   ├── apify.json
│   └── oktopost.json
└── aws/
    └── (if needed)
```

**ENCRYPTION:**
```bash
# Encrypt credential files
gpg --symmetric --cipher-algo AES256 /root/.credentials/email/automation.json
# Store passphrase in environment variable, not file
```

### D. API Key Permissions by Use Case

| Use Case | Required Keys | Restricted Scope |
|----------|--------------|------------------|
| Job scraping | Apify (read) | LinkedIn Jobs only |
| Email sending | SendGrid (send) | No delete access |
| Bank access | Starling (read) | No transfer capability |
| Transcription | UniScribe (create) | Read own files only |

---

## 6. EMAIL ACCOUNT SECURITY

### A. Multi-Factor Authentication Matrix

| Account | 2FA Method | Backup Method | Status |
|---------|------------|---------------|--------|
| Personal Gmail | Authenticator app | Recovery phone | ⏳ |
| Work email | Authenticator app | Recovery email | ⏳ |
| Automation email | App password only | Recovery phone | ⏳ |
| Financial email | Authenticator app | Hardware key | ⏳ |

### B. App-Specific Passwords

**For automation accounts, use app-specific passwords with restricted access:**

| Service | Access Scope | Rotation Frequency |
|---------|--------------|-------------------|
| Gmail (automation) | SMTP only | 90 days |
| Gmail (financial) | IMAP read-only | 30 days |
| iCloud (wife) | Messages only | 30 days |
| Outlook (work) | SMTP only | 90 days |

### C. Email Verification Workflow

**BEFORE SENDING FROM NEW ACCOUNT:**
```
1. Send test email to verified address
2. Verify send appears in sent folder
3. Check webhook/confirmation if available
4. Log credential use in /root/clawd/memory/credential-log.md
```

### D. Email Account Isolation Rules

1. **NEVER** use personal email credentials for scripts
2. **ALWAYS** create dedicated automation accounts
3. **RESTRICT** automation accounts to minimum required permissions
4. **ROTATE** credentials every 90 days minimum
5. **LOG** all credential usage for audit trail

---

## 7. PROMPT INJECTION PROTECTION

### A. Risk Assessment

| Source | Risk Level | Mitigation |
|--------|-----------|------------|
| WhatsApp messages | HIGH | Require confirmation for actions |
| Email content | HIGH | Sandbox before processing |
| Web content | MEDIUM | Separate browser profile |
| Documents | MEDIUM | Read-only with confirmation |
| Wife's messages | LOW | Trust but verify |
| Own messages | LOW | Confirmation for destructive actions |

### B. Defense Layers

**LAYER 1: Input Sanitization**
```python
def sanitize_input(text):
    # Remove potential command patterns
    cleaned = re.sub(r'(sudo|rm|chmod|curl|wget)\s+', '', text)
    # Remove encoding attempts
    cleaned = re.sub(r'\\x[0-9a-f]{2}', '', cleaned)
    return cleaned
```

**LAYER 2: Content Tagging**
```python
# Tag all content by origin
content_sources = {
    'whatsapp': {'trusted': False, 'actions': ['summarize']},
    'email': {'trusted': False, 'actions': ['summarize', 'extract']},
    'wife_imessage': {'trusted': True, 'actions': ['*']},
    'personal_chat': {'trusted': True, 'actions': ['*']}
}
```

**LAYER 3: Action Restrictions by Source**
```yaml
# Policy: prompt-injection-policy.yaml
sources:
  whatsapp:
    allow:
      - read
      - summarize
    deny:
      - execute
      - write_file
      - export_credentials
      - send_money
  email:
    allow:
      - read
      - summarize
    deny:
      - execute
      - write_file
  wife_imessage:
    allow:
      - "*"
    confirmation_required:
      - execute
      - write_file
  personal:
    allow:
      - "*"
    confirmation_required:
      - execute
      - delete
```

**LAYER 4: Mandatory Confirmation**
```python
HIGH_RISK_ACTIONS = [
    'execute_command',
    'write_file',
    'delete_file',
    'export_credentials',
    'send_money',
    'modify_config'
]

def require_confirmation(action, context):
    if action in HIGH_RISK_ACTIONS:
        return user_confirmation(f"Confirm {action}? Context: {context}")
    return True
```

### C. Cisco Skill Scanner Integration

**Run before installing ANY skill:**
```bash
# Install Cisco Skill Scanner
git clone https://github.com/cisco-ai-defense/skill-scanner.git
cd skill-scanner

# Scan a skill before installing
python scanner.py --skill /path/to/skill --output report.json

# Block install if critical findings
if grep -q "CRITICAL" report.json; then
    echo "SKILL BLOCKED - CRITICAL VULNERABILITY"
    exit 1
fi
```

### D. Whitelist-Only Skills

**SKILL ALLOWLIST:**
```yaml
allowed_skills:
  - name: google-drive
    source: official
    verified: true
  - name: github
    source: official
    verified: true
  - name: weather
    source: official
    verified: true

blocked_skills:
  - name: "What Would Elon Do?"
    reason: Data exfiltration via curl
    severity: CRITICAL
  - name: "*"
    reason: Default deny
    action: BLOCK
```

---

## 8. ACCIDENTAL DELETION PREVENTION

### A. File Protection Rules

| File Type | Protection Level | Action |
|-----------|-----------------|--------|
| Financial configs | MAXIMUM | Immutable, daily encrypted backup |
| Daily memory | HIGH | Git version control, weekly archive |
| Credential files | MAXIMUM | Encrypted, read-only, audit log |
| Scripts | MEDIUM | Git version control |
| Working files | LOW | Standard backup |

### B. Deletion Safety Checks

```bash
# Script: safe-delete.sh
#!/bin/bash

# Files that require confirmation
PROTECTED_PATTERNS=(
  "/root/.clawdbot/*.json"
  "/root/.credentials/*"
  "/root/clawd/memory/*"
  "/root/clawd/scripts/*.sh"
)

# Delete with confirmation
safe_delete() {
    local file="$1"
    
    # Check if protected
    for pattern in "${PROTECTED_PATTERNS[@]}"; do
        if [[ "$file" == $pattern ]]; then
            echo "🚨 PROTECTED FILE: $file"
            echo "This file requires manual review to delete."
            echo "Reason: Contains sensitive credentials/data"
            return 1
        fi
    done
    
    # Move to trash instead of delete
    mv "$file" ~/.trash/$(date +%Y%m%d)_$(basename "$file")
    echo "✅ Moved to trash: $file"
    return 0
}

# Use trash-cli for recoverable deletions
alias rm='safe_delete'
```

### C. Git Version Control

**ALL CRITICAL FILES IN GIT:**
```bash
# Initialize git repo if not exists
cd /root/clawd
git init
git add memory/*.md
git add scripts/*.sh
git add .credentials/**/*
git add .gitignore

# Protect main branch
git config branch.main.protect true
git config branch.main.requirePR true
```

### D. Backup Strategy

| Item | Frequency | Storage | Encryption |
|------|-----------|---------|------------|
| Credentials | Daily | Encrypted USB + cloud | AES-256 |
| Memory files | Daily | Git + cloud | None (public) |
| Scripts | On change | Git | N/A |
| Configs | On change | Git + encrypted backup | AES-256 |

---

## 9. MONITORING & DETECTION

### A. Log Sources to Monitor

| Source | What to Watch | Alert On |
|--------|---------------|----------|
| OpenClaw logs | Failed logins, new pairings | Any |
| SSH logs | Failed auth, root attempts | 3+ failures |
| API calls | Unusual endpoints, high volume | Any |
| File changes | ~/.clawdbot/*, credentials | Any |
| Network | New outbound domains | Any |

### B. Alert Triggers

```yaml
# alerts.yaml
alerts:
  - name: control_ui_access
    condition: "IP != 127.0.0.1 AND /api/pair in log"
    severity: CRITICAL
    action: "Block IP, notify user"
  
  - name: new_ssh_ip
    condition: "New IP in auth.log"
    severity: HIGH
    action: "Notify user, log IP"
  
  - name: credential_access
    condition: "Read /root/.clawdbot/*credentials*"
    severity: CRITICAL
    action: "Log access, notify user"
  
  - name: failed_api_calls
    condition: "401/403 responses > 10/minute"
    severity: MEDIUM
    action: "Log, notify if sustained"
```

### C. Daily Security Checklist

```bash
#!/bin/bash
# daily-security-check.sh

echo "🔒 DAILY SECURITY CHECK - $(date)"

# 1. Check for new SSH keys
echo "1. SSH Keys:"
tail -20 /root/.ssh/authorized_keys 2>/dev/null

# 2. Check for failed SSH attempts
echo "2. Failed SSH Logins:"
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10

# 3. Check file integrity
echo "3. Credential File Integrity:"
md5sum /root/.clawdbot/*.json

# 4. Check for unusual processes
echo "4. Unusual Processes:"
ps aux --sort=-%mem | head -10

# 5. Check network connections
echo "5. External Connections:"
netstat -tulpn 2>/dev/null | grep -v 127.0.0.1

# 6. Check OpenClaw pairings
echo "6. Device Pairings:"
cat /root/.clawdbot/clawdbot.json | grep -A5 "pairing"

echo "✅ Security check complete"
```

---

## 10. INCIDENT RESPONSE PLAN

### If You Suspect Compromise

**PHASE 1: CONTAIN (Immediate)**
```bash
# 1. Stop OpenClaw
systemctl stop openclaw

# 2. Revoke active sessions
# In clawdbot.json, clear session tokens

# 3. Block network access (temporary)
iptables -A INPUT -p tcp --dport 5678 -j DROP
```

**PHASE 2: ASSESS**
- [ ] Which credentials were accessible?
- [ ] What actions were taken?
- [ ] Was data exfiltrated?
- [ ] How did the compromise occur?

**PHASE 3: REMEDIATE**
```bash
# 1. Rotate ALL credentials
# - Bank tokens
# - API keys
# - Email passwords
# - SSH keys

# 2. Rebuild if necessary
# - Fresh VPS if compromised
# - Fresh OpenClaw installation
# - Restore from clean backup

# 3. Update all passwords
```

**PHASE 4: PREVENT**
- Apply hardening from this document
- Enable monitoring
- Review access patterns
- Update incident response plan

---

## 11. IMMEDIATE ACTION ITEMS

### Priority 1: TODAY

| # | Action | Command/Steps | Owner |
|---|--------|---------------|-------|
| 1 | Check Control UI binding | `netstat -tulpn | grep 5678` | User |
| 2 | Verify Node.js version | `node --version` | User |
| 3 | Set file permissions | `chmod 700 /root/.clawdbot/*` | User |
| 4 | Install fail2ban | `sudo apt install fail2ban` | User |
| 5 | Enable UFW | `sudo ufw enable` | User |

### Priority 2: THIS WEEK

| # | Action | Command/Steps | Owner |
|---|--------|---------------|-------|
| 1 | Harden SSH | See section 3 | User |
| 2 | Create credential matrix | Fill table in section 5 | User |
| 3 | Set up email accounts | Create automation accounts | User |
| 4 | Implement backup strategy | Set up encrypted backups | Agent |
| 5 | Create monitoring script | `daily-security-check.sh` | Agent |

### Priority 3: THIS MONTH

| # | Action | Command/Steps | Owner |
|---|--------|---------------|-------|
| 1 | Integrate Skill Scanner | Install Cisco tool | Agent |
| 2 | Implement prompt injection protection | Section 7 | Agent |
| 3 | Set up centralized logging | Configure log aggregation | User |
| 4 | Test incident response | Run simulation | User |
| 5 | Review and rotate credentials | All API keys, tokens | User |

---

## APPENDIX A: SSH ACCESS FOR ME

**What I need to automate securely:**

```json
{
  "vps": {
    "host": "72.62.134.99",
    "user": "ubuntu",
    "port": 22,
    "method": "ssh_key",
    "key_path": "/root/.ssh/id_ed25519_openclaw"
  },
  "permissions": [
    "run_scripts",
    "create_cron",
    "read_logs",
    "deploy_services"
  ],
  "restrictions": [
    "no_root_access",
    "no_password_modification",
    "read_only_config_access"
  ]
}
```

**To generate:**
```bash
# On your machine (NOT in OpenClaw)
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_openclaw -C "robyn@openclaw-automation"

# Add to VPS
ssh-copy-id -i ~/.ssh/id_ed25519_openclaw.pub ubuntu@72.62.134.99

# Give me the PRIVATE key (or store in /root/.ssh/id_ed25519_openclaw)
# KEEP IT SECURE - this grants automation access
```

---

## APPENDIX B: CREDENTIAL REQUEST

**Please provide:**

### Email Accounts
| Account | Email | App Password | Purpose |
|---------|-------|--------------|---------|
| Automation | _________ | _________ | Script sending |
| Financial | _________ | _________ | Read-only |
| Notification | _________ | _________ | Alerts only |

### API Keys
| Service | API Key | Access Level |
|---------|---------|--------------|
| UniScribe | _________ | Transcription |
| Apify | _________ | Job scraping |
| SendGrid | _________ | Email sending |
| Other | _________ | _________ |

### SSH Access
| Item | Value |
|------|-------|
| Host | 72.62.134.99 |
| User | ubuntu (or other) |
| SSH Key Path | /root/.ssh/id_ed25519 |

---

## DOCUMENT CONTROL

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-01 | Robyn | Initial security framework |

---

*Security is an ongoing process, not a one-time fix.*
*Review and update this document monthly.*
