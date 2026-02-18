#!/bin/bash
# Daily Bank Balance Check
# Pulls real-time balances from Kobestarr and Stripped Media

TOKEN_KSD="eyJhbGciOiJQUzI1NiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAA_0WPTU7EMAyFr4KyHo_i_Ls7dlyAAziJg6opbdV0JCTE3ckAEkvb73t-71PNvatJ8T5f-8nHMq9vmdfbtWzv6qL6PY8jJskUI4IR7cBZHSEbdGBIW0YmE2wdYvnY1eTI-ICeQriomU81YQxEztjHgkvZ7uv5si1Vjte5Dm9HOiG3CkmQwLXkgJ1HCClrgyIt2jS8z-0m6y-BQo2TF_BEbRAtQoo1Q6DKyUn21oZBjEbPpUjv_5SJQsPYD4qyGR_FQsRA2kTbWOhRuGy7DHnmhdci0yFcn_5i_wzq6xti2PpjMwEAAA.AxJ5hQxOO-5Hpo57Taf77zO84KOE5ZY2cLdmy8JqRlG3DOHaApvJHCax0eVmR529fNPMTP_tQSb8GEQqVQwRneLp01-CvB_HPiB8UQN_slYh3ez7eIvA4QyjMz1G_G3sHNsWmLE2GSfpxes4BMYUrEQ2Rzxfw8Zm9TU8CI9Rlwv_sshEJYk_advRtzql0Ha_Q515UCA_sEj3DgWoc-YBmY3xb_PhUceWyaVEOHtQRIfBiQCjKuLhFblFblMmpLw-IQ5kKDrnCFd2MGsSKyPcCyB6opqxyHeDg8DZJKx13ADJ4r7qr-1JLQNREbU4JXH7FVMmxwXHZJGxc1iKuwykXA_QDuFJiW97Sm5HwoZtUmae4AmA-o0O7IqCRyxfDxzwIBSgyNkGg2X1TH1ODU909KObBLCnNC1vwL7U_MSOvUGKAW_BwU1pR6keqTLWgJoBa6vNbvB7-EmPHPB7HF3fCzZBRdtq-rnkM8B3Cr1tt3-GLJkE1gORldiSNtVnEdeWfFxfbdWx_t8zaA8hrcZuDJ21UBoq6TnlVav8VXRHMziPUC6q1MQakmC8o8WqehhU0GgZ9BRIioasipAyF4xnKepSJRLeSynH3vATaPZPwkRxCuvrsCL2bsMwQR57BO_ltwQrKJZ5HkJSXu5lxgmQ4ehPWkKmeDfPwxBIRyEGIck"
TOKEN_SMEDIA="eyJhbGciOiJQUzI1NiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAA_0WPwU7EMAxEfwXlvF4ljpM0vXHjB_gAx3FRtaWtmq6EhPh3soDE0Z55o5lPM7dmRsP7fG0nH8u8vhVeb1fZ3s3FtHvpohu05JQcoFoC8jZBQUeA2Xp2nDH62s36sZuRMobooo3xYmY-zehSzJmQHg8W2e7r-bItVY_XufbslGRSWyagFCNQUAdDDRYmktqFXKaAPfvcbrr-Ek7ZDRP73sF3zFcFFkLwJSn7NNiiuRN90bOItvZPIaODkmoAwlqA0TJMoYp1kpULPQbLtmu3F154FR0P5fr0V_vnMF_f73ighDMBAAA.na5wH8vWQ7VEz8shL0QITauUdU6aC5feU9_0Ao6C05Lmz_gpfLniw4LVhZDBbb9kFjd06emmK44Y2hWYUXkQGH0Ynia8prbt2wO4RvFU55tuAzBMIOmmetRRi6DPoYVeQMZlShXGGuY1kRHI7dM5cYYsZkmJBI-tJy0BBsNN1jA26HKYw0VbtZeQhs20Rpqe-9ViKH5XWUjBGHbYKdJjlaf-FpxCUBb6UX7abATYbVXi_oHAa8zIGd_OWJPhvRmO-hiW5TQKrGyBef6no2VIF898J_A6C0o81gkIqSYYpaQMMKb5xUnIJBqj-WYrIlzw-Uaj7m8OHbQPmVFYFg9gSJXrl_Qh2LO-BefB8Zszei-R61NjKlCq29FMw84UUTAv-qhYwU7ow1H_JtEYwcFnvud2OSbGB8z3da_piZkDhQq8kUev4fOGAwzSX8gb5tJ-0qy-2jPmay1qmGlgsqgAgjcSHhBouL1hXi0JeYcx1pB7J1wni62JVpRyK8G9BtO8dkqe5kwMDj6lkVGbMMOzB9TANjCGWH1l4ub0s4r0ErcCVSPgkc6GtadopOjcfDfqA1hobOnL-mVK9DlrJ-y-n-J_z2UP12W_t-DJv8iu0onO2OY97F4yjoLOXu65cXtsvTjLKLjsZApcaGIAO0oebw-rR-jqLFip_Y26hjtCl4Y"

ACCT_KSD="f995afcb-f666-4943-9c99-038ee4e65f60"
ACCT_SMEDIA="d4a2cb5f-d419-41a9-8ba8-ef86249c82e2"

# Get KSD balance
KSD_JSON=$(curl -s -H "Authorization: Bearer $TOKEN_KSD" \
  "https://api.starlingbank.com/api/v2/accounts/$ACCT_KSD/balance")
KSD_MAIN=$(echo "$KSD_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['effectiveBalance']['minorUnits']/100)")
KSD_TOTAL=$(echo "$KSD_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['totalEffectiveBalance']['minorUnits']/100)")
KSD_SPACES=$(echo "$KSD_TOTAL - $KSD_MAIN" | bc)

# Get Stripped Media balance
SMEDIA_JSON=$(curl -s -H "Authorization: Bearer $TOKEN_SMEDIA" \
  "https://api.starlingbank.com/api/v2/accounts/$ACCT_SMEDIA/balance")
SMEDIA_TOTAL=$(echo "$SMEDIA_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['totalEffectiveBalance']['minorUnits']/100)")

# Calculate grand total
GRAND_TOTAL=$(echo "$KSD_TOTAL + $SMEDIA_TOTAL" | bc)

echo "=== DAILY BALANCE CHECK ==="
echo ""
echo "🐆 KOBESTARR ENGINEERING"
echo "   Main Account:    £$KSD_MAIN"
echo "   Savings (Spaces): £$KSD_SPACES"
echo "   TOTAL:           £$KSD_TOTAL"
echo ""
echo "🐆 STRIPPED MEDIA"
echo "   TOTAL:           £$SMEDIA_TOTAL"
echo ""
echo "========================================"
echo "💰 GRAND TOTAL:      £$GRAND_TOTAL"
echo "========================================"
