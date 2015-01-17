function create_group_callback( json ) {
  console.log(json)
}
function add_user_callback( json ) {
  $("#user-name").html(json["userName"]);
  var storage = window.localStorage;
  window.localStorage.setItem("person_id", json["userID"]);
}

document.addEventListener("deviceready", check_id, false);
function check_id() {
  var storage = window.localStorage;
  person_id = window.localStorage.getItem("person_id");
  if(!person_id) {
    $( "#add-user" ).popup();
    $( "#add-user" ).popup("open");
  }
})

$("#add-user-submit").click(function() {
  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/addUser?callback=?",
    dataType:"jsonp",
    data: {username: $("#add-user-value").val()}
  }).done({

  })
})

$("#create-group-submit").click(function() {
  var groupname = $("#group-name").val();
  var timeset = $("#time-set").val();
  if($("#day-set-sun").attr("data-cacheval") == "false") {
    var daysetsun = true;
  }
  else {
    var daysetsun = false;
  }
  if($("#day-set-mon").attr("data-cacheval") == "false") {
    var daysetmon = true;
  }
  else {
    var daysetmon = false;
  }
  if($("#day-set-tue").attr("data-cacheval") == "false") {
    var daysettue = true;
  }
  else {
    var daysettue = false;
  }
  if($("#day-set-wed").attr("data-cacheval") == "false") {
    var daysetwed = true;
  }
  else {
    var daysetwed = false;
  }
  if($("#day-set-thu").attr("data-cacheval") == "false") {
    var daysetthu = true;
  }
  else {
    var daysetthu = false;
  }
  if($("#day-set-fri").attr("data-cacheval") == "false") {
    var daysetfri = true;
  }
  else {
    var daysetfri = false;
  }
  if($("#day-set-sat").attr("data-cacheval") == "false") {
    var daysetsat = true;
  }
  else {
    var daysetsat = false;
  }
  var defaulttoeat = $("#default-to-eat").val();

  $.ajax({
    type: "GET",
    url: "http://128.199.152.153:8000/addGroup?callback=?",
    dataType:"jsonp",
    data: { groupname: groupname, timeset: timeset, daysetsun: daysetsun, daysetmon: daysetmon, daysettue: daysettue, daysetwed: daysetwed, daysetthu: daysetthu, daysetfri: daysetfri, daysetsat: daysetsat, defaulttoeat: defaulttoeat }
  }).done(function( msg ) {
  });
});
