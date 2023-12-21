package com.example.supotify

import android.os.Bundle
import android.widget.ListView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import org.json.JSONObject
import java.net.URL
import android.widget.AdapterView
import android.widget.ArrayAdapter

class PlaylistViewActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_playlist_view)

        val playlistListView = findViewById<ListView>(R.id.playlistListView)

        // Playlist Listesi
        val playlistList = mutableListOf<String>() // Playlist isimleri buraya eklenecek

        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, playlistList)
        playlistListView.adapter = adapter

        // Playlist Listesini Çek ve Göster
        fetchAndDisplayPlaylists()

        // Playliste Tıklanınca Detay Sayfasına Git
        playlistListView.setOnItemClickListener(AdapterView.OnItemClickListener { _, _, position, _ ->
            val selectedPlaylist = playlistList[position]
            // TODO: Detay sayfasına yönlendirme işlemleri burada yapılacak
        })
    }

    private fun fetchAndDisplayPlaylists() {
        GlobalScope.launch(Dispatchers.IO) {
            try {
                val url = URL("http://10.0.2.2:5000/playlist/all")
                val response = url.readText()
                val playlistData = JSONObject(response)

                val playlistArray = playlistData.getJSONArray("playlist_ids")
                val playlistList = mutableListOf<String>()

                for (i in 0 until playlistArray.length()) {
                    val playlistId = playlistArray.getString(i)
                    val playlistInfoUrl = URL("http://10.0.2.2:5000/playlist/$playlistId")
                    val playlistInfoResponse = playlistInfoUrl.readText()
                    val playlistInfoData = JSONObject(playlistInfoResponse)
                    val playlistName = playlistInfoData.getJSONObject("playlist").getString("Name")
                    playlistList.add(playlistName)
                }

                launch(Dispatchers.Main) {
                    val adapter = ArrayAdapter(
                        this@PlaylistViewActivity,
                        android.R.layout.simple_list_item_1,
                        playlistList
                    )
                    val playlistListView = findViewById<ListView>(R.id.playlistListView)
                    playlistListView.adapter = adapter
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}