$(document).ready(function() {
  // $('td:nth-of-type(6):not(:contains("1"))').css('font-weight', 'bold');
  // $('td:nth-of-type(6):contains("10")').css('font-weight', 'bold');
  $(".dataframe td:nth-child(6)").each(function() {
    if (parseInt($(this).html()) > 1) {
      $(this).css({
        "font-size": "140%",
        "font-weight": "bold"
      });
    }
  });
});
$(document).ready(function() {
  $(".dataframe td:nth-child(3)").each(function() {
    let html = $(this).html();
    let eans = html.split(/[ ,]+/);
    $(this).html(
      eans
        .map(
          e =>
            `${e.substr(
              0,
              e.length - 4
            )}<span style='font-weight: bold; font-size: 140%'>${e.substr(
              -4
            )}</span>`
        )
        .join(" ")
    );
  });
});
$(document).ready(function() {
  $("tr td:nth-child(2)").each(function() {
    var t = $(this);
    var n = t.next();
    t.html(t.html() + "<br>" + n.html());
    n.remove();
  });
});
$(document).ready(function() {
  $("tr th:nth-child(3)").each(function() {
    var t = $(this);
    // var n = t.next()
    t.remove();
  });
});
$(document).ready(function() {
  $(".dataframe td:nth-child(4)").each(function() {
    if ($(this).html() == "KOMPL") {
      $(this).css("font-weight", "bold");
    }
    if ($(this).html() == "GAR") {
      $(this).css("font-weight", "bold");
    }
    if ($(this).html() == "BIOS Update") {
      $(this).css("font-weight", "bold");
    }
    if ($(this).html() == "OTSE") {
      $(this).css("font-weight", "bold");
    }
    if ($(this).html() == "EXTRA") {
      $(this).css("font-weight", "bold");
    }
    if ($(this).html() == "ILJA") {
      $(this).css("font-weight", "bold");
    }
  });
});
