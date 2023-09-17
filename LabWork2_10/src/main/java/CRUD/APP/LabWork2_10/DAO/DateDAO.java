package CRUD.APP.LabWork2_10.DAO;

import CRUD.APP.LabWork2_10.Models.Date;
import CRUD.APP.LabWork2_10.Models.Month;

import java.util.*;

public class DateDAO {
    private static int DATE_COUNT;
    TreeSet<Date> dateComp = new TreeSet<>(new Comparator<Date>() {
        @Override
        public int compare(Date o1, Date o2) {
            if ((Month.valueOf(String.valueOf(o1.getMonth())).ordinal()) > (Month.valueOf(String.valueOf(o2.getMonth())).ordinal())){
                return 1;
            } else if ((Month.valueOf(String.valueOf(o1.getMonth())).ordinal()) < (Month.valueOf(String.valueOf(o2.getMonth())).ordinal())){
                return -1;
            } else{
                if (o1.getDay() > o2.getDay()){
                    return 1;
                } else if (o1.getDay() < o2.getDay()){
                    return -1;
                } else return 0;
            }
        }
    });
    private List<Date> dates;
    {
        dates = new ArrayList<>();
        dates.add(new Date(++DATE_COUNT, 9, "MAY", "Day of Victory"));
        dates.add(new Date(++DATE_COUNT, 25, "DEC", "Birthday"));
        dates.add(new Date(++DATE_COUNT, 1, "MAY", "Labor Day"));
        dates.add(new Date(++DATE_COUNT, 1, "JAN", "New Year"));
        dateComp.addAll(dates);
        dates.removeAll(dates);
        dates.addAll(dateComp);
    }

    public List<Date> index(){
        return dates;
    }

    public Date show(int id){
        return dates.stream().filter(date -> date.getId() == id).findAny().orElse(null);
    }

    public void save(Date date){
        System.out.println(date);
        date.setId(++DATE_COUNT);
        dateComp.add(date);
        dates.removeAll(dates);
        dates.addAll(dateComp);
    }

    public void update(int id, Date date){
        Date upDate = show(id);
        delete(id);
        upDate.setDay(date.getDay());
        upDate.setMonth(date.getMonth());
        upDate.setDesc(date.getDesc());
        dateComp.add(upDate);
        dates.removeAll(dates);
        dates.addAll(dateComp);
    }

    public void delete(int id){
        dateComp.removeIf(date -> date.getId()==id);
        dates.removeIf(date -> date.getId()==id);
    }
}
