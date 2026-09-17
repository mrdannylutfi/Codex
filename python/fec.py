import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

def calculate_kp4_fec_plr(pre_fec_ber):
    """
    Calculates the Post-FEC Block/Packet Error Rate for KP4 FEC.
    Standard: RS(544, 514) where symbols are m=10 bits.
    Can correct up to t = (n - k) // 2 = 15 symbol errors.
    """
    n = 544
    k = 514
    m = 10
    t = (n - k) // 2  # 15 symbols
    
    # Step 1: Convert Bit Error Rate (BER) to Symbol Error Rate (SER)
    # Probability that at least 1 bit in a 10-bit symbol is flipped
    symbol_error_rate = 1 - (1 - pre_fec_ber) ** m
    
    # Step 2: Calculate the probability of a codeword failing
    # Survival function (sf) yields P(X > t), which is the uncorrectable block rate
    post_fec_plr = binom.sf(t, n, symbol_error_rate)
    
    return post_fec_plr

# 1. Generate a range of Pre-FEC BER values spanning across the threshold
# Slicing from pristine (1e-5) up to completely broken (1e-3)
pre_fec_ber_range = np.logspace(-5, -3, 500)

# 2. Compute corresponding Post-FEC PLR values
post_fec_plr_range = [calculate_kp4_fec_plr(ber) for ber in pre_fec_ber_range]

# 3. Plot the data to visualize the 'Cliff Effect'
plt.figure(figsize=(10, 6))
plt.plot(pre_fec_ber_range, post_fec_plr_range, color='crimson', lw=2.5, label='KP4 FEC Performance')

# Highlight the exact standard operational cliff threshold (2.2 x 10^-4)
threshold_ber = 2.2e-4
plt.axvline(x=threshold_ber, color='black', linestyle='--', alpha=0.7, 
            label=f'Standard KP4 Limit ({threshold_ber:.1e})')

# Format the chart to clearly illustrate the sharp transition
plt.xscale('log')
plt.title('The Paradox of Signal Phenomena: KP4 FEC Cliff Effect', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Pre-FEC Bit Error Rate (BER) [Log Scale]', fontsize=12)
plt.ylabel('Post-FEC Packet/Block Loss Ratio (PLR)', fontsize=12)
plt.grid(True, which="both", ls=":", alpha=0.5)

# Visual Shading of Zones
plt.fill_between(pre_fec_ber_range, post_fec_plr_range, where=(pre_fec_ber_range <= threshold_ber), 
                 color='green', alpha=0.1, label='Masked Error Zone (PLR ~ 0%)')
plt.fill_between(pre_fec_ber_range, post_fec_plr_range, where=(pre_fec_ber_range > threshold_ber), 
                 color='red', alpha=0.1, label='Link Failure Zone (PLR Spikes)')

plt.legend(loc='upper left', fontsize=11)
plt.tight_layout()

# Show the plot
plt.show()
