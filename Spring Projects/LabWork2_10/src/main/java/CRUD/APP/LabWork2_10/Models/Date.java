package CRUD.APP.LabWork2_10.Models;

import java.io.Serializable;

public class Date implements Serializable {
    private int id;
    private int day;
    private String month;
    private String desc;

    public Date(int id, int day, String month, String desc){
        this.id = id;
        this.day = day;
        this.month = month;
        this.desc = desc;
    }

    public Date(){

    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getDay() {
        return day;
    }

    public void setDay(int day) {
        this.day = day;
    }

    public String getMonth() {
        return month;
    }

    public void setMonth(String month) {
        this.month = month;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    @Override
    public String toString() {
        return "Date{" +
                "id=" + id +
                ", day=" + day +
                ", month='" + month + '\'' +
                ", desc='" + desc + '\'' +
                '}';
    }
}
