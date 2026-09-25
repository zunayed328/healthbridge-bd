# ADR-001: Hybrid Firebase Authentication with FastAPI and PostgreSQL

## Status
Accepted

## Date
2026-09-25

## Context
HealthBridge BD needs authentication that is:
- Easy to implement for a beginner team
- Supports Phone OTP (important for Bangladesh)
- Supports Google Sign-in
- Secure and scalable
- Connected to a proper relational database

We evaluated three options:
1. Firebase Auth only (simple but limited)
2. Custom JWT auth from scratch (complex for beginners)
3. Firebase Auth + FastAPI backend + PostgreSQL (hybrid)

## Decision
We will use Firebase Authentication as the identity provider
for OTP and Google sign-in only.

FastAPI backend will:
- Verify Firebase ID tokens on every request
- Map Firebase UID to internal PostgreSQL user records
- Handle all business logic and authorization
- Implement role-based access control (RBAC)

PostgreSQL will be the source of truth for:
- User profiles and roles
- All business data
- Inventory, orders, prescriptions
- Audit logs

Firebase will NOT be used for:
- Inventory management
- Order processing
- Payment logic
- Prescription storage
- ML/research data

## Consequences
Positive:
- Phone OTP works out of the box (critical for Bangladesh)
- Google sign-in is easy
- FastAPI handles all security logic
- PostgreSQL gives us proper joins and transactions
- Firebase token verification is well-documented

Negative:
- Two systems to maintain (Firebase + PostgreSQL)
- Must sync Firebase UID with internal user ID
- Firebase dependency for auth layer

## Alternatives Rejected
- Firebase-only: Cannot handle complex queries, joins, or ML data
- Custom JWT: Too complex for 3-month capstone timeline

## Implementation Notes
- Every API request must include Firebase ID token in header
- Backend verifies token with Firebase Admin SDK
- On first login, create internal user record in PostgreSQL
- Store firebase_uid as unique field in users table
- Never expose internal user IDs to client directly
