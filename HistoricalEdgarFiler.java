/** 
 * A small program that tells the user about all the filings the SEC's EDGAR 
 * system has about a list of companies the user provides
 * 
 * @author Josh Stowell
 * @since 2016
 * @version 1.0
 */
package com.bigbangboxes.newstrader.companyutils;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class HistoricalEdgarFiler {

    public static void main(String[] args){
        String[] companies = {"aapl", "bby", "hon", "mmm", "msft", "ups", "yhoo"};
        for(String s : companies){
            run(s);
        }
    }
    
    /*Prints out ALL the filings the company has done with the SEC in an excel accessible file*/
    public static void run(String symbol){
        PrintWriter p1 = null;
        try {
            p1 = new PrintWriter("C://datafiles//Edgar//"+symbol+"_filings.csv");
            String stats = "";
            int i = 0;
            
            while(true){
                try {
                    String link = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+symbol+"&type=&dateb=&owner=exclude&start="+i+"&count=40&output=atom";
                    Document doc = Jsoup.connect(link).timeout(3000).get();
                    Elements entries = doc.getElementsByTag("entry");
                    for(Element e : entries){
                        stats += symbol +","+e.getElementsByTag("category").first().attr("term")+",";
                        stats += e.getElementsByTag("updated").first().ownText()+",";
                        p1.println(stats);
                        System.out.println(stats);
                        stats = "";
                    }
                } catch (org.jsoup.HttpStatusException ex) {
                    //you've reached the end of available filings
                    break;
                } catch (IOException ex) {
                    //something with the connection went wrong
                    Logger.getLogger(HistoricalEdgarFiler.class.getName()).log(Level.SEVERE, null, ex);
                    break;
                }
                i+=40;  //increment by 40 because the link has a filing count of 40
            }
        } catch (FileNotFoundException ex) {
            Logger.getLogger(HistoricalEdgarFiler.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            p1.close();
        }
    }    
}
