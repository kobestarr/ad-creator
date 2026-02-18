# Bluprintx LinkedIn Job Scraper - Complete Design Specification

## Project Overview
Complete web-based MVP for LinkedIn job scraping targeting Bluprintx (Salesforce consulting) use case. Replaces Google Sheets integration with integrated web interface for better UX.

**Status**: Ready for development - all specifications complete
**Repository**: kobestarr/linkedin-job-scraper (existing Apify-based foundation)
**Target Client**: Bluprintx (Salesforce partner)
**Business Case**: Track Salesforce-related hiring to identify consulting prospects

## Core Architecture
- **Backend**: Node.js/Express with Apify integration
- **Frontend**: Single-page application (HTML/JS/CSS)
- **Deployment**: Vercel (serverless functions)
- **Data Storage**: Session-based (no database needed for MVP)
- **Export**: CSV download functionality

## User Interface Design

### Main Search Interface
```
┌────────────────────────────────────────────────────────────────┐
│  🔍 Bluprintx LinkedIn Job Tracker                          │
├────────────────────────────────────────────────────────────────┤
│  Job Title: [Salesforce Administrator________]               │
│  Locations: [UK ▼] [+ Add Location]                          │
│  🔧 Advanced Filters ▼                                        │
├────────────────────────────────────────────────────────────────┤
│  📊 Company Size: [Any ▼] → Startup | SMB | Enterprise       │
│  👔 Seniority: [Any ▼] → Entry | Mid | Senior | Executive    │
│  💰 Salary: [Any ▼] → <$50k | $50-100k | $100k+ | $150k+     │
│  📅 Posted: [Last 24h ▼] → 24h | 3d | 7d | 30d | Any        │
├────────────────────────────────────────────────────────────────┤
│  ✅ Job MUST contain: [salesforce, admin_____]               │
│  ❌ Job EXCLUDE: [senior, architect_________]                │
│  ❌ Company EXCLUDE: [Oracle, SAP, Microsoft___]             │
├────────────────────────────────────────────────────────────────┤
│  👁️ View: [Cards ▼] → Cards | Table | Compact                 │
│  🔽 Sort by: [Date Posted ▼] → Date | Company | Salary       │
│  📊 Quick Filters: [🎯 Hot Leads] [⚡ Quick Wins] [🐟 Big Fish]│
│  [🚀 Start Scraping] [💾 Save Search] [📊 Export Results]     │
└────────────────────────────────────────────────────────────────┘
```

### View Options

**1. Card View (Default)**
```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│ 🏢 Salesforce               │  │ 🏢 SmallCo (50 employees)   │
│ 📊 Enterprise (10k+ emp)    │  │ 📊 SMB (50-500 emp)         │
│ 💼 Salesforce Admin         │  │ 💼 Salesforce Developer     │
│ 📍 London, UK               │  │ 📍 Manchester, UK           │
│ 💰 £60k-£80k | 👔 Mid-level │  │ 💰 £40k-£60k | 👔 Entry      │
│ ⏰ Posted 1 day ago          │  │ ⏰ Posted 3 days ago        │
│ [👁️ View] [💾 Save] [🔗 URL] │  │ [👁️ View] [💾 Save] [🔗 URL] │
└─────────────────────────────┘  └─────────────────────────────┘
```

**2. Table View**
```
Company    | Role          | Size    | Seniority | Location | Salary   | Posted
Salesforce | SF Admin     | Enterprise | Mid     | London   | £60k-80k | 1d
SmallCo    | SF Developer | SMB        | Entry   | MCR      | £40k-60k | 3d
```

**3. Compact View**
```
Salesforce (Enterprise) - SF Admin - London - £70k - 1d ago
SmallCo (SMB) - SF Developer - Manchester - £50k - 3d ago
```

## Filter System

### Basic Filters
- **Job Title**: Text input with autocomplete
- **Locations**: Multi-select with common presets (UK, US, Europe)
- **Date Range**: Last 24h, 3d, 7d, 30d, Any
- **Max Results**: 10, 25, 50, 100, 200

### Advanced Filters
- **Company Size**: Startup (<50), SMB (50-500), Enterprise (500+)
- **Seniority**: Entry, Mid, Senior, Executive
- **Salary Range**: Bands based on market data
- **Job Keywords**: Must contain/exclude (comma-separated)
- **Company Exclude**: Case-insensitive partial matching

### Smart Filters (Sales-Ready)
- **Salesforce Role Detection**: Auto-tags admin, developer, consultant roles
- **Partner Ecosystem**: Identifies existing Salesforce partners
- **Territory Grouping**: Pre-defined sales regions

## Sorting Options

### Primary Sorting
- **Date Posted**: Newest/Oldest First
- **Company Size**: Largest/Smallest First  
- **Salary Range**: Highest/Lowest First
- **Location**: Proximity-based
- **Company Name**: A-Z/Z-A

### Quick-Sort Buttons (Sales Workflows)
- **🎯 Hot Leads**: Large companies + posted in last 3 days
- **⚡ Quick Wins**: SMB companies + entry/mid-level roles
- **🐟 Big Fish**: Enterprise + senior/executive roles
- **🔥 Urgent**: Posted today (any size)
- **💰 Big Budgets**: Salary $100k+ or senior roles at large companies

## Technical Implementation

### Frontend Components
1. **Search Form**: Input fields, filters, view toggles
2. **Progress Indicator**: Real-time scraping status
3. **Results Display**: Card/Table/Compact views with sorting
4. **Export Controls**: CSV download, save search functionality

### Backend Endpoints
- `POST /api/scrape` - Start scraping job
- `GET /api/status/:jobId` - Check scraping progress
- `GET /api/results/:jobId` - Get formatted results
- `GET /api/export/:jobId` - Download CSV
- `POST /api/save-search` - Save search configuration

### Real-time Updates
- WebSocket connection for progress updates
- Polling fallback for compatibility
- Status indicators: Searching → Processing → Complete

### Cost Display
- Real-time cost estimation based on Apify pricing
- Show $0.35 per 1,000 jobs rate
- Display estimated total before starting

## Bluprintx-Specific Features

### Salesforce Focus
- Auto-detect Salesforce-related job titles
- Highlight Salesforce partner companies
- Filter by Salesforce ecosystem relevance

### Sales Intelligence
- **Prospect Scoring**: Company size + role seniority matrix
- **Contact Finder**: Integration with Hunter.io/Apollo for emails
- **CRM Ready**: Export in Salesforce/HubSpot format

### Territory Management
- UK regions: London, South, Midlands, North, Scotland
- US regions: East, West, Central, South
- Europe: DACH, Nordics, Benelux, France

## Export Options

### CSV Export
- Standard CSV with all job data
- Sales-team formatted CSV with prospect scores
- CRM-ready format with custom fields

### Advanced Export
- JSON format for API integration
- Filtered exports (only saved jobs)
- Bulk exports with multiple searches

## User Experience

### Progressive Enhancement
- Works without JavaScript (basic form submission)
- Enhanced experience with JS for real-time updates
- Mobile-responsive design

### Performance Optimization
- Lazy loading for large result sets
- Virtual scrolling for table view
- Client-side caching of searches

### Error Handling
- Graceful degradation for API failures
- Clear error messages with recovery options
- Retry logic with exponential backoff

## Deployment Strategy

### Vercel Configuration
- Serverless functions for API endpoints
- Static assets served from CDN
- Environment variables for credentials
- Custom domain support

### Security
- API rate limiting
- Input validation and sanitization
- CORS configuration for frontend
- Secure credential storage

## Cost Management

### Apify Integration
- Use cheapest actor: `2rJKkhh7vjpX7pvjg` ($0.35/1K jobs)
- Built-in deduplication to reduce costs
- Pay-per-use billing model

### Usage Tracking
- Display estimated cost before scraping
- Show running total during scraping
- Monthly usage dashboard

## Future Enhancements

### Phase 2 Features
- User accounts and saved searches
- Email notifications for new jobs
- Advanced analytics and reporting
- Integration with CRM systems

### Phase 3 Features
- AI-powered job categorization
- Predictive prospect scoring
- Automated outreach sequences
- Competitor analysis dashboard

## Success Metrics

### MVP Success Criteria
- Scrapes complete in under 2 minutes
- Results display within 5 seconds of completion
- CSV export works on all devices
- Zero setup required for basic usage

### Business Metrics
- Time saved vs manual LinkedIn searching
- Lead quality improvement for sales team
- Cost per lead vs traditional methods
- User adoption and retention rates

## Technical Specifications

### Browser Support
- Chrome, Firefox, Safari, Edge (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)
- Progressive enhancement for older browsers

### Performance Targets
- Page load: <2 seconds
- Search initiation: <500ms
- Results display: <1 second after completion
- CSV export: <3 seconds for 100 jobs

This design provides Bluprintx with a professional, user-friendly tool that eliminates friction and provides immediate value for their sales prospecting efforts.