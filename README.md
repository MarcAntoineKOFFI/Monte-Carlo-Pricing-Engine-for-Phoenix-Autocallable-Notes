# Autocall Pricer

## Overview
This project is a Monte Carlo pricing engine for Autocallable Notes (Phoenix structure) with a Down-and-In Knock-In barrier. It calculates the fair value of the financial product and its associated risk sensitivities (Greeks).

## How It Works
The program uses a **Monte Carlo simulation** to price the option:
1.  **Simulates** thousands of potential future asset price paths using Geometric Brownian Motion (daily steps).
2.  **Monitors** each path for:
    *   **Autocall Events**: Early redemption if price $\ge$ Autocall Barrier.
    *   **Coupons**: Periodic payments if price $\ge$ Coupon Barrier.
    *   **Knock-In**: Capital loss if the price drops below the safety barrier (KI) at any point during its life.
3.  **Averages** the discounted cashflows of all paths to estimate the fair price.

## Usage
You can run the pricing engine directly or use the simple interface:

```bash
python interface.py
```

## Disclaimer
This project was coded by Marc-Antoine Koffi for **academic purposes**. It is intended to demonstrate the mathematical principles of derivatives pricing and Monte Carlo methods. It is **not** intended for replication.
