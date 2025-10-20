# DNA/RNA Sequence Analyzer with Tkinter GUI
# Description: Analyzes DNA sequences for GC content, complementary strand,
# RNA transcription, and motif positions. Can plot GC% for multiple genes.

import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt

# ------------------- Core Functions ------------------- #
def gc_content(seq):
    seq = seq.upper()
    gc_count = seq.count('G') + seq.count('C')
    return (gc_count / len(seq)) * 100 if len(seq) > 0 else 0

def complementary_strand(seq):
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join([complement.get(base, base) for base in seq.upper()])

def transcribe_to_rna(seq):
    transcription = {'A': 'U', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join([transcription.get(base, base) for base in seq.upper()])

def find_motifs(seq, motif):
    seq = seq.upper()
    motif = motif.upper()
    positions = []
    for i in range(len(seq) - len(motif) + 1):
        if seq[i:i+len(motif)] == motif:
            positions.append(i + 1)  # 1-based index
    return positions

def plot_gc_content(sequences):
    labels = [f"Gene {i+1}" for i in range(len(sequences))]
    gc_values = [gc_content(seq) for seq in sequences]

    plt.bar(labels, gc_values, color='teal')
    plt.title("GC Content of DNA Sequences")
    plt.xlabel("Gene")
    plt.ylabel("GC Content (%)")
    plt.ylim(0, 100)
    plt.show()

# ------------------- GUI ------------------- #
class DNAAnalyzerGUI: 
    def __init__(self, root): 
        self.root = root 
        self.root.title("DNA/RNA Sequence Analyzer") 
        self.root.geometry("500x500") 
        
        # Input Sequence 
        tk.Label(root, text="Enter DNA Sequence:").pack(pady=5) 
        self.seq_entry = tk.Entry(root, width=50) 
        self.seq_entry.pack(pady=5) 
        
        # Motif 
        tk.Label(root, text="Enter Motif to Find:").pack(pady=5) 
        self.motif_entry = tk.Entry(root, width=20) 
        self.motif_entry.pack(pady=5) 
        
        # Buttons 
        tk.Button(root, text="Analyze Sequence", command=self.analyze_sequence).pack(pady=10) 
        tk.Button(root, text="Plot GC% for Multiple Sequences", command=self.plot_multiple_sequences).pack(pady=10) 
        
        # Results 
        self.result_text = tk.Text(root, height=15, width=60) 
        self.result_text.pack(pady=10)

    
    def analyze_sequence(self):
        seq = self.seq_entry.get().strip().upper()
        motif = self.motif_entry.get().strip().upper()
        
        if not seq:
            messagebox.showerror("Error", "Please enter a DNA sequence.")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"GC Content: {gc_content(seq):.2f}%\n")
        self.result_text.insert(tk.END, f"Complementary Strand: {complementary_strand(seq)}\n")
        self.result_text.insert(tk.END, f"Transcribed RNA: {transcribe_to_rna(seq)}\n")
        
        if motif:
            positions = find_motifs(seq, motif)
            if positions:
                self.result_text.insert(tk.END, f"Motif '{motif}' found at positions: {positions}\n")
            else:
                self.result_text.insert(tk.END, f"Motif '{motif}' not found in the sequence.\n")
    
    def plot_multiple_sequences(self):
        try:
            n = simpledialog.askinteger("Input", "How many sequences?", minvalue=1)
            if not n:
                return
            sequences = []
            for i in range(n):
                seq_i = simpledialog.askstring("Input", f"Enter sequence {i+1}:")
                if seq_i:
                    sequences.append(seq_i.strip())
            if sequences:
                plot_gc_content(sequences)
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")

# ------------------- Run GUI ------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = DNAAnalyzerGUI(root)
    root.mainloop()
