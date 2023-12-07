// SongAdapter.kt
package com.example.supotify

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.TextView


class SongAdapter(context: Context, resource: Int, objects: Array<String>) :
    ArrayAdapter<String>(context, resource, objects) {

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val inflater = context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
        val rowView = inflater.inflate(R.layout.custom_list_item, parent, false)

        // Şarkı adını al
        val song = getItem(position)

        // TextView'e şarkı adını ayarla
        val songTextView = rowView.findViewById<TextView>(R.id.text1)
        songTextView.text = song

        return rowView
    }
}
