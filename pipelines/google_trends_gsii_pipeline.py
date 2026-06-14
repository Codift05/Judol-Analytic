from __future__ import annotations

import argparse
import importlib
import importlib.util
import os
import re
import warnings
from pathlib import Path
from typing import Any

Path("outputs/.matplotlib").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(Path("outputs") / ".matplotlib"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


DEFAULT_INPUT = Path("Dataset/time_series_ID_20200101-0000_20260614-1837.csv")
OUTPUT_DIR = Path("outputs")
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"
PROCESSED_DIR = OUTPUT_DIR / "processed"

PRIMARY_KEYWORDS = ["slot_gacor", "judi_slot", "judi_online"]
RANDOM_STATE = 42


def ensure_output_dirs() -> None:
    for directory in [FIGURES_DIR, TABLES_DIR, PROCESSED_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def detect_google_trends_header(csv_path: Path) -> int:
    """Find the first likely tabular header row in Google Trends exports."""
    with csv_path.open("r", encoding="utf-8-sig", errors="replace") as file:
        for row_number, line in enumerate(file):
            normalized = line.strip().lower().replace('"', "")
            first_cell = normalized.split(",")[0].strip()
            if first_cell in {"time", "date", "tanggal", "minggu", "bulan"}:
                return row_number
    return 0


def clean_column_name(column: str) -> str:
    column = str(column).strip().lower()
    column = re.sub(r"\s*:\s*\([^)]*\)\s*$", "", column)
    column = re.sub(r"[^0-9a-zA-Z]+", "_", column)
    column = re.sub(r"_+", "_", column).strip("_")
    return column


def load_google_trends_csv(csv_path: Path) -> pd.DataFrame:
    header_row = detect_google_trends_header(csv_path)
    df = pd.read_csv(csv_path, skiprows=header_row)
    df = df.dropna(axis=1, how="all")
    df.columns = [clean_column_name(column) for column in df.columns]

    date_candidates = ["time", "date", "tanggal", "bulan", "minggu"]
    date_column = next((column for column in date_candidates if column in df.columns), None)
    if date_column is None:
        date_column = df.columns[0]

    df = df.rename(columns={date_column: "date"})
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)

    keyword_columns = [column for column in df.columns if column != "date"]
    for column in keyword_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.replace("<1", "0", regex=False)
            .str.replace(",", ".", regex=False)
            .str.replace("%", "", regex=False)
            .str.strip()
        )
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def print_dataset_overview(df: pd.DataFrame) -> None:
    print("\n=== 5 Data Awal ===")
    print(df.head())

    print("\n=== Informasi Dataset ===")
    print(f"Jumlah baris: {len(df)}")
    print(f"Jumlah kolom: {len(df.columns)}")
    print("\nKolom dan tipe data:")
    print(df.dtypes)
    print("\nMissing value per kolom:")
    print(df.isna().sum())


def build_keyword_summary(df: pd.DataFrame) -> pd.DataFrame:
    keyword_columns = [column for column in df.columns if column != "date"]
    summary = pd.DataFrame(
        {
            "mean": df[keyword_columns].mean(),
            "median": df[keyword_columns].median(),
            "std": df[keyword_columns].std(),
            "max": df[keyword_columns].max(),
            "non_zero_count": (df[keyword_columns] != 0).sum(),
        }
    )
    min_non_zero = max(3, int(np.ceil(len(df) * 0.1)))
    summary["recommended_for_model"] = summary["non_zero_count"] >= min_non_zero
    summary = summary.sort_values(["recommended_for_model", "non_zero_count", "mean"], ascending=False)
    return summary


def plot_keyword_trends(df: pd.DataFrame) -> None:
    keyword_columns = [column for column in df.columns if column != "date"]

    plt.figure(figsize=(14, 7))
    for column in keyword_columns:
        plt.plot(df["date"], df[column], linewidth=1.8, label=column)
    plt.title("Tren Interest Over Time Keyword Judi Online")
    plt.xlabel("Tanggal")
    plt.ylabel("Interest")
    plt.legend(ncol=2, fontsize=9)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "keyword_trends_all.png", dpi=300)
    plt.close()

    for column in keyword_columns:
        plt.figure(figsize=(12, 4.5))
        plt.plot(df["date"], df[column], marker="o", linewidth=1.8)
        plt.title(f"Tren Waktu: {column}")
        plt.xlabel("Tanggal")
        plt.ylabel("Interest")
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / f"trend_{column}.png", dpi=300)
        plt.close()


def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    keyword_columns = [column for column in df.columns if column != "date"]
    corr = df[keyword_columns].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="RdYlBu_r", center=0, fmt=".2f", linewidths=0.5)
    plt.title("Heatmap Korelasi Antar Keyword")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "keyword_correlation_heatmap.png", dpi=300)
    plt.close()


def add_gsii(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    available_primary = [column for column in PRIMARY_KEYWORDS if column in df.columns]
    if not available_primary:
        available_primary = [
            column
            for column in df.columns
            if column != "date" and (df[column] != 0).sum() >= max(3, int(np.ceil(len(df) * 0.1)))
        ]
    if not available_primary:
        raise ValueError("Tidak ada kolom keyword yang cukup valid untuk membentuk GSII.")

    df = df.copy()
    df["GSII"] = df[available_primary].mean(axis=1)
    return df, available_primary


def create_time_series_features(df: pd.DataFrame) -> pd.DataFrame:
    featured = df[["date", "GSII"]].copy()
    featured["lag_1"] = featured["GSII"].shift(1)
    featured["lag_2"] = featured["GSII"].shift(2)
    featured["lag_3"] = featured["GSII"].shift(3)
    featured["rolling_mean_3"] = featured["GSII"].shift(1).rolling(window=3).mean()
    featured["rolling_std_3"] = featured["GSII"].shift(1).rolling(window=3).std()
    featured["month"] = featured["date"].dt.month
    featured["year"] = featured["date"].dt.year
    featured["target_next_month"] = featured["GSII"].shift(-1)
    return featured.dropna().reset_index(drop=True)


def mean_absolute_percentage_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    non_zero_mask = y_true != 0
    if not np.any(non_zero_mask):
        return float("nan")
    mape = np.mean(np.abs((y_true[non_zero_mask] - y_pred[non_zero_mask]) / y_true[non_zero_mask])) * 100
    return float(mape)


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "MAPE": mean_absolute_percentage_error(y_true, y_pred),
    }


def fit_optional_booster(model_name: str, X_train: pd.DataFrame, y_train: pd.Series) -> Any | None:
    if model_name == "XGBoost":
        if importlib.util.find_spec("xgboost") is None:
            print("XGBoost belum terinstall. Untuk memakai model ini: pip install xgboost lightgbm")
            return None
        XGBRegressor = importlib.import_module("xgboost").XGBRegressor

        model = XGBRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=3,
            subsample=0.9,
            colsample_bytree=0.9,
            objective="reg:squarederror",
            random_state=RANDOM_STATE,
        )
    elif model_name == "LightGBM":
        if importlib.util.find_spec("lightgbm") is None:
            print("LightGBM belum terinstall. Untuk memakai model ini: pip install xgboost lightgbm")
            return None
        LGBMRegressor = importlib.import_module("lightgbm").LGBMRegressor

        model = LGBMRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=3,
            random_state=RANDOM_STATE,
            verbosity=-1,
        )
    else:
        raise ValueError(f"Model opsional tidak dikenal: {model_name}")

    model.fit(X_train, y_train)
    return model


def fit_model_by_name(model_name: str, X_train: pd.DataFrame, y_train: pd.Series) -> Any | None:
    if model_name == "Random_Forest":
        model = RandomForestRegressor(
            n_estimators=300,
            max_depth=6,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
        )
        model.fit(X_train, y_train)
        return model
    if model_name in {"XGBoost", "LightGBM"}:
        return fit_optional_booster(model_name, X_train, y_train)
    if model_name == "Baseline_Naive":
        return None
    raise ValueError(f"Model tidak dikenal: {model_name}")


def train_and_evaluate(featured: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    feature_columns = ["GSII", "lag_1", "lag_2", "lag_3", "rolling_mean_3", "rolling_std_3", "month", "year"]
    split_index = int(len(featured) * 0.8)
    train = featured.iloc[:split_index].copy()
    test = featured.iloc[split_index:].copy()

    if train.empty or test.empty:
        raise ValueError("Data tidak cukup untuk time-based split 80:20.")

    X_train = train[feature_columns]
    y_train = train["target_next_month"]
    X_test = test[feature_columns]
    y_test = test["target_next_month"]

    predictions: dict[str, np.ndarray] = {
        "Baseline_Naive": test["GSII"].to_numpy(),
    }

    rf_model = RandomForestRegressor(
        n_estimators=300,
        max_depth=6,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
    )
    rf_model.fit(X_train, y_train)
    predictions["Random_Forest"] = rf_model.predict(X_test)

    for model_name in ["XGBoost", "LightGBM"]:
        model = fit_optional_booster(model_name, X_train, y_train)
        if model is not None:
            predictions[model_name] = model.predict(X_test)

    evaluation_rows = []
    prediction_table = test[["date", "GSII", "target_next_month"]].copy()
    for model_name, y_pred in predictions.items():
        metrics = evaluate_predictions(y_test.to_numpy(), y_pred)
        evaluation_rows.append({"Model": model_name, **metrics})
        prediction_table[f"pred_{model_name}"] = y_pred

    evaluation = pd.DataFrame(evaluation_rows).sort_values(["RMSE", "MAE"], ascending=True)
    best_model = evaluation.iloc[0]["Model"]
    return evaluation, prediction_table, best_model


def plot_predictions(prediction_table: pd.DataFrame, best_model: str) -> None:
    model_columns = [column for column in prediction_table.columns if column.startswith("pred_")]

    for column in model_columns:
        model_name = column.replace("pred_", "")
        plt.figure(figsize=(12, 5))
        plt.plot(
            prediction_table["date"],
            prediction_table["target_next_month"],
            marker="o",
            linewidth=2,
            label="Aktual bulan depan",
        )
        plt.plot(prediction_table["date"], prediction_table[column], marker="s", linewidth=2, label=f"Prediksi {model_name}")
        plt.title(f"Aktual vs Prediksi GSII: {model_name}")
        plt.xlabel("Tanggal observasi")
        plt.ylabel("GSII bulan depan")
        plt.legend()
        plt.tight_layout()
        plt.savefig(FIGURES_DIR / f"actual_vs_prediction_{model_name}.png", dpi=300)
        plt.close()

    best_column = f"pred_{best_model}"
    plt.figure(figsize=(13, 5.5))
    plt.plot(prediction_table["date"], prediction_table["target_next_month"], marker="o", linewidth=2.4, label="Aktual bulan depan")
    plt.plot(prediction_table["date"], prediction_table[best_column], marker="s", linewidth=2.4, label=f"Prediksi {best_model}")
    plt.title(f"Model Terbaik: {best_model}")
    plt.xlabel("Tanggal observasi")
    plt.ylabel("GSII bulan depan")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "best_model_actual_vs_prediction.png", dpi=300)
    plt.close()


def build_latest_feature_row(df_gsii: pd.DataFrame) -> pd.DataFrame:
    if len(df_gsii) < 4:
        raise ValueError("Minimal diperlukan 4 baris data untuk membuat fitur prediksi bulan berikutnya.")

    latest = df_gsii.iloc[-1]
    recent_gsii = df_gsii["GSII"].iloc[-4:]
    return pd.DataFrame(
        [
            {
                "GSII": latest["GSII"],
                "lag_1": df_gsii["GSII"].iloc[-2],
                "lag_2": df_gsii["GSII"].iloc[-3],
                "lag_3": df_gsii["GSII"].iloc[-4],
                "rolling_mean_3": recent_gsii.iloc[:3].mean(),
                "rolling_std_3": recent_gsii.iloc[:3].std(),
                "month": latest["date"].month,
                "year": latest["date"].year,
            }
        ]
    )


def forecast_next_month(df_gsii: pd.DataFrame, featured: pd.DataFrame, best_model: str) -> float:
    latest_feature_row = build_latest_feature_row(df_gsii)
    if best_model == "Baseline_Naive":
        return float(latest_feature_row["GSII"].iloc[0])

    feature_columns = ["GSII", "lag_1", "lag_2", "lag_3", "rolling_mean_3", "rolling_std_3", "month", "year"]
    model = fit_model_by_name(best_model, featured[feature_columns], featured["target_next_month"])
    if model is None:
        return float(latest_feature_row["GSII"].iloc[0])
    return float(model.predict(latest_feature_row[feature_columns])[0])


def create_early_warning(df_gsii: pd.DataFrame, featured: pd.DataFrame, best_model: str) -> pd.DataFrame:
    latest_current_gsii = float(df_gsii["GSII"].iloc[-1])
    next_month_prediction = forecast_next_month(df_gsii, featured, best_model)

    if latest_current_gsii == 0:
        percent_change = np.inf if next_month_prediction > 0 else 0.0
    else:
        percent_change = ((next_month_prediction - latest_current_gsii) / latest_current_gsii) * 100

    if percent_change >= 40:
        status = "Tinggi"
    elif percent_change >= 20:
        status = "Waspada"
    elif percent_change > 0:
        status = "Perhatian"
    else:
        status = "Normal"

    next_month = df_gsii["date"].iloc[-1] + pd.DateOffset(months=1)
    warning = pd.DataFrame(
        [
            {
                "date_current": df_gsii["date"].iloc[-1],
                "date_forecast": next_month,
                "model": best_model,
                "current_GSII": latest_current_gsii,
                "predicted_next_month_GSII": next_month_prediction,
                "predicted_change_percent": percent_change,
                "warning_status": status,
            }
        ]
    )
    return warning


def run_pipeline(input_csv: Path) -> None:
    ensure_output_dirs()
    sns.set_theme(style="whitegrid")
    warnings.filterwarnings("ignore", category=UserWarning)

    print(f"Memuat dataset: {input_csv}")
    df = load_google_trends_csv(input_csv)
    print_dataset_overview(df)

    keyword_summary = build_keyword_summary(df)
    print("\n=== Statistik Deskriptif Keyword ===")
    print(keyword_summary)
    keyword_summary.to_csv(TABLES_DIR / "keyword_summary.csv", index_label="keyword")

    plot_keyword_trends(df)
    plot_correlation_heatmap(df)

    df_gsii, gsii_columns = add_gsii(df)
    print("\nKolom pembentuk GSII:", ", ".join(gsii_columns))
    df_gsii.to_csv(PROCESSED_DIR / "google_trends_gsii.csv", index=False)

    featured = create_time_series_features(df_gsii)
    featured.to_csv(PROCESSED_DIR / "google_trends_gsii_features.csv", index=False)

    evaluation, prediction_table, best_model = train_and_evaluate(featured)
    evaluation.to_csv(TABLES_DIR / "model_evaluation.csv", index=False)
    prediction_table.to_csv(TABLES_DIR / "model_predictions.csv", index=False)
    print("\n=== Evaluasi Model ===")
    print(evaluation)
    print(f"\nModel terbaik berdasarkan RMSE: {best_model}")

    plot_predictions(prediction_table, best_model)

    warning = create_early_warning(df_gsii, featured, best_model)
    warning.to_csv(TABLES_DIR / "early_warning_status.csv", index=False)
    print("\n=== Early Warning ===")
    print(warning)

    print("\nOutput tersimpan di:")
    print(f"- {PROCESSED_DIR / 'google_trends_gsii.csv'}")
    print(f"- {PROCESSED_DIR / 'google_trends_gsii_features.csv'}")
    print(f"- {TABLES_DIR / 'keyword_summary.csv'}")
    print(f"- {TABLES_DIR / 'model_evaluation.csv'}")
    print(f"- {TABLES_DIR / 'model_predictions.csv'}")
    print(f"- {TABLES_DIR / 'early_warning_status.csv'}")
    print(f"- {FIGURES_DIR}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline Google Trends GSII untuk early warning judi online.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path file CSV Google Trends. Default: {DEFAULT_INPUT}",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args.input)
