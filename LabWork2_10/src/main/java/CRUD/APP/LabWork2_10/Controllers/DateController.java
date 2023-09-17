package CRUD.APP.LabWork2_10.Controllers;

import CRUD.APP.LabWork2_10.DAO.DateDAO;
import CRUD.APP.LabWork2_10.Models.Date;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/dates")
public class DateController {
    private final DateDAO dateDAO = new DateDAO();

    @GetMapping()
    public String index(Model model){
        model.addAttribute("dates", dateDAO.index());
        return "dates/index";
    }
    @GetMapping("/{id}")
    public String show(@PathVariable("id") int id, Model model){
        model.addAttribute("date", dateDAO.show(id));
        return "dates/show";
    }
    @GetMapping("/new")
    public String newDate(Model model){
        model.addAttribute("date", new Date());
        return "dates/new";
    }
    @PostMapping()
    public String create(@ModelAttribute("date") Date date){
        dateDAO.save(date);
        return "redirect:/dates";
    }
    @GetMapping("/{id}/edit")
    public String edit(Model model, @PathVariable("id") int id){
        model.addAttribute("date",dateDAO.show(id));
        return "dates/edit";
    }
    @PostMapping("/{id}")
    public String update(@ModelAttribute("date") Date date, @PathVariable("id") int id){
        dateDAO.update(id,date);
        return "redirect:/dates";
    }
    @DeleteMapping("/{id}")
    public String delete(@PathVariable("id") int id){
        dateDAO.delete(id);
        return "redirect:/dates";
    }
}
