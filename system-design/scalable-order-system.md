# Scalable Order Processing System

## Architecture

* Controller → Service → Payment Strategy → Repository

## Key Components

### 1. Order Service

Handles orchestration and transaction management

### 2. Payment Strategy

* CardPaymentStrategy
* UssdPaymentStrategy

### 3. Factory / Registry

Resolves payment strategy dynamically

### 4. Validation Layer

Ensures request integrity

### 5. Idempotency Layer

Prevents duplicate transactions

## Improvements

* Use @Transactional
* Secure payment handling (tokenization)
* Add logging and monitoring
