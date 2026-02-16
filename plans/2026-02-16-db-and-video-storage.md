# Database & Video Storage Decisions

**Datum:** 2026-02-16
**Prompt:** Database choice (SQLite vs PostgreSQL) and video storage for ~30k videos

## 1. Database: SQLite vs PostgreSQL

### Current Setup
- SQLite (`database.db`) - single file, zero config
- Works fine for development and small-scale apps

### When SQLite is Enough
- 4-8 coaches, small number of athletes
- Read-heavy workload (browsing videos, categories)
- Single-server deployment
- No concurrent heavy writes

### When to Switch to PostgreSQL
- Deploying to a cloud server (Render, Railway, etc.) - SQLite doesn't work well with ephemeral filesystems
- Need concurrent writes from multiple coaches at the same time
- Want full-text search, JSON operators, or advanced queries
- Planning to scale beyond a single server

### Migration Effort
- **Low** - SQLModel/SQLAlchemy abstracts the DB
- Change `DATABASE_URL` from `sqlite:///database.db` to `postgresql://user:pass@host/db`
- Install `psycopg2` (PostgreSQL driver)
- Minor syntax differences (e.g., auto-increment)
- Run `create_db_and_tables()` on the new DB

### Recommendation
- **Stay with SQLite for now** (development + testing)
- **Switch to PostgreSQL when deploying to production** - most cloud platforms (Render, Railway, Supabase) offer free/cheap PostgreSQL
- The migration is minimal since we use SQLModel

---

## 2. Video Storage (~30k Videos)

### Current Setup
- Videos on Vimeo (paid hosting)
- Local file storage via `storage.py` (for development)

### Storage Options Comparison

| Provider | Free Tier | Storage Cost | Bandwidth Cost | Best For |
|----------|-----------|-------------|----------------|----------|
| **Cloudflare R2** | 10 GB/month | $0.015/GB | **Free egress** | Best overall value |
| **Backblaze B2** | 10 GB | $0.006/GB | $0.01/GB (free via CF) | Cheapest raw storage |
| **AWS S3** | 5 GB (12 months) | $0.023/GB | $0.09/GB | Enterprise standard |
| **Google Cloud Storage** | 5 GB | $0.020/GB | $0.12/GB | GCP ecosystem |
| **Vimeo Pro** | - | $20/month (plan) | Included | Player + streaming |

### Cost Estimate for 30k Videos

Assuming average 50 MB per video = ~1.5 TB total storage:

| Provider | Monthly Storage | Monthly Bandwidth (est. 500 GB) | Total/Month |
|----------|----------------|--------------------------------|-------------|
| **Cloudflare R2** | ~$22.50 | $0 (free!) | ~$22.50 |
| **Backblaze B2** | ~$9 | $0 (via Cloudflare) | ~$9 |
| **B2 + Cloudflare** | ~$9 | $0 | ~$9 |
| **AWS S3** | ~$34.50 | ~$45 | ~$79.50 |
| **Vimeo Pro** | $20 flat | Included | $20 |

### Recommendation

**Option A: Stay on Vimeo** (if already paying and using their player)
- Pros: Built-in video player, adaptive streaming, no migration needed
- Cons: $20+/month, locked into their platform

**Option B: Cloudflare R2** (best value for self-hosting)
- Pros: Zero egress fees, S3-compatible API, global CDN
- Cons: No built-in video player (need to use HTML5 video or a JS player)

**Option C: Backblaze B2 + Cloudflare CDN** (cheapest)
- Pros: Cheapest storage, free bandwidth through Cloudflare
- Cons: More complex setup, two services to manage

### Migration Plan (when ready)
1. Choose provider (R2 recommended)
2. Create bucket with organized folder structure (category/subcategory/video)
3. Upload existing videos (bulk migration script)
4. Update `storage.py` to use S3-compatible SDK (`boto3`)
5. Update Video model to store cloud URL instead of local path
6. Serve videos through signed URLs (time-limited access)

---

## 3. Email Sending (Training Sessions to Athletes)

### Use Case
- Coach creates a new training session
- Coach selects athletes to notify
- App sends an email with training details (exercises, videos, schedule)

### Options

| Approach | Free Tier | Cost After | Complexity |
|----------|-----------|------------|------------|
| **Resend** | 3,000 emails/month | $20/month for 50k | Low - simple API |
| **SMTP (Gmail)** | 500/day | Free (with limits) | Low - built-in Python |
| **SendGrid** | 100/day | $20/month for 50k | Medium |
| **AWS SES** | 3,000/month (EC2) | $0.10/1,000 emails | Medium |
| **Mailgun** | 1,000/month (trial) | $35/month | Medium |

### Recommendation
For 4-8 coaches sending training to their athletes:
- **Start with SMTP (Gmail)** - zero cost, Python has built-in `smtplib`
- **Upgrade to Resend** if you need better deliverability or templates

### Implementation Plan
1. Create `EmailService` in backend
2. Add email template for training sessions (HTML)
3. Add `POST /training-session` endpoint that creates session + sends emails
4. Store email sending config in `.env` (SMTP host, credentials)
5. Consider background task (FastAPI `BackgroundTasks`) so API doesn't block while sending

### Backend Code (SMTP approach)
```python
# email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_training_email(to_email: str, athlete_name: str, training_details: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = "New Training Session"
    msg.attach(MIMEText(training_details, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
```

---

## Priority Order
1. **Frontend login form** (NOW) - backend is ready
2. **Email sending** (after core app works) - start with SMTP
3. **PostgreSQL migration** (when deploying) - minimal effort
4. **Video storage migration** (when Vimeo costs become a concern) - bigger project
