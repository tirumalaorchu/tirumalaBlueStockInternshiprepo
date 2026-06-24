-- 1. Top 5 funds by AUM by fund house
SELECT fund_house,
       SUM(aum_crore) AS total_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY SUM(aum_crore) DESC
FETCH FIRST 5 ROWS ONLY;

-- 2. Average NAV per month
SELECT SUBSTR(date_key, 1, 7) AS year_month,
       AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY year_month
ORDER BY year_month;

-- 3. SIP YoY growth in total invested amount without window functions
WITH yearly AS (
    SELECT SUBSTR(date_key, 1, 4) AS year,
           SUM(amount_inr) AS total_sip_amount
    FROM fact_transactions
    WHERE transaction_type = 'SIP'
    GROUP BY SUBSTR(date_key, 1, 4)
)
SELECT y.year,
       y.total_sip_amount,
       p.total_sip_amount AS prior_year_amount,
       CASE
           WHEN p.total_sip_amount IS NULL THEN NULL
           ELSE ROUND((y.total_sip_amount - p.total_sip_amount) * 100.0 / p.total_sip_amount, 2)
       END AS yoy_growth_pct
FROM yearly y
LEFT JOIN yearly p ON CAST(p.year AS INTEGER) = CAST(y.year AS INTEGER) - 1
ORDER BY y.year;

-- 4. Transactions by state
SELECT state,
       COUNT(*) AS transaction_count,
       SUM(amount_inr) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;

-- 5. Funds with expense_ratio_pct < 1%
SELECT amfi_code,
       fund_house,
       scheme_name,
       expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Top 5 categories by average 3-year return
SELECT f.category,
       AVG(p.return_3yr_pct) AS avg_return_3yr
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
GROUP BY f.category
ORDER BY avg_return_3yr DESC
FETCH FIRST 5 ROWS ONLY;

-- 7. Average transaction amount by payment mode
SELECT payment_mode,
       COUNT(*) AS transactions,
       AVG(amount_inr) AS avg_amount_inr
FROM fact_transactions
GROUP BY payment_mode
ORDER BY avg_amount_inr DESC;

-- 8. Monthly redemption share of total transaction value
WITH monthly_totals AS (
    SELECT SUBSTR(date_key, 1, 7) AS year_month,
           SUM(amount_inr) AS total_amount
    FROM fact_transactions
    GROUP BY SUBSTR(date_key, 1, 7)
),
redemption_totals AS (
    SELECT SUBSTR(date_key, 1, 7) AS year_month,
           SUM(amount_inr) AS redemption_amount
    FROM fact_transactions
    WHERE transaction_type = 'Redemption'
    GROUP BY SUBSTR(date_key, 1, 7)
)
SELECT m.year_month,
       m.total_amount,
       COALESCE(r.redemption_amount, 0) AS redemption_amount,
       ROUND(100.0 * COALESCE(r.redemption_amount, 0) / m.total_amount, 2) AS redemption_pct
FROM monthly_totals m
LEFT JOIN redemption_totals r ON m.year_month = r.year_month
ORDER BY m.year_month;

-- 9. Unique investors by state and city tier
SELECT state,
       city_tier,
       COUNT(DISTINCT investor_id) AS unique_investors
FROM fact_transactions
GROUP BY state,
         city_tier
ORDER BY unique_investors DESC;

-- 10. Funds with the highest Sharpe Ratio and expense ratio under 1.5%
SELECT f.amfi_code,
       f.scheme_name,
       p.sharpe_ratio,
       p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1.5
ORDER BY p.sharpe_ratio DESC
FETCH FIRST 10 ROWS ONLY;
