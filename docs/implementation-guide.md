# Multi-Account Management System - Implementation Guide

## Quick Start Setup (Day 1)

### Step 1: Infrastructure Setup
```bash
# Create project directory
mkdir -p /root/clawd/multi-account-system
cd /root/clawd/multi-account-system

# Create business-specific directories
mkdir -p {bluprintx,kobestarr-digital,deal-flow-media}/{config,workflows,logs}

# Set up n8n using Docker
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n-multi-account
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=kobi
      - N8N_BASIC_AUTH_PASSWORD=secure_password_here
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - N8N_EMAIL_MODE=smtp
      - N8N_SMTP_HOST=smtp.gmail.com
      - N8N_SMTP_PORT=587
      - N8N_SMTP_USER=kobi@kobestarr.com
      - N8N_SMTP_PASS=app_password_here
    volumes:
      - ./n8n-data:/home/node/.n8n
      - ./workflows:/workflows
      - ./config:/config
    restart: unless-stopped
EOF

# Start n8n
docker-compose up -d
```

### Step 2: Business Account Configuration

#### Email Setup (Himalaya Multi-Account)
```bash
# Create Himalaya config for each business
cat > ~/.config/himalaya/config.toml << 'EOF'
# Bluprintx Account
[accounts.bluprintx]
email = "kobi@bluprintx.com"
display-name = "Kobi Omenaka - Bluprintx"
default = false

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "kobi@bluprintx.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show bluprintx/gmail"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "kobi@bluprintx.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show bluprintx/gmail-smtp"

# Kobestarr Digital Account
[accounts.kobestarr]
email = "kobi@kobestarr.com"
display-name = "Kobi Omenaka - Kobestarr Digital"
default = true

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "kobi@kobestarr.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show kobestarr/gmail"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "kobi@kobestarr.com"
message.send.backend.auth.type = "password"
backend.auth.cmd = "pass show kobestarr/gmail-smtp"

# Deal Flow Media Account
[accounts.deal-flow]
email = "kobi@dealflowmedia.com"
display-name = "Kobi Omenaka - Deal Flow Media"
default = false

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "kobi@dealflowmedia.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show deal-flow/gmail"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "kobi@dealflowmedia.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show deal-flow/gmail-smtp"
EOF
```

#### Google API Setup
```bash
# Create credentials directory
mkdir -p ~/.config/google-apis

# Set up OAuth credentials for each business
echo "bluprintx-credentials.json" > ~/.config/google-apis/bluprintx.json
echo "kobestarr-credentials.json" > ~/.config/google-apis/kobestarr.json  
echo "deal-flow-credentials.json" > ~/.config/google-apis/deal-flow.json
```

## Core Workflow Templates

### Workflow 1: Email Auto-Categorization
```json
{
  "name": "Email Auto-Categorization - Bluprintx",
  "nodes": [
    {
      "name": "Email Trigger",
      "type": "n8n-nodes-base.emailReadImap",
      "parameters": {
        "mailbox": "INBOX",
        "postProcessAction": "nothing",
        "options": {
          "allowUnauthorizedCerts": false
        }
      },
      "credentials": {
        "imap": {
          "user": "kobi@bluprintx.com",
          "password": "{{$credentials.bluprintxEmail}}",
          "host": "imap.gmail.com",
          "port": 993,
          "secure": true
        }
      }
    },
    {
      "name": "Classify Email",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "const subject = items[0].json.subject.toLowerCase();\nconst from = items[0].json.from.toLowerCase();\n\nlet category = 'general';\nlet priority = 'medium';\n\nif (subject.includes('salesforce') || subject.includes('consulting')) {\n  category = 'salesforce-consulting';\n  priority = 'high';\n} else if (subject.includes('invoice') || subject.includes('payment')) {\n  category = 'financial';\n  priority = 'high';\n} else if (from.includes('linkedin.com') || subject.includes('linkedin')) {\n  category = 'social-media';\n  priority = 'medium';\n}\n\nreturn [{\n  json: {\n    ...items[0].json,\n    category,\n    priority,\n    business: 'bluprintx'\n  }\n}];"
      }
    },
    {
      "name": "Route by Category",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.category }}",
              "operation": "equals",
              "value2": "salesforce-consulting"
            }
          ]
        }
      }
    },
    {
      "name": "Move to Consulting Folder",
      "type": "n8n-nodes-base.emailMove",
      "parameters": {
        "mailbox": "INBOX",
        "targetMailbox": "Bluprintx/Consulting",
        "messageId": "={{ $json.messageId }}"
      },
      "credentials": {
        "imap": {
          "user": "kobi@bluprintx.com",
          "password": "{{$credentials.bluprintxEmail}}",
          "host": "imap.gmail.com",
          "port": 993,
          "secure": true
        }
      }
    },
    {
      "name": "Send Discord Alert",
      "type": "n8n-nodes-base.discord",
      "parameters": {
        "channel": "bluprintx-alerts",
        "text": "🚀 New consulting inquiry: {{ $json.subject }} from {{ $json.from }}"
      }
    }
  ]
}
```

### Workflow 2: LinkedIn Content Scheduler
```json
{
  "name": "LinkedIn Content Scheduler - Multi-Business",
  "nodes": [
    {
      "name": "Notion Content Calendar",
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "operation": "getAll",
        "databaseId": "{{$credentials.contentCalendarDb}}",
        "filter": {
          "and": [
            {
              "property": "Status",
              "select": {
                "equals": "Scheduled"
              }
            },
            {
              "property": "Publish Date",
              "date": {
                "equals": "{{ $today.format('YYYY-MM-DD') }}"
              }
            }
          ]
        }
      },
      "credentials": {
        "notionApi": {
          "apiKey": "{{$credentials.notionApiKey}}"
        }
      }
    },
    {
      "name": "Route by Business",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "dataType": "string",
        "value1": "={{ $json.properties.Business.select.name }}",
        "rules": {
          "rules": [
            {
              "output": 0,
              "value2": "Bluprintx"
            },
            {
              "output": 1,
              "value2": "Kobestarr Digital"
            },
            {
              "output": 2,
              "value2": "Deal Flow Media"
            }
          ]
        }
      }
    },
    {
      "name": "Post to LinkedIn - Bluprintx",
      "type": "n8n-nodes-base.linkedIn",
      "parameters": {
        "operation": "create",
        "resource": "post",
        "personId": "={{ $credentials.bluprintxLinkedInId }}",
        "text": "={{ $json.properties.Content.rich_text[0].text.content }}",
        "visibility": "connections"
      },
      "credentials": {
        "linkedInOAuth2Api": {
          "clientId": "{{$credentials.bluprintxLinkedInClientId}}",
          "clientSecret": "{{$credentials.bluprintxLinkedInClientSecret}}"
        }
      }
    },
    {
      "name": "Post to LinkedIn - Kobestarr",
      "type": "n8n-nodes-base.linkedIn",
      "parameters": {
        "operation": "create",
        "resource": "post",
        "personId": "={{ $credentials.kobestarrLinkedInId }}",
        "text": "={{ $json.properties.Content.rich_text[0].text.content }}",
        "visibility": "connections"
      },
      "credentials": {
        "linkedInOAuth2Api": {
          "clientId": "{{$credentials.kobestarrLinkedInClientId}}",
          "clientSecret": "{{$credentials.kobestarrLinkedInClientSecret}}"
        }
      }
    },
    {
      "name": "Update Notion Status",
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "operation": "update",
        "databaseId": "{{$credentials.contentCalendarDb}}",
        "pageId": "={{ $json.id }}",
        "properties": {
          "Status": {
            "select": {
              "name": "Published"
            }
          },
          "Published Date": {
            "date": {
              "start": "{{ $now.format('YYYY-MM-DD') }}"
            }
          }
        }
      }
    }
  ]
}
```

### Workflow 3: Lead Generation Automation
```json
{
  "name": "LinkedIn Lead Generation - Bluprintx",
  "nodes": [
    {
      "name": "Daily Trigger",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "triggerTimes": {
          "item": [
            {
              "hour": 9,
              "minute": 0
            }
          ]
        }
      }
    },
    {
      "name": "Search LinkedIn Prospects",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "GET",
        "url": "https://api.linkedin.com/v2/peopleSearch",
        "authentication": "oAuth2",
        "options": {
          "headers": {
            "X-Restli-Protocol-Version": "2.0.0"
          }
        },
        "queryParameters": {
          "keywords": "Salesforce Consultant",
          "location": "United Kingdom",
          "industry": "Technology",
          "companySize": "11-50"
        }
      },
      "credentials": {
        "linkedInOAuth2Api": {
          "clientId": "{{$credentials.bluprintxLinkedInClientId}}",
          "clientSecret": "{{$credentials.bluprintxLinkedInClientSecret}}"
        }
      }
    },
    {
      "name": "Filter Qualified Leads",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "const leads = items[0].json.elements;\nconst qualifiedLeads = leads.filter(lead => {\n  const title = lead.title?.toLowerCase() || '';\n  const company = lead.company?.toLowerCase() || '';\n  \n  return title.includes('salesforce') || \n         title.includes('crm') || \n         title.includes('consultant') ||\n         company.includes('tech') ||\n         company.includes('digital');\n}).slice(0, 10); // Limit to 10 leads per day\n\nreturn qualifiedLeads.map(lead => ({\n  json: {\n    id: lead.id,\n    name: `${lead.firstName} ${lead.lastName}`,\n    title: lead.title,\n    company: lead.company,\n    profileUrl: lead.publicIdentifier,\n    business: 'bluprintx',\n    status: 'new'\n  }\n}));"
      }
    },
    {
      "name": "Add to CRM Database",
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "operation": "create",
        "databaseId": "{{$credentials.bluprintxCrmDb}}",
        "properties": {
          "Name": {
            "title": [
              {
                "text": {
                  "content": "={{ $json.name }}"
                }
              }
            ]
          },
          "Title": {
            "rich_text": [
              {
                "text": {
                  "content": "={{ $json.title }}"
                }
              }
            ]
          },
          "Company": {
            "rich_text": [
              {
                "text": {
                  "content": "={{ $json.company }}"
                }
              }
            ]
          },
          "LinkedIn URL": {
            "url": "={{ $json.profileUrl }}"
          },
          "Status": {
            "select": {
              "name": "New Lead"
            }
          },
          "Source": {
            "select": {
              "name": "LinkedIn Search"
            }
          }
        }
      }
    },
    {
      "name": "Send Connection Request",
      "type": "n8n-nodes-base.linkedIn",
      "parameters": {
        "operation": "create",
        "resource": "invitation",
        "personId": "={{ $json.id }}",
        "message": "Hi {{ $json.name }}, I noticed your expertise in {{ $json.title }}. I'd love to connect and share insights about Salesforce optimization strategies. - Kobi from Bluprintx"
      }
    },
    {
      "name": "Send Discord Notification",
      "type": "n8n-nodes-base.discord",
      "parameters": {
        "channel": "bluprintx-leads",
        "text": "🎯 New qualified lead added: {{ $json.name }} ({{ $json.title }} at {{ $json.company }})"
      }
    }
  ]
}
```

## Notion Database Templates

### Content Calendar Database
```json
{
  "parent": {
    "type": "page_id",
    "page_id": "parent_page_id"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "Content Calendar - Multi-Business"
      }
    }
  ],
  "properties": {
    "Title": {
      "title": {}
    },
    "Content": {
      "rich_text": {}
    },
    "Business": {
      "select": {
        "options": [
          {"name": "Bluprintx", "color": "blue"},
          {"name": "Kobestarr Digital", "color": "green"},
          {"name": "Deal Flow Media", "color": "purple"}
        ]
      }
    },
    "Platform": {
      "select": {
        "options": [
          {"name": "LinkedIn", "color": "blue"},
          {"name": "Reddit", "color": "orange"},
          {"name": "Twitter", "color": "gray"},
          {"name": "Blog", "color": "brown"}
        ]
      }
    },
    "Status": {
      "select": {
        "options": [
          {"name": "Idea", "color": "gray"},
          {"name": "Writing", "color": "yellow"},
          {"name": "Scheduled", "color": "blue"},
          {"name": "Published", "color": "green"}
        ]
      }
    },
    "Publish Date": {
      "date": {}
    },
    "Published Date": {
      "date": {}
    },
    "Author": {
      "rich_text": {}
    }
  }
}
```

### CRM Database Template
```json
{
  "parent": {
    "type": "page_id",
    "page_id": "parent_page_id"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "CRM - Bluprintx"
      }
    }
  ],
  "properties": {
    "Name": {
      "title": {}
    },
    "Title": {
      "rich_text": {}
    },
    "Company": {
      "rich_text": {}
    },
    "LinkedIn URL": {
      "url": {}
    },
    "Email": {
      "email": {}
    },
    "Phone": {
      "phone_number": {}
    },
    "Status": {
      "select": {
        "options": [
          {"name": "New Lead", "color": "gray"},
          {"name": "Contacted", "color": "yellow"},
          {"name": "Qualified", "color": "blue"},
          {"name": "Proposal Sent", "color": "purple"},
          {"name": "Closed Won", "color": "green"},
          {"name": "Closed Lost", "color": "red"}
        ]
      }
    },
    "Source": {
      "select": {
        "options": [
          {"name": "LinkedIn Search", "color": "blue"},
          {"name": "Referral", "color": "green"},
          {"name": "Website", "color": "purple"},
          {"name": "Event", "color": "orange"}
        ]
      }
    },
    "Last Contact": {
      "date": {}
    },
    "Next Action": {
      "rich_text": {}
    }
  }
}
```

## Security and Compliance

### Account Separation Rules
1. **Never cross-post between business accounts**
2. **Use separate API keys for each business**
3. **Implement request rate limiting per account**
4. **Monitor for unusual activity patterns**
5. **Regular security audits and updates**

### Overemployment Protection
1. **Separate infrastructure per job**
2. **Staggered automation schedules**
3. **Business-specific notification channels**
4. **Activity pattern randomization**
5. **Emergency shutdown procedures**

## Monitoring and Maintenance

### Daily Checks (Automated)
- Workflow execution status
- API rate limit status
- Error log review
- Account health monitoring

### Weekly Reviews (Manual)
- Performance metrics analysis
- Cost optimization review
- Security audit
- Content performance analysis

### Monthly Maintenance
- Workflow optimization
- API credential rotation
- Database cleanup
- System performance tuning

## Troubleshooting Guide

### Common Issues
1. **API Rate Limits**: Implement exponential backoff
2. **Authentication Failures**: Check credential expiration
3. **Workflow Errors**: Review execution logs
4. **Performance Issues**: Monitor resource usage

### Emergency Procedures
1. **Account Suspension**: Immediate workflow shutdown
2. **Security Breach**: Credential rotation protocol
3. **System Failure**: Backup activation procedures

This implementation guide provides the technical foundation for Kobi's multi-account management system. The modular design allows for gradual rollout and scaling based on business needs.