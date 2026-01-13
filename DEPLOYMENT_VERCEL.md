# Deploying to Vercel

⚠️ **Warning**: Vercel is not ideal for Django applications. Consider using **Railway** or **Render** instead for a better experience.

## Quick Setup for Vercel

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Environment Variables** in Vercel Dashboard:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.vercel.app`
   - `STRIPE_SECRET_KEY`
   - `STRIPE_PUBLISHABLE_KEY`
   - `DATABASE_URL` (use external database like Supabase or Railway PostgreSQL)

5. **Important Limitations**:
   - Media files won't persist (use AWS S3 or Cloudinary)
   - Database connections may timeout (use connection pooling)
   - Some Django features may not work in serverless environment

## Better Alternatives

- **Railway**: https://railway.app (Recommended - easiest for Django)
- **Render**: https://render.com (Free tier available)
- **Heroku**: https://heroku.com (Classic, paid plans)
