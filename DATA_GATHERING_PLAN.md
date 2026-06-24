# Current UAT Testing Cycle & Data Gathering Requirements

## Current Manual UAT Process (Existing Workflow)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CURRENT MAYBANK UAT CYCLE                        │
└─────────────────────────────────────────────────────────────────────┘

STEP 1: Story Creation (Business)
┌────────────────────────────────────────────┐
│ Business creates user story in JIRA        │
│ • Title: "SST for Bakong on MAE"          │
│ • Description: Requirements                │
│ • Acceptance Criteria                      │
│ • Assign to Project: BAKONG, FTT, MOT      │
└────────────────────────────────────────────┘
                    ↓
STEP 2: Team Assignment (IT/JIRA Admin)
┌────────────────────────────────────────────┐
│ Story assigned to team (e.g., Bakong Team) │
│ • Project key: BAKONG                      │
│ • Team members identified                  │
└────────────────────────────────────────────┘
                    ↓
STEP 3: Access Request (QA Team Lead)
┌────────────────────────────────────────────┐
│ QA Team Lead collects:                     │
│ • PF Numbers of all QA engineers           │
│ • Names & emails                           │
│ • Forward to Business/ITBM                 │
│ • Request JIRA access for team             │
│ • Request access to UAT environment        │
│ • Request access to GitHub (for devs)     │
└────────────────────────────────────────────┘
                    ↓
STEP 4: Access Provisioning (ITBM/Security)
┌────────────────────────────────────────────┐
│ ITBM grants access:                        │
│ • JIRA read access (all team members)      │
│ • UAT environment access (all QA)          │
│ • GitHub repo access (developers)          │
│ • Confluence access (for documentation)    │
└────────────────────────────────────────────┘
                    ↓
STEP 5: Story Review (QA Team)
┌────────────────────────────────────────────┐
│ QA team reviews story in JIRA:             │
│ • Read requirements                        │
│ • Understand acceptance criteria           │
│ • Ask clarification questions (if needed)  │
└────────────────────────────────────────────┘
                    ↓
STEP 6: Test Case Preparation (QA Team)
┌────────────────────────────────────────────┐
│ QA engineers create test cases:            │
│ • Manual creation (currently)               │
│ • Cover acceptance criteria                │
│ • Include positive + negative scenarios    │
│ • Edge cases & boundary conditions         │
│ • Business rule validations                │
│                                             │
│ WHERE: Local document / JIRA comment       │
│ FORMAT: Excel? Word? JIRA subtasks?        │
│ APPROX TIME: 4-8 hours per story           │
└────────────────────────────────────────────┘
                    ↓
STEP 7: Test Case Verification (QA Lead)
┌────────────────────────────────────────────┐
│ Team Lead verifies test cases:             │
│ • Check coverage of acceptance criteria    │
│ • Validate test logic                      │
│ • Ensure no duplicates                     │
│ • Approve test cases                       │
└────────────────────────────────────────────┘
                    ↓
STEP 8: Upload to JIRA (QA Lead)
┌────────────────────────────────────────────┐
│ Test cases uploaded to JIRA:               │
│ • As attachments? Comments? Subtasks?      │
│ • Store for reference & traceability       │
│ • Mark story as "Ready for Testing"        │
└────────────────────────────────────────────┘
                    ↓
STEP 9: Development (Developers)
┌────────────────────────────────────────────┐
│ Developers code the feature:               │
│ • Work on changes (SIT environment)        │
│ • Code review & approval                   │
│ • Push to UAT branch                       │
│ • Notify QA when ready for testing         │
└────────────────────────────────────────────┘
                    ↓
STEP 10: Story Moved to QA (Dev/ITBM)
┌────────────────────────────────────────────┐
│ Development notifies QA:                   │
│ • Story pushed to UAT environment          │
│ • Story status: "Ready for QA"             │
│ • Feature available in UAT to test         │
│ • Notify team (Slack? Email?)              │
└────────────────────────────────────────────┘
                    ↓
STEP 11: Test Assignment (QA Team Lead)
┌────────────────────────────────────────────┐
│ Team Lead assigns story to QA engineers:   │
│ • Story: "SST for Bakong"                  │
│ • Assign equally by workload               │
│ • QA1 tests: 15 test cases                 │
│ • QA2 tests: 15 test cases                 │
│ • QA3 tests: 15 test cases                 │
│ • Notify assigned QA engineers             │
└────────────────────────────────────────────┘
                    ↓
STEP 12: Manual Test Execution (QA Team)
┌────────────────────────────────────────────┐
│ QA engineers execute tests in UAT:         │
│ • Login to UAT environment                 │
│ • Follow test steps manually               │
│ • Verify results against expectations      │
│ • If PASS: Mark in JIRA                    │
│ • If FAIL: Document issue, take screenshot │
│ • If BLOCKED: Note blocker reason          │
│                                             │
│ TIME PER TEST: 5-15 minutes (avg 8 min)    │
│ WHERE: Manual execution on UAT             │
└────────────────────────────────────────────┘
                    ↓
STEP 13: Status Update in JIRA (QA Team)
┌────────────────────────────────────────────┐
│ QA engineer updates JIRA:                  │
│ • Story status → "In Testing"              │
│ • Test result: PASS / FAIL / BLOCKED       │
│ • Add comment with execution details       │
│ • Link to defect (if FAIL)                 │
│ • Attach screenshot (if FAIL)              │
│                                             │
│ TIME: 2-3 minutes per test result          │
└────────────────────────────────────────────┘
                    ↓
STEP 14: Screenshot/Evidence Upload (QA Team)
┌────────────────────────────────────────────┐
│ Upload test evidence:                      │
│ • Screenshots of failed tests              │
│ • Screen recordings (sometimes)            │
│ • Uploaded WHERE?                          │
│   - JIRA Cloud comments?                   │
│   - Confluence page?                       │
│   - Shared drive?                          │
│ • FOR QA LEAD REVIEW                       │
│ • FOR COMPLIANCE/AUDIT TRAIL               │
└────────────────────────────────────────────┘
                    ↓
STEP 15: QA Lead Review (QA Lead)
┌────────────────────────────────────────────┐
│ Team Lead reviews all test results:        │
│ • Check: All tests executed?               │
│ • Check: Pass rate acceptable?             │
│ • Check: Failed tests have screenshots?    │
│ • Check: Defects filed for failures?       │
│ • Decision: Story PASS or FAIL             │
└────────────────────────────────────────────┘
                    ↓
STEP 16: Defect Triage (QA Lead + Developers)
┌────────────────────────────────────────────┐
│ If failures found:                         │
│ • Categorize severity (Critical/High/Med)  │
│ • Assign to developer for fix              │
│ • Developer fixes in code                  │
│ • Push to UAT again                        │
│ • QA retests (regression)                  │
│ • Repeat until PASS                        │
└────────────────────────────────────────────┘
                    ↓
STEP 17: Story Sign-Off (QA Lead)
┌────────────────────────────────────────────┐
│ Once all tests pass:                       │
│ • Mark story: "Testing Complete"           │
│ • Update JIRA status to "Done"             │
│ • Generate test execution report           │
│ • Archive screenshots                      │
│ • Story ready for Production UAT / Go-Live │
└────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

CURRENT PAIN POINTS:
  ✗ Manual test case creation: Slow (4-8 hours per story)
  ✗ Manual test execution: Repetitive (8 min × 45 tests = 6 hours/story)
  ✗ Manual result tracking: Error-prone (JIRA updates, screenshot uploads)
  ✗ Screenshot management: Scattered (JIRA? Confluence? Shared drive?)
  ✗ No traceability: Hard to link story → test → result → screenshot
  ✗ Runtime changes: If requirement changes mid-UAT, manually redo tests
  ✗ Velocity metrics: Hard to calculate (no centralized tracking)
```

---

## Hybrid Approach: Manual + Automated

```
PROPOSED SYSTEM: Keep manual + ADD automation where possible

STEP 1-11: SAME (Manual)
  └─ Business creates story
  └─ Team assignment
  └─ Access request
  └─ Story review
  └─ Test case creation (NOW: AUTO-GENERATED by AI agent)
  └─ Test case verification (QA Lead still reviews)
  └─ Development
  └─ Story moved to QA
  └─ Test assignment (AUTO by workload balancer)

STEP 12: Test Execution (HYBRID)
  ├─ Manual Execution (QA engineer does it manually):
  │   • Login to UAT environment
  │   • Execute steps manually
  │   • Verify results
  │   • Attach screenshots
  │
  └─ Optional Automation (For future, Phase 2):
      • Selenium tests for UI flows
      • Postman/API tests for backend
      • Database validation tests
      • Both results feed same system

STEP 13-14: Result Tracking (AUTOMATED)
  ├─ QA logs result in portal (PASS/FAIL/BLOCKED)
  ├─ Screenshots auto-stored (S3/NFS)
  ├─ Results stored in local database
  └─ Traceability auto-maintained (story → test → result → screenshot)

STEP 15-17: SAME (Manual)
  └─ QA Lead reviews results
  └─ Defect triage
  └─ Sign-off

```

---

## Data Gathering: What to Collect from Each Team

### **TEAM 1: JIRA / IT Administration**

**Point of Contact:** JIRA Admin, IT Infrastructure

**Information to Gather:**

```
JIRA Configuration
  ☐ JIRA URL: https://jira.maybank.com (or internal URL?)
  ☐ JIRA version: (Server? Cloud? On-Prem Prime?)
  ☐ Read-only API token for service account: ____________________
  ☐ API token expiration date: ____________________
  ☐ Rate limiting on API: (requests/second?)
  ☐ Can we create custom fields in JIRA? (YES/NO)
  ☐ Can we create custom workflows? (YES/NO)
  ☐ RSS feed export enabled? (YES/NO)
  ☐ REST API v2 or v3 available? (Both? Which preferred?)

Project Configuration
  ☐ List all projects we need to connect:
      • BAKONG
      • FTT
      • MOT
      • VISADIRECT
      • WESTERNUNION
      • EIPO
      • Others: _________________
  
  ☐ For each project, provide:
      • Project Key (e.g., BAKONG)
      • Project Name (full name)
      • Number of stories per release (avg?)
      • Story status workflow (what states exist?)

Story Format
  ☐ Where are acceptance criteria stored?
      • In Description field?
      • In custom field?
      • In comments?
  ☐ Sample story ID for testing: ____________________
  ☐ Can you export 10 sample stories (CSV/JSON)?
  ☐ Story creation rate (per day/week/sprint)?
  ☐ Average stories per UAT wave?

Test Case Storage
  ☐ Where should test cases be stored?
      • JIRA comments/description?
      • JIRA attachments?
      • Confluence?
      • Shared drive?
  ☐ Current naming convention for test cases?
  ☐ How are test cases versioned (if at all)?

Reporting
  ☐ Can we query JIRA via API for:
      • Stories by project?
      • Stories created after date X?
      • Stories with custom field = value?
  ☐ Are there existing reports/dashboards we should use?
```

---

### **TEAM 2: Development / Git**

**Point of Contact:** Development Manager, Lead Developer

**Information to Gather:**

```
GitHub/Code Repository
  ☐ GitHub Enterprise URL or public GitHub?
  ☐ Repositories we need to scan:
      • banking-transfer-system (main?)
      • Others: ____________________
  ☐ GitHub token for API access: ____________________
  ☐ Token permissions: (read-only code? Read commits? Read PRs?)
  ☐ Branch naming convention:
      • Main branch: (main? master? release?)
      • Feature branch format: (feature/BAKONG-123?)
      • UAT branch: (uat? qa?)

Code Quality & Risk Signals
  ☐ What are the critical code patterns we should detect?
      • Fee calculations? (Where in code?)
      • Validation logic? (Where in code?)
      • Limit checks? (Where in code?)
      • Error handling? (Where in code?)
  ☐ Historical bugs:
      • What types of bugs most common?
      • Any recurring risk areas?
  ☐ Code review process:
      • Who approves code before UAT?
      • Are there code quality metrics?
      • Static analysis tools used? (Sonarqube? Semgrep?)

Story Linkage
  ☐ How are stories linked to code changes?
      • Branch name contains story ID? (e.g., feature/SSTMAEM2U-16?)
      • Commit messages contain story ID?
      • Pull request references story?
  ☐ Can we trace: Story → GitHub changes → Code risk?

Development Status
  ☐ When developers push to UAT branch, how do they notify QA?
      • Slack message? Email? Manual?
      • Is there a webhook?
      • Can we subscribe to branch updates?
  ☐ Average development time per story?
  ☐ Code review turnaround time?
```

---

### **TEAM 3: QA / Testing Team**

**Point of Contact:** QA Lead, QA Manager

**Information to Gather:**

```
Current Testing Process
  ☐ Where are test cases currently created?
      • Excel? Word? Google Sheets? Confluence?
      • JIRA? If yes, how (comments? attachments? subtasks?)
  ☐ Average time to create test case per story: _____ hours
  ☐ Average time to execute test per story: _____ hours
  ☐ How many test cases per story on average? (30? 50? 100?)
  ☐ Test case format/template:
      • What fields required? (Title, Steps, Expected, Preconditions?)
      • Is there a standard template?
      • Can we reuse format for agent generation?

Test Execution
  ☐ Who executes tests manually?
      • All 50 QA engineers? Or subset?
      • Any specialization? (UI testing vs API vs Database?)
  ☐ Test execution environment:
      • UAT URL/server: ____________________
      • Test user accounts available?
      • How many concurrent testers? (10? 20? 50?)
  ☐ Test data:
      • Are test data accounts provided? (Yes/No)
      • Sample amounts for transfers? (100k? 500k? 1M?)
      • Sample currencies needed?
      • Is data reset between tests?
  ☐ Average execution time per test: _____ minutes
  ☐ Pass rate typically: _____ %

Test Result Tracking
  ☐ Currently, how are test results captured?
      • Manual JIRA updates? (Comments? Custom fields?)
      • Spreadsheet?
      • Email?
  ☐ Where are screenshots/evidence stored?
      • JIRA attachments?
      • Confluence?
      • Shared drive? (Path: ____________________?)
      • OneDrive/Google Drive?
  ☐ How long does it take to update results & upload screenshots?
      • Time per test: _____ minutes
  ☐ Who reviews test results?
      • QA Lead only?
      • QA Lead + PM?
      • QA Lead + Compliance?

Coverage & Metrics
  ☐ What makes a story "fully tested"?
      • Coverage threshold: _____ %
      • Pass rate threshold: _____ %
  ☐ How are coverage metrics calculated?
      • Manually? Automatically?
      • From JIRA? Spreadsheet?
  ☐ Are there test execution velocity metrics tracked?
      • Tests per day?
      • Pass rate trends?
  ☐ Average UAT cycle time: _____ days

Challenges & Pain Points
  ☐ What takes the MOST time currently?
      • Creating test cases?
      • Executing tests?
      • Tracking results?
      • Managing screenshots?
  ☐ What's the biggest source of errors?
      • Manual tracking errors?
      • Screenshot management?
      • Duplicate tests?
  ☐ What would improve UAT efficiency most?
      • Faster test generation?
      • Better result tracking?
      • Automated screenshot capture?
      • Centralized reporting?

Team Structure
  ☐ QA Lead name/email: ____________________
  ☐ Number of QA engineers per project:
      • Bakong: _____
      • FTT: _____
      • MOT: _____
      • Others: _____
  ☐ Total QA team size: _____
  ☐ Are QA engineers dedicated to one project or rotated?
  ☐ Skill distribution:
      • % UI testing specialists
      • % API testing specialists
      • % Database testing specialists
      • % General testers
  ☐ QA engineer contact info (will be needed for portal access):
      • List: ____________________

Reporting Needs
  ☐ What reports does QA Lead need?
      • Daily progress?
      • Pass rate trend?
      • Coverage status?
      • Defect summary?
  ☐ What reports does PM need?
      • UAT readiness estimate?
      • Risk assessment?
      • GO/NO-GO recommendation?
  ☐ What reports does Compliance need?
      • Audit trail?
      • Test traceability?
      • Sign-off documentation?
```

---

### **TEAM 4: Business Analyst / Product Manager**

**Point of Contact:** Product Manager, Business Analyst, Release Manager

**Information to Gather:**

```
Story Requirements
  ☐ How are stories created/formatted?
      • Who writes stories? (Business analyst? Product manager?)
      • Template used? (Can we see example?)
      • Are acceptance criteria always included?
      • Any variation in format per project?
  ☐ Average acceptance criteria per story: _____ criteria
  ☐ How often do requirements change mid-UAT?
      • Rarely? Weekly? Daily?
      • What's the change process?
      • How quickly must QA adapt?
  ☐ Sample stories for testing:
      • Can you provide 10 real stories?
      • Preferably from different project domains?

UAT Timeline & Schedule
  ☐ When does UAT start (next release)? ____________________
  ☐ How long is UAT window? _____ days
  ☐ Multiple UAT waves or single wave?
      • Wave 1: Date? Duration? Scope?
      • Wave 2: Date? Duration? Scope?
  ☐ Parallel streams (multiple modules testing simultaneously)?
      • Bakong + FTT + MOT at same time?
      • Or sequential?
  ☐ Hard deadline for UAT completion (go-live date)?
  ☐ Flexibility if tests need more time?

Business Rules & Critical Features
  ☐ What are the most critical features for each module?
      • Bakong: (SST calculation? Limit checks?)
      • FTT: (Fee handling? Validation?)
      • MOT: ____________________
  ☐ What business rules are non-negotiable?
      • Must never fail (e.g., amount validation)?
      • Must be tested every release?
  ☐ Any regulatory/compliance rules?
      • PCI-DSS? SWIFT compliance? Anti-money laundering?
  ☐ Risk tolerance:
      • Which failures are critical vs acceptable?
      • What pass rate required to go live?
      • Any critical defects allowed?

Success Criteria
  ☐ How do we know UAT is successful?
      • Coverage threshold: _____ %
      • Pass rate threshold: _____ %
      • Defect resolution: All critical? Or accept some medium?
      • Time constraint: Must finish by ____________________?
  ☐ Who approves UAT completion?
      • QA Lead alone? Or multiple sign-offs?
      • Business? Product Manager? Compliance? Release Manager?
  ☐ Sign-off mechanism:
      • Email approval?
      • Document signature?
      • JIRA workflow state?

Defect Management
  ☐ How are defects categorized?
      • Critical / High / Medium / Low?
      • Blocker / Major / Minor?
  ☐ What's acceptable for UAT completion?
      • Zero defects? (Unrealistic)
      • Zero critical defects? (Typical)
      • Max N medium defects?
  ☐ Who decides if defect is critical vs high vs medium?
      • Developer?
      • QA?
      • Business?
      • Product Manager?
  ☐ Defect resolution SLA:
      • How quickly must developer fix?
      • How quickly must QA retest?
      • Escalation process if SLA missed?

Compliance & Audit
  ☐ Audit trail requirements:
      • Must track who tested what when?
      • Must store screenshots for 2 years?
      • Must have immutable log?
  ☐ Approval process:
      • Who signs off each story?
      • Who signs off entire UAT?
      • Multiple levels of approval?
  ☐ Compliance standards applicable:
      • PCI-DSS?
      • ISO 27001?
      • SOX?
      • Maybank-specific policies?
```

---

### **TEAM 5: Security & Compliance**

**Point of Contact:** CISO, Security Officer, Compliance Officer

**Information to Gather:**

```
Data Protection Requirements
  ☐ Encryption required?
      • At rest? (AES-256?)
      • In transit? (TLS 1.3?)
  ☐ Test data handling:
      • Can we use production customer data?
      • Must all PII be masked?
      • Must credit card data be redacted?
      • Policy document: ____________________?
  ☐ Data retention:
      • How long keep test results? (1 year? 2 years? Forever?)
      • How long keep screenshots?
      • Archive strategy (cold storage? Delete?)
      • Secure deletion required?

Authentication & Authorization
  ☐ Authentication method:
      • LDAP? (DC address: ____________________?)
      • SAML? (IdP URL: ____________________?)
      • OAuth? (Provider: ____________________?)
      • MFA required? (Yes/No)
  ☐ Authorization (roles):
      • How to define: QA Engineer, QA Lead, Admin?
      • Where stored: LDAP groups? JIRA groups?
      • Can we create custom roles?
  ☐ Access control:
      • QA can only see assigned tests?
      • QA can only see own project's tests?
      • QA can see all test results?
      • Admin see everything?

Audit & Logging
  ☐ Audit trail required?
      • All user actions logged? (Who, what, when, where?)
      • Immutable log? (Can't be deleted/modified?)
      • Timestamped with UTC?
      • How long retain? (1 year? 2 years? Forever?)
  ☐ What actions must be logged?
      • Test case created?
      • Test executed?
      • Result updated?
      • Screenshot uploaded?
      • Report exported?
  ☐ Audit log access:
      • Who can view audit logs?
      • Export for external audit? (Yes/No)
      • Format requirements? (CSV? PDF?)

Vulnerability & Risk Management
  ☐ Security testing required before launch?
      • Penetration testing? (Yes/No)
      • Vulnerability scanning? (Yes/No)
      • Code review by security team? (Yes/No)
  ☐ Secrets management:
      • How to store API tokens? (Vault? K8s secrets?)
      • Password rotation policy?
      • Token expiration policy?
  ☐ Network security:
      • IP whitelist required?
      • VPN required to access?
      • Firewall rules needed?

Compliance Standards
  ☐ Which compliance standards apply?
      • PCI-DSS (payment card data)?
      • ISO 27001 (information security)?
      • SOX (financial controls)?
      • GDPR (personal data)?
      • Others: ____________________?
  ☐ Compliance documentation:
      • Policy documents available?
      • Checklists we must follow?
      • Pre-launch review required?
  ☐ Third-party audit:
      • Will system be audited?
      • Audit frequency?
      • What must be demonstrated?

Data Privacy
  ☐ PII handling:
      • What counts as PII? (Name? Email? Customer ID?)
      • Must be masked/redacted?
      • Separate classification for sensitive data?
  ☐ Customer data:
      • Can we store customer account info in test results?
      • Screenshots with customer data allowed?
      • Data anonymization required?

Breach & Incident Response
  ☐ Incident response plan:
      • Who to notify if data breached?
      • Documentation requirement?
      • Communication timeline?
```

---

### **TEAM 6: IT Infrastructure / DevOps**

**Point of Contact:** Infrastructure Manager, Cloud/On-Prem Admin

**Information to Gather:**

```
Server / Hosting Infrastructure
  ☐ Where should application run?
      • On-premises VM? (Yes/No)
      • Docker? (Yes/No)
      • Kubernetes cluster? (Yes/No)
      • Cloud? (AWS? Azure? GCP? Maybank's private cloud?)
  ☐ Server specifications:
      • CPU cores needed: _____
      • RAM needed: _____ GB
      • Storage needed: _____ GB
      • OS preferred: (Linux? Windows? Both?)
  ☐ Server location:
      • Data center location: ____________________
      • Rack/subnet: ____________________
      • Network access (internal/external)?

Database Infrastructure
  ☐ PostgreSQL available?
      • Version: ____________________
      • Already provisioned? (Yes/No)
      • If NO, when can it be?
      • Connection string: ____________________
      • Database credentials: (Will provide separately)
  ☐ Database backup:
      • Backup frequency: (Daily? Weekly?)
      • Backup location/storage?
      • Restoration testing done? (Yes/No)
      • RTO/RPO requirements?
  ☐ Database size estimate:
      • Initial size: _____ GB
      • Growth rate: _____ GB/month
      • Storage capacity available? (Yes/No)

File Storage / Artifact Storage
  ☐ Where to store screenshots?
      • NFS mount available? (Path: ____________________?)
      • S3-equivalent (MinIO)? (Available? Yes/No)
      • CIFS/SMB share? (Path: ____________________?)
  ☐ Storage capacity:
      • Available now: _____ GB
      • Growth projection: _____ GB/year
  ☐ Access method:
      • Direct mount? API? HTTP?
      • Credentials/access key needed?
  ☐ Backup for storage:
      • Backup frequency?
      • Retention policy?

Container / Deployment
  ☐ Docker registry available?
      • Harbor? Artifactory? Docker Hub?
      • Internal or external?
      • Credentials provided?
  ☐ Kubernetes cluster:
      • Available? (Yes/No)
      • Namespace provided?
      • Cluster details (version, nodes, capacity)?
      • Ingress/LoadBalancer available?
  ☐ Or simple deployment:
      • VM + systemd?
      • Cron jobs for scheduling?
      • Supervisor for process management?

Networking & Firewall
  ☐ Network connectivity:
      • Can agent reach JIRA on-prem? (Yes/No)
      • Can agent reach GitHub? (Yes/No)
      • Can agent reach UAT environment? (Yes/No)
      • Can agent send HTTPS requests? (Yes/No)
  ☐ Firewall rules needed:
      • Outbound to JIRA (IP:port): ____________________
      • Outbound to GitHub (IP:port): ____________________
      • Outbound to Slack webhook (IP:port): ____________________
      • Inbound API traffic (IP:port): ____________________
  ☐ VPN / Proxy:
      • VPN required to access services? (Yes/No)
      • HTTP proxy? (Yes/No)
      • SSL inspection? (Yes/No)
  ☐ SSL/TLS Certificates:
      • Internal CA available? (Yes/No)
      • Certificate format? (PEM? DER?)
      • Who manages certificates?

Monitoring & Logging
  ☐ Monitoring tools available?
      • Prometheus? Grafana? Datadog? Others?
      • Can we export metrics?
  ☐ Logging infrastructure:
      • ELK stack? Splunk? CloudWatch?
      • Log aggregation available?
      • Retention policy?
  ☐ Alerting:
      • Alert system available?
      • Who gets notified? (On-call? Team? Slack?)

DNS & Load Balancing
  ☐ DNS entry needed?
      • DNS name for application: ____________________?
      • Who manages DNS?
  ☐ Load balancer:
      • Required? (Yes/No)
      • Already configured? (Yes/No)
      • Health check endpoints? (Yes/No)

UAT Environment Infrastructure
  ☐ UAT environment details:
      • URL/IP: ____________________
      • How many concurrent users supported?
      • Reset/refresh frequency?
      • Data available? (Sample transfer data?)
      • Test accounts available? (How many? Credentials?)
```

---

### **TEAM 7: Slack / Internal Communications**

**Point of Contact:** Slack Admin, Team Leads

**Information to Gather:**

```
Slack Integration
  ☐ Slack workspace available?
      • Workspace URL: ____________________
      • Slack admin contact: ____________________
  ☐ Channels for notifications:
      • #qa-bot (all events): Create? Already exists?
      • #qa-leads (blockers): Create? Already exists?
      • #compliance (gates): Create? Already exists?
      • Others: ____________________
  ☐ Slack webhook URL for bot:
      • (Will be provided during setup)
  ☐ Notification preferences:
      • What events to notify? (Generation done? Requirement changed? Gate status?)
      • Frequency? (Real-time? Daily summary? On-demand?)
      • Who should be tagged in notifications?
      • Mention format? (@john.smith? @team-lead?)

Alternative to Slack (if not available)
  ☐ If no Slack, what's the alternative?
      • Microsoft Teams?
      • Email distribution list?
      • Internal portal?
      • Others: ____________________
```

---

### **TEAM 8: Release / Deployment Team**

**Point of Contact:** Release Manager, Deployment Engineer

**Information to Gather:**

```
Release Process
  ☐ UAT process in release cycle:
      • When does UAT start (relative to code freeze)?
      • When does UAT end (relative to go-live)?
      • Duration: _____ days
  ☐ Multiple release waves:
      • Wave 1: ____________________
      • Wave 2: ____________________
      • Schedule: Sequential or parallel?
  ☐ Go-live process:
      • Who approves go-live? (QA Lead? Release Manager? Business?)
      • Sign-off mechanism?
      • Go-live schedule: ____________________?

Deployment Process
  ☐ Code promotion path:
      • SIT → UAT → Production?
      • How is code moved between environments?
      • Who has deployment access?
  ☐ UAT environment refresh:
      • Frequency? (Daily? Weekly?)
      • Data reset between releases? (Yes/No)
      • Time window for refresh?
  ☐ Rollback plan:
      • If UAT fails, can we rollback?
      • Rollback process?
      • Estimated time?

Notification to QA
  ☐ How does QA know code is ready to test?
      • Email notification?
      • Slack message?
      • Manual check of UAT environment?
      • Webhook/automated notification?
  ☐ Notification timing:
      • When pushed to UAT?
      • Any notification frequency? (Hourly? Daily?)

Go/No-Go Decision
  ☐ Who decides if UAT is complete?
      • QA Lead? Release Manager? Business? All?
  ☐ Decision criteria:
      • Coverage threshold?
      • Pass rate threshold?
      • Defect status?
  ☐ Sign-off documentation:
      • Email? JIRA status? Formal document?
```

---

## Data Collection Spreadsheet Template

```
Team               Contact Name      Email             Phone         Questionnaire Status
───────────────────────────────────────────────────────────────────────────────────────
JIRA Admin         John Doe          john@maybank.com  +60-XXX-XXX  ☐ Pending ☐ In Progress ☐ Complete
Development Mgr    Jane Smith        jane@maybank.com  +60-XXX-XXX  ☐ Pending ☐ In Progress ☐ Complete
QA Lead            Ali Hassan        ali@maybank.com   +60-XXX-XXX  ☐ Pending ☐ In Progress ☐ Complete
Product Manager    Sarah Khan        sarah@maybank.com +60-XXX-XXX  ☐ Pending ☐ In Progress ☐ Complete
Security Officer   Raj Patel         raj@maybank.com   +60-XXX-XXX  ☐ Pending ☐ In Progress ☐ Complete
Infrastructure Mgr Tom Wong          tom@maybank.com   +60-XXX-XXX  ☐ Pending ☐ In Progress ☐ Complete
Slack Admin        Lisa Chen         lisa@maybank.com  +60-XXX-XXX  ☐ Pending ☐ In Progress ☐ Complete
Release Manager    Mike Brown        mike@maybank.com  +60-XXX-XXX  ☐ Pending ☐ In Progress ☐ Complete
```

---

## Timeline: Data Collection Phase

```
Week 1: Send Questionnaires
  □ Email questionnaires to all 8 teams
  □ Set deadline: 1 week to respond
  □ Schedule follow-up calls if needed

Week 2: Follow-Up & Clarification
  □ Review responses from each team
  □ Schedule calls for incomplete answers
  □ Clarify contradictions
  □ Collect missing information

Week 3: Consolidation & Planning
  □ Compile all answers into master document
  □ Identify blockers early
  □ Refine architecture based on actual constraints
  □ Update timeline if needed

Week 4: Kickoff
  □ Present consolidated findings to team
  □ Get approval on technical approach
  □ Resolve any remaining questions
  □ Start development (Week 1 implementation)
```

---

## Red Flags to Watch For

🚩 **If any team says "Don't know"** → Escalate for clarification
🚩 **If JIRA is truly read-only but they expect writes** → Clarify expectations
🚩 **If infrastructure is "maybe" available** → Request confirmed provision date
🚩 **If security requirements are vague** → Demand specific compliance standards
🚩 **If UAT date is unclear** → This is critical, must pin down
🚩 **If QA team size is unknown** → Can't size solution properly
🚩 **If no one knows the test process** → Need to document existing workflow first

---

## Success Criteria: Data Collection Complete When:

✅ All 8 teams have responded to questionnaire
✅ JIRA read-only status 100% confirmed
✅ Infrastructure capacity confirmed (DB, storage, server)
✅ UAT timeline locked in
✅ QA team structure and size confirmed
✅ Security & compliance requirements documented
✅ All blockers identified and escalated
✅ Team leads aligned on approach

**Only after this is complete should development start.**
