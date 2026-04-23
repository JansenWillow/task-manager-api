# Task Manager API

![CI](https://github.com/JansenWillow/task-manager-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-3776AB)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![pytest](https://img.shields.io/badge/pytest-30%20tests-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-80%25-success)

REST API untuk manajemen tugas berbasis FastAPI + SQLite. Final Project Mata Kuliah Software Testing.

## Fitur
- CRUD Task (create, read, update, delete)
- Filter berdasarkan status & prioritas
- Statistik task
- Validasi input dengan Pydantic
- CI/CD dengan GitHub Actions

## Cara Menjalankan

    pip install -r requirements.txt
    uvicorn app.main:app --reload

Buka http://localhost:8000/docs

## Cara Menjalankan Test

    pytest

## Strategi Pengujian
- 22 Unit Tests (schema validation, service logic)
- 8 Integration Tests (API endpoints, database)
- Target coverage: 60%, aktual >80%

## CI/CD Pipeline
Workflow GitHub Actions otomatis menjalankan test pada setiap push & pull request.

## Coverage Report

Lihat laporan coverage interaktif di: https://jansenwillow.github.io/task-manager-api/
