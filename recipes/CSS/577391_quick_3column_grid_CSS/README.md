## quick 3-column grid CSS  
Originally published: 2010-09-15 17:13:25  
Last updated: 2010-09-15 17:13:26  
Author: Trent Mick  
  
CSS snippet for a 3-column grid. Based on that used for some Apple product pages.

HTML:

    <div class="grid3col">
      <div class="column first">
        ...
      </div>
      <div class="column">
        ...
      </div>
      <div class="column last">
        ...
      </div>
    </div>

In general, you have to recalculate the widths based on (a) the available full width in your pages and (b) the amount a spacing you want between columns.