# Exchange Platform — Premium Telegram Fintech Mini App

منصة صرافة رقمية احترافية داخل Telegram.

## المميزات

- 🚀 **Telegram Mini App** — واجهة فانتيش قيادية
- 💱 **أسعار LIVE** — سعر الصرف كبطل للمنتج
- 🧮 **محاسبة ذكية** — اقتراحات سعرية مع عد تنازلي
- 💳 **نظام دفع** — Mock / Manual / AsiaCell
- 🔒 **أمان** — لا نخزن OTP/PIN/Seed Phrase
- 👨‍💻 **لوحة تحكم** — Admin Dashboard
- 📱 **تصميم Responsive** — يعمل على جميع الشاشات

## الهيكل

```
exchange-platform/
├── backend/           # Python FastAPI + aiogram
│   ├── app/
│   │   ├── api/       # REST API endpoints
│   │   ├── bot/       # Telegram bot
│   │   ├── core/      # Config, database
│   │   ├── database/  # Models, repositories
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   └── tests/
├── frontend/          # React + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── services/
│   │   └── types/
│   └── dist/
├── docker-compose.yml
└── README.md
```

## التثبيت

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up -d
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram Bot Token | - |
| `DATABASE_URL` | PostgreSQL URL | sqlite+aiosqlite:///./exchange.db |
| `ADMIN_IDS_RAW` | Admin Telegram IDs | - |
| `WEBAPP_URL` | Mini App URL | - |
| `JWT_SECRET` | JWT secret key | - |
| `TEST_MODE` | Test mode | true |
| `PAYMENT_PROVIDER` | mock/manual/asiacell | mock |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/rates` | Get exchange rates |
| POST | `/api/quotes` | Create a quote |
| GET | `/api/quotes/{id}` | Get quote |
| POST | `/api/orders` | Create order |
| GET | `/api/orders` | List orders |
| GET | `/api/orders/{id}` | Get order |
| POST | `/api/orders/{id}/wallet` | Set wallet |
| POST | `/api/orders/{id}/confirm` | Confirm order |
| GET | `/api/wallets` | List wallets |
| POST | `/api/wallets` | Add wallet |
| DELETE | `/api/wallets/{id}` | Delete wallet |
| GET | `/api/admin/stats` | Admin stats |
| GET | `/api/admin/rates` | Admin rates |
| PUT | `/api/admin/rates/{c}/{n}` | Update rate |

## الاختبارات

```bash
cd backend
python -m pytest tests/ -v
```

## تغيير الأسعار

### عبر API (Admin)
```bash
curl -X PUT http://localhost:8000/api/admin/rates/USDT/TRC20 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"rate": 0.000750}'
```

### عبر البوت (Admin)
أرسل: `👨‍💻 لوحة الإدارة` → `💱 أسعار الصرف` → اختر العملة

## ربط Telegram Mini App

1. أرسل `/setmenubutton` لـ @BotFather
2. اختر البوت
3. أدخل رابط Mini App

## للإنتاج

1. غيّر `TEST_MODE=false`
2. أضف `JWT_SECRET` قوي
3. استخدم PostgreSQL
4. فعّل HTTPS
5. أضف Admin IDs في `ADMIN_IDS_RAW`

## الترخيص

MIT
