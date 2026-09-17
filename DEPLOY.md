# Deploy to Railway (مجاني $5 شهرياً)

## الخطوة 1: أنشئ حساب Railway

1. افتح https://railway.app
2. سجل بحساب GitHub أو Email

## الخطوة 2: ارفع المشروع على GitHub

```bash
cd /public/.cache/exchange-platform
git init
git add .
git commit -m "Exchange Platform v1"
```

أو أنشئ repo جديد على GitHub وارفع الملفات.

## الخطوة 3: أنشئ مشروع على Railway

1. اضغط "New Project"
2. اختر "Deploy from GitHub Repo"
3. اختر repo المشروع

## الخطوة 4: أضف PostgreSQL

1. داخل المشروع اضغط "+" 
2. اختر "Database" → "PostgreSQL"
3. Railway يعطيك DATABASE_URL تلقائياً

## الخطوة 5: أضف Environment Variables

اذهب到 Variables واضف:

```
BOT_TOKEN=8693832759:AAGqIc11Eb4ylU7XTxiuO40sPwRG6JGMU5Q
ADMIN_IDS_RAW=8550715795
DATABASE_URL=${{Postgres.DATABASE_URL}}
TEST_MODE=true
PAYMENT_PROVIDER=mock
JWT_SECRET=اكتب_نص_عشوائي_طويل_هنا
WEBAPP_URL=
```

## الخطوة 6: Webhook

بمجرد نشر المشروع:

```
https://your-project.up.railway.app
```

اضغط "Settings" → "Networking" → "Generate Domain"

حتى تحصل على رابط مثل:
```
https://exchange-bot-production.up.railway.app
```

ثم عيّن WEBAPP_URL في المتغيرات.

---

# Deploy to Render (مجاني)

## الخطوة 1: ارفع على GitHub

## الخطوة 2: أنشئ Web Service على Render

1. افتح https://render.com
2. سجل حساب
3. اضغط "New" → "Web Service"
4. اختر GitHub Repo

## الخطوة 3: الإعدادات

- **Name**: exchange-bot
- **Runtime**: Python
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && python main.py`
- **Instance Type**: Free

## الخطوة 4: Environment Variables

```
BOT_TOKEN=8693832759:AAGqIc11Eb4ylU7XTxiuO40sPwRG6JGMU5Q
ADMIN_IDS_RAW=8550715795
DATABASE_URL=sqlite+aiosqlite:///./exchange.db
TEST_MODE=true
PAYMENT_PROVIDER=mock
JWT_SECRET=اكتب_نص_عشوائي_طويل
WEBAPP_URL=https://exchange-bot.onrender.com
```

---

# Deploy to VPS (أفضل خيار)

## تحتاج:
- VPS (DigitalOcean $4/أو AWS Lightsail)
- Node.js
- Python 3.12

## الخطوات:

```bash
# 1. اتصل بالـ VPS
ssh root@your-vps-ip

# 2. نزّل Python
apt update && apt install -y python3.12 python3.12-venv git

# 3. انسخ المشروع
git clone https://github.com/your/repo.git
cd exchange-platform

# 4. أنشئ بيئة افتراضية
python3.12 -m venv venv
source venv/bin/activate

# 5. نزّل المتطلبات
pip install -r backend/requirements.txt

# 6. اضبط .env
cp backend/.env backend/.env.production
nano backend/.env.production

# 7. شغّل
cd backend
nohup python main.py > exchange.log 2>&1 &

# 8. لتشغيل تلقائي عند إعادة التشغيل
# أنشئ systemd service
```

## systemd Service:

```bash
cat > /etc/systemd/system/exchange.service << 'EOF'
[Unit]
Description=Exchange Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/exchange-platform/backend
ExecStart=/root/exchange-platform/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable exchange
systemctl start exchange
```

## Nginx + SSL:

```bash
apt install -y nginx certbot python3-certbot-nginx

cat > /etc/nginx/sites-available/exchange << 'EOF'
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/exchange /etc/nginx/sites-enabled/
certbot --nginx -d your-domain.com
systemctl restart nginx
```

---

# ملاحظات مهمة

## Telegram BotFather

1. أرسل `/setmenubutton` لـ @BotFather
2. اختر بوتك
3. أدخل رابط Mini App:
   ```
   https://your-domain.com
   ```

## BotFather Settings

1. أرسل `/mybots`
2. اختر البوت
3. Bot Settings → Menu Button
4. أدخل URL الـ Mini App

## تغيير الأسعار

```bash
# عبر API
curl -X PUT https://your-domain.com/api/admin/rates/USDT/TRC20 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"rate": 0.000750}'
```

## التحقق من التشغيل

```bash
# Health Check
curl https://your-domain.com/api/health

# Rates
curl https://your-domain.com/api/rates
```
