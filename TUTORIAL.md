# Tutorial: Membangun dApp P2P Dispute Resolution dengan AI di GenLayer

**Repositori Proyek:** [https://github.com/yoiioy700/genlayer-dispute-resolver](https://github.com/yoiioy700/genlayer-dispute-resolver)

Blockchain tradisional hanya bisa mengeksekusi logika deterministik (jika A maka B). Blockchain tersebut tidak bisa menjawab pertanyaan subjektif seperti: *"Apakah pekerjaan ini sudah dilakukan dengan cukup baik dan layak dibayar?"* karena membutuhkan sebuah penilaian.

**GenLayer** mengubah batasan ini dengan memperkenalkan **Intelligent Contracts**, yaitu smart contract berbasis Python yang bisa memanggil LLM (Large Language Model), menelusuri web, dan membuat keputusan yang subjektif, semuanya dicapai melalui konsensus jaringan terdesentralisasi.

Dalam tutorial pengguna GenLayer pemula ini, kita akan membuat aplikasi **P2P Dispute Resolution**—sebuah kontrak arbitrase tanpa perantara pihak ketiga yang diselesaikan oleh konsensus AI.

---

## Part 1: Konsep Optimistic Democracy + Equivalence Principle

Sebelum mulai coding, mari pahami dua konsep inti yang membuat GenLayer sangat berbeda.

### 1.1 Optimistic Democracy Consensus
Di GenLayer, saat kontrak menanyakan bentuk penilaian subjektif (misal: *"Apakah desain logo memuaskan?"*), model AI yang berbeda mungkin memberikan jawaban berbeda.

Konsensus **Optimistic Democracy** berjalan seperti ini:
1. **Leader Validator** mengeksekusi kontrak (memanggil LLM, menelusuri web, dan memberikan hasil).
2. **Follower Validators** secara independen memverifikasi (menjalankan logika yang sama dan membandingkan outputnya dengan milik Leader).
3. Berdasarkan hasil, **Mayoritas Setuju** berarti Transaksi Diterima. Jika Terjadi Ketidaksepakatan, proses Banding (Appeal) akan dipicu.

Sistem ini *optimistic* (dimulai dengan 5 validator agar cepat & murah), *scalable* (bisa ditingkatkan hingga 1.000 validator jika ada sengketa), *AI-native*, dan memberikan insentif/penalti sesuai hasil suara mayoritas.

### 1.2 The Equivalence Principle
Jika AI Validator A berkata *"Ya, pekerjaan memuaskan"* dan AI Validator B berkata *"Ya, hasil sesuai persyaratan"*, mereka sebetulnya sepakat meski kalimatnya beda. 

Sebagai developer, Anda akan mendefinisikan apa arti kata "ekuivalen" untuk setiap operasi non-deterministik. Terdapat dua mode:
- `gl.eq_principle_strict_eq`: Untuk angka atau True/False (jawaban validator harus identik).
- `gl.eq_principle_prompt_comparative`: Untuk teks subjektif. LLM lain akan digunakan untuk menilai apakah jawaban antar validator memiliki makna yang sama.

---

## Part 2: Setup (GenLayer CLI, Studio, dsb)

### 2.1 Prasyarat
Pastikan di sistem Anda sudah terinstal:
- Node.js (v18+)
- Docker (v26+)
- Python (v3.8+)

### 2.2 Install GenLayer CLI
```bash
npm install -g genlayer
genlayer --version
```

### 2.3 Jalankan GenLayer Studio
GenLayer Studio adalah sandbox pengembangan lokal (IDE visual + full GenLayer network via Docker).
```bash
genlayer init   # Setup untuk pertama kali
genlayer up     # Menjalankan Studio
```
Buka browser Anda di **http://localhost:8080** atau gunakan versi hosted di **https://studio.genlayer.com**.

---

## Part 3: Python Contract (Dispute Resolver AI Judgment)

Ini adalah **Intelligent Contract** yang kita buat di repositori: `/contracts/dispute_resolver.py`.

Alur kerjanya:
1. **Employer** membuat komplain dengan bukti (URL).
2. **Worker** memberi pembelaan dengan bukti (URL).
3. Fungsi `resolve_dispute()` dipanggil, AI akan membaca kedua bukti dan menentukan pemenang.
4. Dana langsung dicairkan ke pemenang.

### Potongan Kode Penting:
Di dalam Python, bagian *AI magic* dibungkus dalam blok non-deterministik sebagai plain function:

```python
# Bagian dari file dispute_resolver.py
def ai_judgment() -> str:
    # Membaca web dan informasi dari parameter
    employer_evidence = gl.get_webpage(employer_url, mode="text")
    worker_evidence = gl.get_webpage(worker_url, mode="text")
    
    prompt = f"""Posisikan dirimu sebagai dewan arbitrase netral untuk sengketa ini.
    ... Deskripsi Pekerjaan, Klaim Employer, Pembelaan Worker ...
    Tentukan pemenangnya: EMPLOYER atau WORKER.
    """
    return gl.exec_prompt(prompt)

# Menggunakan Equivalence Principle untuk mencari kesepakatan
verdict = gl.eq_principle_prompt_comparative(
    ai_judgment,
    "Apakah respons tersebut dengan jelas menyatakan EMPLOYER atau WORKER? Kesepakatan dicapai jika mereka memberikan kemenangan pada pihak yang sama."
)
```

Setelah kesepakatan (*verdict*) tercapai oleh mayoritas validator, proses *state update* (menentukan `self.winner`) berjalan secara **deterministik**.

---

## Part 4: Testing di GenLayer Studio

1. Buka GenLayer Studio (**http://localhost:8080**).
2. Klik **"New Contract"**, paste kode `dispute_resolver.py` yang sudah dibuat.
3. Masukkan parameter *constructor* (alamat `worker`, pesan `job_description`, dan `value` sejumlah aset escrow).
4. Klik **Deploy** dan salin *Contract Address* yang dihasilkan.

Sebagai simulasi UI Studio, Anda bisa:
- Memanggil metode `submit_employer_evidence` (dengan URL bukti klaim/keluhan).
- Beralih ke alamat *worker* dan panggil `submit_worker_evidence` (URL bukti laporan kerja).
- Memanggil `resolve_dispute()`. Di panel Studio, 5 simulator AI validator akan berdiskusi. Hasil menang akan tampak di metode `get_dispute_details()` sebagai `status: resolved`.

---

## Part 5: React + genlayer-js frontend

Di folder `/frontend` (Next.js), Anda menggunakan instalasi `genlayer-js`.

```bash
npm install genlayer-js
```

Frontend ini membaca status dari GenLayer menggunakan `@tanstack/react-query` dan menangani *writeContract* layaknya di Web3 biasa, namun terhubung langsung ke Localnet/Testnet.

Contoh konfigurasi `genlayer.ts`:
```typescript
import { createClient, createAccount } from "genlayer-js";
import { localnet } from "genlayer-js/chains";

const account = createAccount();
export const client = createClient({
  chain: localnet,
  account,
});
export const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS as `0x${string}`;
```

Pengguna dapat berinteraksi melampirkan URL, dan dengan tombol *Resolve*, sistem API `genlayer-js` akan berinteraksi menjalankan proses di belakang layar, lalu mengembalikan transaksi ketika setatus sudah `FINALIZED`.

---

## Part 6: Diagram AI Resolution

Apa yang sebenarnya terjadi di belakang ketika Anda meng-klik tombol *"Resolve with AI"*?

```text
Pengguna (Mengeklik Resolve Dispue)
       ↓ 
[genlayer-js] mengirim transaksi ke Jaringan GenLayer
       ↓ 
[Network] Memilih 5 Validators
       ↓ 
Validator 1 (Leader): 
 - Fetches employer_url & worker_url.
 - Memanggil LLM untuk keputusan.
 - Proposes hasilnya: "WORKER menang karena spesifikasi terpenuhi"
       ↓ 
Validator 2-5 (Followers):
 - Fetching independen, juga mengeksekusi LLM-nya masing-masing.
 - Mendapat kesimpulan sejenis yang memenangkan WORKER.
       ↓ 
[Equivalence Principle Check]:
 - Apakah semantic keputusannya sepakat WORKER? Ya. ✓
 - Konsensus tercapai.
       ↓ 
*State Blockchain Diperbarui*
       ↓ 
UI di Frontend otomatis memuat hasil akhir.
```

---

## Part 7: Next Steps & Pengembangan Lanjutan

Selamat! Anda telah memiliki dApp arbitrase fungsional. Beberapa ide untuk pengembangan selanjutnya:

- **Refund Berbasis Deadline**: Fitur *auto-refund* jika bukti tidak dikirimkan ke dalam waktu N-block penciptaan (karena macet).
- **Sistem Appeal**: Menambahkan opsi untuk memperbanyak eskalasi jumlah validator GenLayer.
- **Storage Bukti Secara Desentralisasi**: Menggunakan IPFS (contoh: Pinata) dibandingkan hanya menyalin URL raw.

Dengan alat yang sudah Anda pelajari; ide seperti sistem *AI Oracle*, *P2P Betting Subjektif*, atau *Sistem Reputasi Worker Otomatis* sekarang bisa diwujudkan dengan cerdas di **GenLayer**.

Jangan lupa mengeksplor kode dan berkontribusi langsung ke repositori sumber:
[https://github.com/yoiioy700/genlayer-dispute-resolver](https://github.com/yoiioy700/genlayer-dispute-resolver)