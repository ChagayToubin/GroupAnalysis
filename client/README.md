הרמת צד לקוח (React + Vite) — מדריך קצר
1) בדוק שיש Node ו־npm (ב־Terminal של PyCharm)
node -v
npm -v


צריך Node ≥ 20.19 (או 22 LTS). אם הגרסה נמוכה, התקן Node LTS מחדש ופתח את PyCharm שוב.

2 ) התקנת תלויות והרצה
npm install
copy .env.example .env
notepad .env


בחלון שנפתח ודא שיש:

VITE_API_BASE=http://localhost:8000


סגור את הקובץ ואז:

npm run dev


פתח בדפדפן:
http://localhost:5173/