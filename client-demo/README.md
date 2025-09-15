# React Processing Client (No Auth, Manual Status Check)

צד לקוח מינימליסטי ב-React עבור זרימת עיבוד:
- טופס עם שני שדות (A: טקסט יחיד, B: כמה טקסטים)
- שליחה לשרת (`/api/process/start`) וקבלת `requestId`
- כפתור "הצג תוצאות" ששואל את השרת (`/api/process/status`)
- אם בעיבוד — מציג סטטוס
- אם מוכן — מציג גרף עמודות של `results.metrics`

## דרישות מוקדמות
- Node.js LTS + npm מותקן (בדיקה: `node -v` ו-`npm -v`)

## התקנה והרצה (PowerShell, צעד-אחר-צעד)
1) התקנת תלויות:
```powershell
npm install
```
2) יצירת קובץ .env מקומי והגדרת כתובת השרת שלך:
```powershell
Copy-Item .env.example .env
# ערוך את .env אם צריך; ברירת מחדל מצביע ל- http://localhost:8000
```
3) הרצה לפיתוח:
```powershell
npm run dev
```
הלקוח יפתח בדפדפן (ברירת מחדל: http://localhost:5173).  
אם השרת לא באותה כתובת/פורט, עדכן את `VITE_API_BASE` ב-`.env`.

## מבנה API שמצופה מהשרת
- **POST** `${VITE_API_BASE}/api/process/start`
  - Body:
    ```json
    { "text": "string", "texts": ["string"] }
    ```
  - Response (202):
    ```json
    { "requestId": "123e4567", "status": "queued" }
    ```
- **GET** `${VITE_API_BASE}/api/process/status?requestId=123e4567`
  - Processing:
    ```json
    { "requestId": "123e4567", "status": "processing", "progress": 42 }
    ```
  - Ready:
    ```json
    {
      "requestId": "123e4567",
      "status": "ready",
      "results": { "metrics": [ { "name": "scoreA", "value": 0.83 } ] }
    }
    ```
  - Error:
    ```json
    { "requestId": "123e4567", "status": "error", "message": "processing failed" }
    ```

## הסברים מהירים על קבצים חשובים
- `src/app/api.js` — פונקציות `startProcess` ו-`getStatus`, קוראות לשרת.
- `src/app/storage.js` — שמירת וקריאת `requestId` מ-LocalStorage.
- `src/features/processing/pages/ProcessingPage.jsx` — מרכיב את כל הזרימה (טופס, סטטוס, גרף).
- `src/features/processing/components/InputForm.jsx` — איסוף A+B עם ולידציה.
- `src/features/processing/components/ResultActions.jsx` — הצגת מזהה/סטטוס וכפתור "הצג תוצאות".
- `src/features/processing/components/Chart.jsx` — גרף עמודות פשוט (SVG).
- `src/shared/components/Spinner.jsx` / `Alert.jsx` — מצבי טעינה והודעות.

## Build לייצור
```powershell
npm run build; npm run preview
```
`npm run preview` ידמה סרבר סטטי לבדיקת הבילד.

---
♥ בהמשך אפשר להוסיף:
- בחירת סוג גרף
- Polling אוטומטי (כיבוי/הדלקה)
- i18n מלא
- עיצוב מתקדם / Tailwind