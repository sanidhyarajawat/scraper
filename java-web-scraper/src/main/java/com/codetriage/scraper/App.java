package com.codetriage.scraper;

import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class App {

  public static void main(String[] args) {

    try {
      //Create Jsoup object
      Document doc = Jsoup.connect("https://www.techmeme.com/events").get();
      
      //Fetch title
      System.out.printf("\nWebsite Title: %s\n\n", doc.title());

      // Get events row
      Elements events = doc.getElementsByClass("rhov");

      for (Element event : events) {
        Elements divs = event.getElementsByTag("div");
        System.out.println("==================================================");
        System.out.println("EVENT DATE: "+divs.get(1).text());
        System.out.println("EVENT NAME: "+divs.get(2).text());
        System.out.println("EVENT LOCATION: "+divs.get(3).text());
      }

    } catch (IOException e) {
      e.printStackTrace();
    }

  }
}
