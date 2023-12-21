// PodcastViewActivity.kt
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

class PodcastViewActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_podcast_view)

        val podcastListView = findViewById<ListView>(R.id.podcastListView)

        // Podcast Listesi
        val podcastList = mutableListOf<String>() // Podcast isimleri buraya eklenecek

        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, podcastList)
        podcastListView.adapter = adapter

        // Podcast Listesini Çek ve Göster
        fetchAndDisplayPodcasts()

        // Podcaste Tıklanınca Detay Sayfasına Git
        podcastListView.setOnItemClickListener(AdapterView.OnItemClickListener { _, _, position, _ ->
            val selectedPodcast = podcastList[position]
            // TODO: Detay sayfasına yönlendirme işlemleri burada yapılacak
        })
    }

    private fun fetchAndDisplayPodcasts() {
        GlobalScope.launch(Dispatchers.IO) {
            try {
                val url = URL("http://10.0.2.2:5000/podcast/all")
                val response = url.readText()
                val podcastData = JSONObject(response)

                val podcastArray = podcastData.getJSONArray("podcast_ids")
                val podcastList = mutableListOf<String>()

                for (i in 0 until podcastArray.length()) {
                    val podcastId = podcastArray.getString(i)
                    val podcastInfoUrl = URL("http://10.0.2.2:5000/podcast/$podcastId")
                    val podcastInfoResponse = podcastInfoUrl.readText()
                    val podcastInfoData = JSONObject(podcastInfoResponse)
                    val podcastName = podcastInfoData.getJSONObject("podcast").getString("Name")
                    podcastList.add(podcastName)
                }

                launch(Dispatchers.Main) {
                    val adapter = ArrayAdapter(
                        this@PodcastViewActivity,
                        android.R.layout.simple_list_item_1,
                        podcastList
                    )
                    val podcastListView = findViewById<ListView>(R.id.podcastListView)
                    podcastListView.adapter = adapter
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
