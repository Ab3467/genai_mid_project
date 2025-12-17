# FRONTEND BUILD
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

# BACKEND
FROM python:3.10
WORKDIR /app
COPY backend ./backend
COPY --from=frontend-build /app/frontend/dist ./frontend/dist
RUN pip install -r backend/requirements.txt

EXPOSE 8000
CMD ["python", "backend/main.py"]
