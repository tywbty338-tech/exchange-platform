#!/bin/bash
# ==============================
# رفع المشروع على GitHub يدوياً
# شغّل هذا السكريبت على جهازك
# ==============================

# 1. تأكد إنك مسجّل دخول GitHub
# افتح: https://github.com/new

# 2. أنشئ repo جديد:
#    Name: exchange-platform
#    Description: Premium Telegram Exchange Mini App
#    Public
#    ❌ لا تفعّل Add README

# 3. شغّل الأوامر التالية:

cd /public/.cache/exchange-platform

# إذا ما عندك المشروع محلي، نزّله من السيرفر أو انسخ المجلد

git init
git branch -M main
git add -A
git commit -m "Exchange Platform v1.0"

# غيّر YOUR_USERNAME باسم حسابك
git remote add origin https://github.com/YOUR_USERNAME/exchange-platform.git

# هذا السطر يطلب كلمة مرور GitHub
# استخدم التوكن بدلاً من كلمة المرور
git push -u origin main

# ==============================
# عند الإدخال:
# Username: YOUR_USERNAME
# Password: (التوكن ghp_xxxxx)
# ==============================
