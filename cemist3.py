# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PcoSqZ2WMpNdDEaFSptg4Skux6BhUhfI
"""

import streamlit as st
import pandas as pd

# Data awal dari gambar
data = {
    "Cement Type": [
        "NAR1 PCC (Transisi)", "NAR1 OPC", "NAR1 OPC - SG", "NAR1 RFP", "NAR1 OWC",
        "NAR1 Type V", "NAR1 PwrPro", "NAR2 PCC Regular", "NAR2 RFP", "NAR2 PwrPro",
        "CIL PCC",
        "TQ1 PCC (Transisi)", "TQ1 OPC - SG", "TQ1 RFP", "TQ1 Type V",
        "TQ2 PCC Regular", "TQ2 Type V", "TQ2 RFP", "TQ2 OPC", "TQ2 PCC (Transisi)",
        "LHO PCC Regular", "LHO OPC"
    ],
    "Plant": [
        "NAR1", "NAR1", "NAR1", "NAR1", "NAR1",
        "NAR1", "NAR1", "NAR2", "NAR2", "NAR2",
        "CIL",
        "TQ1", "TQ1", "TQ1", "TQ1",
        "TQ2", "TQ2", "TQ2", "TQ2", "TQ2",
        "LHO", "LHO"
    ],
    "Cement Production (ton)": [
        93568, 203975, 649126, 1203648, 50770,
        21581, 178172, 2532986, 50428, 0,
        2482850,
        94029, 0, 260539, 380682,
        777580, 0, 260539, 338676, 0,
        1094242, 331684
    ],
    "Clinker Factor (%)": [
        88.50, 94.60, 88.00, 87.30, 96.40,
        93.00, 70.00, 58.00, 91.12, 0.0,
        58.00,
        84.78, 0.0, 86.96, 95.50,
        62.71, 0.0, 86.96, 90.32, 0.0,
        58.50, 85.50
    ]
}

# Load ke DataFrame
df = pd.DataFrame(data)
df["Kode"] = df["Plant"] + " " + df["Tipe"]

# Hitung clinker consumption awal
df["Clinker Consumption (ton)"] = df["Clinker Factor (%)"] * df["Cement Production (ton)"] / 100

# Hitung CF konsolidasi awal
total_clinker_awal = df["Clinker Consumption (ton)"].sum()
total_cement = df["Cement Production (ton)"].sum()
cf_konsolidasi_awal = total_clinker_awal / total_cement * 100

st.title("Simulasi Penyesuaian Clinker Factor Konsolidasi")

# Input dari user
cf_target = st.number_input("Masukkan CF Konsolidasi target (%):", min_value=0.0, max_value=100.0, value=68.0)
semen_dipilih = st.multiselect("Pilih jenis semen yang akan disesuaikan:", df["Kode"].tolist())

if cf_target and semen_dipilih:
    # Hitung klinker total baru
    clinker_target_total = cf_target * total_cement / 100
    gap = total_clinker_awal - clinker_target_total

    # Salin dataframe untuk modifikasi
    df_result = df.copy()

    # Jumlah semen yang dipilih
    n = len(semen_dipilih)
    clinker_per_semen = gap / n

    for kode in semen_dipilih:
        idx = df_result[df_result["Kode"] == kode].index[0]
        clinker_lama = df_result.at[idx, "Clinker Consumption (ton)"]
        semen_produksi = df_result.at[idx, "Cement Production (ton)"]

        clinker_baru = clinker_lama - clinker_per_semen
        cf_baru = clinker_baru / semen_produksi * 100

        df_result.at[idx, "Clinker Consumption (ton)"] = clinker_baru
        df_result.at[idx, "Clinker Factor (%)"] = cf_baru

    # Hitung CF konsolidasi baru
    cf_konsolidasi_baru = df_result["Clinker Consumption (ton)"].sum() / total_cement * 100

    st.subheader("Hasil Simulasi")
    st.dataframe(df_result[["Plant", "Tipe", "Clinker Factor (%)", "Cement Production (ton)", "Clinker Consumption (ton)"]])
    st.success(f"CF Konsolidasi Awal: {cf_konsolidasi_awal:.2f}%")
    st.success(f"CF Konsolidasi Baru: {cf_konsolidasi_baru:.2f}%")
else:
    st.info("Masukkan target CF dan pilih jenis semen yang akan disesuaikan.")