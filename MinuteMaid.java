/** 
 * MinuteMaid class has methods to file the minute data one might read from a
 * Yahoo Finance chart for a list of specific companies. 
 * Running as is will file today's data for company ticker symbols listed at 
 * C:\datafiles\stockList.txt within the datafiles directory in .dat format.
 * Missing data is averaged over the missing period.
 * 
 * @author Josh Stowell
 * @since 2016
 * @version 1.0
 */

package minutedataapp;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.text.DecimalFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.json.*;


public class MinuteMaid {
    static DecimalFormat df = new DecimalFormat("#.00"); 
    static String DATAHOME = "C:\\datafiles\\";
    
    public static void main(String[] args) {
        MinuteMaid.doFilingList();
    }

    
    public static void doFilingList(){
        try {
            FileReader fr = new FileReader(DATAHOME+"stockList.txt");
            BufferedReader br = new BufferedReader(fr);
            String ticker;
            while((ticker = br.readLine()) != null){
                fileMinuteData(ticker);
            }
            
            br.close();
            fr.close();
        } catch (FileNotFoundException ex) {
            //Logger.getLogger(MinuteMaid.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println(ex.getMessage()+". Filing data for AAPL only");
            fileMinuteData("AAPL");
        } catch (IOException ex) {
            Logger.getLogger(MinuteMaid.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    public static void fileMinuteData(String ticker){
        String closes = getClosesString(getMinuteTicks(ticker));
        ticker = ticker.replaceAll("^", "");
        File dataFile = new File(DATAHOME+ticker+".dat");
        BufferedWriter bw;
        FileWriter fw;
                    
        try {    
            fw = new FileWriter(dataFile,true);
            bw = new BufferedWriter(fw);
            bw.write(closes);
            bw.close();		
            fw.close();     
        } catch (Exception ex) {
        }
    }

    public static JSONArray getMinuteTicks(String ticker) {
        JSONArray arr = null;
        try {
            URL url = new URL("http://chartapi.finance.yahoo.com/instrument/1.0/"+ticker+"/chartdata;type=quote;range=1d/json?callback=mycallback");
            InputStream input = url.openStream();
            String response = convertStreamToString(input);
            response = response.substring(12, response.length()-2);
            JSONObject obj = new JSONObject(response);
            arr = obj.getJSONArray("series");
            
        } catch (Exception ex) {
            System.out.println("error: "+ticker);
        }

        return arr;        
    }
    
    public static String convertStreamToString(InputStream is) {
        java.util.Scanner s = new java.util.Scanner(is).useDelimiter("\\A");
        return s.hasNext() ? s.next() : "";
    }
    
    public static String getClosesString(JSONArray jsonCloses){
        Double ticks[] = new Double[391];
        for(int i =0; i<ticks.length; i++){
            ticks[i] = 0.0;
        }
        String result = "";
        Double price;
        LocalDateTime tickTime;

        
        for(int i = 0; i< jsonCloses.length(); i++){
            price = Double.parseDouble(jsonCloses.getJSONObject(i).get("close").toString());
            tickTime = LocalDateTime.ofInstant(Instant.ofEpochSecond(Long.parseLong(jsonCloses.getJSONObject(i).get("Timestamp").toString())), ZoneId.systemDefault());
            
            if(jsonCloses.length()>300){
                ticks[fullDayTimeToPosition(tickTime)] = price;
            }
        }   
            
        ticks = averageMissingValues(ticks);
        
        for (Double tick : ticks) {
            result += String.format("%.2f", tick) + "\n";
        }
        
        
        return result;
    }

    
    public static int fullDayTimeToPosition(LocalDateTime time){
        int hour = time.getHour() - 8;
        int minute = time.getMinute() + 60 * hour - 30;
        return minute;
    }
    
    public static Double[] averageMissingValues(Double[] ticks){
        for(int i =0; i<ticks.length; i++){
            if(ticks[i]==0.0){
                int j = i;
                int a = j;
                int b = j;
                while(a!=0 && ticks[a]==0.0){
                    a--;
                }
                while(b!=390 && ticks[b]==0.0){
                    b++;
                }
                
                if(a==0 && b==390){
                    //leave them at 0.0 
                }else if(a==0 && b!=390){
                    while(b!=0){
                        ticks[b-1] = ticks[b--];
                    }
                }else if(a!=0 && b==390){
                    while(a!=390){
                        ticks[a+1] = ticks[a++];
                    }
                }else if(a!=0 && b!= 390){
                    int gapWidth = b-a;
                    Double aPrice = ticks[a];
                    Double bPrice = ticks[b];
                    Double difference = bPrice - aPrice;
                    Double increment = difference/gapWidth;
                    while(a!=b){
                        ticks[a+1] = ticks[a]+increment;
                        a++;
                    }
                }
            }
        }
        
        return ticks;
    }
}