# Final Project Magang Bayucaraka 2023

## Identitas

Nama : Rigel Ramadhani Waloni

NRP  : 5024221058

## Nama Project

Membuat sistem kontrol drone di Gazebo dengan input dari Webcam yang membaca QR Code.

## Inti Program

Inti dari program yang telah saya buat adalah pada saat sebelum takeoff, webcam akan menyala untuk mencari atau mendeteksi perintah dari QR Code. Jika terdapat suatu QR Code yang terdeteksi, maka program akan mengambil data dari QR Code tersebut, webcam akan mati, dan akan menjalankan perintah yang sesuai dengan data dari QR Code yang telah didapat.

> Jika terbaca **"House"**, maka program akan menampilkan log berupa **"QR Code Detected! Draw a HOUSE!"** dan drone akan bergerak sesuai dengan perintah yang ada di bawahnya. Setelah selesai melakukan semua perintah, webcam akan kembali menyala untuk mencari perintah dari QR Code.

![Sketch Control Drone - Assignment 3(2)(1)(1)](https://user-images.githubusercontent.com/115273885/220659399-9acab8af-81d5-48fd-ac01-2daf77bd2dc2.png)

> Jika terbaca **"Square"**, maka program akan menampilkan log berupa **"QR Code Detected! Draw a SQUARE!"** dan drone akan bergerak sesuai dengan perintah yang ada di bawahnya. Setelah selesai melakukan semua perintah, webcam akan kembali menyala untuk mencari perintah dari QR Code.

![Sketch Control Drone - Assignment 3(3)(1)(1)](https://user-images.githubusercontent.com/115273885/220659448-dda683f5-8ab2-41dc-b9dd-a470cb9a198c.png)

> Jika terbaca **"Stop"**, maka program akan menampilkan log berupa **"QR Code Detected!: Stop!"** dan program akan berhenti mengeksekusi kode dan webcam akan mati.

> Jika terbaca selain dari yang telah disebutkan, maka program akan menampilkan log berupa **"QR Code Detected! {data dari QR Code} - - Sorry, I don't recognize that command. Try another QR Code!"** dan program akan tetap menyalakan webcam hingga mendapatkan data yang sesuai.
