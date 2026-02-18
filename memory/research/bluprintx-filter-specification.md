# Bluprintx Job Scraper - Filter System Technical Specification
**Detailed Filter Logic & Implementation**

## 🎯 Filter Philosophy: Sales Team First

Every filter is designed around **how sales teams actually think** when prospecting:
- "I want companies hiring Salesforce people, but NOT architects" 
- "I want big companies, but not the usual suspects (Oracle, SAP)"
- "I want recent hires - old postings are dead leads"
- "I want decision-makers, not junior roles"

## 🔧 Core Filter Categories

### 1. JOB TITLE FILTERING (Most Critical)

#### "Job MUST Contain" Filter
**Purpose**: Ensure we're targeting the RIGHT Salesforce roles
**Logic**: OR-based keyword matching (inclusive)

```javascript
// Implementation Logic
const mustContainKeywords = ["salesforce", "admin", "crm"];
const jobTitle = "Senior Salesforce Administrator";

// Returns TRUE if ANY keyword matches
mustContainKeywords.some(keyword => 
  jobTitle.toLowerCase().includes(keyword.toLowerCase())
);
// Result: TRUE (matches "salesforce" and "admin")
```

**Example Use Cases:**
```
Input: "salesforce, admin, developer"
Matches: "Salesforce Administrator", "Salesforce Developer", "CRM Administrator"
Does NOT Match: "Java Developer", "System Administrator", "CRM Manager"
```

#### "Job EXCLUDE" Filter  
**Purpose**: Eliminate roles we DON'T want to target
**Logic**: OR-based keyword matching (exclusive)

```javascript
// Implementation Logic
const excludeKeywords = ["senior", "architect", "lead"];
const jobTitle = "Senior Salesforce Architect";

// Returns FALSE if ANY keyword matches (excludes)
!excludeKeywords.some(keyword => 
  jobTitle.toLowerCase().includes(keyword.toLowerCase())
);
// Result: FALSE (excluded because of "senior" and "architect")
```

**Example Use Cases:**
```
Input: "senior, architect, principal, lead"
Excludes: "Senior Salesforce Admin", "Salesforce Architect", "Lead Developer"
Includes: "Salesforce Administrator", "Salesforce Developer", "CRM Specialist"
```

#### Why This Matters for Bluprintx:
- **Avoid Senior Roles**: They want experienced consultants, not to train juniors
- **Exclude Architects**: Different budget, longer sales cycle
- **Target Implementers**: Administrators, developers = immediate consulting need

---

### 2. COMPANY SIZE FILTERING (Budget Indicator)

#### Size Categories & Logic
```javascript
const companySizeRanges = {
  "startup": { min: 1, max: 50 },
  "smb": { min: 51, max: 500 }, 
  "enterprise": { min: 501, max: Infinity }
};

// Extract employee count from LinkedIn data
const employeeCount = extractEmployeeCount(job.listing);
const sizeCategory = determineSizeCategory(employeeCount);
```

#### Data Source Extraction
```javascript
// Multiple data sources for employee count
function extractEmployeeCount(jobData) {
  const sources = [
    jobData.company.employeeCount,
    jobData.company.followerCount, // LinkedIn proxy
    jobData.company.sizeText, // "51-200 employees"
    extractFromDescription(jobData.description) // "Growing team of 150"
  ];
  
  return sources.find(count => count > 0) || null;
}
```

#### Bluprintx Size Strategy:
- **SMB (51-500)**: Sweet spot - have budget, faster decisions
- **Enterprise (500+)**: Big contracts, longer cycles, need patience
- **Startup (1-50)**: Quick wins, but smaller budgets

---

### 3. SENIORITY LEVEL FILTERING (Decision Speed)

#### Title Analysis Logic
```javascript
const seniorityKeywords = {
  "entry": ["junior", "associate", "coordinator", "assistant"],
  "mid": ["analyst", "specialist", "administrator", "developer"],
  "senior": ["senior", "lead", "principal", "specialist senior"],
  "executive": ["director", "vp", "head of", "chief", "c-level"]
};

function determineSeniority(jobTitle) {
  const titleLower = jobTitle.toLowerCase();
  
  for (const [level, keywords] of Object.entries(seniorityKeywords)) {
    if (keywords.some(keyword => titleLower.includes(keyword))) {
      return level;
    }
  }
  
  return "mid"; // Default for unclear titles
}
```

#### Salesforce-Specific Seniority:
```javascript
const salesforceSeniority = {
  "entry": ["administrator", "developer", "support"],
  "mid": ["senior administrator", "developer", "consultant"],
  "senior": ["senior developer", "lead consultant", "architect"],
  "executive": ["director", "head of salesforce", "vp technology"]
};
```

#### Why This Matters:
- **Entry/Mid Level**: Faster hiring decisions, more open to consulting
- **Senior Level**: Longer process, but bigger budgets
- **Executive Level**: Strategic decisions, need C-suite access

---

### 4. COMPANY EXCLUDE FILTERING (Competitor Removal)

#### Logic Implementation
```javascript
const excludeCompanies = ["oracle", "sap", "microsoft", "salesforce"];

function shouldExcludeCompany(companyName, excludeList) {
  const companyLower = companyName.toLowerCase();
  
  return excludeList.some(excludeTerm => 
    companyLower.includes(excludeTerm.toLowerCase())
  );
}

// Usage
if (shouldExcludeCompany("Oracle Corporation", excludeCompanies)) {
  return false; // Skip this job
}
```

#### Bluprintx Exclude Strategy:
```javascript
const bluprintxExcludes = [
  // Direct Competitors
  "oracle", "sap", "microsoft", "salesforce", "hubspot",
  
  // Consulting Giants (too big, already have solutions)
  "accenture", "deloitte", "pwc", "kpmg", "ibm",
  
  // Staffing Agencies (not real hiring)
  "robert half", "teksystems", "modis", "apex systems"
];
```

#### Why Exclude These:
- **Oracle/SAP**: Direct competitors, won't use Salesforce consulting
- **Big 4 Consulting**: Already have internal Salesforce practices
- **Staffing Agencies**: Just recruiting, not real hiring need

---

### 5. DATE RANGE FILTERING (Freshness)

#### Time-Based Filtering
```javascript
const dateFilters = {
  "24h": { hours: 24 },
  "3d": { hours: 72 },
  "7d": { hours: 168 },
  "30d": { hours: 720 }
};

function isWithinDateRange(postedDate, filterType) {
  const jobDate = new Date(postedDate);
  const cutoffDate = new Date();
  cutoffDate.setHours(cutoffDate.getHours() - dateFilters[filterType].hours);
  
  return jobDate >= cutoffDate;
}
```

#### Bluprintx Date Strategy:
- **Last 24h**: Hottest leads, actively hiring NOW
- **Last 3 days**: Still warm, good timing
- **Last 7 days**: Acceptable freshness
- **Last 30 days**: Maximum age for relevance

#### Freshness Logic:
- **Recent posts** = Active hiring, budget allocated
- **Older posts** = May be filled, stale opportunity
- **Sales timing**: Recent = better chance of engagement

---

## 🎯 Bluprintx-Specific Filter Combinations

### Sales Playbook Filters

#### **"Quick Wins" Strategy**
```javascript
filters: {
  companySize: ["smb"],           // 51-500 employees
  seniority: ["entry", "mid"],    // Not senior+ roles
  dateRange: "3d",                // Posted in last 3 days
  mustContain: "salesforce, admin, developer",
  exclude: "senior, architect, lead"
}
// Result: SMB companies hiring Salesforce implementers recently
```

#### **"Big Fish" Strategy**
```javascript
filters: {
  companySize: ["enterprise"],    // 500+ employees
  seniority: ["senior", "executive"], // Senior roles
  dateRange: "7d",                // Posted in last week
  mustContain: "salesforce",
  exclude: "junior, associate"
}
// Result: Large companies hiring senior Salesforce people
```

#### **"Hot Leads" Strategy**
```javascript
filters: {
  dateRange: "24h",               // Posted TODAY
  mustContain: "salesforce",
  exclude: "oracle, sap, microsoft"
}
// Result: Any company actively hiring Salesforce TODAY
```

## 🔄 Filter Processing Pipeline

### Data Flow Through Filters
```
Raw LinkedIn Jobs → Job Title Filter → Company Size Filter → 
Seniority Filter → Company Exclude Filter → Date Filter → 
Clean Results → Export
```

### Filter Efficiency Logic
```javascript
// Process cheapest filters first to reduce data volume
const filterPipeline = [
  "dateFilter",        // Cheapest: date comparison
  "companyExclude",    // Fast: string matching
  "jobTitleMust",      // Medium: keyword matching
  "jobTitleExclude",   // Medium: keyword exclusion
  "companySize",       // Expensive: employee count lookup
  "seniority"          // Expensive: title analysis
];
```

## 📊 Filter Performance Metrics

### Success Benchmarks
- **Job Title Accuracy**: >90% correctly categorized
- **Company Size**: >85% correctly sized
- **Date Filtering**: >95% within range
- **Exclude Accuracy**: >95% correctly excluded/included

### Cost Efficiency
- **Filter Processing**: <0.1 seconds per job
- **API Calls**: Minimize expensive company lookups
- **Data Quality**: Balance speed vs accuracy

## 🚀 Implementation Priority

### Phase 1: Essential Filters (MVP)
1. **Job Title Must/Exclude** - Core targeting
2. **Date Range** - Freshness control
3. **Company Exclude** - Remove competitors

### Phase 2: Advanced Targeting
1. **Company Size** - Budget indication
2. **Seniority Level** - Decision speed
3. **Multi-location** - Territory management

### Phase 3: Sales Intelligence
1. **Smart categorization** - AI-powered role detection
2. **Partner identification** - Salesforce ecosystem
3. **Territory optimization** - Sales region mapping

## 💡 Sales Team Workflow Integration

### Daily Usage Pattern
```
Morning: "Hot Leads" (24h + Salesforce) → Call immediately
Mid-day: "Quick Wins" (SMB + Recent) → Email outreach  
Afternoon: "Big Fish" (Enterprise + Senior) → Research & plan
```

### Filter Presets for Sales
```javascript
const salesPresets = {
  "morning_hustle": {
    dateRange: "24h",
    mustContain: "salesforce",
    sortBy: "datePosted",
    view: "cards"
  },
  "territory_uk": {
    location: "United Kingdom",
    companySize: ["smb", "enterprise"],
    mustContain: "salesforce"
  },
  "budget_conscious": {
    companySize: ["smb"],
    seniority: ["entry", "mid"],
    mustContain: "salesforce, admin, developer"
  }
};
```

This specification gives your developer the complete logic behind each filter, why it matters for sales, and exactly how to implement it. Every filter is designed around **real sales psychology** - not just technical functionality.