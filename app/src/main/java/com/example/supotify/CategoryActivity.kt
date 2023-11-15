package com.example.supotify

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView

class CategoryActivity : AppCompatActivity() {
    private val categories = arrayOf(
        "Rock", "Pop", "Rap",
        "Classic", "Jazz", "Electro",
        "Soul", "Country", "Reggae",
        "Metal", "Blues", "Folk"
    )

    private val images = arrayOf(
        R.drawable.category_rock,
        R.drawable.category_pop,
        R.drawable.category_rap,
        R.drawable.category_classic,
        R.drawable.category_jazz,
        R.drawable.category_electro,
        R.drawable.category_soul,
        R.drawable.category_country,
        R.drawable.category_reggae,
        R.drawable.category_metal,
        R.drawable.category_blues,
        R.drawable.category_folk
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_category)

        val recyclerView = findViewById<RecyclerView>(R.id.categoryRecyclerView)
        recyclerView.layoutManager = GridLayoutManager(this, 3)
        recyclerView.adapter = CategoryAdapter(categories)
    }
}
