## Student Performance Indicator (ML + Flask + AWS)

A complete end‑to‑end machine learning project that predicts student performance from demographic and study-related inputs. The app is built with Flask, uses a trained model and preprocessing pipeline stored in `artifacts/`, and supports containerized deployment. CI/CD builds and pushes Docker images to Amazon ECR and can deploy to a self-hosted runner.

### Features
- **Web UI** with Flask templates (`templates/index.html`, `templates/home.html`)
- **Prediction pipeline** using saved `artifacts/model.pkl` and `artifacts/preprocessor.pkl`
- **Training artifacts** and sample data (`artifacts/`, `notebook/`)
- **Dockerized** application for reproducible deployment
- **GitHub Actions** workflow for CI, image build/push to ECR, and deploy

### Tech Stack
- **Backend**: Flask (Python)
- **ML**: scikit-learn, CatBoost (training artifacts)
- **Infra**: Docker, AWS ECR, GitHub Actions

---

## Repository Structure
```
.
├─ app.py                       # Flask app entrypoint
├─ artifacts/                   # Trained model, preprocessor, data splits
├─ src/                         # Package: data ingestion, transform, training, pipelines
│  ├─ components/
│  ├─ pipeline/
│  ├─ logger.py, exception.py, utils.py
├─ templates/                   # Flask HTML templates
├─ notebook/                    # EDA and model training notebooks
├─ requirements.txt             # Python dependencies
├─ Dockerfile                   # Container build
├─ .github/workflows/main.yaml  # CI/CD pipeline
└─ README.md
```

---

## Local Development

### 1) Prerequisites
- Python 3.12 (recommended to match `venv`)
- pip
- Git
- (Optional) Docker

### 2) Setup virtual environment and install deps
```bash
# from repo root
python -m venv venv
# Windows PowerShell
./venv/Scripts/Activate.ps1
# or CMD
venv\Scripts\activate.bat

pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Run the app
```bash
# from repo root with venv activated
python app.py
# App listens on 0.0.0.0:5000 by default
```
Open `http://localhost:5000`.

---

## App Endpoints
- `GET /` → renders `templates/index.html`
- `GET /predictdata` → renders `templates/home.html` (the prediction form)
- `POST /predictdata` → accepts form fields and returns prediction on the same page

Expected form fields (names in HTML):
- `gender`
- `ethnicity`
- `parental_level_of_education`
- `lunch`
- `test_preparation_course`
- `reading_score` (numeric)
- `writing_score` (numeric)

Note: In `app.py`, `reading_score` and `writing_score` values are read from the opposite form keys, so ensure the template aligns or adjust accordingly.

---

## Docker

### Build
```bash
docker build -t student-performance:latest .
```

### Run
```bash
docker run -d -p 8080:8080 --name studentperformanceindicator \
  -e PORT=8080 \
  student-performance:latest
```
If your app expects port 5000, either change the `Dockerfile`/app to bind 8080 or map `-p 8080:5000`.

---

## CI/CD (GitHub Actions → AWS ECR → Deploy)
Workflow: `.github/workflows/main.yaml`

### What it does
- On push to `main` (except README changes):
  - Run basic CI steps
  - Build the Docker image and push to AWS ECR repository from secrets
  - On a self-hosted runner, pull and run the latest image

### Required GitHub Secrets
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (e.g., `us-east-1`)
- `AWS_ECR_LOGIN_URI` (e.g., `123456789012.dkr.ecr.us-east-1.amazonaws.com`)
- `ECR_REPOSITORY_NAME` (e.g., `student-performance`)

### Self-hosted Runner Notes
- Ensure Docker is installed and the runner user can run docker
- The deploy step stops/removes any existing container and runs the latest image
- Container name used in the workflow: `studentperformanceindicator`

---

## Training and Artifacts
- Notebooks under `notebook/` show EDA and model training
- Final model and preprocessing pipeline are stored in `artifacts/`
- Inference is performed via `src/pipeline/predict_pipeline.py` using these artifacts

---

## Troubleshooting
- Port conflicts: stop existing containers or change published ports
- Docker run failing on Windows self‑hosted runner: use single-line `docker run` without line continuations in the workflow
- Missing secrets: verify all required GitHub Secrets are configured
- Model load errors: confirm `artifacts/model.pkl` and `artifacts/preprocessor.pkl` exist and match code expectations

---

