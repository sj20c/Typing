# Typing

Minimal journaling web application built with Next.js + Django REST Framework

# Overview

Typing은 하루의 기록을 저장하고 관리할 수 있는 웹 애플리케이션입니다.
프론트엔드와 백엔드를 분리한 구조로 설계했으며, JWT 기반 인증과 RESTful API 설계를 중심으로 개발했습니다.

# Architecture
Next.js (Client)
        ↓
Django REST API
        ↓
PostgreSQL


Frontend / Backend 분리 구조

JWT 기반 인증 처리

RESTful API 설계

모바일 퍼스트 UI

# Tech Stack

Frontend

Next.js (App Router)

React

TypeScript

Tailwind CSS

Axios

Backend

Django

Django REST Framework

PostgreSQL

JWT Authentication

# Features

사용자 인증 (JWT)

기록 CRUD 기능

RESTful API 통신 구조

재사용 가능한 컴포넌트 설계

확장 가능한 폴더 구조

# Run Locally
Frontend
npm install
npm run dev

Backend
pip install -r requirements.txt
python manage.py runserver

# Focus

실서비스 구조를 고려한 프론트/백엔드 분리 설계

인증 흐름 설계 및 API 구조 설계 경험

유지보수와 확장성을 고려한 프로젝트 구조 구성
