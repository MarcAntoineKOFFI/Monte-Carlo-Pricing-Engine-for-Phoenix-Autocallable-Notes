import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

r = 0.2 
S = 100 
B = 80 
KI = 60 
A = 100 
n = 3 
N = 100 
T_period = 1 
C = 0.1 
sigma = 0.2 

def simulate_geometric_brownian_motion_paths(num_simulations, num_time_steps, spot, T_total, r, sigma):
    dt = T_total / num_time_steps
    prices = np.zeros((num_simulations, num_time_steps + 1))
    prices[:, 0] = spot 

    for i in range(1, num_time_steps + 1):
        z = np.random.standard_normal(num_simulations)
        prices[:, i] = prices[:, i-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    
    return prices

def compute_autocall_price(S, B, KI, A, N, n, T_period, r, C, sigma, num_simulations=10000):
    steps_per_year = 252 
    T_total = n * T_period
    
    num_time_steps = int(round(T_total * steps_per_year))
    
    paths = simulate_geometric_brownian_motion_paths(num_simulations, num_time_steps, S, T_total, r, sigma)
    
    observation_indices = [int(round(i * T_period * steps_per_year)) for i in range(1, n + 1)]
    
    observation_prices = paths[:, observation_indices]
    
    full_path_prices = paths[:, 1:]
    min_prices_daily = np.min(full_path_prices, axis=1)
    knock_in_event = (min_prices_daily < KI)
    
    payoffs = np.zeros(num_simulations)
    active_paths = np.ones(num_simulations, dtype=bool)
    
    for i in range(n):
        current_prices = observation_prices[:, i]
        current_time = (i + 1) * T_period
        df = np.exp(-r * current_time) 
        
        autocall_condition = (current_prices >= A) & active_paths
        
        coupon_amount = N * C
        payoffs[autocall_condition] += (N + coupon_amount) * df
        active_paths[autocall_condition] = False 
        
        still_active_mask = active_paths 
        coupon_condition = (current_prices >= B) & still_active_mask
        
        payoffs[coupon_condition] += coupon_amount * df
        
    final_prices = observation_prices[:, -1]
    df_final = np.exp(-r * T_total)
    
    capital_return = np.ones(num_simulations)
    
    capital_loss_mask = active_paths & (final_prices < B) & knock_in_event
    
    capital_return[capital_loss_mask] = final_prices[capital_loss_mask] / S
    
    payoffs[active_paths] += N * capital_return[active_paths] * df_final
    
    price = np.mean(payoffs)
    std_err = np.std(payoffs) / np.sqrt(num_simulations)
    
    return price, std_err

def pricing_engine(S_val, sigma_val):
    p, _ = compute_autocall_price(
        S=S_val, B=B, KI=KI, A=A, N=N, n=n, T_period=T_period, 
        r=r, C=C, sigma=sigma_val, num_simulations=50000
    )
    return p

def calculate_greeks(S, sigma):
    dS = S * 0.01
    p_up = pricing_engine(S + dS, sigma)
    p_down = pricing_engine(S - dS, sigma)
    delta = (p_up - p_down) / (2 * dS)
    
    p_mid = pricing_engine(S, sigma)
    gamma = (p_up - 2*p_mid + p_down) / (dS**2)
    
    dSigma = 0.01 
    p_vol_up = pricing_engine(S, sigma + dSigma)
    p_vol_down = pricing_engine(S, sigma - dSigma)
    vega = (p_vol_up - p_vol_down) / (2 * dSigma)
    
    return delta, gamma, vega, p_mid

if __name__ == "__main__":
    print(f"Parameters: S={S}, B={B}, KI={KI}, A={A}, C={C}, r={r}, sigma={sigma}, T={T_period}, n={n}")
    
    price, err = compute_autocall_price(S, B, KI, A, N, n, T_period, r, C, sigma)
    print(f"Autocall Price: {price:.4f} +/- {1.96*err:.4f} (95% Confidence Interval)")
    
    print("Calculating Greeks...")
    delta, gamma, vega, _ = calculate_greeks(S, sigma)
    print(f"Delta: {delta:.4f}")
    print(f"Gamma: {gamma:.6f}")
    print(f"Vega:  {vega:.4f}")