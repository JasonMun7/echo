# Echo

Next.js frontend + FastAPI backend with Firebase Auth, Firestore, and Google Cloud Storage.

## Project Structure

```
├── frontend/           # Next.js app (Firebase Auth, Firestore)
│   └── DESIGN_SYSTEM.md  # Design system - follow for all UI work
├── backend/            # FastAPI app (Firebase Admin, GCS)
```

## Prerequisites

- Node.js 18+
- Python 3.11+
- Firebase project
- Google Cloud project (for GCS)

## Setup

### 1. Firebase

1. Create a project at [Firebase Console](https://console.firebase.google.com)
2. Enable **Authentication** → Email/Password and Google sign-in
3. Create a **Firestore** database
4. Register a Web app and copy the config object

### 2. Frontend

```bash
cd frontend
cp .env.local.example .env.local
# Fill in NEXT_PUBLIC_FIREBASE_* from Firebase Console
npm install
npm run dev
```

Sign-in: [http://localhost:3000/signin](http://localhost:3000/signin)  
Dashboard (after sign-in): [http://localhost:3000/dashboard](http://localhost:3000/dashboard)

### 3. Backend

```bash
cd backend
cp .env.example .env
# Set GOOGLE_APPLICATION_CREDENTIALS to path of your GCP service account JSON
# Set GCS_BUCKET to your bucket name
pip install -r requirements.txt
uvicorn main:app --reload
```

API: [http://localhost:8000](http://localhost:8000)  
Health: [http://localhost:8000/health](http://localhost:8000/health)

### 4. Firestore Security Rules

The app syncs user profiles to Firestore on sign-in. You must deploy rules that allow authenticated users to write their own document:

**Option A – Firebase Console:**
1. Go to [Firebase Console](https://console.firebase.google.com) → Firestore Database → Rules
2. Replace the rules with:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

3. Click **Publish**

**Option B – Firebase CLI:**
```bash
firebase init firestore  # if not done
firebase deploy --only firestore:rules
```
(Ensure `firestore.rules` in the project root matches the rules above.)

### 5. Google Cloud Storage

1. Enable Cloud Storage API in GCP
2. Create a bucket
3. Create a service account with Storage Object Admin role
4. Download the JSON key and set `GOOGLE_APPLICATION_CREDENTIALS` in backend `.env`

### 6. Docker (Backend)

```bash
cd backend
docker build -t echo-backend .
docker run -p 8000:8000 -e GCS_BUCKET=your-bucket -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/key echo-backend
```

## Scripts (from root)

| Script           | Description                    |
|------------------|--------------------------------|
| `npm run dev`    | Start Next.js dev server       |
| `npm run build`  | Build Next.js                  |
| `npm run start`  | Start Next.js production       |
| `npm run backend:dev`   | Start FastAPI with hot reload  |
| `npm run backend:docker`| Build and run backend in Docker|

## Environment Variables

### Frontend (`.env.local`)

| Variable                          | Description                    |
|-----------------------------------|--------------------------------|
| `NEXT_PUBLIC_FIREBASE_API_KEY`    | Firebase config                |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`| Firebase config                |
| `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | Firebase config                |
| `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` | Firebase config            |
| `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | Firebase config         |
| `NEXT_PUBLIC_FIREBASE_APP_ID`     | Firebase config                |
| `NEXT_PUBLIC_API_URL`             | Backend URL (optional)         |

### Backend (`.env`)

| Variable                       | Description                         |
|--------------------------------|-------------------------------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account JSON  |
| `GCS_BUCKET`                  | GCS bucket name                     |
| `FIREBASE_PROJECT_ID`         | Firebase project ID (optional)      |
