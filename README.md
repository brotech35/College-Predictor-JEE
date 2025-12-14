# 🎓 JEE College Predictor  
*A Domain-Driven, Rule-Based College Eligibility System*

🚀 **Live Application**: (https://college-predictor-jee.streamlit.app/)  
📊 **Kaggle Dataset (Created by Me)**: (https://www.kaggle.com/datasets/ramram234/jee-cutoff-2018-2025-round-1to6)

**(Can't Provide Whole Dataset Here as it is too big)**
---

## 📌 Project Overview

The **JEE College Predictor** is a rule-based decision support system designed to help students explore **eligible engineering colleges** using **historical JoSAA counselling cutoffs**.

This project intentionally avoids machine learning and instead follows **real counselling logic**, ensuring predictions are:
- Transparent
- Explainable
- Domain-correct
- Ethically constrained

The system supports **JEE Main**, **JEE Advanced**, or **both exams together**, and presents results from **best to worst eligible colleges** based on the student’s performance.

---

## 🎯 Problem Statement

Most online predictors:
- Mix JEE Main and JEE Advanced data
- Show colleges even at unrealistic scores
- 
This project solves those issues by:
- Strictly separating exam pipelines
- Enforcing realistic cutoff thresholds
- Using eligibility logic instead of probability guessing

---

## 🗂️ Data Creation & Collection

The dataset was **created manually** from official **JoSAA counselling cutoff PDFs** spanning multiple years and rounds.

### Data creation process:
- Year-wise and round-wise cutoff files collected
- Raw data cleaned, standardized, and merged using Python
- Duplicate and inconsistent records removed
- Validity checks applied (e.g., opening rank ≤ closing rank)

The final cleaned dataset was also published on **Kaggle** for transparency and reuse.

---

## 🚫 Why No Machine Learning?

This is an **eligibility problem**, not a prediction problem.

- There is no labeled target variable
- Admissions are governed by fixed cutoff rules
- ML would add false confidence and reduce trust

A **rule-based expert system** is the correct and ethical approach.

---

## 🖥️ Application Logic (Streamlit)

### User Inputs:
- Exam type: JEE Main / JEE Advanced / Both
- Input type: Rank / Percentile / Marks
- Gender
- Category
- PwD status
- Preferred branch

### Core logic:
- Separate pipelines for Main and Advanced
- Input validation using confidence thresholds
- Eligibility filtering using closing cutoffs
- Sorting colleges from **best to worst possible option**

---

## 🚧 Confidence Thresholds

To avoid misleading results, predictions are blocked below realistic limits.

### JEE Main:
- Rank ≤ 400,000  
- Percentile ≥ 75  
- Marks ≥ 95  

### JEE Advanced:
- Rank ≤ 29,247  
- Percentile ≥ 97  
- Marks ≥ 220  

If a student’s input is below these thresholds, the app clearly shows:
> **No reliable predictions available**

---

## 📌 Output Design

- Only **eligible colleges** are shown
- Best options appear first
- No dataset dumping
- No false guarantees

---

## ⚠️ Disclaimer

- Predictions are based on historical JoSAA cutoffs
- Counselling outcomes vary year to year
- This tool does not guarantee admission
- Intended strictly for guidance and exploration

---

## 🧠 Skills Demonstrated

- Data collection and engineering
- Data cleaning and EDA
- Feature engineering
- Domain-driven problem solving
- Rule-based system design
- Streamlit application development
