# MASTER BUILD PROMPT

## AI Career Application Agent — V1

You are a **Senior AI Engineer, Backend Architect, Distributed Systems Engineer, Full-Stack Engineer, and Product Architect**.

Build a production-quality V1 of an **AI Career Application Agent**.

The product is a backend-first SaaS platform that continuously finds relevant jobs, analyzes them, determines compensation, compares them against the user's single active resume, prepares the application, and provides the user with a simple mobile/desktop interface to **APPLY** or **REJECT**.

The final application submission in V1 is performed by the **user on the original job platform**.

The system must NOT automatically submit applications to LinkedIn, Indeed, or Glassdoor in V1.

---

# 1. PRODUCT VISION

The user should be able to:

1. Create an account.
2. Upload one resume.
3. Define job preferences.
4. Give the AI Agent authority to search for jobs.
5. Let the Agent continuously discover relevant jobs.
6. Let the Agent analyze each job.
7. Determine whether the job is Paid, Unpaid, Stipend, or Not Disclosed.
8. Determine whether the job has an in-platform Apply/Easy Apply flow.
9. Match the job against the user's resume.
10. Calculate an explainable match score.
11. Prepare application information.
12. Receive a mobile-friendly notification.
13. Select **APPLY** or **REJECT**.
14. If APPLY is selected, redirect/open the original application flow on LinkedIn, Indeed, or Glassdoor.
15. The user completes the final submission on that platform.
16. Track the application status inside our system.

The product should feel like:

> **"Give me your resume and job preferences. I'll continuously find the opportunities worth applying to, tell you why you're a match, tell you whether they're paid, prepare the application, and take you directly to the application page."**

---

# 2. V1 PLATFORM SCOPE

V1 focuses on:

* LinkedIn
* Indeed
* Glassdoor

Target only jobs with an in-platform:

* Easy Apply
* Apply
* equivalent native application flow

The system must detect the application method.

Use:

```text
LINKEDIN_APPLY
INDEED_APPLY
GLASSDOOR_APPLY
EXTERNAL_APPLICATION
UNKNOWN
```

If the job redirects to:

```text
Company Career Website
Greenhouse
Lever
Workday
SmartRecruiters
Other ATS
```

classify it as:

```text
EXTERNAL_APPLICATION
```

External applications are **not part of the V1 application workflow**.

They may optionally be displayed as opportunities, but clearly mark:

> External Application — Not Supported in V1

---

# 3. CRITICAL V1 APPLICATION RULE

The backend does NOT submit applications.

The backend performs:

```text
DISCOVER
   ↓
ANALYZE
   ↓
MATCH
   ↓
FILTER
   ↓
COMPENSATION
   ↓
PREPARE
   ↓
NOTIFY USER
   ↓
USER SELECTS APPLY
   ↓
OPEN ORIGINAL PLATFORM
   ↓
USER COMPLETES APPLICATION
```

The APPLY button in our product means:

> **"Continue to the original job platform and apply there."**

It does NOT mean:

> "Our backend has submitted the application."

Never mark an application as `APPLIED` simply because the user clicked our APPLY button.

Use:

```text
READY
USER_APPROVED
APPLICATION_HANDOFF
AWAITING_SUBMISSION
APPLIED
```

Only mark `APPLIED` when there is a reliable confirmation mechanism.

Otherwise remain:

```text
AWAITING_SUBMISSION
```

---

# 4. PLATFORM COMPLIANCE

Do NOT build:

* CAPTCHA bypass
* Anti-bot bypass
* Bot detection evasion
* Rate-limit bypass
* Authentication bypass
* Session hijacking
* Credential harvesting
* Unauthorized scraping
* Unauthorized browser automation
* Automated clicking designed to circumvent platform restrictions

Use official APIs, permitted feeds, approved integrations, public job data, or other authorized mechanisms.

The system should store the original job URL and use it for user handoff.

For V1, the safest application execution mechanism is:

```text
Backend
   ↓
Generate application handoff URL
   ↓
Frontend
   ↓
Open original platform
   ↓
User completes application
```

---

# 5. SINGLE ACTIVE RESUME

V1 supports exactly **ONE active resume**.

Supported formats:

```text
PDF
DOCX
```

The system stores:

1. Original resume
2. Parsed candidate profile

The Agent must NEVER automatically modify the resume.

Do NOT:

* Rewrite resume
* Optimize resume
* Add skills
* Remove skills
* Change experience
* Create job-specific resume
* Generate resume variants

The same uploaded resume is used for all jobs.

Only the user can replace it.

---

# 6. USER ONBOARDING

Keep onboarding minimal.

Required:

### Resume

Upload one PDF/DOCX.

### Target Roles

Examples:

```text
AI Engineer
ML Engineer
Backend Engineer
Software Engineer
Data Engineer
```

Allow custom roles.

### Experience Level

```text
Internship
Entry Level
0–2 Years
2–5 Years
5+ Years
```

### Preferred Locations

Allow multiple:

```text
Remote
Pune
Mumbai
Bangalore
Hyderabad
Delhi NCR
Chennai
```

### Work Mode

```text
Remote
Hybrid
On-site
Any
```

### Employment Type

```text
Internship
Full-time
Part-time
Contract
Any
```

### Compensation

```text
Paid Only
Paid + Not Disclosed
Any
```

Allow:

```text
Minimum stipend
Minimum salary
```

---

# 7. OPTIONAL USER DATA

Do not make these mandatory during signup.

Allow later:

```text
Preferred companies
Companies to avoid
Industries
Technologies
Keywords
Relocation preference
Work authorization
Visa requirements
Notice period
```

The Agent must work without them.

---

# 8. AGENT AUTHORITY

Provide:

## DISCOVERY_ONLY

Agent:

* Finds jobs
* Analyzes jobs
* Matches jobs
* Notifies user

## PREPARE_APPLICATION

Agent additionally:

* Prepares application
* Generates cover letter
* Prepares screening answers
* Validates candidate information

V1 should primarily operate in:

```text
PREPARE_APPLICATION
+
USER_APPROVAL
```

The user always controls the final application handoff.

---

# 9. JOB DISCOVERY

Create a pluggable job-source architecture.

```text
JobSource
├── LinkedInAdapter
├── IndeedAdapter
├── GlassdoorAdapter
└── FutureAdapters
```

Common interface:

```python
class JobSource(Protocol):

    async def search_jobs(...):
        ...

    async def get_job_details(...):
        ...

    async def normalize_job(...):
        ...

    async def get_application_method(...):
        ...
```

Do not couple the core business logic to any individual platform.

---

# 10. JOB NORMALIZATION

Normalize all discovered jobs into a common schema.

Required fields:

```text
job_id
source
source_job_id
title
company
description
location
remote_status
employment_type
experience_required
required_skills
preferred_skills
technologies
education
salary
stipend
currency
compensation_status
application_method
application_supported
application_url
source_url
posted_at
deadline
```

Deduplicate jobs.

The same job appearing on LinkedIn, Indeed, and Glassdoor should ideally be recognized as the same opportunity.

---

# 11. APPLICATION METHOD DETECTION

Every job must have:

```text
application_method
```

Possible values:

```text
LINKEDIN_APPLY
INDEED_APPLY
GLASSDOOR_APPLY
EXTERNAL_APPLICATION
UNKNOWN
```

And:

```text
application_supported
```

Example:

```json
{
  "application_method": "LINKEDIN_APPLY",
  "application_supported": true
}
```

External:

```json
{
  "application_method": "EXTERNAL_APPLICATION",
  "application_supported": false
}
```

Only supported in-platform applications should receive the V1 **APPLY** action.

---

# 12. JOB INTELLIGENCE AGENT

Create a Job Intelligence Agent.

Extract:

```text
Job Title
Company
Location
Work Mode
Employment Type
Experience
Required Skills
Preferred Skills
Technologies
Education
Salary
Stipend
Application Method
Posted Date
Deadline
```

Use structured outputs.

Every important field should have a confidence/source where practical.

Never hallucinate missing information.

---

# 13. COMPENSATION INTELLIGENCE

Compensation is a core feature.

Classify:

```text
PAID
UNPAID
STIPEND
EQUITY_ONLY
PERFORMANCE_BASED
NOT_DISCLOSED
UNKNOWN
```

CRITICAL:

```text
Missing salary ≠ UNPAID
```

If compensation is not mentioned:

```text
NOT_DISCLOSED
```

If the job explicitly says unpaid:

```text
UNPAID
```

Example:

```json
{
  "status": "PAID",
  "minimum": 25000,
  "maximum": 30000,
  "currency": "INR",
  "period": "MONTH",
  "confidence": 0.96
}
```

Store:

```text
compensation_status
amount_min
amount_max
currency
period
confidence
source_text
```

---

# 14. CANDIDATE INTELLIGENCE

Parse the single active resume.

Create:

```text
CandidateProfile
```

Fields:

```text
Name
Education
Experience
Projects
Skills
Programming Languages
Frameworks
Databases
Cloud
AI/ML
Certifications
Achievements
Domains
```

The profile must be grounded entirely in the resume.

Never fabricate candidate information.

---

# 15. MATCHING AGENT

Build an explainable matching system.

Example:

```text
MATCH SCORE: 94%

Skills              96%
Experience          90%
Education           100%
Location            100%
Employment Type     100%
Domain               91%
```

Also identify:

```text
Strong Matches
Missing Required Skills
Missing Preferred Skills
Potential Gaps
Experience Conflicts
Education Conflicts
Location Conflicts
Compensation Conflicts
```

Use:

```text
Deterministic Rules
+
Embeddings
+
Semantic Similarity
+
LLM Reasoning
```

Do not allow the LLM to arbitrarily determine the final score.

---

# 16. POLICY ENGINE

Create user-specific rules.

Example:

```text
Minimum Match Score: 85%

Roles:
AI Engineer
Backend Engineer
ML Engineer

Locations:
Remote
Pune
Bangalore

Employment:
Internship
Full-time

Compensation:
Paid Only

Minimum Stipend:
₹15,000/month

Application:
In-platform only
```

Output:

```text
QUALIFIED
NOT_QUALIFIED
REQUIRES_REVIEW
```

---

# 17. APPLICATION PREPARATION AGENT

When a job is qualified, prepare:

```text
Existing Resume
Cover Letter
Application Answers
Screening Questions
Candidate Information
```

The resume must remain unchanged.

If the Agent cannot confidently answer a question:

```text
REQUIRES_USER_INPUT
```

The Agent must never guess or fabricate.

---

# 18. MOBILE OPPORTUNITY CARD

The primary experience should be mobile-first.

Example:

```text
AI Engineer Intern

XYZ Technologies

94% MATCH

💰 PAID — ₹25,000/month
📍 Pune / Remote
🎓 Internship
⚡ LinkedIn Apply

WHY YOU MATCH

✓ Python
✓ FastAPI
✓ LLM/RAG
✓ PostgreSQL
✓ Backend

POTENTIAL GAP

⚠ Kubernetes

APPLICATION READY

✓ Resume
✓ Cover Letter
✓ Questions

[ APPLY ]    [ REJECT ]
```

---

# 19. APPLY ACTION

When the user clicks:

```text
APPLY
```

the backend should:

1. Verify the job exists.
2. Verify the job is still actionable.
3. Verify application method.
4. Verify policy eligibility.
5. Verify application preparation.
6. Record `USER_APPROVED`.
7. Generate/store the original application URL.
8. Return the handoff URL.
9. Frontend opens the original platform.

Example:

```text
User
 ↓
APPLY
 ↓
Backend
 ↓
USER_APPROVED
 ↓
APPLICATION_HANDOFF
 ↓
Open LinkedIn / Indeed / Glassdoor
 ↓
User completes application
```

Do not automatically submit.

Do not claim the application was submitted.

---

# 20. REJECT ACTION

When user selects:

```text
REJECT
```

store:

```text
user_id
job_id
timestamp
reason
```

Optional reasons:

```text
Low Salary
Wrong Role
Wrong Location
Unpaid
Not Interested
Experience Mismatch
Other
```

Remove the job from the active opportunity queue.

Do not automatically change user preferences because of one rejection.

---

# 21. LANGGRAPH

Use **LangGraph as the Agent orchestration layer**.

Do not create one giant agent.

Create a stateful graph:

```text
START
 ↓
DISCOVER
 ↓
NORMALIZE
 ↓
ANALYZE
 ↓
COMPENSATION
 ↓
MATCH
 ↓
POLICY
 ↓
PREPARE_APPLICATION
 ↓
WAIT_FOR_USER
 ↓
 ┌─────────────┐
 │             │
APPLY        REJECT
 │             │
 ▼             ▼
HANDOFF       END
 │
 ▼
TRACK
 ↓
END
```

Use conditional routing.

The graph must support pausing/resuming around user interaction.

---

# 22. LANGGRAPH STATE

Use a strongly typed state.

Example:

```python
class CareerAgentState(TypedDict):
    user_id: str
    job_id: str | None

    job_data: dict | None
    candidate_profile: dict | None

    match_score: float | None
    match_analysis: dict | None

    compensation: dict | None

    application_method: str | None
    application_supported: bool

    policy_result: str | None

    application_data: dict | None

    user_decision: str | None

    status: str

    errors: list[str]
```

Keep graph state lightweight.

Do not store unnecessarily large documents directly in graph state.

Store large data in PostgreSQL/object storage and reference it by ID.

---

# 23. AI PROVIDER ARCHITECTURE

Implement a provider abstraction.

Priority:

```text
1. Gemini
2. Groq
3. Fallback Provider
```

Environment variables:

```text
GEMINI_API_KEY=
GROQ_API_KEY=
FALLBACK_API_KEY=
FALLBACK_PROVIDER=
FALLBACK_MODEL=
```

All AI calls happen server-side.

Never expose API keys to the frontend.

---

# 24. LLM FALLBACK

Create a centralized LLM service:

```text
LLM Request
    ↓
Gemini
    │
    ├── SUCCESS → Return
    │
    └── FAILURE
           ↓
         Groq
           │
           ├── SUCCESS → Return
           │
           └── FAILURE
                  ↓
              Fallback
                  │
                  ├── SUCCESS
                  │
                  └── FAILURE → Error
```

Use:

* bounded retries
* short timeouts
* exponential backoff
* provider logging
* usage tracking

Do not retry indefinitely.

---

# 25. BACKEND STACK

Use:

```text
Python
FastAPI
LangGraph
PostgreSQL
SQLAlchemy
Pydantic
```

Redis is optional and should only be added if required.

Do NOT use in V1:

```text
Kafka
Celery
Kubernetes
Multiple backend services
Large local AI models
Permanent browser automation workers
```

The goal is a lightweight backend that can run under severe resource constraints.

---

# 26. RENDER BACKEND

Deploy the backend on:

**Render Web Service**

Target:

```text
0.1 CPU
512 MB RAM
```

The application must be optimized for these constraints.

Use:

* Async FastAPI
* Efficient database queries
* Small connection pools
* Lightweight imports
* Small LangGraph state
* External LLM APIs
* PostgreSQL for persistent state

Avoid:

* Local LLMs
* Large ML models
* Continuous browser processes
* Heavy background workers
* Multiple worker processes
* Unnecessary services

Use:

```text
GET /health
```

for health checks.

---

# 27. FRONTEND

Build a responsive web application.

Recommended:

```text
React
TypeScript
Vite
Tailwind CSS
```

Deploy as a:

**Render Static Site**

The same application must work on:

```text
Mobile browser
Tablet
Desktop
```

Do NOT create a separate native mobile app in V1.

The frontend should feel like a mobile application when accessed from a phone.

---

# 28. FRONTEND PAGES

Implement:

### Dashboard

```text
Jobs Found
High Matches
Ready to Apply
Awaiting Submission
Applied
Interviews
Offers
```

### Opportunities

Ranked opportunity cards.

### Job Details

Show:

* Match score
* Compensation
* Location
* Work mode
* Employment type
* Application method
* Why it matches
* Potential gaps
* AI recommendation

### Applications

Statuses:

```text
Ready
Awaiting Submission
Applied
Interview
Rejected
Offer
```

### Resume

```text
Active Resume
resume.pdf

[VIEW]
[REPLACE]
```

### Preferences

Allow modification of:

* Roles
* Locations
* Work mode
* Employment type
* Compensation
* Minimum match
* Agent authority

---

# 29. DATABASE

Use PostgreSQL.

Minimum tables:

```text
users
resumes
candidate_profiles
user_preferences
agent_policies
job_sources
jobs
job_matches
applications
application_answers
application_events
notifications
agent_runs
```

Requirements:

* One active resume per user.
* Job deduplication.
* Idempotent application operations.
* Valid state transitions.
* Audit trail.
* Source tracking.
* Compensation source tracking.

---

# 30. APPLICATION STATE MACHINE

Implement:

```text
DISCOVERED
    ↓
ANALYZED
    ↓
MATCHED
    ↓
QUALIFIED
    ↓
PREPARING
    ↓
READY
    ↓
USER_APPROVED
    ↓
APPLICATION_HANDOFF
    ↓
AWAITING_SUBMISSION
    ↓
APPLIED
```

Alternative states:

```text
REJECTED
REQUIRES_USER_INPUT
FAILED
INTERVIEW
OFFER
WITHDRAWN
```

The state machine must prevent invalid transitions.

---

# 31. NOTIFICATIONS

Implement in-app notifications first.

Example:

```text
🔔 New 94% Match

AI Engineer Intern
XYZ Technologies

₹25,000/month
Remote
LinkedIn Apply

[Review]
```

Application:

```text
📋 Application Ready

AI Engineer Intern

Resume ✓
Cover Letter ✓
Questions ✓

[Apply]
```

User input:

```text
⚠️ Your Input Required

Question:
Are you willing to relocate?

[Answer]
```

Design the notification layer so push notifications can be added later.

---

# 32. OBSERVABILITY

Every Agent execution must have:

```text
agent_run_id
user_id
job_id
timestamp
status
duration
provider
model
```

Track:

```text
LLM latency
LLM failures
Token usage
Estimated cost
Agent failures
Retries
Job-source failures
Application handoff failures
```

Use structured logging.

Never log API keys.

---

# 33. SECURITY

Implement:

* Authentication
* Authorization
* Password hashing
* Secure resume uploads
* Input validation
* CORS
* Rate limiting
* Secure headers
* Audit logging
* Secret management

Never expose:

```text
GEMINI_API_KEY
GROQ_API_KEY
FALLBACK_API_KEY
```

to the frontend.

---

# 34. COST OPTIMIZATION

The backend is resource-constrained and AI APIs cost money.

Optimize:

```text
Prompt size
LLM calls
Resume parsing
Repeated job analysis
Candidate profile reuse
Database queries
```

Do not repeatedly send the complete resume to the LLM.

Instead:

```text
Resume
 ↓
Parse once
 ↓
Candidate Profile
 ↓
Reuse for matching
```

Cache safe deterministic results.

---

# 35. PROJECT STRUCTURE

Use a clean monorepo:

```text
ai-career-agent/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── agents/
│   │   │   ├── graph/
│   │   │   ├── nodes/
│   │   │   └── state.py
│   │   ├── ai/
│   │   │   ├── providers/
│   │   │   ├── prompts/
│   │   │   └── llm_service.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── integrations/
│   │   │   ├── linkedin/
│   │   │   ├── indeed/
│   │   │   └── glassdoor/
│   │   ├── core/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── agents.md
│   └── deployment.md
│
├── render.yaml
└── README.md
```

---

# 36. TESTING

Implement:

### Unit Tests

* Resume parsing
* Job normalization
* Compensation classification
* Matching
* Policy engine
* Application state machine
* LLM provider fallback
* Application URL generation

### Integration Tests

* FastAPI
* PostgreSQL
* LangGraph
* LLM provider abstraction
* Complete application workflow

### Frontend Tests

* Apply
* Reject
* Mobile responsiveness
* Job cards
* Authentication
* Preferences

---

# 37. RENDER DEPLOYMENT

Provide a working:

```text
render.yaml
```

Configure:

```text
Backend Web Service
Frontend Static Site
PostgreSQL
```

Frontend environment:

```text
VITE_API_URL=
```

Backend:

```text
DATABASE_URL=
SECRET_KEY=
FRONTEND_URL=
CORS_ORIGINS=

GEMINI_API_KEY=
GROQ_API_KEY=
FALLBACK_API_KEY=
FALLBACK_PROVIDER=
FALLBACK_MODEL=
```

Never put secret keys in frontend environment variables.

---

# 38. V1 DEVELOPMENT ORDER

Implement incrementally.

### Phase 1 — Foundation

```text
FastAPI
PostgreSQL
SQLAlchemy
Authentication
```

### Phase 2 — Resume

```text
Upload
Storage
Parsing
Candidate Profile
```

### Phase 3 — AI

```text
Gemini
Groq
Fallback Provider
Structured Outputs
```

### Phase 4 — LangGraph

```text
State
Nodes
Graph
Conditional Routing
Human-in-the-loop
```

### Phase 5 — Job Intelligence

```text
Job Schema
Normalization
Compensation
Application Method
Matching
Policy
```

### Phase 6 — Application

```text
Preparation
Apply
Reject
Handoff
Tracking
```

### Phase 7 — Frontend

```text
Dashboard
Opportunities
Job Details
Apply/Reject
Applications
Resume
Preferences
```

### Phase 8 — Deployment

```text
Render Backend
Render Frontend
PostgreSQL
Environment Variables
CORS
Health Checks
```

### Phase 9 — Testing

Optimize for:

```text
0.1 CPU
512 MB RAM
```

---

# 39. V1 SUCCESS CRITERIA

A V1 is complete when a user can:

```text
1. Register
        ↓
2. Upload one resume
        ↓
3. Configure job preferences
        ↓
4. Start the Agent
        ↓
5. Agent discovers jobs
        ↓
6. Agent identifies supported Apply flows
        ↓
7. Agent analyzes jobs
        ↓
8. Agent determines compensation
        ↓
9. Agent matches jobs against resume
        ↓
10. Agent filters according to preferences
        ↓
11. Agent prepares application
        ↓
12. User receives opportunity
        ↓
13. User taps APPLY
        ↓
14. Original LinkedIn/Indeed/Glassdoor
    application page opens
        ↓
15. User completes application
        ↓
16. Application can be tracked
```

The user can also:

```text
REJECT
```

any opportunity at any time.

---

# 40. FINAL PRODUCT PRINCIPLE

The product is NOT:

> "A bot that applies to hundreds of jobs."

It is:

> **"An AI Career Agent that continuously finds the right jobs for me, understands them, filters them according to my preferences, tells me whether they are paid or unpaid, explains why I'm a good match, prepares my application, and takes me directly to the correct application page."**

Architecture principles:

```text
Mobile/Desktop Frontend
        ↓
FastAPI
        ↓
LangGraph
        ↓
AI Intelligence
        ↓
PostgreSQL
```

AI provider:

```text
Gemini
  ↓ fallback
Groq
  ↓ fallback
Configured API Provider
```

Deployment:

```text
Render Frontend
+
Render Backend
+
Render PostgreSQL
```

Backend constraint:

```text
0.1 CPU
512 MB RAM
```

V1 application model:

```text
AI PREPARES
      ↓
USER APPROVES
      ↓
OPEN ORIGINAL PLATFORM
      ↓
USER SUBMITS
```

Build V1 as a **real, maintainable SaaS product**, not a demo.

Prioritize correctness, security, low resource consumption, explainability, modularity, and platform compliance.

Before implementation, first produce:

1. System architecture
2. LangGraph architecture
3. Database ERD
4. API specification
5. Application state machine
6. AI provider abstraction
7. Platform integration abstraction
8. Security architecture
9. Render deployment architecture
10. Complete V1 implementation plan

Then implement the system incrementally.

# ADDITIONAL V1 REQUIREMENTS

## Scheduled Agent Execution, API Quotas & Resource Management

Add the following requirements to the existing AI Career Application Agent V1 specification.

---

# 1. NO CONTINUOUS PLATFORM POLLING

The Agent must NOT continuously run or continuously poll LinkedIn, Indeed, or Glassdoor.

Do NOT implement:

```text
while True:
    search_platform()
    sleep()
```

Do NOT maintain a permanently running discovery loop.

Job discovery must be **scheduled and bounded**.

The system should execute discovery jobs at configured intervals and terminate/return to an idle state after processing.

---

# 2. SCHEDULED JOB DISCOVERY

Use scheduled execution for job discovery.

Recommended initial V1 frequency:

```text
Every 30–60 minutes
```

The exact frequency must be configurable.

Architecture:

```text
Render Cron
      ↓
Discovery Scheduler
      ↓
Find users whose next_check_at <= NOW()
      ↓
Process eligible users
      ↓
Discover jobs
      ↓
Process jobs
      ↓
Update next_check_at
      ↓
Execution ends
```

Do NOT create a separate cron job per user.

Use one centralized scheduler.

---

# 3. USER-SPECIFIC SCHEDULING

Store scheduling information per user:

```text
last_checked_at
next_check_at
discovery_interval
agent_enabled
```

Example:

```text
User A
30-minute interval

User B
2-hour interval

User C
Daily interval
```

The scheduler should only process users whose:

```text
next_check_at <= current_time
```

This prevents unnecessary platform requests.

---

# 4. RENDER RESOURCE CONSTRAINT

The backend is deployed on:

```text
CPU: 0.1
RAM: 512 MB
```

Therefore the system must be designed as a **lightweight, event-driven, scheduled service**.

Avoid:

```text
Permanent worker processes
Multiple backend workers
Large in-memory queues
Local LLMs
Large embedding models
Permanent browser instances
Selenium servers
Playwright servers
Kafka
Celery
Kubernetes
```

Use external APIs for AI processing.

Persist important state in PostgreSQL.

Keep LangGraph state lightweight.

---

# 5. RENDER CRON ARCHITECTURE

Use a Render Cron Job for scheduled discovery where appropriate.

Conceptually:

```text
                 RENDER CRON
                     │
              Every 30–60 min
                     │
                     ▼
             DISCOVERY RUN
                     │
                     ▼
          SELECT ELIGIBLE USERS
                     │
                     ▼
              DISCOVER JOBS
                     │
                     ▼
           DEDUPLICATE / FILTER
                     │
                     ▼
              LANGGRAPH RUN
                     │
                     ▼
              STORE RESULTS
                     │
                     ▼
             UPDATE SCHEDULE
                     │
                     ▼
                    END
```

The discovery execution must be bounded and safe to terminate.

---

# 6. PLATFORM REQUEST BUDGET

Implement a centralized request-budget mechanism.

Track requests per:

```text
Platform
User
Time window
Job source
```

For example:

```text
platform_request_usage

platform
user_id
window_start
request_count
last_request_at
```

Before making a platform request:

```text
Check budget
      ↓
Within allowed limit?
   ┌──┴──┐
   YES   NO
    │     │
    ▼     ▼
 Request  Skip / Delay
```

Never intentionally exceed known platform limits.

Platform-specific limits must be configurable rather than hardcoded.

---

# 7. RATE LIMITING

Every platform adapter must implement rate limiting.

Example abstraction:

```python
class RateLimiter:

    async def acquire(
        self,
        platform: str,
        user_id: str
    ) -> bool:
        ...
```

Support:

```text
Requests per minute
Requests per hour
Requests per day
Minimum delay between requests
```

If a platform returns a rate-limit response:

```text
429 / equivalent
```

the system must:

1. Stop additional requests for that platform/user.
2. Record the event.
3. Apply exponential backoff.
4. Reschedule the operation.
5. Never attempt to bypass the limit.

---

# 8. LLM QUOTA MANAGEMENT

Implement a centralized LLM usage manager.

Providers:

```text
Gemini
   ↓
Groq
   ↓
Fallback Provider
```

Track:

```text
provider
model
user_id
request_count
input_tokens
output_tokens
timestamp
status
estimated_cost
```

Before every LLM request:

```text
LLM Request
     ↓
Quota Manager
     ↓
Is provider available?
     │
 ┌───┴────┐
 YES      NO
 │         │
 ▼         ▼
Gemini    Groq
           │
           ▼
        Fallback
```

The system must respect configured provider quotas.

Do not make unlimited retries.

---

# 9. LLM REQUEST BUDGETS

Implement configurable limits:

```text
MAX_LLM_REQUESTS_PER_RUN
MAX_LLM_REQUESTS_PER_USER_PER_DAY
MAX_LLM_TOKENS_PER_USER_PER_DAY
MAX_RETRIES_PER_REQUEST
```

These must be environment/configuration values.

Example:

```text
MAX_LLM_REQUESTS_PER_RUN=100
MAX_LLM_REQUESTS_PER_USER_PER_DAY=500
MAX_RETRIES_PER_REQUEST=2
```

Use sensible defaults, but make them configurable.

Do not hardcode provider-specific limits because those can change.

---

# 10. SMART LLM USAGE

Do NOT send every discovered job to an LLM.

Use a multi-stage filtering pipeline.

```text
1000 Jobs
    ↓
Deduplication
    ↓
Deterministic Filtering
    ↓
500
    ↓
Cheap metadata filtering
    ↓
150
    ↓
LLM Job Analysis
    ↓
80
    ↓
Semantic Matching
    ↓
30
    ↓
Deep Application Analysis
    ↓
10
```

Use deterministic filtering before expensive AI calls.

---

# 11. DO NOT REPROCESS JOBS

Store:

```text
job_hash
source_job_id
last_analyzed_at
content_hash
analysis_version
```

Before calling an LLM:

```text
Is this job already analyzed?
        │
    ┌───┴───┐
   YES      NO
    │        │
   SKIP    ANALYZE
```

If the job description has not changed, do not re-analyze it unnecessarily.

If the job changes significantly:

```text
content_hash changed
        ↓
Re-analyze
```

---

# 12. CANDIDATE PROFILE CACHING

Parse the user's resume once.

```text
Resume
  ↓
Candidate Profile
  ↓
Store in PostgreSQL
```

Do NOT send the original resume to the LLM for every job.

Use the structured candidate profile for matching.

Only re-parse when:

```text
User replaces resume
```

---

# 13. LANGGRAPH EXECUTION MODEL

LangGraph must be executed **on demand**, not as a permanently running agent.

Example:

```text
Render Cron
     ↓
Start LangGraph
     ↓
Process job
     ↓
Save checkpoint/state
     ↓
Finish
```

For user approval:

```text
Application Ready
       ↓
LangGraph Interrupt
       ↓
Persist checkpoint/state
       ↓
Process can terminate
       ↓
User taps APPLY
       ↓
Resume graph
```

Do not keep a Python process alive waiting for user input.

---

# 14. HUMAN-IN-THE-LOOP CHECKPOINT

When an application reaches:

```text
APPLICATION_READY
```

pause the graph.

Store:

```text
thread_id
graph_state_id
user_id
job_id
application_id
status
```

Set:

```text
status = WAITING_FOR_USER
```

When the user taps:

```text
APPLY
```

resume the appropriate workflow.

When the user taps:

```text
REJECT
```

terminate the workflow.

---

# 15. SCHEDULER SAFETY

The scheduler must be idempotent.

If two scheduler executions accidentally overlap, the same user/job must not be processed twice.

Use database-level protection such as:

```text
execution_lock
unique constraints
idempotency keys
```

Example:

```text
user_id + job_id + analysis_version
```

must not generate duplicate processing.

---

# 16. JOB DEDUPLICATION

The same job can appear on multiple platforms.

Example:

```text
LinkedIn
AI Engineer Intern
XYZ Technologies

Indeed
AI Engineer Intern
XYZ Technologies

Glassdoor
AI Engineer Intern
XYZ Technologies
```

Attempt to identify the same underlying opportunity.

Use:

```text
source_job_id
company
normalized_title
location
description_hash
```

to create a canonical job record.

The user should not receive three notifications for the same job.

---

# 17. NOTIFICATION THROTTLING

Do not send a notification for every discovered job.

Only notify when:

```text
Match score >= user threshold
AND
Application method is supported
AND
Policy conditions pass
AND
Job has not already been notified
```

Optional configurable notification limits:

```text
MAX_NOTIFICATIONS_PER_USER_PER_DAY
```

Group multiple opportunities where appropriate.

Example:

```text
🔔 5 New Opportunities

3 AI Engineer
2 Backend Engineer

Highest Match: 96%

[View Opportunities]
```

---

# 18. ADAPTIVE DISCOVERY

Design the scheduler so V1 can later support adaptive intervals.

Possible future logic:

```text
High-priority user
→ Every 30 min

Normal user
→ Every 2 hours

Low activity
→ Every 6–24 hours
```

Do not implement complex adaptive scheduling unless required for V1.

The architecture should simply support it.

---

# 19. FAILURE AND BACKOFF

For platform/API failures:

```text
Request
  ↓
Failure
  ↓
Retry 1
  ↓
Retry 2
  ↓
Backoff
  ↓
Reschedule
```

Use exponential backoff with jitter.

Do not retry indefinitely.

For repeated failures:

```text
PLATFORM_TEMPORARILY_UNAVAILABLE
```

Store the failure and wait until the next scheduled execution.

---

# 20. DAILY RESOURCE BUDGET

Maintain a system-level resource budget.

Track:

```text
Platform Requests
LLM Requests
LLM Tokens
Database Queries where practical
Notifications
Agent Runs
```

The system should be able to answer:

```text
How many platform requests did we make today?

How many Gemini requests?

How many Groq requests?

How many fallback requests?

How many LLM tokens?

How many jobs were analyzed?

How many jobs were skipped?
```

This should be available through an internal/admin endpoint or dashboard.

---

# 21. PROVIDER FALLBACK MUST NOT CREATE DUPLICATE WORK

Important:

If Gemini times out after potentially processing the request, blindly retrying with Groq could result in duplicate LLM usage.

Use request IDs/idempotency where supported.

At minimum:

```text
Generate internal request_id
Track provider attempt
Track request status
```

Example:

```text
request_id = llm_req_8291

Gemini
→ TIMEOUT

System
→ record Gemini attempt

Groq
→ fallback
```

The system should know that the fallback is part of the same logical AI operation.

---

# 22. MODEL SELECTION

Do not use the most expensive model for every operation.

Define task-level model configuration:

```text
Resume parsing
→ efficient model

Job classification
→ efficient model

Compensation extraction
→ efficient model

Matching
→ stronger model when required

Application writing
→ stronger model
```

Models must be configurable through environment variables.

Example:

```text
GEMINI_MODEL=
GROQ_MODEL=
FALLBACK_MODEL=
```

---

# 23. RESOURCE-AWARE CONCURRENCY

Because the backend has only:

```text
0.1 CPU
512 MB RAM
```

do NOT process hundreds of jobs concurrently.

Use a small configurable concurrency limit.

Example:

```text
MAX_CONCURRENT_JOBS=2
```

The exact value should be configurable.

Prefer:

```text
Async I/O
+
Small concurrency
+
Batch processing
```

over large parallel workloads.

---

# 24. BATCH PROCESSING

Where possible, process lightweight operations in batches.

Example:

```text
Fetch jobs
    ↓
Normalize batch
    ↓
Deduplicate
    ↓
Filter
    ↓
Process small AI batches
```

Do not create one process/thread per job.

Avoid memory-heavy queues.

---

# 25. DATABASE AS SOURCE OF TRUTH

Do not rely on:

```text
Python memory
Redis memory
LangGraph in-memory state
```

for critical application state.

PostgreSQL must contain:

```text
User
Resume
Candidate Profile
Job
Match
Application
Agent Run
Scheduler State
LLM Usage
Platform Usage
```

LangGraph checkpoints should be persistent.

---

# 26. V1 EXECUTION MODEL

The final V1 architecture should operate like this:

```text
                 RENDER CRON
              Every 30–60 min
                     │
                     ▼
            DISCOVERY SCHEDULER
                     │
                     ▼
        Users whose next_check_at <= NOW
                     │
                     ▼
             PLATFORM DISCOVERY
                     │
                     ▼
               RATE LIMITER
                     │
                     ▼
             JOB NORMALIZATION
                     │
                     ▼
              DEDUPLICATION
                     │
                     ▼
        DETERMINISTIC FILTERING
                     │
                     ▼
              NEW JOBS ONLY
                     │
                     ▼
                LANGGRAPH
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     ANALYSIS    COMPENSATION   MATCHING
        └────────────┼────────────┘
                     ▼
                 POLICY
                     │
                     ▼
          APPLICATION PREPARATION
                     │
                     ▼
                READY
                     │
                     ▼
              📱 NOTIFICATION
                     │
                     ▼
            WAIT FOR USER
                     │
              ┌──────┴──────┐
              ▼             ▼
            APPLY         REJECT
              │             │
              ▼             ▼
         APPLICATION       END
           HANDOFF
              │
              ▼
     ORIGINAL PLATFORM
              │
              ▼
       USER COMPLETES
       FINAL APPLICATION
```

---

# 27. IMPORTANT V1 PRINCIPLE

The Agent should be **event-driven and scheduled, not continuously polling**.

The Agent should consume resources only when it has work to perform.

The desired model is:

```text
Wake
 ↓
Discover
 ↓
Process
 ↓
Notify
 ↓
Persist
 ↓
Sleep/Terminate
```

not:

```text
Start Agent
 ↓
Run Forever
 ↓
Continuously Poll
```

---

# 28. FINAL RESOURCE OBJECTIVE

The V1 system must be designed so that:

```text
Render Backend
0.1 CPU
512 MB RAM
```

is sufficient for normal V1 workloads.

The system must scale through:

```text
Scheduling
Database persistence
Controlled concurrency
External LLM APIs
Efficient filtering
Caching
Rate limiting
Batching
```

rather than by keeping large processes running.

The architecture must make it possible to increase resources later without changing the fundamental Agent design.
