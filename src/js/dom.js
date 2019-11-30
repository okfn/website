$(document).ready(function() {
  // menus
  $("#mmenu").mmenu({
     // options
     searchfield: true,
     extensions: [
       "position-right",
       "theme-dark"
     ]
  }, {
     // configuration
     classNames: {
       selected: "active"
     }
  });
  $("#side-nav").mmenu({
     // options
     offCanvas: false,
     autoHeight: true
  }, {
     // configuration
     classNames: {
       selected: "active"
     }
  });


  // show / hide search bar
  $('#display-search-bar').on('click', function () {
      $('#main-search-bar').addClass("active");
  });
  $('#main-search-bar .cancel').on('click', function (event) {
      event.preventDefault();
      $('#main-search-bar').removeClass("active");
  });


  // external links
  $('a[rel*=external]').click(function () {
      window.open(this.href);
      return false;
  });
});
