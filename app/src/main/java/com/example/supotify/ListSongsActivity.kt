package com.example.supotify

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ListView
import android.widget.TextView
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity

class ListSongsActivity : AppCompatActivity() {

    private lateinit var songAdapter: SongAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_listsongs)
        supportActionBar?.title = "SUpotify"

        val songList = findViewById<ListView>(R.id.songList)
        val addSongButton = findViewById<Button>(R.id.addSongButton)

        // Manuel olarak şarkıları ekleyin
        val songs = arrayOf(
            "Enerci - Dilan Polat",
            "Hele Bi (Club Version) - Alişan",
            "Başıma Belasın - Aleyna Tilki",
            "Bellydancing - INJI",
            "Sarışınlar Çat - Mert Kurt",
            "İki Hece - Berkay",
            "Tövbe - Derya Bedavacı",
            "Heated - Beyonce",
            "Hata - Tan Taşçı",
            "Biz Burdayız - Hadise",
            "Uzaktan - Göksel",
            "Gölge - Demet Akalın",
            "Bana Anlat - Hande Yener",
            "Kuzu Kuzu - Tarkan"
            // Daha fazla şarkı ekleyin
        )

        // Özel ArrayAdapter'ı oluşturun
        songAdapter = SongAdapter(this, R.layout.custom_list_item, songs)
        songList.adapter = songAdapter

        // Liste öğelerine tıklanıldığında bir işlem yapmak için listener ekleyin
        songList.setOnItemClickListener { _, _, position, _ ->
            val selectedSong = songs[position]
            showSongDetailsDialog(selectedSong)
        }

        // "Add Song" butonuna tıklama işlemini dinle
        addSongButton.setOnClickListener {
            openAddSongActivity()
        }
    }

    private fun showSongDetailsDialog(song: String) {
        // Özel bir layout dosyası kullanarak AlertDialog oluşturun
        val inflater = layoutInflater
        val dialogLayout = inflater.inflate(R.layout.custom_alert_dialog, null)

        val songTextView = dialogLayout.findViewById<TextView>(R.id.songTextView)
        songTextView.text = "Selected Song: $song"

        val builder = AlertDialog.Builder(this, R.style.AlertDialogCustom)
            .setView(dialogLayout)
            .setPositiveButton("OK") { dialog, _ ->
                dialog.dismiss()
            }

        val alert: AlertDialog = builder.create()
        alert.setTitle("Song Details")
        alert.show()
    }

    private fun openAddSongActivity() {
        val intent = Intent(this, AddSongActivity::class.java)
        startActivity(intent)
    }
}
