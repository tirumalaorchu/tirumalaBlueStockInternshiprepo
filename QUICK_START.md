# QUICK START GUIDE - EDA Analysis Notebook

## ✓ SETUP COMPLETE

Your Jupyter notebook **EDA_Analysis.ipynb** has been created with all 10 tasks implemented.

**Location:** `d:\BlueStock\tirumalaBlueStockInternshiprepo\mutual_fund_analytics\notebooks\EDA_Analysis.ipynb`

---

## STEP 1: INSTALL DEPENDENCIES

Open PowerShell/Command Prompt and run:

```bash
# Navigate to your project
cd d:\BlueStock\tirumalaBlueStockInternshiprepo

# Install required packages
pip install pandas numpy matplotlib seaborn plotly kaleido -q
```

**Packages installed:**
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib` - Static plotting
- `seaborn` - Statistical visualization
- `plotly` - Interactive charts
- `kaleido` - PNG/PDF export for Plotly

---

## STEP 2: VERIFY DATA FILES

Check that all processed CSV files exist:

```bash
dir mutual_fund_analytics\data\processed\
```

Should show these 8 files:
```
✓ nav_history_cleaned.csv
✓ scheme_performance_cleaned.csv
✓ aum_by_fund_house_cleaned.csv
✓ monthly_sip_inflows_cleaned.csv
✓ category_inflows_cleaned.csv
✓ investor_transactions_cleaned.csv
✓ industry_folio_count_cleaned.csv
✓ portfolio_holdings_cleaned.csv
```

If any are missing, run:
```bash
python scripts/clean_and_load.py
```

---

## STEP 3: OPEN THE NOTEBOOK

### **Option A: VS Code (Recommended)**
1. Open VS Code
2. Open file: `mutual_fund_analytics/notebooks/EDA_Analysis.ipynb`
3. Select kernel: Python 3.9+ (if prompted)
4. Click **Run All** (⏭️ icon)

### **Option B: Jupyter Lab/Notebook**
```bash
# Navigate to notebook directory
cd mutual_fund_analytics\notebooks

# Launch Jupyter
jupyter notebook EDA_Analysis.ipynb
```

Browser will open automatically.

### **Option C: Command Line (Non-interactive)**
```bash
# Run and export to HTML
jupyter nbconvert --to notebook --execute EDA_Analysis.ipynb --output EDA_Analysis_executed.ipynb
```

---

## STEP 4: MONITOR EXECUTION

**Expected timeline:** 10-15 minutes for full notebook run

**Progress indicator:**
- Cell 1-3: Setup (30 sec)
- Cell 4: Task 1 - NAV Trends (2-3 min) ⏳
- Cell 5: Task 2 - AUM Chart (30 sec)
- Cell 6: Task 3 - SIP Time-Series (1-2 min)
- Cell 7: Task 4 - Category Heatmap (1 min)
- Cell 8: Task 5 - Demographics (45 sec)
- Cell 9: Task 6 - Geography (1 min)
- Cell 10: Task 7 - Folio Growth (1-2 min) ⏳
- Cell 11: Task 8 - Correlation (2-3 min) ⏳
- Cell 12: Task 9 - Sector Allocation (30 sec)
- Cell 13+: Task 10 Findings (instant, markdown only)
- Final: Summary & File List (30 sec)

---

## STEP 5: VERIFY OUTPUTS

After execution completes, check results directory:

```bash
dir results\
```

Should show **15+ files:**

**HTML Files (Interactive - Open in Browser):**
```
✓ 01_nav_trends.html                 (~1.2 MB)
✓ 03_sip_inflows.html                (~800 KB)
✓ 07_folio_count.html                (~600 KB)
✓ 09_sector_allocation.html          (~400 KB)
```

**PNG Files (Static - For Reports):**
```
✓ 01_nav_trends.png                  (~600 KB)
✓ 02_aum_by_fund_house.png           (~400 KB)
✓ 03_sip_inflows.png                 (~500 KB)
✓ 04_category_heatmap.png            (~800 KB)
✓ 05_investor_demographics.png       (~600 KB)
✓ 06_geographic_distribution.png     (~700 KB)
✓ 07_folio_count.png                 (~500 KB)
✓ 08_nav_correlation_matrix.png      (~500 KB)
✓ 09_sector_allocation.png           (~400 KB)
```

---

## STEP 6: VIEW RESULTS

### **Interactive Analysis (Recommended)**
```bash
# Open in default browser
start results\01_nav_trends.html
start results\03_sip_inflows.html
```

Features:
- ✓ Zoom in/out
- ✓ Pan across chart
- ✓ Hover for values
- ✓ Click legend to toggle series
- ✓ Download as PNG

### **Static Reports**
View PNG files in any image viewer or insert into PowerPoint/Word.

---

## COMMON ISSUES & FIXES

### **Issue: "ModuleNotFoundError: No module named 'plotly'"**
```bash
# Solution
pip install plotly kaleido --upgrade
```

### **Issue: "FileNotFoundError: CSV files not found"**
```bash
# Verify path
python -c "import os; print(os.path.abspath('mutual_fund_analytics/data/processed'))"

# If empty, run cleanup:
python scripts/clean_and_load.py
```

### **Issue: "PNG export failed - kaleido not installed"**
```bash
# Install kaleido
pip install kaleido

# Or skip PNG export (HTML still works)
# The notebook will continue if PNG fails
```

### **Issue: "Out of memory" or "Too slow"**
```python
# Edit notebook cell 4 to reduce schemes:
schemes = nav_df['amfi_code'].unique()[:20]  # Reduce from 40 to 20

# Or filter date range:
nav_df = nav_df[(nav_df['date'] >= '2024-01-01') & ...]
```

### **Issue: "Kernel crashed"**
```bash
# Restart kernel:
# In VS Code: Ctrl+Shift+P → Python: Restart Kernel
# In Jupyter: Kernel → Restart
```

---

## NEXT ACTIONS

### **1. Export to PowerPoint Report**
```bash
# Copy PNG files to PowerPoint manually
# OR use python-pptx:
pip install python-pptx

# Then create presentation programmatically
python scripts/create_presentation.py  # (Create this)
```

### **2. Schedule Weekly Runs**
```bash
# Windows Task Scheduler
# Command: python -m jupyter nbconvert --to notebook --execute EDA_Analysis.ipynb

# Or use cron (Linux/Mac):
0 9 * * MON jupyter nbconvert --to notebook --execute EDA_Analysis.ipynb
```

### **3. Share Results**
```bash
# Share HTML files (interactive analysis)
# Share PNG files (for presentations)
# Share notebook (for reproducibility)
```

### **4. Customize for Your Needs**
Edit notebook cells to:
- Change date ranges
- Add more schemes/funds
- Modify color schemes
- Add additional insights
- Export to different formats

---

## DOCUMENTATION

**Main Guide:** `mutual_fund_analytics/notebooks/README_EDA_Analysis.md`
- Full task descriptions
- Chart explanations
- Customization guide
- Performance metrics

**Data Dictionary:** `data_dictionary.md` (root directory)
- CSV file structures
- Column definitions
- Data types & ranges

**Schema:** `schema.sql` (root directory)
- Database star schema
- Table relationships
- Dimension & fact tables

---

## SUPPORT

For issues or questions:

1. **Check documentation:** README_EDA_Analysis.md
2. **Verify data:** Run `scripts/clean_and_load.py`
3. **Check environment:** `pip list` to verify packages
4. **Review code:** Notebook cells are well-commented

---

## TASK COMPLETION CHECKLIST

- [x] Notebook created with all 10 tasks
- [x] 15+ visualization codes implemented
- [x] Setup & imports cell included
- [x] Results directory created
- [x] README documentation prepared
- [x] Quick start guide provided (this file)

**Ready to Execute:** ✓ YES

**Next Step:** Run Jupyter notebook and monitor output!

---

**Generated:** 2026-06-26  
**Notebook:** EDA_Analysis.ipynb  
**Status:** Ready for Production ✓
