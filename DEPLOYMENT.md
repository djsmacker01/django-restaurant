# Deployment Guide

## 🚀 Deploy to Railway (Recommended - Easiest)

Railway is the easiest platform for deploying Django apps.

### Steps:

1. **Sign up at Railway**: https://railway.app
2. **Connect your GitHub repository**
3. **Add a PostgreSQL database**:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set `DATABASE_URL` environment variable
4. **Set environment variables** in Railway dashboard:
   ```
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   STRIPE_SECRET_KEY=sk_live_your_live_stripe_key
   STRIPE_PUBLISHABLE_KEY=pk_live_your_live_stripe_key
   SITE_ID=1
   ```
5. **Deploy**: Railway will automatically detect Django and deploy!

That's it! Your app will be live at `https://your-app-name.railway.app`

---

## 🌐 Deploy to Render

1. **Sign up at Render**: https://render.com
2. **Create a new Web Service** and connect your GitHub repo
3. **Settings**:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn flavour.wsgi:application`
4. **Add PostgreSQL database** (free tier available)
5. **Set environment variables** (same as Railway above)
6. **Deploy!**

---

## ⚠️ Deploy to Vercel (Not Recommended)

Vercel is designed for serverless functions, not full Django apps. It requires significant modifications and has limitations:

- No persistent file storage (media files won't work)
- Database connections can timeout
- Some Django features may not work

If you still want to try:

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Set environment variables in Vercel dashboard
4. You'll need to use external storage (AWS S3) for media files

**I strongly recommend Railway or Render instead!**

---

## 📋 Pre-Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Generate a new `SECRET_KEY` for production
- [ ] Set up PostgreSQL database
- [ ] Configure Stripe live keys (not test keys)
- [ ] Set up email backend (SMTP) for production
- [ ] Run `python manage.py collectstatic`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

---

## 🔧 Post-Deployment

1. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Load sample data** (optional):
   ```bash
   python manage.py create_sample_data --full
   ```

---

## 💡 Tips

- Use Railway for the easiest deployment experience
- Always use environment variables for secrets
- Set up a PostgreSQL database (don't use SQLite in production)
- Use Stripe live keys in production
- Configure proper email backend for user registration emails
