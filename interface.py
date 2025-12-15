import tkinter as tk
from tkinter import messagebox
import autocall

def calculate():
    try:
        S = float(entry_S.get())
        B = float(entry_B.get())
        KI = float(entry_KI.get())
        A = float(entry_A.get())
        C = float(entry_C.get())
        r = float(entry_r.get())
        sigma = float(entry_sigma.get())
        T = float(entry_T.get())
        n = int(entry_n.get())
        
        price, err = autocall.compute_autocall_price(
            S, B, KI, A, 100, n, T, r, C, sigma, num_simulations=5000
        )
        
        result_text.set(f"Price: {price:.4f}")
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

window = tk.Tk()
window.title("Autocall Pricer")
window.geometry("300x600")

labels = ["Spot (S)", "Coupon Barr (B)", "Knock-In (KI)", "Autocall Barr (A)", 
          "Coupon (C)", "Rate (r)", "Vol (sigma)", "Period (T)", "Obs (n)"]
defaults = ["100", "80", "60", "100", "0.1", "0.2", "0.2", "1", "3"]
entries = []

for i, lab in enumerate(labels):
    tk.Label(window, text=lab).pack()
    e = tk.Entry(window)
    e.insert(0, defaults[i])
    e.pack()
    entries.append(e)

entry_S, entry_B, entry_KI, entry_A, entry_C, entry_r, entry_sigma, entry_T, entry_n = entries

tk.Button(window, text="Calculate", command=calculate).pack(pady=10)

result_text = tk.StringVar()
tk.Label(window, textvariable=result_text, font=("Arial", 14, "bold")).pack(pady=20)

window.mainloop()
