# app_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def merge_csv(files, output_path, sort_col="timeStamp"):
    dfs = []
    for f in files:
        try:
            dfs.append(pd.read_csv(f))
        except Exception as e:
            messagebox.showerror("오류", f"{f} 읽는 중 오류 발생:\n{e}")
            return

    if len(dfs) < 2:
        messagebox.showerror("오류", "최소 2개의 CSV 파일을 선택해야 합니다.")
        return

    df_all = pd.concat(dfs, ignore_index=True)

    if sort_col in df_all.columns:
        df_all = df_all.sort_values(sort_col)

    try:
        df_all.to_csv(output_path, index=False)
        messagebox.showinfo("완료", f"병합 완료!\n\n저장 경로: {output_path}")
    except Exception as e:
        messagebox.showerror("오류", f"파일 저장 실패:\n{e}")

def open_gui():
    root = tk.Tk()
    root.title("CSV 병합 도구")
    root.geometry("480x320")
    root.resizable(False, False)

    files = []

    def select_files():
        nonlocal files
        files = filedialog.askopenfilenames(
            title="병합할 CSV 파일 선택",
            filetypes=[("CSV files", "*.csv")]
        )
        file_list.delete(0, tk.END)
        for f in files:
            file_list.insert(tk.END, os.path.basename(f))

    def select_output():
        output_path = filedialog.asksaveasfilename(
            title="결과 파일 저장",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_path)

    def run_merge():
        output_path = output_entry.get()
        sort_col = sort_entry.get().strip() or "timeStamp"

        if not files:
            messagebox.showerror("오류", "CSV 파일을 선택하세요.")
            return
        if not output_path:
            messagebox.showerror("오류", "결과 파일 저장 경로를 지정하세요.")
            return
        merge_csv(files, output_path, sort_col)

    # UI 구성
    tk.Label(root, text="CSV 병합 도구", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(root, text="CSV 파일 선택", command=select_files).pack()

    file_list = tk.Listbox(root, height=5, width=60)
    file_list.pack(pady=5)

    tk.Label(root, text="정렬 기준 컬럼명 (기본값: timeStamp)").pack()
    sort_entry = tk.Entry(root)
    sort_entry.pack(pady=2)

    tk.Button(root, text="결과 파일 경로 지정", command=select_output).pack(pady=3)
    output_entry = tk.Entry(root, width=50)
    output_entry.pack()

    tk.Button(root, text="병합 실행", command=run_merge, bg="#4CAF50", fg="white").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    open_gui()
